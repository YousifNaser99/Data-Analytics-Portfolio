import streamlit as st
import pandas as pd

from utils.connection import load_view

from utils.helpers import (
    page_title,
    divider,
    format_currency,
    format_number,
    format_percent,
)

from utils.metrics import (
    total_revenue,
    total_profit,
    total_units,
)

from utils.dashboard_helpers import (
    validate_dashboard,
    show_kpi_row,
)

# ==========================================================
# Page Header
# ==========================================================

page_title(
    "📅 Time Intelligence Dashboard",
    "Trend & Seasonality Analysis",
)

divider()

# ==========================================================
# Load Data
# ==========================================================

df = load_view("vw_MonthlyPerformance")

validate_dashboard(
    df,
    "Time Intelligence data could not be loaded."
)

# ==========================================================
# Sidebar Filters
# ==========================================================

with st.sidebar:

    st.header("Time Filters")

    years = sorted(
        df["CalendarYear"]
        .dropna()
        .unique()
    )

    selected_years = st.multiselect(
        "Calendar Year",
        years,
        default=years,
    )

    divider()

    if st.button(
        "Reset Filters",
        width="stretch",
    ):
        st.rerun()

# ==========================================================
# Apply Filters
# ==========================================================

if selected_years:

    df = df[
        df["CalendarYear"].isin(selected_years)
    ]


validate_dashboard(
    df,
    "No data available for selected years."
)


df = df.sort_values(
    [
        "CalendarYear",
        "MonthNumberOfYear",
    ]
)

# ==========================================================
# Cached Summary
# ==========================================================

@st.cache_data
def prepare_summary(data: pd.DataFrame):

    revenue = total_revenue(data)

    profit = total_profit(data)

    units = total_units(data)

    avg_monthly_revenue = data["Revenue"].mean()

    avg_monthly_profit = data["Profit"].mean()


    revenue_yoy = data["YoYRevenue"].mean()

    profit_yoy = data["YoYProfit"].mean()


    monthly = (
        data.groupby(
            [
                "CalendarYear",
                "MonthName"
            ],
            as_index=False
        )
        ["Revenue"]
        .sum()
    )


    best_month = (
        monthly
        .loc[
            monthly["Revenue"].idxmax()
        ]
    )


    best_month_name = (
        f"{best_month['MonthName']} "
        f"{best_month['CalendarYear']}"
    )


    highest_monthly_revenue = best_month["Revenue"]


    return (

        revenue,

        profit,

        units,

        avg_monthly_revenue,

        avg_monthly_profit,

        revenue_yoy,

        profit_yoy,

        best_month_name,

        highest_monthly_revenue,

    )


(
    revenue,
    profit,
    units,
    avg_monthly_revenue,
    avg_monthly_profit,
    revenue_yoy,
    profit_yoy,
    best_month_name,
    highest_monthly_revenue,

) = prepare_summary(df)

# ==========================================================
# KPI Cards
# ==========================================================

show_kpi_row(

    [

        (
            "Revenue",
            format_currency(revenue),
        ),

        (
            "Profit",
            format_currency(profit),
        ),

        (
            "Units",
            format_number(units),
        ),

    ]

)

show_kpi_row(

    [

        (
            "Revenue YoY",
            format_percent(revenue_yoy),
        ),

        (
            "Profit YoY",
            format_percent(profit_yoy),
        ),

        (
            "Avg Monthly Revenue",
            format_currency(
                avg_monthly_revenue
            ),
        ),

    ]

)

show_kpi_row(

    [

        (
            "Avg Monthly Profit",
            format_currency(
                avg_monthly_profit
            ),
        ),

        (
            "Best Month",
            best_month_name,
        ),

        (
            "Highest Monthly Revenue",
            format_currency(
                highest_monthly_revenue
            ),
        ),

    ]

)

divider()
from utils.charts import (
    line_chart,
    bar_chart,
)

# ==========================================================
# Cached Chart Data
# ==========================================================

@st.cache_data
def prepare_charts(data: pd.DataFrame):

    seasonality = (
        data.groupby(
            "MonthName",
            as_index=False
        )
        .agg(
            Revenue=("Revenue", "mean"),
            Profit=("Profit", "mean"),
            Units=("Units", "mean"),
        )
    )

    best_month = (
        data.sort_values(
            "Revenue",
            ascending=False,
        )
        .head(1)
    )

    worst_month = (
        data.sort_values(
            "Revenue",
            ascending=True,
        )
        .head(1)
    )

    return (
        seasonality,
        best_month,
        worst_month,
    )


(
    seasonality,
    best_month,
    worst_month,
) = prepare_charts(df)

# ==========================================================
# Revenue Trend
# ==========================================================

fig = line_chart(
    df,
    x="Period",
    y="Revenue",
    title="Revenue Trend",
)

st.plotly_chart(
    fig,
    width="stretch",
)

divider()

# ==========================================================
# Running Totals
# ==========================================================

left, right = st.columns(2)

with left:

    fig = line_chart(
        df,
        x="Period",
        y="RunningRevenue",
        title="Running Revenue",
    )

    st.plotly_chart(
        fig,
        width="stretch",
    )

with right:

    fig = line_chart(
        df,
        x="Period",
        y="RunningProfit",
        title="Running Profit",
    )

    st.plotly_chart(
        fig,
        width="stretch",
    )

divider()

# ==========================================================
# Rolling Average
# ==========================================================

left, right = st.columns(2)

with left:

    fig = line_chart(
        df,
        x="Period",
        y="RollingRevenue",
        title="3-Month Rolling Revenue",
    )

    st.plotly_chart(
        fig,
        width="stretch",
    )

with right:

    fig = line_chart(
        df,
        x="Period",
        y="RollingProfit",
        title="3-Month Rolling Profit",
    )

    st.plotly_chart(
        fig,
        width="stretch",
    )

divider()

# ==========================================================
# Month over Month
# ==========================================================

left, right = st.columns(2)

with left:

    fig = bar_chart(
        df,
        x="Period",
        y="MoMRevenue",
        title="Month over Month Revenue %",
    )

    st.plotly_chart(
        fig,
        width="stretch",
    )

with right:

    fig = bar_chart(
        df,
        x="Period",
        y="MoMProfit",
        title="Month over Month Profit %",
    )

    st.plotly_chart(
        fig,
        width="stretch",
    )

divider()

# ==========================================================
# Year over Year
# ==========================================================

left, right = st.columns(2)

with left:

    fig = bar_chart(
        df,
        x="Period",
        y="YoYRevenue",
        title="Year over Year Revenue %",
    )

    st.plotly_chart(
        fig,
        width="stretch",
    )

with right:

    fig = bar_chart(
        df,
        x="Period",
        y="YoYProfit",
        title="Year over Year Profit %",
    )

    st.plotly_chart(
        fig,
        width="stretch",
    )

divider()

# ==========================================================
# Seasonality
# ==========================================================

left, right = st.columns(2)

with left:

    fig = bar_chart(
        seasonality,
        x="MonthName",
        y="Revenue",
        title="Average Monthly Revenue",
    )

    st.plotly_chart(
        fig,
        width="stretch",
    )

with right:

    fig = bar_chart(
        seasonality,
        x="MonthName",
        y="Profit",
        title="Average Monthly Profit",
    )

    st.plotly_chart(
        fig,
        width="stretch",
    )

divider()
from utils.dashboard_helpers import (
    show_table,
    show_export_button,
    show_summary,
    show_footer,
)

# ==========================================================
# Best & Worst Month
# ==========================================================

left, right = st.columns(2)

with left:

    if not best_month.empty:

        month = best_month.iloc[0]

        st.metric(
            "Best Month",
            f"{month['MonthName']} {int(month['CalendarYear'])}",
            format_currency(month["Revenue"]),
        )

with right:

    if not worst_month.empty:

        month = worst_month.iloc[0]

        st.metric(
            "Worst Month",
            f"{month['MonthName']} {int(month['CalendarYear'])}",
            format_currency(month["Revenue"]),
        )

divider()

# ==========================================================
# Monthly Performance Table
# ==========================================================

display = df[
    [
        "CalendarYear",
        "MonthName",
        "Revenue",
        "Profit",
        "Units",
        "MoMRevenue",
        "MoMProfit",
        "YoYRevenue",
        "YoYProfit",
    ]
].copy()

show_table(
    display,
    "Monthly Performance",
    height=450,
)

divider()

# ==========================================================
# Export
# ==========================================================

show_export_button(
    dataframe=display,
    filename="Time_Intelligence_Report",
    label="📥 Download Time Intelligence Report",
)

divider()

# ==========================================================
# Executive Summary
# ==========================================================

positive_months = (
    df["MoMRevenue"] > 0
).sum()

negative_months = (
    df["MoMRevenue"] < 0
).sum()

highest_growth = df["MoMRevenue"].max()

average_growth = df["MoMRevenue"].mean()

show_summary(

    left_title="Time Performance",

    left_items={

        "Revenue": format_currency(revenue),

        "Profit": format_currency(profit),

        "Units": format_number(units),
    },

    right_title="Growth Insights",

    right_items={

        "Positive Months": format_number(positive_months),

        "Negative Months": format_number(negative_months),

        "Highest Growth": (
            f"{highest_growth:.2f}%"
            if pd.notna(highest_growth)
            else "-"
        ),

        "Average Growth": (
            f"{average_growth:.2f}%"
            if pd.notna(average_growth)
            else "-"
        ),

    },

)

divider()

# ==========================================================
# Footer
# ==========================================================

show_footer(

    records=len(df),

    Years=df["CalendarYear"].nunique(),

    Revenue=format_currency(df["Revenue"].sum()),

    Profit=format_currency(df["Profit"].sum()),

)
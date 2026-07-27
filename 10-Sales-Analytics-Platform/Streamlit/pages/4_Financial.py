import streamlit as st
import pandas as pd

from utils.connection import load_view

from utils.helpers import (
    page_title,
    divider,
    has_data,
    format_currency,
    format_number,
    format_percent,
)

from utils.metrics import (
    total_revenue,
    total_profit,
    total_units,
    gross_margin,
)

from utils.dashboard_helpers import (
    validate_dashboard,
    show_kpi_row,
)

# ==========================================================
# Page Header
# ==========================================================

page_title(
    "💵 Financial Dashboard",
    "Financial Performance Analysis"
)

divider()

# ==========================================================
# Load Data
# ==========================================================

financial = load_view("vw_FinancialAnalysis")

validate_dashboard(
    financial,
    "Financial data could not be loaded."
)

# ==========================================================
# Sidebar Filters
# ==========================================================

with st.sidebar:

    st.header("Financial Filters")

    selected_years = st.multiselect(
        "Year",
        sorted(financial["CalendarYear"].dropna().unique()),
        default=sorted(financial["CalendarYear"].dropna().unique()),
        key="financial_year"
    )

    selected_quarters = st.multiselect(
        "Quarter",
        sorted(financial["CalendarQuarter"].dropna().unique()),
        default=sorted(financial["CalendarQuarter"].dropna().unique()),
        key="financial_quarter"
    )

    selected_categories = st.multiselect(
        "Category",
        sorted(financial["Category"].dropna().unique()),
        default=sorted(financial["Category"].dropna().unique()),
        key="financial_category"
    )

    selected_countries = st.multiselect(
        "Country",
        sorted(financial["Country"].dropna().unique()),
        default=sorted(financial["Country"].dropna().unique()),
        key="financial_country"
    )

    divider()

# ==========================================================
# Apply Filters
# ==========================================================

filtered_financial = financial.copy()


if selected_years:

    filtered_financial = filtered_financial[
        filtered_financial["CalendarYear"].isin(selected_years)
    ]


if selected_quarters:

    filtered_financial = filtered_financial[
        filtered_financial["CalendarQuarter"].isin(selected_quarters)
    ]


if selected_categories:

    filtered_financial = filtered_financial[
        filtered_financial["Category"].isin(selected_categories)
    ]


if selected_countries:

    filtered_financial = filtered_financial[
        filtered_financial["Country"].isin(selected_countries)
    ]


if not has_data(filtered_financial):

    st.warning(
        "No financial records found."
    )

    st.stop()

# ==========================================================
# Cached KPI Calculations
# ==========================================================

@st.cache_data
def financial_summary(df: pd.DataFrame):

    revenue = total_revenue(df)

    cost = df["Cost"].sum()

    profit = total_profit(df)

    units = total_units(df)

    margin = gross_margin(df)

    tax = df["Tax"].sum()

    freight = df["Freight"].sum()

    avg_monthly_revenue = (

        df.groupby(
            ["CalendarYear", "MonthNumberOfYear"]
        )["Revenue"]
        .sum()
        .mean()

    )

    avg_monthly_profit = (

        df.groupby(
            ["CalendarYear", "MonthNumberOfYear"]
        )["Profit"]
        .sum()
        .mean()

    )

    return (
        revenue,
        cost,
        profit,
        units,
        margin,
        tax,
        freight,
        avg_monthly_revenue,
        avg_monthly_profit,
    )


(
    revenue,
    cost,
    profit,
    units,
    margin,
    tax,
    freight,
    avg_monthly_revenue,
    avg_monthly_profit,
) = financial_summary(filtered_financial)

# ==========================================================
# KPI Cards
# ==========================================================

show_kpi_row(

    [

        (
            "Revenue",
            format_currency(revenue)
        ),

        (
            "Cost",
            format_currency(cost)
        ),

        (
            "Profit",
            format_currency(profit)
        ),

        (
            "Gross Margin",
            format_percent(margin)
        ),

    ]

)


show_kpi_row(

    [

        (
            "Units Sold",
            format_number(units)
        ),

        (
            "Tax",
            format_currency(tax)
        ),

        (
            "Freight",
            format_currency(freight)
        ),

        (
            "Average Monthly Revenue",
            format_currency(avg_monthly_revenue)
        ),

    ]

)

divider()
from utils.charts import (
    line_chart,
    multi_line_chart,
    bar_chart,
    horizontal_bar,
    donut_chart,
    world_map,
    gauge,
)

# ==========================================================
# Cached Chart Data
# ==========================================================

@st.cache_data
def prepare_charts(df: pd.DataFrame):

    monthly = (
        df.groupby(
            [
                "CalendarYear",
                "MonthNumberOfYear",
                "MonthName",
            ],
            as_index=False,
        )
        .agg(
            Revenue=("Revenue", "sum"),
            Cost=("Cost", "sum"),
            Profit=("Profit", "sum"),
            Units=("Units", "sum"),
        )
        .sort_values(
            ["CalendarYear", "MonthNumberOfYear"]
        )
    )

    category = (
        df.groupby(
            "Category",
            as_index=False,
        )
        .agg(
            Revenue=("Revenue", "sum"),
            Cost=("Cost", "sum"),
            Profit=("Profit", "sum"),
            Units=("Units", "sum"),
        )
    )

    category["Margin"] = (
        category["Profit"] /
        category["Revenue"]
    ).fillna(0)

    country = (
        df.groupby(
            "Country",
            as_index=False,
        )
        .agg(
            Revenue=("Revenue", "sum"),
            Cost=("Cost", "sum"),
            Profit=("Profit", "sum"),
            Units=("Units", "sum"),
        )
    )

    country["Margin"] = (
        country["Profit"] /
        country["Revenue"]
    ).fillna(0)

    return monthly, category, country


monthly_chart, category_chart, country_chart = prepare_charts(
    filtered_financial
)

# ==========================================================
# Monthly Revenue & Profit
# ==========================================================

left, right = st.columns(2)


# ==========================================================
# Prepare Monthly Trend
# ==========================================================

monthly_trend = (
    monthly_chart
    .sort_values(
        [
            "CalendarYear",
            "MonthNumberOfYear"
        ]
    )
)

monthly_trend["Period"] = (
    monthly_trend["CalendarYear"].astype(str)
    + "-"
    + monthly_trend["MonthName"]
)


# =========================================================
# Monthly Financial Performance
# =========================================================


fig = multi_line_chart(

    monthly_trend,

    x="Period",

    y_columns=[
        "Revenue",
        "Profit"
    ],

    title="Monthly Financial Performance"

)


st.plotly_chart(

    fig,

    width="stretch"

)


divider()

# ==========================================================
# Revenue vs Cost vs Profit
# ==========================================================

monthly_chart["Period"] = (
    monthly_chart["CalendarYear"].astype(str)
    + "-"
    + monthly_chart["MonthName"]
)


trend = monthly_chart.melt(
    id_vars=[
        "Period"
    ],
    value_vars=[
        "Revenue",
        "Cost",
        "Profit",
    ],
    var_name="Metric",
    value_name="Value",
)

st.plotly_chart(

    line_chart(
        trend,
        x="Period",
        y="Value",
        color="Metric",
        title="Revenue vs Cost vs Profit"
    ),

    width="stretch",

)

divider()

# ==========================================================
# Category Analysis
# ==========================================================

left, right = st.columns(2)

with left:

    st.plotly_chart(

        bar_chart(

    category_chart.sort_values(
        "Revenue",
        ascending=False
    ),

    x="Category",

    y="Revenue",

    title="Revenue by Category"
    )
)

with right:

    st.plotly_chart(

        bar_chart(

    category_chart.sort_values(
        "Profit",
        ascending=False
    ),

    x="Category",

    y="Profit",

    title="Category Profitability"
    )
)
    
divider()

# ==========================================================
# Units & Margin
# ==========================================================

left, right = st.columns(2)

with left:

    st.plotly_chart(

        bar_chart(
            category_chart.sort_values(
                "Units",
                ascending=False,
            ),
            x="Category",
            y="Units",
            title="Units Sold by Category"
        ),

        width="stretch",

    )

with right:

    st.plotly_chart(

        bar_chart(
            category_chart.sort_values(
                "Margin",
                ascending=False,
            ),
            x="Category",
            y="Margin",
            title="Profit Margin by Category"
        ),

        width="stretch",

    )

divider()

# ==========================================================
# Country Analysis
# ==========================================================

left, right = st.columns(2)

with left:

    st.plotly_chart(

        horizontal_bar(
            country_chart.sort_values(
                "Revenue"
            ),
            x="Revenue",
            y="Country",
            title="Revenue by Country"
        ),

        width="stretch",

    )

with right:

    st.plotly_chart(

        horizontal_bar(
            country_chart.sort_values(
                "Profit"
            ),
            x="Profit",
            y="Country",
            title="Profit by Country"
        ),

        width="stretch",

    )

divider()

# ==========================================================
# Revenue Map
# ==========================================================

st.plotly_chart(

    world_map(
        country_chart,
        country="Country",
        value="Revenue",
        title="Revenue Distribution"
    ),

    width="stretch",

)

divider()

# ==========================================================
# Gross Margin Gauge
# ==========================================================

st.plotly_chart(

    gauge(
        value=margin * 100,
        maximum=100,
        title="Gross Margin"
    ),

    width="stretch",

)

divider()
from utils.dashboard_helpers import (
    show_table,
    show_summary,
    show_export_button,
    show_footer,
)

# ==========================================================
# Financial Details
# ==========================================================

financial_table = (

    filtered_financial
    .sort_values(
        ["CalendarYear", "MonthNumberOfYear"]
    )
    .copy()

)

show_table(

    financial_table,

    title="Financial Details",

    height=500,

)

divider()

# ==========================================================
# Executive Summary
# ==========================================================

best_category = (

    category_chart
    .sort_values(
        "Revenue",
        ascending=False
    )
    .iloc[0]

)

best_country = (

    country_chart
    .sort_values(
        "Revenue",
        ascending=False
    )
    .iloc[0]

)

show_summary(

    left_title="Financial Performance",

    left_items={

        "Revenue": format_currency(revenue),

        "Cost": format_currency(cost),

        "Profit": format_currency(profit),

        "Gross Margin": format_percent(margin),

    },

    right_title="Business Highlights",

    right_items={

        "Top Category": best_category["Category"],

        "Top Country": best_country["Country"],

        "Units Sold": format_number(units),

        "Average Monthly Revenue": format_currency(
            avg_monthly_revenue
        ),

    }

)

divider()

# ==========================================================
# Export Report
# ==========================================================

show_export_button(

    financial_table,

    "Financial_Report"

)

divider()

# ==========================================================
# Footer
# ==========================================================

show_footer(

    Dashboard="Financial",

    Years=filtered_financial["CalendarYear"].nunique(),

    Countries=filtered_financial["Country"].nunique(),

    Records=len(filtered_financial),

)

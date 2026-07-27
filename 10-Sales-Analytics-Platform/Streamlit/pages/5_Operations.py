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
    "⚙️ Operations Dashboard",
    "Supply Chain & Operations Analytics",
)

divider()

# ==========================================================
# Load Data
# ==========================================================

df = load_view("vw_SalesAnalysis")

validate_dashboard(
    df,
    "Operations data could not be loaded."
)

# ==========================================================
# Sidebar Filters
# ==========================================================

with st.sidebar:

    st.header("Operations Filters")

    years = sorted(
        df["CalendarYear"]
        .dropna()
        .unique()
    )

    selected_years = st.multiselect(
        "Year",
        years,
        default=years,
    )

    categories = sorted(
        df["Category"]
        .dropna()
        .unique()
    )

    selected_categories = st.multiselect(
        "Category",
        categories,
        default=categories,
    )

    regions = sorted(
        df["Region"]
        .dropna()
        .unique()
    )

    selected_regions = st.multiselect(
        "Region",
        regions,
        default=regions,
    )

    countries = sorted(
    df["Country"]
    .dropna()
    .unique()
     )

    selected_countries = st.multiselect(
    "Country",
    countries,
    default=countries,
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


if selected_categories:

    df = df[
        df["Category"].isin(selected_categories)
    ]


if selected_regions:

    df = df[
        df["Region"].isin(selected_regions)
    ]

if selected_countries:

    df = df[
        df["Country"].isin(selected_countries)
    ]

validate_dashboard(
    df,
    "No records match the selected filters."
)

# ==========================================================
# Cached Summary
# ==========================================================

@st.cache_data
def prepare_summary(data):

    revenue = total_revenue(data)

    profit = total_profit(data)

    units = total_units(data)

    margin = gross_margin(data)

    orders = data["SalesOrderNumber"].nunique()

    cost = data["TotalProductCost"].sum()

    freight = data["Freight"].sum()

    avg_order_value = (
        revenue / orders
        if orders
        else 0
    )

    avg_profit = (
        profit / orders
        if orders
        else 0
    )

    avg_cost = (
        cost / orders
        if orders
        else 0
    )

    avg_freight = (
        freight / orders
        if orders
        else 0
    )

    freight_ratio = (
        freight / revenue
        if revenue
        else 0
    )

    cost_ratio = (
        cost / revenue
        if revenue
        else 0
    )

    profit_per_unit = (
        profit / units
        if units
        else 0
    )

    return (
        revenue,
        profit,
        units,
        margin,
        orders,
        cost,
        freight,
        avg_order_value,
        avg_profit,
        avg_cost,
        avg_freight,
        freight_ratio,
        cost_ratio,
        profit_per_unit,
    )


(
    revenue,
    profit,
    units,
    margin,
    orders,
    cost,
    freight,
    avg_order_value,
    avg_profit,
    avg_cost,
    avg_freight,
    freight_ratio,
    cost_ratio,
    profit_per_unit,
) = prepare_summary(df)

# ==========================================================
# KPI Cards
# ==========================================================

show_kpi_row(
    [
        (
            "Orders",
            format_number(orders),
        ),
        (
            "Units",
            format_number(units),
        ),
        (
            "Revenue",
            format_currency(revenue),
        ),
        (
            "Cost",
            format_currency(cost),
        ),
    ]
)

show_kpi_row(
    [
        (
            "Profit",
            format_currency(profit),
        ),
        (
            "Margin",
            format_percent(margin),
        ),
        (
            "Freight",
            format_currency(freight),
        ),
        (
            "Freight %",
            format_percent(freight_ratio),
        ),
    ]
)

divider()

# ==========================================================
# Operational Ratios
# ==========================================================

show_kpi_row(
    [
        (
            "Avg Order Value",
            format_currency(avg_order_value),
        ),
        (
            "Avg Profit / Order",
            format_currency(avg_profit),
        ),
        (
            "Avg Cost / Order",
            format_currency(avg_cost),
        ),
        (
            "Avg Freight / Order",
            format_currency(avg_freight),
        ),
    ]
)

show_kpi_row(
    [
        (
            "Avg Units / Order",
            f"{units / orders:.2f}" if orders else "0",
        ),

        (
            "Avg Selling Price",
            format_currency(
                revenue / units
                if units
                else 0
            ),
        ),

        (
            "Profit / Unit",
            format_currency(profit_per_unit),
        ),

        (
            "Cost Ratio",
            format_percent(cost_ratio),
        ),
    ]
)

divider()
from utils.charts import (
    bar_chart,
    horizontal_bar,
    donut_chart,
)

# ==========================================================
# Cached Aggregations
# ==========================================================

@st.cache_data
def prepare_charts(data: pd.DataFrame):

    freight_country = (
        data.groupby(
            "Country",
            as_index=False
        )
        .agg(
            Freight=("Freight", "sum")
        )
        .sort_values(
            "Freight",
            ascending=False
        )
    )

    freight_category = (
        data.groupby(
            "Category",
            as_index=False
        )
        .agg(
            Freight=("Freight", "sum")
        )
    )

    category = (
        data.groupby(
            "Category",
            as_index=False
        )
        .agg(
            Revenue=("SalesAmount", "sum"),
            Cost=("TotalProductCost", "sum"),
            Profit=("GrossProfit", "sum"),
            Freight=("Freight", "sum"),
            Units=("OrderQuantity", "sum"),
        )
    )

    category["Margin"] = (
        category["Profit"] /
        category["Revenue"]
    ).fillna(0)

    segment = (
        data.groupby(
            "PriceSegment",
            as_index=False
        )
        .agg(
            Revenue=("SalesAmount", "sum"),
            Profit=("GrossProfit", "sum"),
            Units=("OrderQuantity", "sum"),
        )
    )

    return (
        freight_country,
        freight_category,
        category,
        segment,
    )


(
    freight_country,
    freight_category,
    category_chart,
    segment_chart,
) = prepare_charts(df)

# ==========================================================
# Freight Analysis
# ==========================================================

left, right = st.columns(2)


with left:

    fig = horizontal_bar(
        freight_country,
        x="Freight",
        y="Country",
        title="Freight Cost by Country",
    )

    st.plotly_chart(
        fig,
        width="stretch",
        key="freight_country_chart"
    )


with right:

    fig = bar_chart(
        freight_category.sort_values(
            "Freight",
            ascending=False
        ),
        x="Category",
        y="Freight",
        title="Freight by Category"
    )

    st.plotly_chart(
        fig,
        width="stretch",
        key="freight_category_chart"
    )


divider()

# ==========================================================
# Revenue vs Cost
# ==========================================================

left, right = st.columns(2)

with left:

    fig = bar_chart(
        category_chart.sort_values(
            "Revenue",
            ascending=False,
        ),
        x="Category",
        y="Revenue",
        title="Revenue Contribution by Category",
    )

    st.plotly_chart(
        fig,
        width="stretch",
    )

with right:

    fig = bar_chart(
        category_chart.sort_values(
            "Cost",
            ascending=False,
        ),
        x="Category",
        y="Cost",
        title="Cost Contribution by Category",
    )

    st.plotly_chart(
        fig,
        width="stretch",
    )

divider()

# ==========================================================
# Profit vs Margin
# ==========================================================

left, right = st.columns(2)

with left:

    fig = bar_chart(
        category_chart.sort_values(
            "Profit",
            ascending=False,
        ),
        x="Category",
        y="Profit",
        title="Profit by Category",
    )

    st.plotly_chart(
        fig,
        width="stretch",
    )

with right:

    fig = bar_chart(
        category_chart.sort_values(
            "Margin",
            ascending=False,
        ),
        x="Category",
        y="Margin",
        title="Profit Margin by Category",
    )

    st.plotly_chart(
        fig,
        width="stretch",
    )

divider()

# ==========================================================
# Price Segment Performance
# ==========================================================

left, right = st.columns(2)

with left:

    fig = donut_chart(
        segment_chart,
        names="PriceSegment",
        values="Revenue",
        title="Revenue by Price Segment",
    )

    st.plotly_chart(
        fig,
        width="stretch",
    )

with right:

    fig = bar_chart(
        segment_chart.sort_values(
            "Profit",
            ascending=False,
        ),
        x="PriceSegment",
        y="Profit",
        title="Profit by Price Segment",
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
# Top Freight Orders
# ==========================================================

left, right = st.columns(2)

with left:

    freight_orders = (
        df[
            [
                "SalesOrderNumber",
                "ProductName",
                "Country",
                "Freight",
            ]
        ]
        .sort_values(
            "Freight",
            ascending=False,
        )
        .head(10)
    )

    show_table(
        freight_orders,
        "Top Freight Orders",
        height=320,
    )

with right:

    top_cost_products = (
        df.groupby(
            "ProductName",
            as_index=False,
        )
        .agg(
            Cost=("TotalProductCost", "sum"),
            Revenue=("SalesAmount", "sum"),
            Profit=("GrossProfit", "sum"),
        )
        .sort_values(
            "Cost",
            ascending=False,
        )
        .head(10)
    )

    show_table(
        top_cost_products,
        "Top Cost Products",
        height=320,
    )

divider()

# ==========================================================
# Operations Details
# ==========================================================

details = (
    df[
        [
            "OrderDate",
            "SalesOrderNumber",
            "ProductName",
            "Category",
            "PriceSegment",
            "Country",
            "Region",
            "OrderQuantity",
            "SalesAmount",
            "TotalProductCost",
            "GrossProfit",
            "DiscountAmount",
            "Freight",
        ]
    ]
    .sort_values(
        "OrderDate",
        ascending=False,
    )
)

show_table(
    details,
    "Operations Details",
    height=450,
)

divider()

# ==========================================================
# Export Report
# ==========================================================

show_export_button(
    dataframe=details,
    filename="Operations_Report",
    label="📥 Download Operations Report",
)

divider()

# ==========================================================
# Executive Summary
# ==========================================================

best_segment = "-"

if not segment_chart.empty:

    best_segment = (
        segment_chart
        .sort_values(
            "Revenue",
            ascending=False,
        )
        .iloc[0]["PriceSegment"]
    )

highest_freight_country = "-"

if not freight_country.empty:

    highest_freight_country = (
        freight_country
        .sort_values(
            "Freight",
            ascending=False,
        )
        .iloc[0]["Country"]
    )

highest_margin_category = "-"

if not category_chart.empty:

    highest_margin_category = (
        category_chart
        .sort_values(
            "Margin",
            ascending=False,
        )
        .iloc[0]["Category"]
    )

show_summary(

    left_title="Operations Performance",

    left_items={

        "Orders": format_number(orders),

        "Revenue": format_currency(revenue),

        "Cost": format_currency(cost),

        "Profit": format_currency(profit),

        "Margin": format_percent(margin),

    },

    right_title="Operational Insights",

    right_items={

        "Best Price Segment": best_segment,

        "Highest Margin Category": highest_margin_category,

        "Highest Freight Country": highest_freight_country,

        "Freight Ratio": format_percent(freight_ratio),

    },
)

divider()

# ==========================================================
# Footer
# ==========================================================

show_footer(
    records=len(df),
    Products=df["ProductName"].nunique(),
    Countries=df["Country"].nunique(),
    Regions=df["Region"].nunique(),
)
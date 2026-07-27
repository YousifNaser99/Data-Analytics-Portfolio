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
    "📦 Product Dashboard",
    "Product Performance Analytics",
)

divider()

# ==========================================================
# Load Data
# ==========================================================

df = load_view("vw_ProductPerformance")

validate_dashboard(
    df,
    "Product data could not be loaded."
)

# ==========================================================
# Sidebar Filters
# ==========================================================

with st.sidebar:

    st.header("Product Filters")

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

    segments = sorted(
        df["PriceSegment"]
        .dropna()
        .unique()
    )

    selected_segments = st.multiselect(
        "Price Segment",
        segments,
        default=segments,
    )

    abc_classes = sorted(
        df["ABCClass"]
        .dropna()
        .unique()
    )

    selected_abc = st.multiselect(
        "ABC Class",
        abc_classes,
        default=abc_classes,
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

if selected_categories:

    df = df[
        df["Category"].isin(selected_categories)
    ]


if selected_segments:

    df = df[
        df["PriceSegment"].isin(selected_segments)
    ]


if selected_abc:

    df = df[
        df["ABCClass"].isin(selected_abc)
    ]


validate_dashboard(
    df,
    "No products match the selected filters."
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

    products = data["ProductKey"].nunique()

    avg_price = data["AvgSellingPrice"].mean()

    avg_profit_unit = data["ProfitPerUnit"].mean()

    avg_revenue_product = (
        revenue / products
        if products
        else 0
    )

    return (

        revenue,

        profit,

        units,

        margin,

        products,

        avg_price,

        avg_profit_unit,

        avg_revenue_product,

    )


(
    revenue,
    profit,
    units,
    margin,
    products,
    avg_price,
    avg_profit_unit,
    avg_revenue_product,

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
            "Units Sold",
            format_number(units),
        ),

        (
            "Margin",
            format_percent(margin),
        ),

    ]

)

show_kpi_row(

    [

        (
            "Avg Selling Price",
            format_currency(avg_price),
        ),

        (
            "Profit / Unit",
            format_currency(avg_profit_unit),
        ),

        (
            "Products",
            format_number(products),
        ),

        (
            "Avg Revenue / Product",
            format_currency(
            avg_revenue_product),
         ),

    ]

)

divider()
from utils.charts import (
    donut_chart,
    bar_chart,
    horizontal_bar,
)

# ==========================================================
# Cached Aggregations
# ==========================================================

@st.cache_data
def prepare_charts(data: pd.DataFrame):

    category = (
        data.groupby(
            "Category",
            as_index=False
        )
        .agg(
            Revenue=("Revenue", "sum"),
            Profit=("Profit", "sum"),
            Units=("UnitsSold", "sum"),
        )
    )

    segment = (
        data.groupby(
            "PriceSegment",
            as_index=False
        )
        .agg(
            Revenue=("Revenue", "sum"),
            Profit=("Profit", "sum"),
            Units=("UnitsSold", "sum"),
        )
    )

    abc = (
        data.groupby(
            "ABCClass",
            as_index=False
        )
        .agg(
            Products=("ProductKey", "count"),
            Revenue=("Revenue", "sum"),
        )
    )

    top_products = (
        data.sort_values(
            "Revenue",
            ascending=False,
        )
        .head(10)
    )

    top_profit = (
        data.sort_values(
            "Profit",
            ascending=False,
        )
        .head(15)
    )

    pareto = (
        data[
            [
                "ProductName",
                "Revenue",
                "CumRevenuePct",
            ]
        ]
        .sort_values(
            "Revenue",
            ascending=False,
        )
        .head(20)
    )

    ranking = (
        data[
            [
                "ProductName",
                "Revenue",
                "Profit",
                "RevenueRank",
                "ProfitRank",
            ]
        ]
        .sort_values(
            "RevenueRank"
        )
    )

    return (
        category,
        segment,
        abc,
        top_products,
        top_profit,
        pareto,
        ranking,
    )


(
    category_chart,
    segment_chart,
    abc_chart,
    top_products,
    top_profit,
    pareto_table,
    ranking_table,
) = prepare_charts(df)

# ==========================================================
# Revenue Distribution
# ==========================================================

left, right = st.columns(2)

with left:

    fig = donut_chart(
        category_chart,
        names="Category",
        values="Revenue",
        title="Revenue by Category",
    )

    st.plotly_chart(
        fig,
        width="stretch",
    )

with right:

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

divider()

# ==========================================================
# Top Revenue Products
# ==========================================================

fig = horizontal_bar(
    top_products,
    x="Revenue",
    y="ProductName",
    title="Top 10 Products by Revenue",
)

st.plotly_chart(
    fig,
    width="stretch",
)

divider()

# ==========================================================
# Top Profit Products
# ==========================================================

fig = bar_chart(
    top_profit,
    x="ProductName",
    y="Profit",
    title="Top Products by Profit",
)

st.plotly_chart(
    fig,
    width="stretch",
)

divider()

# ==========================================================
# ABC Analysis
# ==========================================================

left, right = st.columns(2)

with left:

    fig = donut_chart(
        abc_chart,
        names="ABCClass",
        values="Products",
        title="ABC Classification",
    )

    st.plotly_chart(
        fig,
        width="stretch",
    )

with right:

    fig = bar_chart(
        abc_chart,
        x="ABCClass",
        y="Revenue",
        title="Revenue by ABC Class",
    )

    st.plotly_chart(
        fig,
        width="stretch",
    )

divider()

# ==========================================================
# Pareto Analysis
# ==========================================================

st.subheader("Pareto Analysis")

st.dataframe(
    pareto_table,
    width="stretch",
    hide_index=True,
    height=350,
)

divider()

# ==========================================================
# Product Ranking
# ==========================================================

st.subheader("Product Ranking")

st.dataframe(
    ranking_table,
    width="stretch",
    hide_index=True,
    height=400,
)

divider()
from utils.dashboard_helpers import (
    show_table,
    show_export_button,
    show_summary,
    show_footer,
)

# ==========================================================
# Top / Bottom Products
# ==========================================================

left, right = st.columns(2)

with left:

    top_products_table = (
        df[
            [
                "ProductName",
                "Category",
                "Revenue",
                "Profit",
                "UnitsSold",
                "ABCClass",
            ]
        ]
        .sort_values(
            "Revenue",
            ascending=False,
        )
        .head(10)
    )

    show_table(
        top_products_table,
        "Top 10 Products",
        height=320,
    )

with right:

    bottom_products_table = (
        df[
            [
                "ProductName",
                "Category",
                "Revenue",
                "Profit",
                "UnitsSold",
                "ABCClass",
            ]
        ]
        .sort_values(
            "Revenue",
            ascending=True,
        )
        .head(10)
    )

    show_table(
        bottom_products_table,
        "Bottom 10 Products",
        height=320,
    )

divider()

# ==========================================================
# Product Details
# ==========================================================

details = (
    df.sort_values(
        "Revenue",
        ascending=False,
    )
)

show_table(
    details,
    "Product Details",
    height=500,
)

divider()

# ==========================================================
# Export
# ==========================================================

show_export_button(
    dataframe=details,
    filename="Product_Report",
    label="📥 Download Product Report",
)

divider()

# ==========================================================
# Executive Summary
# ==========================================================

best_product = "-"

if not details.empty:

    best_product = details.iloc[0]["ProductName"]

best_category = "-"

if not category_chart.empty:

    best_category = (
        category_chart
        .sort_values(
            "Revenue",
            ascending=False,
        )
        .iloc[0]["Category"]
    )

highest_profit_product = "-"

if not details.empty:

    highest_profit_product = (
        details
        .sort_values(
            "Profit",
            ascending=False,
        )
        .iloc[0]["ProductName"]
    )

show_summary(

    left_title="Product Performance",

    left_items={

        "Revenue": format_currency(revenue),

        "Profit": format_currency(profit),

        "Margin": format_percent(margin),

        "Products": format_number(products),

    },

    right_title="Business Insights",

    right_items={

        "Top Product": best_product,

        "Top Category": best_category,

        "Highest Profit Product": highest_profit_product,

        "Average Selling Price": format_currency(avg_price),

    },

)

divider()

# ==========================================================
# Footer
# ==========================================================

show_footer(
    records=len(df),
    Products=df["ProductName"].nunique(),
    Categories=df["Category"].nunique(),
    Price_Segments=df["PriceSegment"].nunique(),
)
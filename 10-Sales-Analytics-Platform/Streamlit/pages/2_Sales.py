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
    dataframe_to_csv,
    export_filename,
    last_refresh,
)

from utils.metrics import (
    total_revenue,
    total_profit,
    total_orders,
    total_units,
    profit_per_order,
    gross_margin,
    average_units_per_order,
    average_order_value,
    average_selling_price,
    average_revenue_per_customer,
)

from utils.charts import (
    line_chart,
    multi_line_chart,
    bar_chart,
    horizontal_bar,
    donut_chart,
    world_map,
)

# =========================================================
# Page Header
# =========================================================

page_title(
    "💰 Sales Dashboard",
    "Sales Performance Analysis"
)

divider()

# =========================================================
# Load Data
# =========================================================

df = load_view("vw_SalesAnalysis")

# =========================================================
# Validation
# =========================================================

if not has_data(df):

    st.error("Sales data could not be loaded.")

    st.stop()

# =========================================================
# Sidebar Filters
# =========================================================

with st.sidebar:

    st.header("Sales Filters")

    years = sorted(df["CalendarYear"].dropna().unique())

    selected_years = st.multiselect(
        "Year",
        years,
        default=years
    )

    categories = sorted(df["Category"].dropna().unique())

    selected_categories = st.multiselect(
        "Category",
        categories,
        default=categories
    )

    countries = sorted(df["Country"].dropna().unique())

    selected_countries = st.multiselect(
        "Country",
        countries,
        default=countries
    )

    products = sorted(
    df["ProductName"].dropna().unique()
     )

    selected_products = st.multiselect(
    "Product",
    products,
    default=products
     )
    
    divider()

    if st.button(
        "Reset Filters",
        width="stretch"
    ):

        st.rerun()

# =========================================================
# Apply Filters
# =========================================================

filtered_df = df.copy()


if selected_years:

    filtered_df = filtered_df[
        filtered_df["CalendarYear"].isin(selected_years)
    ]


if selected_categories:

    filtered_df = filtered_df[
        filtered_df["Category"].isin(selected_categories)
    ]


if selected_countries:

    filtered_df = filtered_df[
        filtered_df["Country"].isin(selected_countries)
    ]

if selected_products:

    filtered_df = filtered_df[
        filtered_df["ProductName"].isin(selected_products)
    ]

if not has_data(filtered_df):

    st.warning(
        "No records match the selected filters."
    )

    st.stop()

# =========================================================
# KPI Cards
# =========================================================

c1, c2, c3 = st.columns(3)

with c1:

    st.metric(
        "Revenue",
        format_currency(
            total_revenue(filtered_df)
        )
    )

with c2:

    st.metric(
        "Profit",
        format_currency(
            total_profit(filtered_df)
        )
    )

with c3:

    st.metric(
        "Profit Margin",
        format_percent(
            gross_margin(filtered_df)
        )
    )

c4, c5, c6 = st.columns(3)

with c4:

    st.metric(
        "Orders",
        format_number(
            total_orders(filtered_df)
        )
    )

with c5:

    st.metric(
        "Units Sold",
        format_number(
            total_units(filtered_df)
        )
    )

with c6:

    st.metric(
        "Average Order Value",
        format_currency(
            average_order_value(filtered_df)
        )
    )

c7, c8, c9 = st.columns(3)

with c7:

    st.metric(
        "Profit / Order",
        format_currency(
            profit_per_order(filtered_df)
        )
    )

with c8:

    st.metric(
        "Avg Units / Order",
        f"{average_units_per_order(filtered_df):.2f}"
    )

with c9:
    st.metric(
        "Average Selling Price",
        format_currency(
            average_selling_price(filtered_df)
        )
    )

divider()

# =========================================================
# Monthly Revenue Trend
# =========================================================

@st.cache_data
def prepare_monthly(data: pd.DataFrame) -> pd.DataFrame:

    return (
        data.groupby(
            [
                "CalendarYear",
                "MonthNumberOfYear",
                "MonthName"
            ],
            as_index=False
        )
        .agg(
            Revenue=("SalesAmount", "sum"),
            Profit=("GrossProfit", "sum")
        )
        .sort_values(
            [
                "CalendarYear",
                "MonthNumberOfYear"
            ]
        )
    )


@st.cache_data
def prepare_category(data: pd.DataFrame) -> pd.DataFrame:

    return (
        data.groupby(
            "Category",
            as_index=False
        )
        .agg(
            Revenue=("SalesAmount", "sum")
        )
        .sort_values(
            "Revenue",
            ascending=False
        )
    )


@st.cache_data
def prepare_country(data: pd.DataFrame) -> pd.DataFrame:

    return (
        data.groupby(
            "Country",
            as_index=False
        )
        .agg(
            Revenue=("SalesAmount", "sum")
        )
        .sort_values(
            "Revenue",
            ascending=False
        )
    )


monthly = prepare_monthly(filtered_df)
category = prepare_category(filtered_df)
territory = prepare_country(filtered_df)

left, right = st.columns([2, 1])


with left:

    monthly_trend = monthly.copy()

    monthly_trend["Period"] = (
        monthly_trend["CalendarYear"].astype(str)
        + "-"
        + monthly_trend["MonthName"]
    )

    fig = multi_line_chart(
    monthly_trend,
    x="Period",
    y_columns=[
        "Revenue",
        "Profit"
    ],
    title="Monthly Sales Performance"
     )

    st.plotly_chart(
        fig,
        width="stretch"
    )


with right:

    fig = donut_chart(
        category,
        names="Category",
        values="Revenue",
        title="Sales Contribution by Category"
    )

    st.plotly_chart(
        fig,
        width="stretch"
    )


divider()

# =========================================================
# Revenue by Country
# =========================================================

fig = horizontal_bar(
    territory.sort_values(
        "Revenue",
        ascending=True
    ),
    x="Revenue",
    y="Country",
    title="Revenue by Country"
)

st.plotly_chart(
    fig,
    width="stretch"
)

divider()

# =========================================================
# Top Products by Sales
# =========================================================

product_chart = (

    filtered_df.groupby(
        "ProductName",
        as_index=False
    )
    .agg(
        Revenue=("SalesAmount", "sum"),
        Profit=("GrossProfit", "sum")
    )
    .sort_values(
        "Revenue",
        ascending=False
    )
    .head(10)

)


fig = bar_chart(

    product_chart,

    x="ProductName",

    y="Revenue",

    title="Top 10 Products by Sales"

)


st.plotly_chart(

    fig,

    width="stretch"

)


divider()

# =========================================================
# Revenue Distribution Map
# =========================================================

fig = world_map(
    territory,
    country="Country",
    value="Revenue",
    title="Global Sales Distribution"
)

st.plotly_chart(
    fig,
    width="stretch"
)

divider()

# =========================================================
# Top SubCategories & Profit by Category
# =========================================================

left, right = st.columns(2)

with left:

    subcategory = (
        filtered_df.groupby(
            "SubCategory",
            as_index=False
        )
        .agg(
            Revenue=("SalesAmount", "sum")
        )
        .sort_values(
            "Revenue",
            ascending=False
        )
        .head(10)
    )

    fig = bar_chart(
        subcategory,
        x="SubCategory",
        y="Revenue",
        title="Top 10 SubCategories by Sales"
    )

    st.plotly_chart(
        fig,
        width="stretch"
    )

with right:

    profit_category = (
        filtered_df.groupby(
            "Category",
            as_index=False
        )
        .agg(
            Profit=("GrossProfit", "sum")
        )
        .sort_values(
            "Profit",
            ascending=False
        )
    )

    fig = bar_chart(
        profit_category,
        x="Category",
        y="Profit",
        title="Category Profitability"
    )

    st.plotly_chart(
        fig,
        width="stretch"
    )

divider()

# =========================================================
# Top Products & Top Customers
# =========================================================

left, right = st.columns(2)

with left:

    products = (
        filtered_df.groupby(
            "ProductName",
            as_index=False
        )
        .agg(
            Revenue=("SalesAmount", "sum"),
            Profit=("GrossProfit", "sum"),
            Units=("OrderQuantity", "sum"),
        )
        .sort_values(
            "Revenue",
            ascending=False,
        )
        .head(10)
    )

    st.subheader("Top 10 Products")

    st.dataframe(
        products.style.format(
            {
                "Revenue": "${:,.2f}",
                "Profit": "${:,.2f}",
                "Units": "{:,.0f}",
            }
        ),
        width="stretch",
        hide_index=True,
    )

with right:

    customers = (
        filtered_df.groupby(
            "Name",
            as_index=False,
        )
        .agg(
            Revenue=("SalesAmount", "sum"),
            Profit=("GrossProfit", "sum"),
            Orders=("SalesOrderNumber", "nunique"),
        )
        .sort_values(
            "Revenue",
            ascending=False,
        )
        .head(10)
    )

    st.subheader("Top 10 Customers")

    st.dataframe(
        customers.style.format(
            {
                "Revenue": "${:,.2f}",
                "Profit": "${:,.2f}",
                "Orders": "{:,.0f}",
            }
        ),
        width="stretch",
        hide_index=True,
    )

divider()

# =========================================================
# Sales Transactions
# =========================================================

st.subheader("Sales Transactions")

display_columns = [
    "OrderDate",
    "SalesOrderNumber",
    "ProductName",
    "Category",
    "SubCategory",
    "Country",
    "SalesAmount",
    "GrossProfit",
    "GrossMarginPercent",
]

sales_table = (
    filtered_df[display_columns]
    .sort_values(
        "OrderDate",
        ascending=False,
    )
    .copy()
)

st.dataframe(
    sales_table,
    width="stretch",
    hide_index=True,
    height=500,
)

divider()

# =========================================================
# Export
# =========================================================

st.download_button(
    label="📥 Download Sales Report",
    data=dataframe_to_csv(sales_table),
    file_name=export_filename("Sales_Report"),
    mime="text/csv",
    width="stretch",
)

divider()

# =========================================================
# Sales Summary
# =========================================================

st.subheader("Sales Summary")

summary_col1, summary_col2 = st.columns(2)

with summary_col1:

    st.info(
        f"""
### Performance Overview

- **Revenue:** {format_currency(total_revenue(filtered_df))}
- **Profit:** {format_currency(total_profit(filtered_df))}
- **Orders:** {format_number(total_orders(filtered_df))}
- **Units Sold:** {format_number(total_units(filtered_df))}
"""
    )

with summary_col2:

    st.success(
        f"""
### Business Metrics

- **Profit Margin:** {format_percent(gross_margin(filtered_df))}
- **Average Order Value:** {format_currency(average_order_value(filtered_df))}
- **Revenue / Customer:** {format_currency(average_revenue_per_customer(filtered_df))}
- **Displayed Rows:** {format_number(len(sales_table))}
"""
    )

divider()

# =========================================================
# Footer
# =========================================================

last_refresh()

st.caption(
    "Sales Analytics Platform • Sales Dashboard • Version 1.0"
)
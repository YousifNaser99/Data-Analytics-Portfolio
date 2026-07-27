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
    total_orders,
    average_order_value,
    average_revenue_per_customer,
    average_profit_per_customer,
    average_orders_per_customer,
)

from utils.dashboard_helpers import (
    validate_dashboard,
    show_kpi_row,
)

# ==========================================================
# Page Header
# ==========================================================

page_title(
    "👥 Customer Dashboard",
    "Customer Performance & RFM Analysis"
)

divider()

# ==========================================================
# Load Data
# ==========================================================

customers = load_view("vw_CustomerPerformance")
rfm = load_view("vw_RFMCustomers")

validate_dashboard(customers, "Customer data could not be loaded.")

# ==========================================================
# Sidebar Filters
# ==========================================================

with st.sidebar:

    st.header("Customer Filters")

    gender_filter = st.multiselect(
        "Gender",
        sorted(customers["Gender"].dropna().unique()),
        default=sorted(customers["Gender"].dropna().unique()),
        key="customer_gender"
    )

    age_filter = st.multiselect(
        "Age Group",
        sorted(customers["AgeGroup"].dropna().unique()),
        default=sorted(customers["AgeGroup"].dropna().unique()),
        key="customer_age"
    )

    income_filter = st.multiselect(
        "Income Segment",
        sorted(customers["IncomeSegment"].dropna().unique()),
        default=sorted(customers["IncomeSegment"].dropna().unique()),
        key="customer_income"
    )

    # Customer Segment from RFM
    customer_segment_filter = st.multiselect(
        "Customer Segment",
        sorted(
            rfm["CustomerSegment"]
            .dropna()
            .unique()
        ),
        default=sorted(
            rfm["CustomerSegment"]
            .dropna()
            .unique()
        ),
        key="customer_segment"
    )


    country_filter = st.multiselect(
        "Country",
        sorted(customers["Country"].dropna().unique()),
        default=sorted(customers["Country"].dropna().unique()),
        key="customer_country"
    )

    divider()



# =========================================================
# Apply Filters
# =========================================================

filtered_customers = customers.copy()


if gender_filter:

    filtered_customers = filtered_customers[
        filtered_customers["Gender"].isin(gender_filter)
    ]


if age_filter:

    filtered_customers = filtered_customers[
        filtered_customers["AgeGroup"].isin(age_filter)
    ]


if income_filter:

    filtered_customers = filtered_customers[
        filtered_customers["IncomeSegment"].isin(income_filter)
    ]


if country_filter:

    filtered_customers = filtered_customers[
        filtered_customers["Country"].isin(country_filter)
    ]



# ==========================================================
# Filter RFM
# ==========================================================

if has_data(rfm):

    filtered_rfm = rfm[
        rfm["CustomerKey"].isin(
            filtered_customers["CustomerKey"]
        )
    ]


    if customer_segment_filter:

        filtered_rfm = filtered_rfm[
            filtered_rfm["CustomerSegment"]
            .isin(customer_segment_filter)
        ]


        filtered_customers = filtered_customers[
            filtered_customers["CustomerKey"].isin(
                filtered_rfm["CustomerKey"]
            )
        ]


else:

    filtered_rfm = pd.DataFrame()

# ==========================================================
# KPI Calculations
# ==========================================================

customer_count = filtered_customers["CustomerKey"].nunique()

repeat_customers = (
    filtered_customers["CustomerType"]
    .eq("Repeat")
    .sum()
)

one_time_customers = (
    filtered_customers["CustomerType"]
    .eq("One-Time")
    .sum()
)

repeat_rate = (
    repeat_customers / customer_count
    if customer_count
    else 0
)

customer_lifetime_value = (

    filtered_customers["Revenue"].sum()
    /
    customer_count

    if customer_count
    else 0

)
# ==========================================================
# KPI Cards
# ==========================================================

show_kpi_row(

    [

        (
            "Customers",
            format_number(customer_count)
        ),

        (
            "Revenue",
            format_currency(
                total_revenue(filtered_customers)
            )
        ),

        (
            "Profit",
            format_currency(
                total_profit(filtered_customers)
            )
        ),

        (
            "Orders",
            format_number(
                total_orders(filtered_customers)
            )
        ),

    ]

)

show_kpi_row(

    [

        (
            "Repeat Customers",
            format_number(repeat_customers)
        ),

        (
            "One-Time Customers",
            format_number(one_time_customers)
        ),

        (
            "Repeat Rate",
            format_percent(repeat_rate)
        ),

        (
            "Profit Margin",
            format_percent(
                filtered_customers["Profit"].sum()
                /
                filtered_customers["Revenue"].sum()
            )
        ),

    ]

)

show_kpi_row(

    [
        (
        "Average Order Value",
        format_currency(
            average_order_value(filtered_customers))
         ),

         (
        "Revenue per Customer",
        format_currency(
            average_revenue_per_customer(filtered_customers))
         ),

         (
        "Profit per Customer",
        format_currency(
            average_profit_per_customer(filtered_customers))
         ),

         (
        "Customer Lifetime Value",
        format_currency(
            customer_lifetime_value)
         ),
    
     ]
)

divider()
from utils.charts import (
    donut_chart,
    bar_chart,
    horizontal_bar,
    world_map,
)

# ==========================================================
# Cached Aggregations
# ==========================================================

@st.cache_data
def revenue_by_gender(df):
    return (
        df.groupby("Gender", as_index=False)
        .agg(Revenue=("Revenue", "sum"))
    )


@st.cache_data
def revenue_by_age(df):
    return (
        df.groupby("AgeGroup", as_index=False)
        .agg(Revenue=("Revenue", "sum"))
        .sort_values("Revenue", ascending=False)
    )


@st.cache_data
def revenue_by_income(df):
    return (
        df.groupby("IncomeSegment", as_index=False)
        .agg(Revenue=("Revenue", "sum"))
        .sort_values("Revenue", ascending=False)
    )


@st.cache_data
def orders_by_income(df):
    return (
        df.groupby("IncomeSegment", as_index=False)
        .agg(Orders=("Orders", "sum"))
    )


@st.cache_data
def revenue_by_country(df):
    return (
        df.groupby("Country", as_index=False)
        .agg(Revenue=("Revenue", "sum"))
        .sort_values("Revenue", ascending=False)
    )


@st.cache_data
def revenue_by_region(df):
    return (
        df.groupby("Region", as_index=False)
        .agg(Revenue=("Revenue", "sum"))
        .sort_values("Revenue", ascending=False)
    )


gender = revenue_by_gender(filtered_customers)
age = revenue_by_age(filtered_customers)
income = revenue_by_income(filtered_customers)
orders = orders_by_income(filtered_customers)
country = revenue_by_country(filtered_customers)
region = revenue_by_region(filtered_customers)

# ==========================================================
# Gender & Age
# ==========================================================

left, right = st.columns(2)

with left:

    st.plotly_chart(

        donut_chart(
            gender,
            names="Gender",
            values="Revenue",
            title="Revenue by Gender"
        ),

        width="stretch"

    )

with right:

    st.plotly_chart(

        bar_chart(
            age,
            x="AgeGroup",
            y="Revenue",
            title="Revenue by Age Group"
        ),

        width="stretch"

    )

divider()

# ==========================================================
# Income Analysis
# ==========================================================

left, right = st.columns(2)

with left:

    st.plotly_chart(

        donut_chart(
            income,
            names="IncomeSegment",
            values="Revenue",
            title="Revenue by Income Segment"
        ),

        width="stretch"

    )

with right:

    st.plotly_chart(

        bar_chart(
            orders,
            x="IncomeSegment",
            y="Orders",
            title="Orders by Income Segment"
        ),

        width="stretch"

    )

divider()

# ==========================================================
# Customer Type Analysis
# ==========================================================

customer_type = (

    filtered_customers
    .groupby(
        "CustomerType",
        as_index=False
    )
    .size()
    .rename(
        columns={
            "size": "Customers"
        }
    )

)


st.plotly_chart(

    donut_chart(
        customer_type,
        names="CustomerType",
        values="Customers",
        title="Customer Type Distribution"
    ),

    width="stretch"

)

divider()

# ==========================================================
# Geography Analysis
# ==========================================================

left, right = st.columns([2, 1])

with left:

    st.plotly_chart(

        horizontal_bar(
            country.sort_values("Revenue"),
            x="Revenue",
            y="Country",
            title="Revenue by Country"
        ),

        width="stretch"

    )

with right:

    st.plotly_chart(

        donut_chart(
            region,
            names="Region",
            values="Revenue",
            title="Revenue by Region"
        ),

        width="stretch"

    )

divider()

# ==========================================================
# Revenue Map
# ==========================================================

st.plotly_chart(

    world_map(
        country,
        country="Country",
        value="Revenue",
        title="Customer Revenue Distribution"
    ),

    width="stretch"

)

divider()

# ==========================================================
# Top Customers
# ==========================================================

left, right = st.columns(2)

with left:

    st.subheader("🏆 Top Revenue Customers")

    st.dataframe(

        filtered_customers
        .sort_values("RevenueRank")
        .head(10)[
            [
                "Name",
                "Country",
                "Revenue",
                "Profit",
                "Orders",
            ]
        ],

        width="stretch",
        hide_index=True,

    )

with right:

    st.subheader("💰 Top Profit Customers")

    st.dataframe(

        filtered_customers
        .sort_values("ProfitRank")
        .head(10)[
            [
                "Name",
                "Country",
                "Profit",
                "Revenue",
                "Orders",
            ]
        ],

        width="stretch",
        hide_index=True,

    )

divider()
from utils.dashboard_helpers import (
    show_table,
    show_summary,
    show_export_button,
    show_footer,
)

# ==========================================================
# RFM Analysis
# ==========================================================

if has_data(filtered_rfm):

    left, right = st.columns(2)

    with left:

        segment = (
            filtered_rfm
            .groupby("CustomerSegment", as_index=False)
            .size()
            .rename(columns={"size": "Customers"})
            .sort_values("Customers", ascending=False)
        )

        st.plotly_chart(

            donut_chart(
                segment,
                names="CustomerSegment",
                values="Customers",
                title="Customer Segments"
            ),

            width="stretch"

        )

    with right:

        score = (
            filtered_rfm
            .groupby("RFM_Score", as_index=False)
            .size()
            .rename(columns={"size": "Customers"})
            .sort_values("Customers", ascending=False)
            .head(15)
        )

        st.plotly_chart(

            horizontal_bar(
                score,
                x="Customers",
                y="RFM_Score",
                title="Top RFM Scores"
            ),

            width="stretch"

        )

divider()

# ==========================================================
# Customer Details
# ==========================================================

customer_table = (

    filtered_customers
    .sort_values("RevenueRank")
    .copy()

)

show_table(

    customer_table,

    title="Customer Details",

    height=500

)

divider()

# ==========================================================
# RFM Details
# ==========================================================

if has_data(filtered_rfm):

    show_table(

        filtered_rfm.sort_values(

            "Monetary",

            ascending=False

        ),

        title="RFM Details",

        height=350

    )

divider()

# ==========================================================
# Executive Summary
# ==========================================================

high_value = (

    filtered_customers["CustomerValue"]

    .eq("High Value")

    .sum()

)

standard = (

    filtered_customers["CustomerValue"]

    .eq("Standard")

    .sum()

)

show_summary(

    left_title="Customer Performance",

    left_items={

        "Customers": format_number(customer_count),

        "Revenue": format_currency(
            total_revenue(filtered_customers)
        ),

        "Profit": format_currency(
            total_profit(filtered_customers)
        ),

        "Orders": format_number(
            total_orders(filtered_customers)
        ),

    },

    right_title="Customer Insights",

    right_items={

        "Repeat Customers": format_number(
            repeat_customers
        ),

        "One-Time Customers": format_number(
            one_time_customers
        ),

        "High Value Customers": format_number(
            high_value
        ),

        "Standard Customers": format_number(
            standard
        ),

    }

)

divider()

# ==========================================================
# Export
# ==========================================================

show_export_button(

    customer_table,

    "Customer_Report"

)

divider()

# ==========================================================
# Footer
# ==========================================================

show_footer(

    Customers=customer_count,

    RFM_Records=len(filtered_rfm),

    Countries=filtered_customers["Country"].nunique(),

    Dashboard="Customer"

)
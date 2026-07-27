import streamlit as st
import pandas as pd

from utils.dashboard_helpers import (
    show_kpi_row,
    show_summary,
)

from utils.connection import load_view

from utils.helpers import (
    page_title,
    divider,
    format_currency,
    format_number,
    format_percent
)


# ==========================================================
# Page Header
# ==========================================================

page_title(
    "🎯 Sales Simulator",
    "Scenario Planning & Profit Simulation"
)

divider()


# ==========================================================
# Load Data
# ==========================================================

df = load_view(
    "vw_SalesSimulator"
)


if df.empty:

    st.warning(
        "No simulation data available."
    )

    st.stop()



# ==========================================================
# Sidebar Parameters
# ==========================================================

st.sidebar.header(
    "Simulation Parameters"
)


category = st.sidebar.selectbox(
    "Category",
    df["Category"].unique()
)


product = st.sidebar.selectbox(

    "Product",

    df[
        df["Category"] == category
    ]["ProductName"].unique()

)


country = st.sidebar.selectbox(
    "Country",
    df["Country"].unique()
)


income_segment = st.sidebar.selectbox(
    "Income Segment",
    df["IncomeSegment"].unique()
)


quantity_change = st.sidebar.slider(
    "Quantity Change %",
    -50,
    200,
    0
)


discount = st.sidebar.slider(
    "Discount %",
    0,
    50,
    0
)



# ==========================================================
# Select Scenario Data
# ==========================================================

selected = df[

    (df["Category"] == category)
    &
    (df["ProductName"] == product)
    &
    (df["Country"] == country)
    &
    (df["IncomeSegment"] == income_segment)

]



# Default Values

current_quantity = 0

current_revenue = 0
current_cost = 0
current_profit = 0
current_margin = 0


revenue = 0
cost = 0
profit = 0
margin = 0



# ==========================================================
# Calculations
# ==========================================================

if not selected.empty:


    current_quantity = (
        selected["AvgQuantity"]
        .iloc[0]
    )


    unit_price = (
        selected["AvgUnitPrice"]
        .iloc[0]
    )


    unit_cost = (
        selected["AvgUnitCost"]
        .iloc[0]
    )


    # --------------------------
    # Current Scenario
    # --------------------------

    current_revenue = (
        current_quantity *
        unit_price
    )


    current_cost = (
        current_quantity *
        unit_cost
    )


    current_profit = (
        current_revenue -
        current_cost
    )


    current_margin = (

        current_profit /
        current_revenue

        if current_revenue
        else 0

    )



    # --------------------------
    # Simulation Scenario
    # --------------------------

    simulation_quantity = (

        current_quantity *
        (1 + quantity_change / 100)

    )


    revenue = (

        simulation_quantity *
        unit_price *
        (1 - discount / 100)

    )


    cost = (

        simulation_quantity *
        unit_cost

    )


    profit = (

        revenue -
        cost

    )


    margin = (

        profit /
        revenue

        if revenue
        else 0

    )

    # --------------------------
    # Profit Per Unit Analysis
    # --------------------------

    current_profit_per_unit = (

        current_profit /
        current_quantity

        if current_quantity
        else 0

    )


    simulation_profit_per_unit = (

        profit /
        simulation_quantity

        if simulation_quantity
        else 0

    )


    profit_unit_change = (

        simulation_profit_per_unit -
        current_profit_per_unit

    )

# ==========================================================
# Simulation KPIs
# ==========================================================

show_kpi_row(

    [

        (
            "Expected Quantity",
            f"{simulation_quantity:.1f}"
        ),

        (
            "Expected Revenue",
            format_currency(revenue)
        ),

        (
            "Expected Cost",
            format_currency(cost)
        ),

        (
            "Expected Profit",
            format_currency(profit)
        ),

        (
            "Profit Margin",
            format_percent(margin)
        ),

    ]

)

divider()

# ==========================================================
# Current vs Simulation
# ==========================================================

show_summary(

    left_title="Current Scenario",

    left_items={

    "Revenue":
        format_currency(current_revenue),

    "Profit":
        format_currency(current_profit),

    "Profit Per Unit":
        format_currency(current_profit_per_unit),

    "Margin":
        format_percent(current_margin),

     },


    right_title="Simulation Scenario",

    right_items={

    "Revenue":
        format_currency(revenue),

    "Profit":
        format_currency(profit),

    "Profit Per Unit":
        format_currency(simulation_profit_per_unit),

    "Margin":
        format_percent(margin),

     },

)

divider()

# ==========================================================
# Impact Analysis
# ==========================================================


revenue_change = (

    (revenue - current_revenue)
    /
    current_revenue

    if current_revenue
    else 0

)


profit_change = (

    (profit - current_profit)
    /
    current_profit

    if current_profit
    else 0

)


margin_change = round(
    margin - current_margin,
    4
)

if abs(margin_change) < 0.0001:
    margin_change = 0



show_kpi_row(

    [

        (
            "Revenue Change",
            format_percent(revenue_change)
        ),

        (
            "Profit Change",
            format_percent(profit_change)
        ),

        (
            "Margin Change",
            format_percent(margin_change)
        ),

        (
            "Profit / Unit Impact",
            format_currency(profit_unit_change)
        ),

    ]

)



divider()



# ==========================================================
# Business Recommendation
# ==========================================================


if profit_change > 0 and margin_change >= -0.001:

    insight = (
        "Recommended scenario. "
        "Profit increased while maintaining profitability."
    )


elif profit_change > 0 and margin_change < -0.001:

    insight = (
        "Revenue increased, but margin decreased. "
        "Review pricing or discount strategy."
    )


else:

    insight = (
        "Scenario is not attractive. "
        "Consider changing quantity or discount."
    )



if profit_change > 0:

    st.success(insight)

else:

    st.warning(insight)
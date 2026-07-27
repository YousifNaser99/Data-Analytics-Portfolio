import streamlit as st

from utils.connection import load_view

from utils.helpers import (
    divider,
    has_data,
    format_currency,
    format_number,
    format_percent,
    last_refresh,
)

from utils.charts import (
    line_chart,
    horizontal_bar,
    donut_chart,
)

# =========================================================
# Page Header
# =========================================================

st.markdown(
    """
    <div class="page-header">

    <h1>📈 Executive Dashboard</h1>

    <p>
    Business Performance Overview
    </p>

    </div>
    """,
    unsafe_allow_html=True
)

divider()

# =========================================================
# Load Data
# =========================================================

kpi = load_view("vw_ExecutiveKPI")
monthly = load_view("vw_MonthlyPerformance")
territory = load_view("vw_TerritoryPerformance")
category = load_view("vw_CategoryPerformance")
products = load_view("vw_ProductPerformance")

# =========================================================
# Validation
# =========================================================

if not has_data(kpi):

    st.error("Unable to load Executive KPI data.")

    st.stop()

if not has_data(monthly):

    st.warning("Monthly Performance data is unavailable.")

if not has_data(territory):

    st.warning("Territory Performance data is unavailable.")

if not has_data(category):

    st.warning("Category Performance data is unavailable.")

if not has_data(products):

    st.warning("Product Performance data is unavailable.")

# =========================================================
# KPI Row
# =========================================================

kpi_row = kpi.iloc[0]

# =========================================================
# KPI Cards
# =========================================================

c1, c2, c3, c4, c5, c6 = st.columns(6)

with c1:

    st.metric(
        "Revenue",
        format_currency(kpi_row["Revenue"])
    )

with c2:

    st.metric(
        "Profit",
        format_currency(kpi_row["Profit"])
    )

with c3:

    st.metric(
        "Units Sold",
        format_number(kpi_row["UnitsSold"])
    )

with c4:

    st.metric(
        "Orders",
        format_number(kpi_row["Orders"])
    )

with c5:

    st.metric(
        "Profit Margin",
        format_percent(kpi_row["GrossMargin"])
    )

with c6:

    st.metric(
        "Average Order Value",
        format_currency(
            kpi_row["AverageOrderValue"]
        )
    )

divider()

# =========================================================
# Monthly Revenue Trend
# =========================================================

if has_data(monthly):

    if {
        "CalendarYear",
        "MonthNumberOfYear"
    }.issubset(monthly.columns):

        monthly = monthly.sort_values(
            [
                "CalendarYear",
                "MonthNumberOfYear"
            ]
        )

left, right = st.columns([2, 1])

with left:

    if has_data(monthly):

        monthly_trend = (
            monthly
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


        fig = line_chart(
            monthly_trend,
            x="Period",
            y="Revenue",
            title="Monthly Revenue Trend"
        )


        st.plotly_chart(
            fig,
            width="stretch"
        )


with right:

    if has_data(category):

        fig = donut_chart(
            category,
            names="Category",
            values="Revenue",
            title="Revenue by Category"
        )

        st.plotly_chart(
            fig,
            width="stretch"
        )


divider()

# =========================================================
# Revenue by Country
# =========================================================

if has_data(territory):

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
# Top Tables
# =========================================================

left, right = st.columns(2)

with left:

    st.subheader("Top Categories")

    if has_data(category):

        st.dataframe(
            category.sort_values(
                "Revenue",
                ascending=False
            ).head(10),
            width="stretch",
            hide_index=True
        )

with right:

    st.subheader("Top Products")

    if has_data(products):

        st.dataframe(
            products.sort_values(
                "Revenue",
                ascending=False
            ).head(10),
            width="stretch",
            hide_index=True
        )

divider()

# =========================================================
# Dashboard Summary
# =========================================================

st.subheader("Executive Summary")

st.info(
    f"""
**Total Revenue:** {format_currency(kpi_row['Revenue'])}

**Total Profit:** {format_currency(kpi_row['Profit'])}

**Profit Margin:** {format_percent(kpi_row['GrossMargin'])}

This dashboard provides a high-level overview of overall business performance,
including sales trends, geographical performance, and product category contribution.
"""
)

divider()

# =========================================================
# Footer
# =========================================================

last_refresh()

st.caption(
    "Sales Analytics Platform • Executive Dashboard"
)

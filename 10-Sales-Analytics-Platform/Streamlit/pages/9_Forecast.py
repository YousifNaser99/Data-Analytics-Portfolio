import streamlit as st
import pandas as pd

from prophet import Prophet
import plotly.graph_objects as go

from utils.connection import load_view

from utils.helpers import (
    page_title,
    divider,
    format_currency,
    format_number,
)

from utils.dashboard_helpers import (
    validate_dashboard,
    show_kpi_row,
)


# ==========================================================
# Header
# ==========================================================

page_title(
    "🔮 Sales Forecast",
    "Revenue Forecasting using Prophet"
)

divider()


# ==========================================================
# Forecast Limitation Notice
# ==========================================================

st.warning(
    """
⚠️ Forecast Limitation

Forecasts are generated from historical data ending in 2004
and are intended for demonstration purposes only.

Results represent historical trend scenarios and should not be
considered as actual business predictions.
"""
)

divider()


# ==========================================================
# Load Data
# ==========================================================

df = load_view(
    "vw_MonthlyPerformance"
)


validate_dashboard(
    df,
    "Monthly performance data could not be loaded."
)


# ==========================================================
# Prepare Dataset
# ==========================================================

MONTHS = {

    "January":1,
    "February":2,
    "March":3,
    "April":4,
    "May":5,
    "June":6,
    "July":7,
    "August":8,
    "September":9,
    "October":10,
    "November":11,
    "December":12,

}


df["Month"] = df["MonthName"].map(MONTHS)


df["ds"] = pd.to_datetime(

    dict(
        year=df["CalendarYear"],
        month=df["Month"],
        day=1
    )

)


forecast_df = (

    df.groupby(
        "ds",
        as_index=False
    )
    ["Revenue"]
    .sum()
    .rename(
        columns={
            "Revenue":"y"
        }
    )

)


# ==========================================================
# Sidebar
# ==========================================================

with st.sidebar:

    st.header(
        "Forecast Settings"
    )


    future_months = st.slider(

        "Forecast Months",

        min_value=3,

        max_value=24,

        value=12,

    )


divider()


# ==========================================================
# Prophet Model
# ==========================================================


@st.cache_resource

def train_model(data):

    model = Prophet(
        yearly_seasonality=True
    )

    model.fit(data)

    return model



model = train_model(
    forecast_df
)


future = model.make_future_dataframe(

    periods=future_months,

    freq="MS"

)


forecast = model.predict(
    future
)


# ==========================================================
# Metrics
# ==========================================================


historical = forecast_df["y"].sum()


forecast_revenue = (

    forecast
    .tail(future_months)
    ["yhat"]
    .sum()

)


best_month = (

    forecast
    .tail(future_months)
    .loc[
        forecast.tail(future_months)["yhat"].idxmax()
    ]

)


worst_month = (

    forecast
    .tail(future_months)
    .loc[
        forecast.tail(future_months)["yhat"].idxmin()
    ]

)



# ==========================================================
# KPI Cards
# ==========================================================


show_kpi_row(

    [

        (
            "Historical Revenue",
            format_currency(historical)
        ),

        (
            "Forecast Revenue",
            format_currency(forecast_revenue)
        ),

        (
            "Forecast Months",
            format_number(future_months)
        ),

        (
            "Model",
            "Prophet"
        ),

    ]

)


divider()
# ==========================================================
# Actual vs Forecast Comparison
# ==========================================================

comparison = forecast[
    [
        "ds",
        "yhat"
    ]
].copy()


comparison = comparison.merge(
    forecast_df,
    on="ds",
    how="left"
)


comparison.columns = [
    "Date",
    "Forecast",
    "Actual"
]


comparison["Variance %"] = (

    (
        comparison["Forecast"]
        -
        comparison["Actual"]
    )

    /

    comparison["Actual"]

    * 100

).fillna(0)


# ==========================================================
# Forecast Chart
# ==========================================================

forecast_fig = go.Figure()


forecast_fig.add_trace(

    go.Scatter(

        x=forecast_df["ds"],

        y=forecast_df["y"],

        mode="lines+markers",

        name="Actual"

    )

)


forecast_fig.add_trace(

    go.Scatter(

        x=forecast["ds"],

        y=forecast["yhat"],

        mode="lines",

        name="Forecast"

    )

)


forecast_fig.update_layout(

    title="Actual Revenue vs Forecast Revenue",

    xaxis_title="Date",

    yaxis_title="Revenue"

)


st.plotly_chart(

    forecast_fig,

    width="stretch",

)


divider()


# ==========================================================
# Confidence Interval
# ==========================================================

interval_fig = go.Figure()


interval_fig.add_trace(

    go.Scatter(

        x=forecast["ds"],

        y=forecast["yhat_upper"],

        mode="lines",

        name="Upper Bound"

    )

)


interval_fig.add_trace(

    go.Scatter(

        x=forecast["ds"],

        y=forecast["yhat_lower"],

        mode="lines",

        fill="tonexty",

        name="Lower Bound"

    )

)


interval_fig.update_layout(

    title="Forecast Confidence Interval",

    xaxis_title="Date",

    yaxis_title="Revenue"

)


st.plotly_chart(

    interval_fig,

    width="stretch",

)


divider()


# ==========================================================
# Trend Component
# ==========================================================

trend_fig = go.Figure()


trend_fig.add_trace(

    go.Scatter(

        x=forecast["ds"],

        y=forecast["trend"],

        mode="lines",

        name="Trend"

    )

)


trend_fig.update_layout(

    title="Trend Component"

)


st.plotly_chart(

    trend_fig,

    width="stretch",

)


divider()


# ==========================================================
# Seasonality Component
# ==========================================================

if "yearly" in forecast.columns:


    seasonality_fig = go.Figure()


    seasonality_fig.add_trace(

        go.Scatter(

            x=forecast["ds"],

            y=forecast["yearly"],

            mode="lines",

            name="Yearly Seasonality"

        )

    )


    seasonality_fig.update_layout(

        title="Yearly Seasonality"

    )


    st.plotly_chart(

        seasonality_fig,

        width="stretch",

    )


    divider()
from utils.dashboard_helpers import (
    show_table,
    show_summary,
)


# ==========================================================
# Forecast Tables
# ==========================================================


forecast_table = forecast[
    [
        "ds",
        "yhat",
        "yhat_lower",
        "yhat_upper",
    ]
].copy()


forecast_table.columns = [

    "Date",

    "Forecast Revenue",

    "Lower Bound",

    "Upper Bound",

]


# ==========================================================
# Growth Analysis
# ==========================================================


future_data = forecast.tail(
    future_months
).copy()


future_data["Growth %"] = (

    future_data["yhat"]
    .pct_change()
    * 100

).fillna(0)



growth_table = future_data[

    [
        "ds",
        "yhat",
        "Growth %",
    ]

].copy()


growth_table.columns = [

    "Date",

    "Forecast Revenue",

    "Growth %",

]



# ==========================================================
# Display Forecast Details
# ==========================================================


show_table(

    forecast_table,

    title="Forecast Details",

    height=400,

)


divider()



show_table(

    growth_table,

    title="Forecast Growth Analysis",

    height=350,

)


divider()



# ==========================================================
# AI Business Insight
# ==========================================================


average_growth = (

    future_data["Growth %"]

    .mean()

)



trend = (

    "Increasing 📈"

    if average_growth >= 0

    else "Decreasing 📉"

)



highest_month = future_data.loc[

    future_data["yhat"].idxmax()

]


lowest_month = future_data.loc[

    future_data["yhat"].idxmin()

]



st.subheader(
    "🤖 AI Business Insight"
)



insight = f"""

The forecast indicates a **{trend}**

over the next **{future_months} months**.



Expected average change:

**{average_growth:.2f}%**



Highest projected revenue month:

**{highest_month['ds'].strftime('%B %Y')}**



Lowest projected revenue month:

**{lowest_month['ds'].strftime('%B %Y')}**



This forecast is generated using historical sales patterns

and should be used as a scenario planning tool.

"""



st.info(insight)



divider()



# ==========================================================
# Forecast Summary
# ==========================================================


show_summary(

    left_title="Forecast Highlights",

    left_items={


        "Highest Forecast":

            format_currency(
                best_month["yhat"]
            ),


        "Best Month":

            best_month["ds"]
            .strftime("%B %Y"),


        "Lowest Forecast":

            format_currency(
                worst_month["yhat"]
            ),


        "Worst Month":

            worst_month["ds"]
            .strftime("%B %Y"),


    },


    right_title="Growth Overview",

    right_items={


        "Average Growth":

            f"{average_growth:.2f}%",


        "Trend":

            trend,


        "Forecast Horizon":

            f"{future_months} Months",


        "Algorithm":

            "Prophet",


    }

)


divider()
from utils.dashboard_helpers import (
    show_export_button,
    show_footer,
)


# ==========================================================
# Export Forecast Report
# ==========================================================

show_export_button(

    dataframe=forecast_table,

    filename="Sales_Forecast_Report",

    label="📥 Download Forecast Report"

)


divider()


# ==========================================================
# Export Actual vs Forecast
# ==========================================================

show_export_button(

    dataframe=comparison,

    filename="Actual_vs_Forecast_Report",

    label="📥 Download Actual vs Forecast"

)


divider()


# ==========================================================
# Footer
# ==========================================================

show_footer(

    records=len(forecast_df),

    Historical_Records=len(forecast_df),

    Forecast_Months=future_months,

    Forecast_Records=len(forecast),

    Model="Prophet",

)
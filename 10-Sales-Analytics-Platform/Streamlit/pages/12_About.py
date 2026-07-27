import streamlit as st

from utils.helpers import (
    page_title,
    divider,
)

from utils.dashboard_helpers import (
    show_kpi_row,
    show_summary,
    show_table,
    show_footer,
)

page_title(

    "ℹ️ About This Project",

    "Enterprise Sales Analytics Platform"

)

divider()

st.markdown("""

# 📊 Sales Analytics Platform

A complete end-to-end Business Intelligence solution built with
Python, SQL Server, Streamlit, Plotly and modern BI practices.

The project transforms transactional sales data into executive dashboards,
AI-powered insights, forecasting models and interactive reports.

""")

divider()

show_kpi_row(

    [

        ("Dashboards", "11"),

        ("SQL Views", "12"),

        ("DAX Measures", "100+"),

        ("Visualizations", "70+"),

        ("Forecasting", "Prophet"),

    ]

)

divider()

tech = {

    "Backend":

        "Python · SQL Server",

    "Visualization":

        "Streamlit · Plotly",

    "Analytics":

        "Pandas · NumPy",

    "Business Intelligence":

        "Star Schema · SQL Views",

    "Machine Learning":

        "Prophet Forecasting",

    "Decision Intelligence":

        "AI Insights Engine",

}

show_summary(

    left_title="Technology Stack",

    left_items=tech,

    right_title="Architecture",

    right_items={

        "Database":"SQL Server",

        "Model":"Star Schema",

        "Dashboards":"11",

        "Deployment":"Streamlit",

    }

)

divider()

dashboards = [

    {

        "Dashboard":"Executive",

        "Purpose":"Executive KPIs"

    },

    {

        "Dashboard":"Sales",

        "Purpose":"Sales Performance"

    },

    {

        "Dashboard":"Customer",

        "Purpose":"Customer Analytics"

    },

    {

        "Dashboard":"Financial",

        "Purpose":"Financial KPIs"

    },

    {

        "Dashboard":"Operations",

        "Purpose":"Operations Metrics"

    },

    {

        "Dashboard":"Product",

        "Purpose":"Product Analytics"

    },

    {

        "Dashboard":"Time Intelligence",

        "Purpose":"YoY / MoM / Running Total"

    },

    {

        "Dashboard":"Market Basket",

        "Purpose":"Association Rules"

    },

    {

        "Dashboard":"Forecast",

        "Purpose":"Sales Forecast"

    },

    {

        "Dashboard":"AI Insights",

        "Purpose":"Decision Intelligence"

    },

    {

        "Dashboard":"Reports",

        "Purpose":"Download Center"

    }

]

show_table(

    dashboards,

    title="Available Dashboards",

    height=420,

)

divider()

features = {

    "Business KPIs":"✔",

    "Forecasting":"✔",

    "AI Insights":"✔",

    "Customer Analytics":"✔",

    "Financial Analytics":"✔",

    "Product Analytics":"✔",

    "Market Basket":"✔",

    "CSV Export":"✔",

    "Interactive Filters":"✔",

    "Decision Support":"✔",

}

show_summary(

    left_title="Platform Features",

    left_items=features,

    right_title="Project Level",

    right_items={

        "Type":"Portfolio",

        "Category":"Business Intelligence",

        "Status":"Completed",

        "Version":"1.0",

    }

)

divider()

st.subheader("Project Architecture")

st.code("""
Excel / CSV
      │
      ▼
Python (Cleaning)
      │
      ▼
SQL Server
      │
      ▼
Star Schema
      │
      ▼
SQL Views
      │
      ▼
Streamlit
      │
      ▼
Interactive Dashboards
      │
      ▼
AI Insights & Forecast
""", language="text")

show_footer(

    Version="1.0",

    Dashboards=11,

    Database="SQL Server",

    Framework="Streamlit",

)
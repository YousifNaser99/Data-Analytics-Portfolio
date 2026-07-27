"""
=========================================================
Sales Analytics Platform

Author : Youssef Naser
=========================================================
"""

from pathlib import Path

import streamlit as st

from utils.connection import load_view

from utils.helpers import (
    divider,
    format_currency,
    format_number,
    last_refresh,
)


# =========================================================
# Constants
# =========================================================

APP_NAME = "Sales Analytics Platform"

APP_SUBTITLE = (
    "AdventureWorks Business Intelligence Platform"
)


CSS_PATH = Path(
    "assets/css/style.css"
)


LOGO_PATH = Path(
    "assets/images/logo.png"
)



# =========================================================
# Page Config
# =========================================================

st.set_page_config(

    page_title=APP_NAME,

    page_icon="📊",

    layout="wide",

    initial_sidebar_state="expanded"

)



# =========================================================
# Load CSS
# =========================================================

@st.cache_resource
def load_css():

    if CSS_PATH.exists():

        st.markdown(

            f"""
            <style>
            {CSS_PATH.read_text(
                encoding="utf-8"
            )}
            </style>
            """,

            unsafe_allow_html=True

        )


load_css()



# =========================================================
# Sidebar
# =========================================================

with st.sidebar:


    if LOGO_PATH.exists():

        st.image(
            str(LOGO_PATH),
            width="stretch"
        )


    st.markdown(
        f"""
        ## 📊 {APP_NAME}
        """
    )


    st.caption(
        APP_SUBTITLE
    )


    divider()


    st.markdown(
        """
        ### Navigation

        Explore Analytics Modules:

        📈 Sales Analytics  
        👥 Customer Insights  
        💰 Financial Analysis  
        ⚙ Operations Analytics  
        📦 Product Intelligence  
        📅 Time Intelligence  
        🛒 Market Basket  
        🔮 Forecasting  
        🤖 AI Insights  
        """
    )


    divider()


    st.success(
        "Version 1.0"
    )


    last_refresh()



# =========================================================
# Load KPI
# =========================================================

executive = load_view(
    "vw_ExecutiveKPI"
)


if executive.empty:

    st.error(
        "Unable to load Executive KPIs."
    )

    st.stop()



kpi = executive.iloc[0]



# =========================================================
# Hero Section
# =========================================================

st.markdown(
    """
    # 📊 Sales Analytics Platform

    ### Business Intelligence & Decision Support System

    Explore business performance, customer behavior,
    profitability analysis, operational efficiency,
    and predictive insights.
    """
)


divider()



# =========================================================
# KPI Overview
# =========================================================

st.subheader(
    "Business Overview"
)


c1,c2,c3,c4 = st.columns(4)



with c1:

    st.metric(

        "💰 Revenue",

        format_currency(
            kpi["Revenue"]
        )

    )



with c2:

    st.metric(

        "📈 Profit",

        format_currency(
            kpi["Profit"]
        )

    )



with c3:

    st.metric(

        "🛒 Orders",

        format_number(
            kpi["Orders"]
        )

    )



with c4:

    st.metric(

        "📦 Units Sold",

        format_number(
            kpi["UnitsSold"]
        )

    )



divider()



# =========================================================
# Platform Overview
# =========================================================


left,right = st.columns(
    [2,1]
)



with left:


    st.subheader(
        "About The Platform"
    )


    st.markdown(
        """
        This platform provides a complete
        Business Intelligence solution built using:

        ### Analytics Modules

        ✅ Executive Dashboard  
        ✅ Sales Analytics  
        ✅ Customer Analytics  
        ✅ Financial Analytics  
        ✅ Operations Analytics  
        ✅ Product Intelligence  
        ✅ Time Intelligence  
        ✅ Market Basket Analysis  
        ✅ Forecasting  
        ✅ AI Insights  


        ### Technology Stack

        🗄 SQL Server  

        🐍 Python  

        📊 Streamlit  

        📈 Plotly  

        🐼 Pandas  
        """
    )



with right:


    st.subheader(
        "Project Statistics"
    )


    st.metric(
        "Dashboards",
        "11"
    )


    st.metric(
        "SQL Views",
        "8"
    )


    st.metric(
        "Database",
        "AdventureWorksDW"
    )


    st.metric(
        "Framework",
        "Streamlit"
    )



divider()



# =========================================================
# Dashboard Cards
# =========================================================


st.subheader(
    "Available Analytics"
)



dashboards = [

    ("📈 Executive",
     "Business Overview",
     "card-executive"),


    ("💰 Sales",
     "Revenue & Profit Analysis",
     "card-sales"),


    ("👥 Customers",
     "Customer Behavior",
     "card-customer"),


    ("🏦 Financial",
     "Cost & Margin",
     "card-financial"),


    ("⚙ Operations",
     "Efficiency Analysis",
     "card-operations"),


    ("📦 Products",
     "Product Performance",
     "card-product"),


    ("📅 Time Intelligence",
     "Trends & Growth",
     "card-time"),


    ("🛒 Market Basket",
     "Recommendations",
     "card-market"),


    ("🔮 Forecast",
     "Future Prediction",
     "card-forecast"),


    ("🤖 AI Insights",
     "Smart Analytics",
     "card-ai"),

    ("🎯 Sales Simulator",
     "Scenario Planning & Profit Simulation",
     "card-simulator"),


    ("📄 Reports",
     "Export Center",
     "card-report"),

]



cols = st.columns(3)



for index,(title,desc,css_class) in enumerate(dashboards):

    with cols[index % 3]:

        st.markdown(
            f"""
             <div class="dashboard-card {css_class}">
             <h2>{title}</h2>
             <p>{desc}</p>
             </div>
             """,
            unsafe_allow_html=True
        )


divider()


# =========================================================
# Footer
# =========================================================


st.caption(
    "Developed with ❤️ using SQL Server, Python, Streamlit and Plotly"
)
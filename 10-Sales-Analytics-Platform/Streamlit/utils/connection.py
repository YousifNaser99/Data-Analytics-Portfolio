# utils/connection.py

import pandas as pd
import streamlit as st
from sqlalchemy import create_engine, text

# ============================================
# SQL Server Configuration
# ============================================

SERVER = "localhost"
DATABASE = "AdventureWorksDW"
DRIVER = "ODBC Driver 17 for SQL Server"

CONNECTION_STRING = (
    f"mssql+pyodbc://@{SERVER}/{DATABASE}"
    f"?driver={DRIVER.replace(' ', '+')}"
    "&trusted_connection=yes"
)

# ============================================
# Engine
# ============================================

@st.cache_resource
def get_engine():
    return create_engine(
        CONNECTION_STRING,
        pool_pre_ping=True,
        pool_recycle=3600,
    )

# ============================================
# Generic View Loader
# ============================================

@st.cache_data(show_spinner=False)
def load_view(view_name: str) -> pd.DataFrame:
    try:
        query = text(f"SELECT * FROM {view_name}")

        return pd.read_sql(
            query,
            get_engine()
        )

    except Exception as e:
        st.error(f"Failed to load view '{view_name}'.")
        st.exception(e)
        return pd.DataFrame()

# ============================================
# Custom SQL Loader
# ============================================

@st.cache_data(show_spinner=False)
def load_query(query: str) -> pd.DataFrame:
    try:
        return pd.read_sql(
            text(query),
            get_engine()
        )

    except Exception as e:
        st.error("Failed to execute SQL query.")
        st.exception(e)
        return pd.DataFrame()

# ============================================
# Cache Helper
# ============================================

def clear_cache():
    st.cache_data.clear()
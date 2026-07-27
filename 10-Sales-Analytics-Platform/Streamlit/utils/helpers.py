"""
=========================================================
Sales Analytics Platform
Helpers Module

Author : Youssef Naser
=========================================================
"""

from datetime import datetime

import pandas as pd
import streamlit as st


# =========================================================
# Currency Formatting
# =========================================================

def format_currency(value: float) -> str:
    """
    Format numeric values as currency.
    """

    if pd.isna(value):
        return "$0"

    if abs(value) >= 1_000_000_000:
        return f"${value / 1_000_000_000:.2f}B"

    if abs(value) >= 1_000_000:
        return f"${value / 1_000_000:.2f}M"

    if abs(value) >= 1_000:
        return f"${value / 1_000:.2f}K"

    return f"${value:,.2f}"


# =========================================================
# Number Formatting
# =========================================================

def format_number(value: float) -> str:
    """
    Format integer values with thousand separators.
    """

    if pd.isna(value):
        return "0"

    return f"{round(value):,}"


# =========================================================
# Percentage Formatting
# =========================================================

def format_percent(value: float) -> str:
    """
    Format percentage values.

    Supports both:
        0.25 -> 25%
        25   -> 25%
    """

    if pd.isna(value):
        return "0%"

    if abs(value) > 1:
        value /= 100

    return f"{value:.2%}"


# =========================================================
# Page Title
# =========================================================

def page_title(title: str, subtitle: str = "") -> None:

    st.title(title)

    st.caption(subtitle)


# =========================================================
# Section Title
# =========================================================

def section_title(title: str) -> None:
    """
    Display section title.
    """

    st.markdown(
        f"""
        <h3 style="
            margin-top:20px;
            margin-bottom:15px;
            font-weight:600;
        ">
            {title}
        </h3>
        """,
        unsafe_allow_html=True,
    )


# =========================================================
# Divider
# =========================================================

def divider() -> None:
    """
    Display section divider.
    """

    st.divider()


# =========================================================
# Last Refresh
# =========================================================

def last_refresh() -> None:
    """
    Display current refresh timestamp.
    """

    st.caption(
        f"Last Refresh: {datetime.now().strftime('%d %b %Y - %I:%M %p')}"
    )


# =========================================================
# Empty Data Message
# =========================================================

def empty_message(message: str = "No data available.") -> None:
    """
    Display warning when dataframe is empty.
    """

    st.warning(message)


# =========================================================
# DataFrame Validation
# =========================================================

def has_data(df: pd.DataFrame) -> bool:
    """
    Check whether dataframe contains data.
    """

    return df is not None and not df.empty


# =========================================================
# CSV Export
# =========================================================

def dataframe_to_csv(df: pd.DataFrame) -> bytes:
    """
    Convert dataframe to CSV bytes.
    """

    return df.to_csv(index=False).encode("utf-8")


# =========================================================
# Export Filename
# =========================================================

def export_filename(
    prefix: str,
    extension: str = "csv"
) -> str:
    """
    Generate export filename.
    """

    timestamp = datetime.now().strftime("%Y%m%d_%H%M")

    return f"{prefix}_{timestamp}.{extension}"


# =========================================================
# Performance Color
# =========================================================

def performance_color(value: float) -> str:
    """
    Return color based on KPI performance.
    """

    if pd.isna(value):
        return "#9CA3AF"

    if value >= 0.50:
        return "#10B981"

    if value >= 0.30:
        return "#F59E0B"

    return "#EF4444"
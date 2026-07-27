import streamlit as st
import pandas as pd
import math
from utils.helpers import (
    has_data,
    dataframe_to_csv,
    export_filename,
    last_refresh,
)

# ==========================================================
# Dashboard Validation
# ==========================================================

def validate_dashboard(
    df: pd.DataFrame,
    message: str = "No data available."
) -> None:
    """
    Validate dashboard dataframe.
    """

    if not has_data(df):

        st.error(message)

        st.stop()


# ==========================================================
# Data Table
# ==========================================================

def show_table(
    dataframe: pd.DataFrame,
    title: str,
    height: int = 350,
) -> None:
    """
    Display dataframe.
    """

    st.subheader(title)

    st.dataframe(
        dataframe,
        width="stretch",
        hide_index=True,
        height=height,
    )


# ==========================================================
# Export Button
# ==========================================================

def show_export_button(
    dataframe: pd.DataFrame,
    filename: str,
    label: str = "📥 Download Report",
):
    """
    Export dataframe to csv.
    """

    st.download_button(
        label=label,
        data=dataframe_to_csv(dataframe),
        file_name=export_filename(filename),
        mime="text/csv",
        width="stretch",
    )
    import math
import streamlit as st

# ==========================================================
# KPI Cards
# ==========================================================

def show_kpi_row(
    metrics: list[tuple[str, str]],
) -> None:
    """
    Display KPI cards dynamically.

    Example
    -------
    show_kpi_row([
        ("Revenue", "$1.2M"),
        ("Profit", "$320K"),
        ("Margin", "26.7%"),
        ("Orders", "18,250"),
    ])
    """

    if not metrics:
        return

    cols = st.columns(len(metrics))

    for col, (label, value) in zip(cols, metrics):

        with col:

            st.metric(
                label=label,
                value=value,
            )


# ==========================================================
# Summary Cards
# ==========================================================

def show_summary(
    left_title: str,
    left_items: dict,
    right_title: str,
    right_items: dict,
) -> None:
    """
    Display executive summary.

    Example
    -------
    show_summary(
        "Performance",
        {
            "Revenue": "$2.4M",
            "Profit": "$620K"
        },
        "Insights",
        {
            "Top Category": "Bikes",
            "Top Country": "United States"
        }
    )
    """

    col1, col2 = st.columns(2)

    with col1:

        markdown = f"### {left_title}\n\n"

        for key, value in left_items.items():

            markdown += f"- **{key}:** {value}\n"

        st.info(markdown)

    with col2:

        markdown = f"### {right_title}\n\n"

        for key, value in right_items.items():

            markdown += f"- **{key}:** {value}\n"

        st.success(markdown)


# ==========================================================
# Footer
# ==========================================================

def show_footer(
    records: int | None = None,
    **stats,
) -> None:

    last_refresh()

    footer = []

    if records is not None:
        footer.append(f"Records: {records:,}")

    for key, value in stats.items():

        if isinstance(value, (int, float)):

            if math.isfinite(value):

                footer.append(f"{key}: {value:,.0f}")

            else:

                footer.append(f"{key}: -")

        else:

            footer.append(f"{key}: {value}")

    st.caption(" • ".join(footer))
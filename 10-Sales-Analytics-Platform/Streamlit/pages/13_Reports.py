import streamlit as st
import pandas as pd

from utils.connection import load_view

from utils.helpers import (
    page_title,
    divider,
    format_number,
)

from utils.dashboard_helpers import (
    validate_dashboard,
    show_kpi_row,
    show_table,
    show_export_button,
    show_footer,
)

# ==========================================================
# Header
# ==========================================================

page_title(
    "📄 Reports Center",
    "Enterprise Report Download Center"
)

divider()

# ==========================================================
# Load Reports
# ==========================================================

@st.cache_data
def load_reports():

    return {

        "Executive KPI": load_view("vw_ExecutiveKPI"),

        "Sales Analysis": load_view("vw_SalesAnalysis"),

        "Customer Performance": load_view("vw_CustomerPerformance"),

        "Product Performance": load_view("vw_ProductPerformance"),

        "Category Performance": load_view("vw_CategoryPerformance"),

        "Territory Performance": load_view("vw_TerritoryPerformance"),

        "Monthly Performance": load_view("vw_MonthlyPerformance"),

    }


reports = load_reports()

validate_dashboard(
    reports["Executive KPI"],
    "Reports could not be loaded."
)

# ==========================================================
# Report Catalog
# ==========================================================

catalog = []

total_rows = 0

total_columns = 0

for name, df in reports.items():

    rows = len(df)

    cols = len(df.columns)

    total_rows += rows

    total_columns += cols

    catalog.append({

        "Report": name,

        "Rows": rows,

        "Columns": cols,

        "Status": "Ready"

    })

catalog = pd.DataFrame(catalog)

# ==========================================================
# KPI
# ==========================================================

show_kpi_row(

    [

        (

            "Reports",

            format_number(len(reports))

        ),

        (

            "Datasets",

            format_number(total_rows)

        ),

        (

            "Columns",

            format_number(total_columns)

        ),

        (

            "Status",

            "Ready"

        ),

    ]

)

divider()

show_table(

    catalog,

    title="Available Reports",

    height=340,

)

divider()

st.subheader("Report Preview")

selected = st.selectbox(

    "Choose Report",

    list(reports.keys())

)

preview = reports[selected]

show_table(

    preview.head(20),

    title=f"{selected} Preview",

    height=420,

)

show_export_button(

    dataframe=preview,

    filename=selected.replace(" ","_"),

    label=f"📥 Download {selected}"

)

divider()

statistics = {

    "Rows":

        format_number(len(preview)),

    "Columns":

        format_number(len(preview.columns)),

    "Missing Values":

        format_number(preview.isna().sum().sum()),

    "Duplicate Rows":

        format_number(preview.duplicated().sum()),

}

dataset = {

    "Dataset":

        selected,

    "Export":

        "CSV",

    "Encoding":

        "UTF-8",

    "Status":

        "Ready",

}

from utils.dashboard_helpers import show_summary

show_summary(

    left_title="Dataset Statistics",

    left_items=statistics,

    right_title="Export Information",

    right_items=dataset,

)

divider()

st.subheader("Bulk Export")

for report_name, dataframe in reports.items():

    show_export_button(

        dataframe=dataframe,

        filename=report_name.replace(" ","_"),

        label=f"⬇ {report_name}"

    )

show_footer(

    Reports=len(reports),

    Total_Rows=total_rows,

    Status="Ready",

)
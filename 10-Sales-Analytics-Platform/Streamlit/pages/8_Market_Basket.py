import streamlit as st
import pandas as pd

from utils.connection import load_view

from utils.helpers import (
    page_title,
    divider,
    format_number,
    format_percent,
)

from utils.dashboard_helpers import (
    validate_dashboard,
    show_kpi_row,
)

# ==========================================================
# Page Header
# ==========================================================

page_title(
    "🛒 Market Basket Analysis",
    "Association Rules & Product Affinity",
)

divider()

# ==========================================================
# Load Data
# ==========================================================

df = load_view("vw_MarketBasketAnalysis")

validate_dashboard(
    df,
    "Market Basket data could not be loaded."
)

# ==========================================================
# Sidebar
# ==========================================================

with st.sidebar:

    st.header("Association Filters")

    min_support = st.slider(
        "Minimum Support",
        min_value=0.0,
        max_value=float(df["Support"].max()),
        value=0.01,
        step=0.01,
    )

    min_confidence = st.slider(
        "Minimum Confidence",
        min_value=0.0,
        max_value=float(df["Confidence"].max()),
        value=0.10,
        step=0.01,
    )

    min_lift = st.slider(
        "Minimum Lift",
        min_value=0.0,
        max_value=float(df["Lift"].max()),
        value=1.0,
        step=0.10,
    )

    association = sorted(
        df["AssociationStrength"]
        .dropna()
        .unique()
    )

    selected_association = st.multiselect(
        "Association Strength",
        association,
        default=association,
    )

    divider()

    if st.button(
        "Reset Filters",
        width="stretch",
    ):
        st.rerun()

# ==========================================================
# Apply Filters
# ==========================================================

df = df[
    (df["Support"] >= min_support)
    &
    (df["Confidence"] >= min_confidence)
    &
    (df["Lift"] >= min_lift)
]


if selected_association:

    df = df[
        df["AssociationStrength"]
        .isin(selected_association)
    ]


validate_dashboard(
    df,
    "No rules match the selected filters."
)

# ==========================================================
# Cached Summary
# ==========================================================

@st.cache_data
def prepare_summary(data: pd.DataFrame):

    rules = len(data)

    avg_support = data["Support"].mean()

    avg_confidence = data["Confidence"].mean()

    avg_lift = data["Lift"].mean()

    unique_products = pd.concat(
        [
            data["ProductA"],
            data["ProductB"],
        ]
    ).nunique()

    return (
        rules,
        avg_support,
        avg_confidence,
        avg_lift,
        unique_products,
    )


(
    rules,
    avg_support,
    avg_confidence,
    avg_lift,
    unique_products,
) = prepare_summary(df)

# ==========================================================
# KPI Cards
# ==========================================================

show_kpi_row(

    [

        (
            "Rules",
            format_number(rules),
        ),

        (
            "Products",
            format_number(unique_products),
        ),

        (
            "Avg Support",
            format_percent(avg_support),
        ),

        (
            "Avg Confidence",
            format_percent(avg_confidence),
        ),

        (
            "Avg Lift",
            f"{avg_lift:.2f}",
        ),

    ]

)

divider()
from utils.charts import (
    bar_chart,
    horizontal_bar,
    donut_chart,
)

# ==========================================================
# Cached Chart Data
# ==========================================================

@st.cache_data
def prepare_charts(data: pd.DataFrame):

    top_rules = (
        data.sort_values("RuleRank")
        .head(15)
    )

    lift_distribution = (
        data.groupby(
            "LiftClass",
            as_index=False
        )
        .size()
        .rename(
            columns={
                "size": "Rules"
            }
        )
    )

    confidence_distribution = (
        data.groupby(
            "ConfidenceClass",
            as_index=False
        )
        .size()
        .rename(
            columns={
                "size": "Rules"
            }
        )
    )

    recommendation = (
        data.groupby(
            "AssociationStrength",
            as_index=False
        )
        .size()
        .rename(
            columns={
                "size": "Rules"
            }
        )
    )

    product_a = (
        data.groupby(
            "ProductA",
            as_index=False
        )
        .size()
        .rename(
            columns={
                "size": "Rules"
            }
        )
        .sort_values(
            "Rules",
            ascending=False
        )
        .head(15)
    )

    product_b = (
        data.groupby(
            "ProductB",
            as_index=False
        )
        .size()
        .rename(
            columns={
                "size": "Rules"
            }
        )
        .sort_values(
            "Rules",
            ascending=False
        )
        .head(15)
    )

    return (

        top_rules,

        lift_distribution,

        confidence_distribution,

        recommendation,

        product_a,

        product_b,

    )


(

    top_rules,

    lift_distribution,

    confidence_distribution,

    recommendation,

    product_a,

    product_b,

) = prepare_charts(df)

# ==========================================================
# Top Rules by Lift
# ==========================================================

fig = horizontal_bar(

    top_rules,

    x="Lift",

    y="Recommendation",

    title="Top Association Rules",

)

st.plotly_chart(

    fig,

    width="stretch",

)

divider()

# ==========================================================
# Support & Confidence
# ==========================================================

left, right = st.columns(2)

with left:

    fig = bar_chart(

        top_rules,

        x="ProductA",

        y="Support",

        title="Support",

    )

    st.plotly_chart(

        fig,

        width="stretch",

    )

with right:

    fig = bar_chart(

        top_rules,

        x="ProductA",

        y="Confidence",

        title="Confidence",

    )

    st.plotly_chart(

        fig,

        width="stretch",

    )

divider()

# ==========================================================
# Product Frequency
# ==========================================================

left, right = st.columns(2)

with left:

    fig = horizontal_bar(

        product_a,

        x="Rules",

        y="ProductA",

        title="Most Frequent Product A",

    )

    st.plotly_chart(

        fig,

        width="stretch",

    )

with right:

    fig = horizontal_bar(

        product_b,

        x="Rules",

        y="ProductB",

        title="Most Frequent Product B",

    )

    st.plotly_chart(

        fig,

        width="stretch",

    )

divider()

# ==========================================================
# Lift & Confidence Distribution
# ==========================================================

left, right = st.columns(2)

with left:

    fig = donut_chart(

        lift_distribution,

        names="LiftClass",

        values="Rules",

        title="Lift Distribution",

    )

    st.plotly_chart(

        fig,

        width="stretch",

    )

with right:

    fig = donut_chart(

        confidence_distribution,

        names="ConfidenceClass",

        values="Rules",

        title="Confidence Distribution",

    )

    st.plotly_chart(

        fig,

        width="stretch",

    )

divider()

# ==========================================================
# Association Strength
# ==========================================================

fig = donut_chart(

    recommendation,

    names="AssociationStrength",

    values="Rules",

    title="Association Strength",

)

st.plotly_chart(

    fig,

    width="stretch",

)

divider()
from utils.dashboard_helpers import (
    show_table,
    show_export_button,
    show_summary,
    show_footer,
)

# ==========================================================
# Association Rules Table
# ==========================================================

rules_table = (
    df.sort_values(
        "RuleRank"
    )
)

show_table(

    rules_table[
        [
            "RuleRank",
            "ProductA",
            "ProductB",
            "Support",
            "Confidence",
            "Lift",
            "AssociationStrength",
        ]
    ],

    "Association Rules",

    height=500,

)

divider()

# ==========================================================
# Export
# ==========================================================

show_export_button(

    dataframe=rules_table,

    filename="Market_Basket_Report",

    label="📥 Download Market Basket Report",

)

divider()

# ==========================================================
# Executive Summary
# ==========================================================

best_rule = rules_table.iloc[0]

strong_rules = (
    df["AssociationStrength"]
    == "Strong Association"
).sum()

moderate_rules = (
    df["AssociationStrength"]
    == "Moderate Association"
).sum()

weak_rules = (
    df["AssociationStrength"]
    == "Weak Association"
).sum()

show_summary(

    left_title="Association Metrics",

    left_items={

        "Rules": format_number(rules),

        "Products": format_number(unique_products),

        "Average Lift": f"{avg_lift:.2f}",

        "Average Confidence": format_percent(avg_confidence),

    },

    right_title="Top Rule",

    right_items={

        "Product A": best_rule["ProductA"],

        "Product B": best_rule["ProductB"],

        "Lift": f"{best_rule['Lift']:.2f}",

        "Support": format_percent(best_rule["Support"]),

    },

)

divider()

# ==========================================================
# Rule Quality
# ==========================================================

show_summary(

    left_title="Rule Quality",

    left_items={

        "Strong Rules": format_number(strong_rules),

        "Moderate Rules": format_number(moderate_rules),

        "Weak Rules": format_number(weak_rules),

    },

    right_title="Coverage",

    right_items={

        "Average Support": format_percent(avg_support),

        "Average Confidence": format_percent(avg_confidence),

        "Average Lift": f"{avg_lift:.2f}",

    },

)

divider()

# ==========================================================
# Footer
# ==========================================================

show_footer(

    records=len(df),

    Rules=len(df),

    Products=unique_products,

    Avg_Lift=f"{avg_lift:.2f}",

)
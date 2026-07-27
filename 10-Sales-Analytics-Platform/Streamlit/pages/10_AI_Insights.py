import streamlit as st
import pandas as pd

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
    show_summary,
)

# ==========================================================
# Header
# ==========================================================

page_title(
    "🤖 AI Insights",
    "AI-Powered Decision Intelligence"
)

divider()

# ==========================================================
# Load Data
# ==========================================================

sales = load_view("vw_ExecutiveKPI")
products = load_view("vw_ProductPerformance")
customers = load_view("vw_CustomerPerformance")
territory = load_view("vw_TerritoryPerformance")
category = load_view("vw_CategoryPerformance")

validate_dashboard(sales, "Executive KPI could not be loaded.")
validate_dashboard(products, "Product Performance could not be loaded.")
validate_dashboard(customers, "Customer Performance could not be loaded.")
validate_dashboard(territory, "Territory Performance could not be loaded.")
validate_dashboard(category, "Category Performance could not be loaded.")

# ==========================================================
# AI Engine
# ==========================================================

@st.cache_data
def prepare_ai_data(
    sales,
    products,
    customers,
    territory,
    category,
):

    revenue = sales.iloc[0]["Revenue"]
    profit = sales.iloc[0]["Profit"]
    orders = sales.iloc[0]["Orders"]
    units = sales.iloc[0]["UnitsSold"]
    margin = sales.iloc[0]["GrossMargin"]

    top_category = category.nlargest(1, "Revenue").iloc[0]

    top_country = territory.nlargest(1, "Revenue").iloc[0]

    top_product = products.nlargest(1, "Revenue").iloc[0]

    top_customer = customers.nlargest(1, "Revenue").iloc[0]

    return {

        "Revenue": revenue,

        "Profit": profit,

        "Orders": orders,

        "Units": units,

        "Margin": margin,

        "TopCategory": top_category,

        "TopCountry": top_country,

        "TopProduct": top_product,

        "TopCustomer": top_customer,

    }


ai = prepare_ai_data(
    sales,
    products,
    customers,
    territory,
    category,
)

# ==========================================================
# KPI Cards
# ==========================================================

show_kpi_row(

    [

        (
            "Revenue",
            format_currency(ai["Revenue"]),
        ),

        (
            "Profit",
            format_currency(ai["Profit"]),
        ),

        (
            "Orders",
            format_number(ai["Orders"]),
        ),

        (
            "Units",
            format_number(ai["Units"]),
        ),

        (
            "Margin",
            f'{ai["Margin"]:.2%}',
        ),

    ]

)

divider()

# ==========================================================
# Executive AI Summary
# ==========================================================

show_summary(

    left_title="Business Performance",

    left_items={

        "Revenue":
            format_currency(ai["Revenue"]),

        "Profit":
            format_currency(ai["Profit"]),

        "Orders":
            format_number(ai["Orders"]),

        "Units":
            format_number(ai["Units"]),

    },

    right_title="Top Performers",

    right_items={

        "Category":
            ai["TopCategory"]["Category"],

        "Country":
            ai["TopCountry"]["Country"],

        "Product":
            ai["TopProduct"]["ProductName"],

        "Customer":
            ai["TopCustomer"]["Name"],

    },

)

divider()
from utils.dashboard_helpers import (
    show_table,
)

# ==========================================================
# AI Scoring Engine
# ==========================================================

@st.cache_data
def calculate_scores(
    ai,
    products,
    customers,
    territory,
    category,
):

    revenue = ai["Revenue"]

    category_share = (
        ai["TopCategory"]["Revenue"] / revenue
    )

    country_share = (
        ai["TopCountry"]["Revenue"] / revenue
    )

    customer_share = (
        ai["TopCustomer"]["Revenue"] / revenue
    )

    product_share = (
        ai["TopProduct"]["Revenue"] / revenue
    )

    business_score = min(
        100,
        round(ai["Margin"] * 100 * 1.8)
    )

    concentration_score = max(
        0,
        round((1 - category_share) * 100)
    )

    customer_score = max(
        0,
        round((1 - customer_share) * 100)
    )

    market_score = max(
        0,
        round((1 - country_share) * 100)
    )

    portfolio_score = round(

        (
            products["Revenue"] >
            products["Revenue"].median()

        ).mean() * 100

    )

    risk_score = round(

        (
            concentration_score +
            customer_score +
            market_score
        ) / 3

    )

    return {

        "Business Health": business_score,

        "Revenue Diversification": concentration_score,

        "Customer Diversification": customer_score,

        "Market Diversification": market_score,

        "Portfolio Strength": portfolio_score,

        "Risk Score": risk_score,

    }


scores = calculate_scores(
    ai,
    products,
    customers,
    territory,
    category,
)

# ==========================================================
# AI Score Cards
# ==========================================================

show_kpi_row(

    [

        (
            "Business Health",
            f'{scores["Business Health"]}/100'
        ),

        (
            "Risk Score",
            f'{scores["Risk Score"]}/100'
        ),

        (
            "Portfolio",
            f'{scores["Portfolio Strength"]}/100'
        ),

        (
            "Market",
            f'{scores["Market Diversification"]}/100'
        ),

        (
            "Customer",
            f'{scores["Customer Diversification"]}/100'
        ),

    ]

)

divider()

# ==========================================================
# AI Alerts
# ==========================================================

@st.cache_data
def generate_alerts(ai, scores, products):

    alerts = []

    if ai["Margin"] >= 0.50:

        alerts.append(

            [

                "🟢",

                "Profitability",

                "Excellent gross margin."

            ]

        )

    if scores["Revenue Diversification"] < 40:

        alerts.append(

            [

                "🟠",

                "Revenue Risk",

                "Revenue is highly concentrated."

            ]

        )

    if scores["Market Diversification"] < 40:

        alerts.append(

            [

                "🟠",

                "Market Risk",

                "Sales depend on one country."

            ]

        )

    low_products = (

        products["Revenue"]

        <=

        products["Revenue"].quantile(.10)

    ).sum()

    if low_products:

        alerts.append(

            [

                "🔴",

                "Product Risk",

                f"{low_products} products generate very low revenue."

            ]

        )

    return pd.DataFrame(

        alerts,

        columns=[

            "Level",

            "Category",

            "Insight"

        ]

    )


alerts = generate_alerts(
    ai,
    scores,
    products,
)

show_table(

    alerts,

    title="AI Business Alerts",

    height=220,

)

divider()

# ==========================================================
# AI Opportunities
# ==========================================================

opportunities = pd.DataFrame({

    "Priority":[

        "High",

        "High",

        "Medium",

        "Medium",

        "Low"

    ],

    "Opportunity":[

        "Expand into additional categories.",

        "Increase revenue outside the top country.",

        "Bundle slow products with best sellers.",

        "Strengthen loyalty programs.",

        "Review low-performing SKUs."

    ]

})

show_table(

    opportunities,

    title="Growth Opportunities",

    height=240,

)

divider()

# ==========================================================
# AI Decision Matrix
# ==========================================================

decision = pd.DataFrame({

    "Decision":[

        "Increase Marketing",

        "Optimize Portfolio",

        "Expand Markets",

        "Customer Loyalty",

        "Inventory Review"

    ],

    "Priority":[

        "High",

        "Medium",

        "High",

        "Medium",

        "Low"

    ]

})

show_table(

    decision,

    title="Executive Decisions",

    height=240,

)

divider()
from utils.dashboard_helpers import (
    show_export_button,
    show_summary,
    show_footer,
)

# ==========================================================
# AI Narrative Generator
# ==========================================================

@st.cache_data
def build_ai_narrative(ai, scores):

    narrative = f"""
The business generated **{format_currency(ai['Revenue'])}** in revenue
and **{format_currency(ai['Profit'])}** in profit with a gross margin of
**{ai['Margin']:.2%}**.

The strongest product category is **{ai['TopCategory']['Category']}**
while **{ai['TopCountry']['Country']}** remains the leading market.

The current Business Health Score is **{scores['Business Health']}/100**
with an overall Risk Score of **{scores['Risk Score']}/100**.

Revenue concentration and customer dependency should continue to be
monitored while expanding into new markets and improving the product mix
to support sustainable growth.
"""

    return narrative


narrative = build_ai_narrative(ai, scores)

st.markdown("### 🤖 Executive AI Narrative")

st.info(narrative)

divider()

# ==========================================================
# AI Health Summary
# ==========================================================

show_summary(

    left_title="Business Performance",

    left_items={

        "Business Health":
            f"{scores['Business Health']}/100",

        "Risk Score":
            f"{scores['Risk Score']}/100",

        "Portfolio":
            f"{scores['Portfolio Strength']}/100",

        "Market":
            f"{scores['Market Diversification']}/100",

    },

    right_title="Key Leaders",

    right_items={

        "Category":
            ai["TopCategory"]["Category"],

        "Country":
            ai["TopCountry"]["Country"],

        "Product":
            ai["TopProduct"]["ProductName"],

        "Customer":
            ai["TopCustomer"]["Name"],

    }

)

divider()

# ==========================================================
# AI Report
# ==========================================================

report = pd.DataFrame({

    "Metric":[

        "Revenue",
        "Profit",
        "Orders",
        "Units Sold",
        "Gross Margin",

        "Business Health",
        "Risk Score",
        "Portfolio Strength",
        "Market Diversification",
        "Customer Diversification",

        "Top Category",
        "Top Country",
        "Top Product",
        "Top Customer"

    ],

    "Value":[

        ai["Revenue"],
        ai["Profit"],
        ai["Orders"],
        ai["Units"],
        ai["Margin"],

        scores["Business Health"],
        scores["Risk Score"],
        scores["Portfolio Strength"],
        scores["Market Diversification"],
        scores["Customer Diversification"],

        ai["TopCategory"]["Category"],
        ai["TopCountry"]["Country"],
        ai["TopProduct"]["ProductName"],
        ai["TopCustomer"]["Name"]

    ]

})

# ==========================================================
# Export
# ==========================================================

show_export_button(

    dataframe=report,

    filename="AI_Insights_Report",

    label="📥 Download AI Insights Report"

)

divider()

# ==========================================================
# AI Decision
# ==========================================================

overall_score = round(

    (
        scores["Business Health"] +
        scores["Portfolio Strength"] +
        scores["Market Diversification"] +
        scores["Customer Diversification"]
    ) / 4

)

if overall_score >= 85:
    decision = "🟢 Excellent Business Performance"

elif overall_score >= 70:
    decision = "🟡 Healthy Business with Growth Opportunities"

elif overall_score >= 50:
    decision = "🟠 Moderate Risk - Monitor KPIs"

else:
    decision = "🔴 High Risk - Immediate Action Required"

st.success(f"### Executive Decision\n\n{decision}")

divider()

# ==========================================================
# Footer
# ==========================================================

show_footer(

    Revenue=format_currency(ai["Revenue"]),

    Profit=format_currency(ai["Profit"]),

    Business_Health=f"{scores['Business Health']}/100",

    Risk_Score=f"{scores['Risk Score']}/100",

)
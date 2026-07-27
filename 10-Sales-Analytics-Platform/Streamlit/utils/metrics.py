"""
=========================================================
Sales Analytics Platform
Metrics Module

Author : Youssef Naser
=========================================================
"""

from typing import Optional

import pandas as pd


# =========================================================
# Internal Helpers
# =========================================================

def _is_empty(df: pd.DataFrame) -> bool:
    """
    Check whether dataframe is empty.
    """

    return df is None or df.empty


def _find_column(
    df: pd.DataFrame,
    columns: list[str]
) -> Optional[str]:
    """
    Return the first matching column.
    """

    for column in columns:

        if column in df.columns:

            return column

    return None


def _safe_sum(
    df: pd.DataFrame,
    columns: list[str]
) -> float:
    """
    Safe sum.
    """

    if _is_empty(df):

        return 0

    column = _find_column(df, columns)

    if column is None:

        return 0

    return float(df[column].sum())


def _safe_unique(
    df: pd.DataFrame,
    column: str
) -> int:
    """
    Safe unique count.
    """

    if _is_empty(df):

        return 0

    if column not in df.columns:

        return 0

    return int(df[column].nunique())


# =========================================================
# Revenue
# =========================================================

def total_revenue(
    df: pd.DataFrame
) -> float:
    """
    Total Revenue.
    """

    return _safe_sum(
        df,
        [
            "Revenue",
            "SalesAmount"
        ]
    )


# =========================================================
# Profit
# =========================================================

def total_profit(
    df: pd.DataFrame
) -> float:
    """
    Total Profit.
    """

    return _safe_sum(
        df,
        [
            "Profit",
            "GrossProfit"
        ]
    )


# =========================================================
# Orders
# =========================================================

def total_orders(
    df: pd.DataFrame
) -> int:
    """
    Total Orders.
    """

    if _is_empty(df):

        return 0

    if "Orders" in df.columns:

        return int(df["Orders"].sum())

    if "SalesOrderNumber" in df.columns:

        return int(df["SalesOrderNumber"].nunique())

    return 0


# =========================================================
# Units
# =========================================================

def total_units(
    df: pd.DataFrame
) -> int:
    """
    Total Units Sold.
    """

    return int(

        _safe_sum(

            df,

            [

                "UnitsSold",

                "Units",

                "OrderQuantity"

            ]

        )

    )


# =========================================================
# Customers
# =========================================================

def total_customers(
    df: pd.DataFrame
) -> int:
    """
    Total Customers.
    """

    return _safe_unique(
        df,
        "CustomerKey"
    )


# =========================================================
# Margin
# =========================================================

def gross_margin(
    df: pd.DataFrame
) -> float:
    """
    Gross Margin.
    """

    revenue = total_revenue(df)

    if revenue == 0:

        return 0

    return total_profit(df) / revenue


# =========================================================
# Average Order Value
# =========================================================

def average_order_value(
    df: pd.DataFrame
) -> float:
    """
    Average Order Value.
    """

    orders = total_orders(df)

    if orders == 0:

        return 0

    return total_revenue(df) / orders


# =========================================================
# Average Revenue Per Customer
# =========================================================

def average_revenue_per_customer(
    df: pd.DataFrame
) -> float:
    """
    Average Revenue Per Customer.
    """

    customers = total_customers(df)

    if customers == 0:

        return 0

    return total_revenue(df) / customers


# =========================================================
# Average Profit Per Customer
# =========================================================

def average_profit_per_customer(
    df: pd.DataFrame
) -> float:
    """
    Average Profit Per Customer.
    """

    customers = total_customers(df)

    if customers == 0:

        return 0

    return total_profit(df) / customers


# =========================================================
# Average Orders Per Customer
# =========================================================

def average_orders_per_customer(
    df: pd.DataFrame
) -> float:
    """
    Average Orders Per Customer.
    """

    customers = total_customers(df)

    if customers == 0:

        return 0

    return total_orders(df) / customers

# =========================================================
# Average Revenue per Product
# =========================================================

def average_revenue_per_product(df):

    products = df["ProductKey"].nunique()

    if products == 0:
        return 0.0

    return float(
        total_revenue(df) / products
    )

# =========================================================
# Top Dimension
# =========================================================

def top_dimension(
    df: pd.DataFrame,
    dimension: str
) -> Optional[pd.Series]:
    """
    Return the highest revenue record for any dimension.
    """

    if _is_empty(df):

        return None

    if dimension not in df.columns:

        return None

    revenue_column = _find_column(
        df,
        [
            "Revenue",
            "SalesAmount"
        ]
    )

    if revenue_column is None:

        return None

    result = (
        df.groupby(dimension, as_index=False)[revenue_column]
        .sum()
        .sort_values(revenue_column, ascending=False)
    )

    if result.empty:

        return None

    return result.iloc[0]


# =========================================================
# Revenue Per Order
# =========================================================

def revenue_per_order(
    df: pd.DataFrame
) -> float:
    """
    Revenue per order.
    """

    orders = total_orders(df)

    if orders == 0:

        return 0

    return total_revenue(df) / orders


# =========================================================
# Profit Per Order
# =========================================================

def profit_per_order(
    df: pd.DataFrame
) -> float:
    """
    Profit per order.
    """

    orders = total_orders(df)

    if orders == 0:

        return 0

    return total_profit(df) / orders


# =========================================================
# Average Selling Price
# =========================================================

def average_selling_price(
    df: pd.DataFrame
) -> float:
    """
    Average selling price.
    """

    units = total_units(df)

    if units == 0:

        return 0

    return total_revenue(df) / units

# =========================================================
# Average Units per Order
# =========================================================

def average_units_per_order(df):

    orders = total_orders(df)

    if orders == 0:
        return 0.0

    return float(
        total_units(df) / orders
    )

# =========================================================
# Cost Ratio
# =========================================================

def cost_ratio(df):

    revenue = total_revenue(df)

    if revenue == 0:
        return 0.0

    return float(
        df["Cost"].sum() / revenue
    )

# =========================================================
# Profit per Unit
# =========================================================

def profit_per_unit(df):

    units = total_units(df)

    if units == 0:
        return 0.0

    return float(
        total_profit(df) / units
    )

# =========================================================
# Growth Percentage
# =========================================================

def growth_percentage(
    current: float,
    previous: float
) -> float:
    """
    Growth percentage.
    """

    if previous in (None, 0):

        return 0

    return ((current - previous) / previous) * 100


# =========================================================
# Running Total
# =========================================================

def running_total(
    df: pd.DataFrame,
    value_column: str
) -> pd.Series:
    """
    Calculate the running total.

    Parameters
    ----------
    df : pd.DataFrame
        Input dataframe.
    value_column : str
        Numeric column.

    Returns
    -------
    pd.Series
    """

    if _is_empty(df):
        return pd.Series(dtype="float64")

    if value_column not in df.columns:
        return pd.Series(dtype="float64")

    return df[value_column].cumsum()


# =========================================================
# Month over Month
# =========================================================

def mom(
    df: pd.DataFrame,
    value_column: str
) -> pd.Series:
    """
    Month-over-Month growth.

    Note
    ----
    The dataframe must be sorted chronologically
    before calling this function.
    """

    if _is_empty(df):
        return pd.Series(dtype="float64")

    if value_column not in df.columns:
        return pd.Series(dtype="float64")

    return df[value_column].pct_change() * 100


# =========================================================
# Year over Year
# =========================================================

def yoy(
    df: pd.DataFrame,
    value_column: str
) -> pd.Series:
    """
    Year-over-Year growth.

    Note
    ----
    The dataframe must be sorted chronologically
    before calling this function.
    """

    if _is_empty(df):
        return pd.Series(dtype="float64")

    if value_column not in df.columns:
        return pd.Series(dtype="float64")

    return df[value_column].pct_change(12) * 100


# =========================================================
# Year To Date
# =========================================================

def ytd(
    df: pd.DataFrame,
    value_column: str
) -> pd.Series:
    """
    Year-To-Date cumulative values.

    Parameters
    ----------
    df : pd.DataFrame
    value_column : str
    """

    if _is_empty(df):
        return pd.Series(dtype="float64")

    if value_column not in df.columns:
        return pd.Series(dtype="float64")

    return df[value_column].cumsum()


# =========================================================
# Executive KPIs
# =========================================================

def executive_kpis(
    df: pd.DataFrame
) -> dict:
    """
    Return executive KPI dictionary.
    """

    return {

        "Revenue": total_revenue(df),

        "Profit": total_profit(df),

        "Orders": total_orders(df),

        "Customers": total_customers(df),

        "Units Sold": total_units(df),

        "Gross Margin": gross_margin(df),

        "Average Order Value": average_order_value(df),

        "Revenue Per Customer": average_revenue_per_customer(df),

        "Profit Per Customer": average_profit_per_customer(df),

        "Orders Per Customer": average_orders_per_customer(df),

        "Revenue Per Order": revenue_per_order(df),

        "Profit Per Order": profit_per_order(df),

        "Cost Ratio": cost_ratio(df),

        "Profit per Unit": profit_per_unit(df),

        "Average Units per Order": average_units_per_order(df),

        "Average Revenue per Product": average_revenue_per_product(df),

        "Average Selling Price": average_selling_price(df)

    }


# =========================================================
# Wrapper Functions
# (Backward Compatibility)
# =========================================================

def top_product(df: pd.DataFrame):
    return top_dimension(df, "ProductName")


def top_customer(df: pd.DataFrame):
    return top_dimension(df, "Name")


def top_country(df: pd.DataFrame):
    return top_dimension(df, "Country")


def top_category(df: pd.DataFrame):
    return top_dimension(df, "Category")
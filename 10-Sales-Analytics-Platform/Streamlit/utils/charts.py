"""
=========================================================
Sales Analytics Platform
Charts Module

Author : Youssef Naser
=========================================================
"""

from typing import Optional

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


# =========================================================
# Theme
# =========================================================

BACKGROUND = "#0E1117"
CARD = "#1A2234"
PRIMARY = "#F97316"
TEXT = "#FFFFFF"

DEFAULT_HEIGHT = 420

COLOR_SEQUENCE = px.colors.sequential.Oranges


# =========================================================
# Internal Helpers
# =========================================================

def _is_empty(df: pd.DataFrame) -> bool:
    """
    Check whether dataframe is empty.
    """

    return df is None or df.empty


# =========================================================
# Default Layout
# =========================================================

def apply_layout(
    fig,
    title: Optional[str] = None,
    height: int = DEFAULT_HEIGHT
):
    """
    Apply a unified Plotly layout.
    """

    fig.update_layout(

        title=dict(
            text=title,
            x=0.02,
            font=dict(
                size=22,
                color=TEXT
            )
        ),

        template="plotly_dark",

        paper_bgcolor=BACKGROUND,
        plot_bgcolor=BACKGROUND,

        font=dict(
            family="Segoe UI",
            color=TEXT,
            size=13
        ),

        height=height,

        margin=dict(
            l=20,
            r=20,
            t=60,
            b=20
        ),

        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),

        hovermode="x unified",

        hoverlabel=dict(
            bgcolor=CARD,
            font_size=13
        )

    )

    fig.update_xaxes(

        showgrid=False,
        zeroline=False

    )

    fig.update_yaxes(

        gridcolor="rgba(255,255,255,.08)",
        zeroline=False

    )

    return fig

# =========================================================
# Multi Line Chart
# =========================================================

def multi_line_chart(
    df,
    x,
    y_columns,
    title
):

    fig = px.line(
        df,
        x=x,
        y=y_columns,
        markers=True,
        title=title
    )

    fig.update_layout(
        template="plotly_dark",
        hovermode="x unified"
    )

    return fig

# =========================================================
# Line Chart
# =========================================================

def line_chart(
    df: pd.DataFrame,
    x: str,
    y: str,
    title: Optional[str] = None,
    color: Optional[str] = None,
    height: int = DEFAULT_HEIGHT
):
    ...
    fig = px.line(
        df,
        x=x,
        y=y,
        color=color,
        markers=True,
        color_discrete_sequence=[PRIMARY] if color is None else None
    )
    """
    Create a line chart.
    """

    if _is_empty(df):
        return go.Figure()

    fig = px.line(

        df,

        x=x,

        y=y,

        color=color,

        markers=True,

        color_discrete_sequence=[PRIMARY]

    )

    fig.update_traces(

        line=dict(width=3),

        marker=dict(size=7)

    )

    return apply_layout(

        fig,

        title,

        height

    )

# =========================================================
# Bar Chart
# =========================================================

def bar_chart(
    df: pd.DataFrame,
    x: str,
    y: str,
    color: Optional[str] = None,
    title: Optional[str] = None,
    height: int = DEFAULT_HEIGHT
):
    """
    Create a vertical bar chart.
    """

    if _is_empty(df):
        return go.Figure()

    fig = px.bar(

        df,

        x=x,

        y=y,

        color=color,

        text_auto=".2s",

        color_discrete_sequence=COLOR_SEQUENCE

    )

    fig.update_traces(

        textposition="outside"

    )

    return apply_layout(

        fig,

        title,

        height

    )


# =========================================================
# Horizontal Bar
# =========================================================

def horizontal_bar(
    df: pd.DataFrame,
    x: str,
    y: str,
    title: Optional[str] = None,
    height: int = DEFAULT_HEIGHT
):
    """
    Create a sorted horizontal bar chart.
    """

    if _is_empty(df):
        return go.Figure()

    data = df.sort_values(

        by=x,

        ascending=True

    )

    fig = px.bar(

        data,

        x=x,

        y=y,

        orientation="h",

        text_auto=".2s",

        color=x,

        color_continuous_scale="Oranges"

    )

    return apply_layout(

        fig,

        title,

        height

    )


# =========================================================
# Area Chart
# =========================================================

def area_chart(
    df: pd.DataFrame,
    x: str,
    y: str,
    title: Optional[str] = None,
    height: int = DEFAULT_HEIGHT
):
    """
    Create an area chart.
    """

    if _is_empty(df):
        return go.Figure()

    fig = px.area(

        df,

        x=x,

        y=y,

        color_discrete_sequence=[PRIMARY]

    )

    return apply_layout(

        fig,

        title,

        height

    )
# =========================================================
# Pie Chart
# =========================================================

def pie_chart(
    df: pd.DataFrame,
    names: str,
    values: str,
    title: Optional[str] = None,
    height: int = DEFAULT_HEIGHT
):
    """
    Create a pie chart.
    """

    if _is_empty(df):
        return go.Figure()

    fig = px.pie(
        df,
        names=names,
        values=values,
        color_discrete_sequence=COLOR_SEQUENCE
    )

    fig.update_traces(
        textinfo="percent+label",
        hovertemplate="<b>%{label}</b><br>Value: %{value:,.0f}<br>Share: %{percent}<extra></extra>"
    )

    return apply_layout(fig, title, height)


# =========================================================
# Donut Chart
# =========================================================

def donut_chart(
    df: pd.DataFrame,
    names: str,
    values: str,
    title: Optional[str] = None,
    height: int = DEFAULT_HEIGHT
):
    """
    Create a donut chart.
    """

    if _is_empty(df):
        return go.Figure()

    fig = px.pie(
        df,
        names=names,
        values=values,
        hole=0.60,
        color_discrete_sequence=COLOR_SEQUENCE
    )

    fig.update_traces(
        textinfo="percent+label",
        hovertemplate="<b>%{label}</b><br>Value: %{value:,.0f}<br>Share: %{percent}<extra></extra>"
    )

    return apply_layout(fig, title, height)


# =========================================================
# Scatter Chart
# =========================================================

def scatter_chart(
    df: pd.DataFrame,
    x: str,
    y: str,
    color: Optional[str] = None,
    size: Optional[str] = None,
    title: Optional[str] = None,
    height: int = DEFAULT_HEIGHT
):
    """
    Create a scatter chart.
    """

    if _is_empty(df):
        return go.Figure()

    fig = px.scatter(
        df,
        x=x,
        y=y,
        color=color,
        size=size,
        color_discrete_sequence=COLOR_SEQUENCE
    )

    fig.update_traces(
        marker=dict(
            opacity=0.85,
            line=dict(width=1, color="white")
        )
    )

    return apply_layout(fig, title, height)


# =========================================================
# Treemap
# =========================================================

def treemap(
    df: pd.DataFrame,
    path: list,
    values: str,
    title: Optional[str] = None,
    height: int = DEFAULT_HEIGHT
):
    """
    Create a treemap.
    """

    if _is_empty(df):
        return go.Figure()

    fig = px.treemap(
        df,
        path=path,
        values=values,
        color=values,
        color_continuous_scale="Oranges"
    )

    fig.update_traces(
        textinfo="label+value"
    )

    return apply_layout(fig, title, height)


# =========================================================
# Histogram
# =========================================================

def histogram(
    df: pd.DataFrame,
    x: str,
    title: Optional[str] = None,
    height: int = DEFAULT_HEIGHT
):
    """
    Create a histogram.
    """

    if _is_empty(df):
        return go.Figure()

    fig = px.histogram(
        df,
        x=x,
        color_discrete_sequence=[PRIMARY]
    )

    return apply_layout(fig, title, height)


# =========================================================
# Box Plot
# =========================================================

def box_plot(
    df: pd.DataFrame,
    x: str,
    y: str,
    title: Optional[str] = None,
    height: int = DEFAULT_HEIGHT
):
    """
    Create a box plot.
    """

    if _is_empty(df):
        return go.Figure()

    fig = px.box(
        df,
        x=x,
        y=y,
        color=x,
        color_discrete_sequence=COLOR_SEQUENCE
    )

    return apply_layout(fig, title, height)


# =========================================================
# Heatmap
# =========================================================

def heatmap(
    df: pd.DataFrame,
    title: Optional[str] = None,
    height: int = DEFAULT_HEIGHT
):
    """
    Create a heatmap.
    """

    if _is_empty(df):
        return go.Figure()

    fig = px.imshow(
        df,
        text_auto=True,
        aspect="auto",
        color_continuous_scale="Oranges"
    )

    fig.update_traces(
        hovertemplate="Value: %{z}<extra></extra>"
    )

    return apply_layout(fig, title, height)
# =========================================================
# World Map
# =========================================================

def world_map(
    df: pd.DataFrame,
    country: str,
    value: str,
    title: Optional[str] = None,
    height: int = 500
):
    """
    Create an interactive choropleth world map.
    """

    if _is_empty(df):
        return go.Figure()

    fig = px.choropleth(
        df,
        locations=country,
        locationmode="country names",
        color=value,
        color_continuous_scale="Oranges",
        projection="natural earth"
    )

    fig.update_geos(
        showframe=False,
        showcoastlines=True,
        coastlinecolor="gray",
        showcountries=True,
        countrycolor="gray",
        showocean=True,
        oceancolor="#0E1117",
        bgcolor="#0E1117"
    )

    fig.update_coloraxes(
        colorbar_title=value
    )

    return apply_layout(fig, title, height)


# =========================================================
# Gauge Chart
# =========================================================

def gauge(
    value: float,
    title: str,
    minimum: float = 0,
    maximum: float = 100
):
    """
    Create KPI Gauge.
    """

    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",

            value=value,

            number={
                "font": {
                    "size": 34
                }
            },

            title={
                "text": title,
                "font": {
                    "size": 18
                }
            },

            gauge={

                "axis": {
                    "range": [minimum, maximum]
                },

                "bar": {
                    "color": PRIMARY
                },

                "bgcolor": CARD,

                "steps": [

                    {
                        "range": [minimum, maximum * .50],
                        "color": "#3B3B3B"
                    },

                    {
                        "range": [maximum * .50, maximum * .80],
                        "color": "#5A5A5A"
                    },

                    {
                        "range": [maximum * .80, maximum],
                        "color": "#7A7A7A"
                    }

                ]

            }

        )
    )

    return apply_layout(
        fig,
        height=350
    )


# =========================================================
# Waterfall Chart
# =========================================================

def waterfall(
    labels: list,
    values: list,
    title: Optional[str] = None,
    height: int = DEFAULT_HEIGHT
):
    """
    Create waterfall chart.
    """

    fig = go.Figure(

        go.Waterfall(

            x=labels,

            y=values,

            connector={
                "line": {
                    "color": "gray"
                }
            }

        )

    )

    return apply_layout(
        fig,
        title,
        height
    )


# =========================================================
# Funnel Chart
# =========================================================

def funnel(
    df: pd.DataFrame,
    x: str,
    y: str,
    title: Optional[str] = None,
    height: int = DEFAULT_HEIGHT
):
    """
    Create funnel chart.
    """

    if _is_empty(df):
        return go.Figure()

    fig = px.funnel(

        df,

        x=x,

        y=y,

        color_discrete_sequence=[PRIMARY]

    )

    return apply_layout(
        fig,
        title,
        height
    )


# =========================================================
# Figure Export
# =========================================================

def save_figure(
    fig,
    filename: str,
    width: int = 1600,
    height: int = 900
):
    """
    Export Plotly figure as PNG.

    Requires:
        pip install kaleido
    """

    fig.write_image(
        filename,
        width=width,
        height=height
    )
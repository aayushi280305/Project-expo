"""
Visualization utilities — Plotly charts for the financial dashboard.
"""

import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

# Dark theme palette
BG       = "#0f0f1a"
SURFACE  = "#1a1a2e"
GOLD     = "#e8d5a3"
AMBER    = "#ef9f27"
GREEN    = "#639922"
MUTED    = "#7a7a9a"
TEXT     = "#c8c8e0"
BORDER   = "#2a2a3d"

PLOTLY_LAYOUT = dict(
    paper_bgcolor=BG,
    plot_bgcolor=SURFACE,
    font=dict(family="sans-serif", color=TEXT, size=12),
    margin=dict(l=16, r=16, t=40, b=16),
    xaxis=dict(gridcolor=BORDER, zerolinecolor=BORDER, tickfont=dict(size=10)),
    yaxis=dict(gridcolor=BORDER, zerolinecolor=BORDER, tickfont=dict(size=10)),
)


def create_roi_chart(strategies: list) -> go.Figure:
    """Grouped bar chart: Cost vs Revenue Gain per strategy."""
    names    = [s["strategy"] for s in strategies]
    costs    = [s["cost_k"]         for s in strategies]
    revenues = [s["revenue_gain_k"] for s in strategies]

    fig = go.Figure()
    fig.add_trace(go.Bar(
        name="Cost ($K)",
        x=names, y=costs,
        marker_color=AMBER,
        text=[f"${c}K" for c in costs],
        textposition="outside",
        textfont=dict(size=10, color=AMBER),
    ))
    fig.add_trace(go.Bar(
        name="Revenue Gain ($K)",
        x=names, y=revenues,
        marker_color=GREEN,
        text=[f"${r}K" for r in revenues],
        textposition="outside",
        textfont=dict(size=10, color=GREEN),
    ))

    fig.update_layout(
        **PLOTLY_LAYOUT,
        title=dict(text="Cost vs Revenue Gain", font=dict(color=GOLD, size=13)),
        barmode="group",
        showlegend=True,
        legend=dict(
            bgcolor=SURFACE, bordercolor=BORDER, borderwidth=1,
            font=dict(size=10, color=TEXT),
        ),
    )
    return fig


def create_strategy_radar(strategies: list) -> go.Figure:
    """Radar chart scoring each strategy on ROI, speed, and scale."""
    names = [s["strategy"] for s in strategies]
    # Normalise ROI 0-100
    max_roi = max(s["roi_pct"] for s in strategies) or 1
    # Speed: invert timeline (shorter = better), normalise 0-100
    max_months = max(s["timeline_months"] for s in strategies) or 1

    categories = ["ROI", "Speed", "Revenue Scale", "Cost Efficiency"]
    colors = [GOLD, AMBER, GREEN, "#5dcaa5"]

    fig = go.Figure()
    for i, s in enumerate(strategies):
        roi_score      = (s["roi_pct"] / max_roi) * 100
        speed_score    = ((max_months - s["timeline_months"]) / max_months) * 100 + 10
        revenue_score  = (s["revenue_gain_k"] / max(ss["revenue_gain_k"] for ss in strategies)) * 100
        cost_eff_score = (1 - s["cost_k"] / max(ss["cost_k"] for ss in strategies)) * 80 + 20
        values = [roi_score, speed_score, revenue_score, cost_eff_score]
        values += values[:1]  # close polygon

        fig.add_trace(go.Scatterpolar(
            r=values,
            theta=categories + [categories[0]],
            name=s["strategy"],
            fill="toself",
            fillcolor=colors[i % len(colors)],
            opacity=0.25,
            line=dict(color=colors[i % len(colors)], width=2),
        ))

    fig.update_layout(
        **PLOTLY_LAYOUT,
        title=dict(text="Strategy Score Radar", font=dict(color=GOLD, size=13)),
        polar=dict(
            bgcolor=SURFACE,
            radialaxis=dict(visible=True, range=[0, 100], gridcolor=BORDER, tickfont=dict(size=9, color=MUTED)),
            angularaxis=dict(gridcolor=BORDER, tickfont=dict(size=10, color=TEXT)),
        ),
        showlegend=True,
        legend=dict(
            bgcolor=SURFACE, bordercolor=BORDER, borderwidth=1,
            font=dict(size=10, color=TEXT),
        ),
    )
    return fig


def create_revenue_waterfall(strategies: list) -> go.Figure:
    """Waterfall chart showing cumulative revenue contribution."""
    names    = [s["strategy"] for s in strategies]
    revenues = [s["revenue_gain_k"] for s in strategies]
    total    = sum(revenues)

    measure = ["relative"] * len(strategies) + ["total"]
    x_vals  = names + ["Total"]
    y_vals  = revenues + [total]
    texts   = [f"+${v}K" for v in revenues] + [f"${total}K"]

    fig = go.Figure(go.Waterfall(
        orientation="v",
        measure=measure,
        x=x_vals,
        y=y_vals,
        text=texts,
        textposition="outside",
        textfont=dict(size=10, color=TEXT),
        connector=dict(line=dict(color=BORDER, width=1)),
        increasing=dict(marker=dict(color=GREEN)),
        totals=dict(marker=dict(color=GOLD)),
        decreasing=dict(marker=dict(color="#e24b4a")),
    ))

    fig.update_layout(
        **PLOTLY_LAYOUT,
        title=dict(text="Cumulative Revenue Waterfall", font=dict(color=GOLD, size=13)),
        showlegend=False,
    )
    return fig

"""Chart theme for the app, matched to daniel-ots.pages.dev.

Typography: Inter for everything in the chart; navy titles, ink text, muted
captions. Chrome: hairline grid (#eef2f6), soft zero line (#cbd5df), no
axis lines, horizontal legend above the plot, unified hover with units,
left-aligned title with a one-line subtitle. Series colours are the
palette validated with the dataviz checker (six adjacent series pass; the
blue/purple pair sits in the 6-8 CVD band and is always accompanied by a
legend, 2-px bar gaps and a table view).

Usage::

    import charts
    fig = charts.figure(title, subtitle, x_title=..., y_money=True)
    charts.line(fig, x, y, name, charts.SERIES["tax"], money=True)
    charts.end_label(fig, x[-1], y[-1], "$1,234", charts.SERIES["tax"])
    st.plotly_chart(fig, use_container_width=True, config=charts.CONFIG)
"""

import textwrap
from pathlib import Path

import plotly.graph_objects as go
import plotly.io as pio
import streamlit as st

# --- site palette (styles.scss) -------------------------------------------
NAVY = "#1f3b57"
NAVY_DARK = "#16293b"
ACCENT = "#2e86ab"
INK = "#1c2733"
MUTED = "#5b6b7a"
SOFT = "#f5f8fb"
LINE = "#e3e8ee"
GRID = "#eef2f6"
ZERO = "#cbd5df"
RED = "#c44e52"
GREEN = "#1e8449"

# --- data series (validated categorical palette) ---------------------------
SERIES = {
    "tax": "#2a78d6",
    "payroll": RED,
    "eitc": "#1baf7a",
    "actc": "#0d7a52",
    "pan": "#c9a227",
    "tanf": "#8e44ad",
    "section8": "#0b8ba6",
    "net": INK,
    "market": "#9aa7b4",
    "reform": "#eb6834",
    "baseline": "#2a78d6",
    "cliff": RED,
    "better": "#2a78d6",
    "worse": RED,
}

FONT = "Inter, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif"
CONFIG = {"displayModeBar": False, "responsive": True}

TEMPLATE = go.layout.Template(
    layout=dict(
        font=dict(family=FONT, size=13, color=INK),
        title=dict(
            font=dict(family=FONT, size=17, color=NAVY),
            x=0,
            xanchor="left",
            pad=dict(l=2),
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=8, r=16, t=56, b=72),
        hovermode="x unified",
        hoverlabel=dict(
            bgcolor="white",
            bordercolor=LINE,
            font=dict(family=FONT, size=12, color=INK),
        ),
        legend=dict(
            orientation="h",
            yanchor="top",
            y=-0.22,
            x=0,
            font=dict(size=12, color=MUTED),
            itemclick="toggleothers",
        ),
        xaxis=dict(
            showgrid=False,
            showline=False,
            zeroline=False,
            ticks="",
            tickfont=dict(size=12, color=MUTED),
            title=dict(font=dict(size=12, color=MUTED), standoff=10),
            automargin=True,
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor=GRID,
            gridwidth=1,
            showline=False,
            zeroline=True,
            zerolinecolor=ZERO,
            zerolinewidth=1,
            ticks="",
            tickfont=dict(size=12, color=MUTED),
            title=dict(font=dict(size=12, color=MUTED)),
            automargin=True,
        ),
        colorway=[
            SERIES["tax"],
            SERIES["payroll"],
            SERIES["eitc"],
            SERIES["actc"],
            SERIES["pan"],
            SERIES["tanf"],
            SERIES["section8"],
        ],
    ),
    data=dict(
        scatter=[go.Scatter(line=dict(width=2), marker=dict(size=7))],
        bar=[go.Bar(marker=dict(line=dict(width=0)))],
    ),
)
pio.templates["pr"] = TEMPLATE


def figure(
    title=None,
    subtitle=None,
    x_title=None,
    y_money=False,
    y_percent=False,
    height=380,
):
    """A themed figure with an optional left-aligned title and subtitle."""
    fig = go.Figure()
    fig.update_layout(template="pr", height=height)
    if title:
        text = f"<b>{title}</b>"
        lines = textwrap.wrap(subtitle, 60) if subtitle else []
        if lines:
            text += (
                f"<br><span style='font-size:12px;color:{MUTED}'>"
                + "<br>".join(lines)
                + "</span>"
            )
        fig.update_layout(
            title=dict(text=text),
            margin=dict(t=64 + 20 * len(lines)),
        )
    if x_title:
        fig.update_xaxes(title_text=x_title)
    if y_money:
        fig.update_yaxes(tickformat="$,.3~s")  # $10k, -$10k
    if y_percent:
        fig.update_yaxes(tickformat=".0%")
    return fig


def line(fig, x, y, name, color, money=True, dash=None, shape=None, width=2):
    fmt = "%{y:$,.0f}" if money else "%{y:.0%}"
    fig.add_trace(
        go.Scatter(
            x=x,
            y=y,
            name=name,
            mode="lines",
            line=dict(color=color, width=width, dash=dash, shape=shape),
            hovertemplate=fmt + "<extra>" + name + "</extra>",
        )
    )


def bars(fig, x, y, name, color, money=True):
    fmt = "%{y:$,.0f}" if money else "%{y:.0%}"
    fig.add_trace(
        go.Bar(
            x=x,
            y=y,
            name=name,
            marker=dict(color=color, line=dict(width=0)),
            hovertemplate=fmt + "<extra>" + name + "</extra>",
        )
    )


def area(fig, x, y, name, color, group, money=True):
    """A stacked area; `group` separates the stack above zero ("pos") from
    the stack below ("neg"). A thin white edge keeps adjacent bands apart."""
    fmt = "%{y:$,.0f}" if money else "%{y:.0%}"
    fig.add_trace(
        go.Scatter(
            x=x,
            y=y,
            name=name,
            mode="lines",
            line=dict(color="white", width=1),
            fillcolor=color,
            stackgroup=group,
            hovertemplate=fmt + "<extra>" + name + "</extra>",
        )
    )


def annotate(fig, x, y, text, color, above=True):
    """A short label with a leader line, for cliffs and zones."""
    fig.add_annotation(
        x=x,
        y=y,
        text=f"<span style='color:{color}'><b>{text}</b></span>",
        showarrow=True,
        arrowhead=0,
        arrowcolor=color,
        arrowwidth=1,
        ax=0,
        ay=-38 if above else 38,
        font=dict(size=11),
        bgcolor="rgba(255,255,255,0.9)",
        bordercolor=color,
        borderwidth=1,
        borderpad=3,
    )


def end_label(fig, x, y, text, color):
    """Direct label at the end of a series (replaces legend hunting)."""
    fig.add_annotation(
        x=x,
        y=y,
        text=f"<span style='color:{color}'><b>{text}</b></span>",
        showarrow=False,
        xanchor="left",
        xshift=6,
        font=dict(size=12),
        bgcolor="rgba(255,255,255,0.85)",
        borderpad=2,
    )


def vline(fig, x, color=ZERO, dash="dot", label=None):
    fig.add_vline(x=x, line=dict(color=color, width=1, dash=dash))
    if label:
        fig.add_annotation(
            x=x,
            y=1,
            yref="paper",
            text=label,
            showarrow=False,
            yanchor="top",
            bgcolor="rgba(255,255,255,0.8)",
            font=dict(size=11, color=MUTED),
        )


def hline(fig, y, color=ZERO, dash="solid", label=None):
    fig.add_hline(y=y, line=dict(color=color, width=1, dash=dash))
    if label:
        fig.add_annotation(
            x=1,
            xref="paper",
            y=y,
            text=label,
            showarrow=False,
            xanchor="right",
            yanchor="bottom",
            font=dict(size=11, color=MUTED),
        )


def _fontface():
    """Self-hosted Inter and Source Serif 4 (Latin subsets) served from
    app/static/ (server.enableStaticServing); system fonts are the fallback."""
    path = Path(__file__).resolve().parent / "static" / "fonts" / "fonts.css"
    return path.read_text() if path.exists() else ""


def mobile_hint(text):
    """A one-line hint shown only on narrow screens (the sidebar with the
    household inputs is hidden behind the » button there)."""
    st.markdown(
        f"<div class='pr-mobile-hint'>{text}</div>", unsafe_allow_html=True
    )


def inject_css():
    """Site typography and KPI styling for the Streamlit page."""
    css = """
        <style>
        %(FONTFACE)s
        .stApp, .stApp p, .stApp li, .stApp label, .stApp input, .stApp button, .stApp td, .stApp th { font-family: %(FONT)s; color: %(INK)s; }
        .stApp h1, .stApp h2, .stApp h3 { font-family: %(FONT)s; color: %(NAVY)s; }
        .stApp h1 { font-weight: 700; letter-spacing: -.01em; }
        .stApp h2, .stApp h3 { font-weight: 600; }
        .stMarkdown p, [data-testid="stCaptionContainer"] p { font-family: "Source Serif 4", Georgia, serif; }
        [data-testid="stMetric"] { background: %(SOFT)s; border: 1px solid %(LINE)s; border-radius: 12px; padding: .9rem 1.1rem; }
        [data-testid="stMetricValue"] { color: %(NAVY)s; font-weight: 700; font-variant-numeric: tabular-nums; letter-spacing: -.01em; }
        [data-testid="stMetricLabel"] p { color: %(MUTED)s; font-size: .82rem; font-family: %(FONT)s; }
        [data-testid="stSidebar"] { background: %(SOFT)s; border-right: 1px solid %(LINE)s; }
        [data-testid="stSidebar"] p, [data-testid="stSidebar"] label { font-family: %(FONT)s; }
        .st-key-tile_pays [data-testid="stMetric"] { border-left: 4px solid %(RED)s; }
        .st-key-tile_gets [data-testid="stMetric"] { border-left: 4px solid %(GREEN)s; }
        .st-key-tile_net [data-testid="stMetric"] { border-left: 4px solid %(NAVY)s; }
        .st-key-tile_rate [data-testid="stMetric"] { border-left: 4px solid %(MUTED)s; }
        .st-key-tile_pays [data-testid="stMetricValue"] { color: %(RED)s; }
        .st-key-tile_gets [data-testid="stMetricValue"] { color: %(GREEN)s; }
        .pr-mobile-hint { display: none; }
        @media (max-width: 640px) {
          .stApp h1 { font-size: 1.6rem; line-height: 1.2; }
          .stApp h2 { font-size: 1.25rem; }
          .stApp h3 { font-size: 1.05rem; }
          .block-container { padding-left: 1rem; padding-right: 1rem; padding-top: 3rem; }
          [data-testid="stHorizontalBlock"] { flex-direction: row !important; flex-wrap: wrap !important; gap: .5rem !important; }
          [data-testid="stHorizontalBlock"] > [data-testid="stColumn"] { flex: 1 1 calc(50%% - .5rem) !important; min-width: calc(50%% - .5rem) !important; width: auto !important; }
          [data-testid="stMetric"] { padding: .6rem .75rem; }
          [data-testid="stMetricValue"] { font-size: 1.45rem; }
          [data-testid="stMetricLabel"] p { font-size: .74rem; }
          .pr-mobile-hint { display: block; background: %(SOFT)s; border: 1px solid %(LINE)s; border-radius: 10px; padding: .5rem .75rem; font-size: .85rem; color: %(MUTED)s; margin-bottom: .5rem; }
        }
        </style>
    """ % dict(
        FONT=FONT,
        INK=INK,
        NAVY=NAVY,
        SOFT=SOFT,
        LINE=LINE,
        MUTED=MUTED,
        FONTFACE=_fontface(),
        RED=RED,
        GREEN=GREEN,
    )
    st.markdown(css, unsafe_allow_html=True)

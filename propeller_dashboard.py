"""
DUCTED FAN PROPELLER ANALYTICS · PROP·LAB DASHBOARD
Built with Streamlit + Plotly
Clean business / eco-friendly visual style

Expected files in the same folder as this app:
- dataset_final.csv
- selected_100.csv
"""

from __future__ import annotations

from pathlib import Path
from textwrap import dedent

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from plotly.subplots import make_subplots
from scipy.interpolate import CubicSpline
from scipy.stats import gaussian_kde


# ─────────────────────────────────────────────────────────────────────────────
# CONFIG
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Propeller Dataset Dashboard",
    page_icon="◎",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ─────────────────────────────────────────────────────────────────────────────
# COLORS AND PLOT STYLE
# ─────────────────────────────────────────────────────────────────────────────
COLORS = {
    "bg_void": "#f4f7f2",
    "bg_carbon": "#eef3ec",
    "bg_panel": "#ffffff",
    "bg_panel_2": "#f7faf6",
    "grid": "#d8e3d3",
    "border": "#c8d6c2",
    "text_primary": "#1f2933",
    "text_dim": "#5f6f63",
    "text_muted": "#8a9a8d",
    "green_main": "#2f7d32",
    "green_soft": "#5f9f62",
    "orange": "#c77d2b",
    "orange_dim": "#9a5f21",
    "green": "#3fa34d",
    "yellow": "#c9a227",
    "red": "#c2413b",
    "magenta": "#8b5e83",
    "violet": "#5d6d7e",
    "blue": "#4f6f91",
}

PLOT_FONT = "Inter, Arial, sans-serif"
AXIS_COLOR = "#35483a"
GRID_COLOR = "#d8e3d3"
ZERO_COLOR = "#9caf99"

PLOTLY_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(
        family=PLOT_FONT,
        color=COLORS["text_primary"],
        size=12,
    ),
    margin=dict(l=64, r=34, t=76, b=64),
    hoverlabel=dict(
        bgcolor=COLORS["bg_panel"],
        bordercolor=COLORS["green_main"],
        font=dict(
            family=PLOT_FONT,
            color=COLORS["text_primary"],
            size=12,
        ),
    ),
    legend=dict(
        bgcolor="rgba(255,255,255,0.92)",
        bordercolor=COLORS["border"],
        borderwidth=1,
        font=dict(color=COLORS["text_primary"], size=11),
    ),
)


def style_fig(fig: go.Figure, height: int | None = None) -> go.Figure:
    fig.update_layout(**PLOTLY_LAYOUT)

    if height is not None:
        fig.update_layout(height=height)

    fig.update_xaxes(
        showline=True,
        linewidth=1.3,
        linecolor=AXIS_COLOR,
        tickcolor=AXIS_COLOR,
        tickfont=dict(color=AXIS_COLOR, size=11),
        title_font=dict(color=AXIS_COLOR, size=12),
        gridcolor=GRID_COLOR,
        zerolinecolor=ZERO_COLOR,
        zerolinewidth=1,
    )

    fig.update_yaxes(
        showline=True,
        linewidth=1.3,
        linecolor=AXIS_COLOR,
        tickcolor=AXIS_COLOR,
        tickfont=dict(color=AXIS_COLOR, size=11),
        title_font=dict(color=AXIS_COLOR, size=12),
        gridcolor=GRID_COLOR,
        zerolinecolor=ZERO_COLOR,
        zerolinewidth=1,
    )

    fig.update_annotations(
        font=dict(
            family=PLOT_FONT,
            size=12,
            color=COLORS["green_main"],
        )
    )

    return fig


def padded_range(values: list[float] | np.ndarray, pad_fraction: float = 0.18) -> list[float]:
    arr = np.asarray(values, dtype=float)
    finite = arr[np.isfinite(arr)]

    if finite.size == 0:
        return [-1.0, 1.0]

    vmin = float(finite.min())
    vmax = float(finite.max())

    if np.isclose(vmin, vmax):
        pad = max(abs(vmin) * 0.2, 1.0)
    else:
        pad = (vmax - vmin) * pad_fraction

    return [vmin - pad, vmax + pad]


# ─────────────────────────────────────────────────────────────────────────────
# CSS
# ─────────────────────────────────────────────────────────────────────────────
def inject_css() -> None:
    st.markdown(
        dedent(
            f"""
            <link rel="preconnect" href="https://fonts.googleapis.com">
            <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
            <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">

            <style>
            :root {{
                --bg-main: {COLORS['bg_void']};
                --bg-soft: {COLORS['bg_carbon']};
                --panel: {COLORS['bg_panel']};
                --panel-2: {COLORS['bg_panel_2']};
                --border: {COLORS['border']};
                --grid: {COLORS['grid']};
                --text: {COLORS['text_primary']};
                --text-dim: {COLORS['text_dim']};
                --text-muted: {COLORS['text_muted']};
                --green: {COLORS['green_main']};
                --green-soft: {COLORS['green_soft']};
                --orange: {COLORS['orange']};
                --red: {COLORS['red']};
            }}

            .stApp {{
                background: linear-gradient(180deg, var(--bg-main) 0%, var(--bg-soft) 100%);
                color: var(--text);
                font-family: 'Inter', Arial, sans-serif;
            }}

            #MainMenu, footer, header {{
                visibility: hidden;
            }}

            .stDeployButton {{
                display: none;
            }}

            .block-container {{
                padding-top: 1.2rem;
                padding-bottom: 3rem;
                max-width: 1450px;
            }}

            h1, h2, h3, h4, h5, h6, p, span, div, label {{
                font-family: 'Inter', Arial, sans-serif;
            }}

            .hud-masthead {{
                display: flex;
                align-items: center;
                justify-content: space-between;
                padding: 22px 28px;
                margin-bottom: 24px;
                background: var(--panel);
                border: 1px solid var(--border);
                border-radius: 18px;
                box-shadow: 0 10px 30px rgba(31, 41, 51, 0.06);
            }}

            .hud-masthead .lhs {{
                display: flex;
                align-items: center;
                gap: 16px;
            }}

            .hud-icon {{
                width: 44px;
                height: 44px;
                border-radius: 14px;
                display: grid;
                place-items: center;
                background: #e3f2df;
                color: var(--green);
                font-size: 22px;
                font-weight: 800;
            }}

            .hud-masthead h1 {{
                font-size: 24px;
                margin: 0;
                font-weight: 800;
                color: var(--text);
                letter-spacing: -0.02em;
                text-transform: none;
            }}

            .hud-masthead .subtitle {{
                color: var(--text-dim);
                font-size: 13px;
                margin-top: 4px;
                letter-spacing: 0;
                text-transform: none;
            }}

            .hud-masthead .rhs {{
                display: flex;
                gap: 18px;
                align-items: center;
            }}

            .hud-stat {{
                text-align: right;
                border-right: 1px solid var(--border);
                padding-right: 18px;
            }}

            .hud-stat:last-child {{
                border-right: none;
                padding-right: 0;
            }}

            .hud-stat .v {{
                font-size: 20px;
                font-weight: 800;
                color: var(--green);
            }}

            .hud-stat .l {{
                font-size: 11px;
                color: var(--text-muted);
            }}

            .section-label {{
                font-size: 13px;
                font-weight: 800;
                color: var(--green);
                text-transform: uppercase;
                letter-spacing: 0.08em;
                margin: 30px 0 12px 0;
            }}

            .panel-header {{
                display: flex;
                justify-content: space-between;
                align-items: baseline;
                margin-top: 22px;
                margin-bottom: 14px;
                padding-bottom: 10px;
                border-bottom: 1px solid var(--grid);
            }}

            .panel-header .ph-title {{
                font-size: 15px;
                font-weight: 800;
                color: var(--text);
                text-transform: none;
                letter-spacing: -0.01em;
            }}

            .panel-header .ph-meta {{
                font-size: 12px;
                color: var(--text-muted);
                text-transform: none;
                letter-spacing: 0;
            }}

            .kpi {{
                background: var(--panel);
                border: 1px solid var(--border);
                padding: 16px 18px;
                border-radius: 16px;
                height: 100%;
                box-shadow: 0 6px 18px rgba(31, 41, 51, 0.04);
            }}

            .kpi .label {{
                font-size: 11px;
                font-weight: 700;
                color: var(--text-muted);
                text-transform: uppercase;
                letter-spacing: 0.06em;
                margin-bottom: 8px;
            }}

            .kpi .value {{
                font-size: 26px;
                font-weight: 800;
                color: var(--text);
                line-height: 1.1;
            }}

            .kpi .unit {{
                font-size: 13px;
                color: var(--text-dim);
                margin-left: 4px;
                font-weight: 500;
            }}

            .kpi .sub {{
                font-size: 12px;
                color: var(--text-dim);
                margin-top: 6px;
            }}

            .detail-panel {{
                background: var(--panel);
                border: 1px solid var(--border);
                border-left: 4px solid var(--green);
                padding: 20px 24px;
                border-radius: 18px;
                box-shadow: 0 8px 24px rgba(31, 41, 51, 0.05);
                margin-bottom: 18px;
            }}

            .badge {{
                display: inline-block;
                padding: 4px 9px;
                border-radius: 999px;
                font-size: 10px;
                font-weight: 700;
                border: 1px solid;
                white-space: nowrap;
            }}

            .badge.cyan {{
                color: var(--green);
                border-color: #b8d8b8;
                background: #eef8ec;
            }}

            .badge.orange {{
                color: var(--orange);
                border-color: #e7c59c;
                background: #fff4e6;
            }}

            .badge.green {{
                color: var(--green);
                border-color: #b8d8b8;
                background: #eef8ec;
            }}

            .badge.red {{
                color: var(--red);
                border-color: #efb7b4;
                background: #fff0ef;
            }}

            .prop-card-link {{
                display: block;
                text-decoration: none !important;
                color: inherit !important;
            }}

            .prop-card-link:hover {{
                text-decoration: none !important;
            }}

            .prop-row-card {{
                display: grid;
                grid-template-columns: 1.45fr 0.95fr;
                gap: 22px;
                align-items: center;
                background: var(--panel);
                border: 1px solid var(--border);
                border-radius: 20px;
                padding: 18px 22px;
                margin-bottom: 14px;
                box-shadow: 0 8px 22px rgba(31, 41, 51, 0.05);
                cursor: pointer;
                transition: all 0.18s ease;
            }}

            .prop-row-card:hover {{
                border-color: #7fb77e;
                box-shadow: 0 12px 32px rgba(47, 125, 50, 0.14);
                transform: translateY(-2px);
            }}

            .prop-card-top {{
                display: flex;
                justify-content: space-between;
                align-items: flex-start;
                margin-bottom: 8px;
            }}

            .prop-card-badges {{
                display: flex;
                gap: 6px;
                flex-wrap: wrap;
                justify-content: flex-end;
            }}

            .prop-main-title {{
                font-size: 20px;
                font-weight: 800;
                color: var(--text);
                margin-bottom: 4px;
            }}

            .prop-subtitle {{
                font-size: 13px;
                color: var(--text-dim);
                margin-bottom: 14px;
            }}

            .prop-metric-grid {{
                display: grid;
                grid-template-columns: repeat(4, minmax(80px, 1fr));
                gap: 12px;
            }}

            .prop-metric {{
                background: var(--panel-2);
                border: 1px solid var(--grid);
                border-radius: 14px;
                padding: 10px 12px;
            }}

            .prop-metric .label {{
                font-size: 10px;
                font-weight: 700;
                color: var(--text-muted);
                text-transform: uppercase;
                margin-bottom: 4px;
            }}

            .prop-metric .value {{
                font-size: 16px;
                font-weight: 800;
                color: var(--text);
            }}

            .prop-preview {{
                height: 150px;
                border-radius: 18px;
                border: 1px dashed #a9bca4;
                background:
                    radial-gradient(circle at 50% 50%, rgba(47,125,50,0.14), transparent 55%),
                    linear-gradient(135deg, #f7faf6, #edf4ea);
                display: flex;
                align-items: center;
                justify-content: center;
                color: var(--text-muted);
                font-size: 13px;
                font-weight: 700;
            }}

            .prop-preview span {{
                color: var(--green);
            }}

            .geo-card-grid {{
                display: grid;
                grid-template-columns: repeat(5, minmax(130px, 1fr));
                gap: 12px;
                margin-bottom: 8px;
            }}

            .geo-card {{
                background: var(--panel);
                border: 1px solid var(--border);
                border-radius: 16px;
                padding: 13px 14px;
                box-shadow: 0 5px 16px rgba(31, 41, 51, 0.035);
            }}

            .geo-card .label {{
                font-size: 10px;
                font-weight: 800;
                color: var(--text-muted);
                text-transform: uppercase;
                letter-spacing: 0.05em;
                margin-bottom: 6px;
            }}

            .geo-card .value {{
                font-size: 18px;
                font-weight: 800;
                color: var(--text);
                line-height: 1.1;
            }}

            .geo-card .unit {{
                font-size: 12px;
                font-weight: 600;
                color: var(--text-dim);
                margin-left: 3px;
            }}

            section[data-testid="stSidebar"] {{
                background: #ffffff !important;
                border-right: 1px solid var(--border) !important;
            }}

            section[data-testid="stSidebar"] * {{
                color: var(--text) !important;
            }}

            .sidebar-title {{
                font-size: 15px;
                font-weight: 800;
                color: var(--green) !important;
                padding-bottom: 10px;
                border-bottom: 1px solid var(--border);
                margin-bottom: 18px;
            }}

            .sidebar-section {{
                color: var(--text-muted) !important;
                font-size: 11px;
                font-weight: 800;
                text-transform: uppercase;
                margin: 18px 0 8px 0;
            }}

            /* Top navigation only */
            div[data-testid="stHorizontalBlock"] > div > div[data-testid="stRadio"] > div[role="radiogroup"] {{
                display: flex;
                gap: 8px;
                background: var(--panel);
                border: 1px solid var(--border);
                border-radius: 16px;
                padding: 6px;
                width: fit-content;
                box-shadow: 0 6px 18px rgba(31, 41, 51, 0.035);
            }}

            div[data-testid="stHorizontalBlock"] > div > div[data-testid="stRadio"] label {{
                background: transparent !important;
                border: 1px solid transparent !important;
                border-radius: 12px !important;
                padding: 8px 14px !important;
                min-height: 0 !important;
                color: var(--text-dim) !important;
                transition: all 0.15s ease !important;
                cursor: pointer !important;
            }}

            div[data-testid="stHorizontalBlock"] > div > div[data-testid="stRadio"] label:hover {{
                background: #eef8ec !important;
                border-color: #d3e4cd !important;
            }}

            div[data-testid="stHorizontalBlock"] > div > div[data-testid="stRadio"] label:has(input:checked) {{
                background: #e3f2df !important;
                border-color: #b8d8b8 !important;
                color: var(--green) !important;
            }}

            div[data-testid="stHorizontalBlock"] > div > div[data-testid="stRadio"] label:has(input:checked) p,
            div[data-testid="stHorizontalBlock"] > div > div[data-testid="stRadio"] label:has(input:checked) span {{
                color: var(--green) !important;
                font-weight: 800 !important;
            }}

            div[data-testid="stHorizontalBlock"] > div > div[data-testid="stRadio"] label p,
            div[data-testid="stHorizontalBlock"] > div > div[data-testid="stRadio"] label span {{
                color: var(--text-dim) !important;
                font-weight: 700 !important;
                font-size: 13px !important;
            }}

            div[data-testid="stHorizontalBlock"] > div > div[data-testid="stRadio"] label > div:first-child {{
                display: none !important;
            }}

            .stSlider [data-baseweb="slider"] > div > div {{
                background: #d9e3d4 !important;
            }}

            .stSlider [data-baseweb="slider"] > div > div > div {{
                background: var(--green) !important;
            }}

            .stSlider [role="slider"] {{
                background: var(--green) !important;
                border-color: var(--green) !important;
                box-shadow: 0 0 0 3px rgba(47, 125, 50, 0.18) !important;
            }}

            .stButton button {{
                background: var(--green) !important;
                border: 1px solid var(--green) !important;
                color: white !important;
                font-size: 13px !important;
                font-weight: 700 !important;
                border-radius: 12px !important;
                transition: all 0.2s ease !important;
            }}

            .stButton button:hover {{
                background: #256828 !important;
                border-color: #256828 !important;
                color: white !important;
            }}

            .stButton button p,
            .stButton button span {{
                color: white !important;
            }}

            [data-testid="stNumberInput"] label {{
                color: var(--text) !important;
                font-weight: 700 !important;
            }}

            [data-testid="stNumberInput"] input {{
                background: #ffffff !important;
                color: var(--text) !important;
                border: 1px solid var(--border) !important;
                border-radius: 12px !important;
                font-size: 16px !important;
                font-weight: 700 !important;
                box-shadow: none !important;
            }}

            [data-testid="stNumberInput"] button {{
                background: #eef8ec !important;
                color: var(--green) !important;
                border: 1px solid var(--border) !important;
                box-shadow: none !important;
            }}

            [data-testid="stNumberInput"] button svg {{
                fill: var(--green) !important;
            }}

            [data-testid="stNumberInput"] div[data-baseweb="input"] {{
                background: #ffffff !important;
                border-color: var(--border) !important;
                border-radius: 12px !important;
            }}

            [data-testid="stMetric"] {{
                background: var(--panel);
                border: 1px solid var(--border);
                padding: 14px 16px;
                border-radius: 16px;
                box-shadow: 0 6px 18px rgba(31, 41, 51, 0.04);
            }}

            [data-testid="stMetric"],
            [data-testid="stMetric"] * {{
                color: var(--text) !important;
            }}

            [data-testid="stMetricLabel"] {{
                color: var(--text-muted) !important;
                font-size: 11px !important;
                font-weight: 700 !important;
            }}

            [data-testid="stMetricValue"] {{
                color: var(--text) !important;
                font-size: 22px !important;
                font-weight: 800 !important;
            }}

            .footer-ribbon {{
                margin-top: 28px;
                padding: 14px 22px;
                background: var(--panel);
                border: 1px solid var(--border);
                border-radius: 18px;
                display: flex;
                justify-content: space-between;
                align-items: center;
                font-size: 11px;
                color: var(--text-muted);
            }}

            .footer-ribbon .blink {{
                display: inline-block;
                width: 7px;
                height: 7px;
                border-radius: 50%;
                background: var(--green);
                margin-right: 6px;
            }}

            @media (max-width: 1100px) {{
                .hud-masthead {{
                    flex-direction: column;
                    align-items: flex-start;
                    gap: 16px;
                }}

                .hud-masthead .rhs {{
                    flex-wrap: wrap;
                }}

                .prop-row-card {{
                    grid-template-columns: 1fr;
                }}

                .prop-metric-grid {{
                    grid-template-columns: repeat(2, minmax(80px, 1fr));
                }}

                .geo-card-grid {{
                    grid-template-columns: repeat(2, minmax(130px, 1fr));
                }}
            }}
            </style>
            """
        ).strip(),
        unsafe_allow_html=True,
    )


# ─────────────────────────────────────────────────────────────────────────────
# DATA
# ─────────────────────────────────────────────────────────────────────────────
@st.cache_data(show_spinner=False)
def load_data() -> tuple[pd.DataFrame, pd.DataFrame]:
    here = Path(__file__).parent

    full = pd.read_csv(here / "dataset_final.csv")
    selected_raw = pd.read_csv(here / "selected_100.csv")

    selected_ids = selected_raw["prop_id"].astype(int).unique()
    full["is_selected"] = full["prop_id"].astype(int).isin(selected_ids)

    selected = full[full["is_selected"]].copy()

    return full, selected


TIPS = {
    "FOM": "Figure of Merit — ratio of ideal hover power to actual power.",
    "T_W": "Thrust-to-Weight ratio.",
    "Pshaft": "Mechanical power required at the rotor shaft, in Watts.",
    "T": "Static thrust at the design RPM, in Newtons.",
    "hover_time_s": "How long the prop can sustain hover on its design battery.",
    "h_max_m": "Maximum altitude reachable on stored energy with this prop.",
    "flight_time_s": "Total endurance under cruise / mission profile.",
    "RPM_hover": "Estimated rotor speed required to sustain hover.",
    "blade_count": "Number of blades.",
}


# ─────────────────────────────────────────────────────────────────────────────
# UI HELPERS
# ─────────────────────────────────────────────────────────────────────────────
def render_masthead(full: pd.DataFrame, sel: pd.DataFrame) -> None:
    html = f"""
<div class="hud-masthead">
<div class="lhs">
<div class="hud-icon">◎</div>
<div>
<h1>IDEAL Propeller Dataset Dashboard</h1>
<div class="subtitle">Dataset Visualization and Testing Input Dashboard</div>
</div>
</div>
<div class="rhs">
<div class="hud-stat"><div class="v">{len(full):,}</div><div class="l">Configs</div></div>
<div class="hud-stat"><div class="v">{len(sel)}</div><div class="l">Testing set</div></div>
</div>
</div>
"""
    st.markdown(html, unsafe_allow_html=True)


def panel_header(title: str, meta: str = "") -> None:
    html = f"""
<div class="panel-header">
<div class="ph-title">{title}</div>
<div class="ph-meta">{meta}</div>
</div>
"""
    st.markdown(html, unsafe_allow_html=True)


def section_label(text: str) -> None:
    st.markdown(
        f'<div class="section-label">{text}</div>',
        unsafe_allow_html=True,
    )


def geo_card(label: str, value: str, unit: str = "") -> str:
    unit_html = f'<span class="unit">{unit}</span>' if unit else ""
    return f"""
<div class="geo-card">
<div class="label">{label}</div>
<div class="value">{value}{unit_html}</div>
</div>
"""


def _station_value(prop: pd.Series, metric: str, station: str) -> float:
    col = f"{station}_{metric}"

    if col in prop.index:
        return float(prop[col])

    if station == "mid":
        t = float(prop["mid_radial_pos"])
        v_in = float(prop[f"inner_{metric}"])
        v_out = float(prop[f"outer_{metric}"])
        return v_in + t * (v_out - v_in)

    raise KeyError(col)


def render_geometric_parameters(prop: pd.Series) -> None:
    section_label("Geometric Parameters")

    mid_thickness = _station_value(prop, "thickness", "mid")
    mid_camber = _station_value(prop, "camber", "mid")

    cards = [
        geo_card("Radius", f"{float(prop['radius']):.0f}", "mm"),
        geo_card("Blade count", f"{int(prop['blade_count'])}", ""),
        geo_card("Inner chord", f"{float(prop['inner_chord']):.1f}", "mm"),
        geo_card("Inner angle", f"{float(prop['inner_angle']):.1f}", "°"),
        geo_card("Inner thickness", f"{float(prop['inner_thickness']):.1f}", "%"),
        geo_card("Inner camber", f"{float(prop['inner_camber']):.1f}", "%"),
        geo_card("Mid radial position", f"{float(prop['mid_radial_pos']):.2f}", "r/R"),
        geo_card("Mid chord", f"{float(prop['mid_chord']):.1f}", "mm"),
        geo_card("Mid angle", f"{float(prop['mid_angle']):.1f}", "°"),
        geo_card("Mid thickness", f"{mid_thickness:.1f}", "%"),
        geo_card("Mid camber", f"{mid_camber:.1f}", "%"),
        geo_card("Outer chord", f"{float(prop['outer_chord']):.1f}", "mm"),
        geo_card("Outer angle", f"{float(prop['outer_angle']):.1f}", "°"),
        geo_card("Outer thickness", f"{float(prop['outer_thickness']):.1f}", "%"),
        geo_card("Outer camber", f"{float(prop['outer_camber']):.1f}", "%"),
        geo_card("Ring height", f"{float(prop['ring_height']):.1f}", "mm"),
        geo_card("Ring thickness", f"{float(prop['ring_thickness']):.1f}", "mm"),
    ]

    html = f"""
<div class="geo-card-grid">
{''.join(cards)}
</div>
"""
    st.markdown(html, unsafe_allow_html=True)


def fleet_kpis(df: pd.DataFrame) -> None:
    cols = st.columns(6)

    kpi_data = [
        ("Configurations", f"{len(df):,}", "", "Total design fleet"),
        ("Mean FOM", f"{df['FOM'].mean():.3f}", "", "Figure of merit"),
        ("Mean Thrust", f"{df['T'].mean():.3f}", "N", "Static hover"),
        ("Mean Mass", f"{df['m_total_g'].mean():.1f}", "g", "Total assembly"),
        (
            "Hover-Capable",
            f"{df['can_hover'].sum():,}",
            "",
            f"{100 * df['can_hover'].mean():.1f}% of fleet",
        ),
        (
            "Peak Endurance",
            f"{df['flight_time_s'].max():.1f}",
            "s",
            "Max flight time",
        ),
    ]

    for col, (label, value, unit, sub) in zip(cols, kpi_data):
        with col:
            unit_html = f'<span class="unit">{unit}</span>' if unit else ""

            html = f"""
<div class="kpi">
<div class="label">{label}</div>
<div class="value">{value}{unit_html}</div>
<div class="sub">{sub}</div>
</div>
"""
            st.markdown(html, unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# GLOBAL CHARTS
# ─────────────────────────────────────────────────────────────────────────────
def chart_radial_evolution(df: pd.DataFrame, sample_n: int = 280) -> go.Figure:
    sample = df.sample(min(sample_n, len(df)), random_state=42)

    fig = make_subplots(
        rows=2,
        cols=2,
        subplot_titles=(
            "Chord [mm]",
            "Pitch Angle [deg]",
            "Thickness [%]",
            "Camber [%]",
        ),
        horizontal_spacing=0.11,
        vertical_spacing=0.22,
    )

    metric_groups = [
        (1, 1, "chord", COLORS["green_main"]),
        (1, 2, "angle", COLORS["orange"]),
        (2, 1, "thickness", COLORS["blue"]),
        (2, 2, "camber", COLORS["green"]),
    ]

    for row, col, metric, color in metric_groups:
        x_arrs = []
        y_arrs = []

        for _, r in sample.iterrows():
            v_mid = _station_value(r, metric, "mid")
            x_arrs.extend([0.0, r["mid_radial_pos"], 1.0, None])
            y_arrs.extend([r[f"inner_{metric}"], v_mid, r[f"outer_{metric}"], None])

        fig.add_trace(
            go.Scatter(
                x=x_arrs,
                y=y_arrs,
                mode="lines",
                line=dict(color=color, width=0.55),
                opacity=0.13,
                showlegend=False,
                hoverinfo="skip",
            ),
            row=row,
            col=col,
        )

        mid_pos_med = float(df["mid_radial_pos"].median())

        if f"mid_{metric}" in df.columns:
            mid_med = float(df[f"mid_{metric}"].median())
        else:
            t = df["mid_radial_pos"]
            interp = df[f"inner_{metric}"] + t * (
                df[f"outer_{metric}"] - df[f"inner_{metric}"]
            )
            mid_med = float(interp.median())

        med_x = [0.0, mid_pos_med, 1.0]
        med_y = [
            float(df[f"inner_{metric}"].median()),
            mid_med,
            float(df[f"outer_{metric}"].median()),
        ]

        fig.add_trace(
            go.Scatter(
                x=med_x,
                y=med_y,
                mode="lines+markers",
                line=dict(color=color, width=3),
                marker=dict(size=10, color=color, line=dict(color="white", width=1.5)),
                showlegend=False,
                hovertemplate=f"r/R=%{{x:.2f}}<br>{metric}=%{{y:.2f}}<extra></extra>",
                cliponaxis=False,
            ),
            row=row,
            col=col,
        )

        all_metric_values = df[f"inner_{metric}"].tolist() + df[f"outer_{metric}"].tolist()
        if f"mid_{metric}" in df.columns:
            all_metric_values += df[f"mid_{metric}"].tolist()
        else:
            all_metric_values += (
                df[f"inner_{metric}"] + df["mid_radial_pos"] * (df[f"outer_{metric}"] - df[f"inner_{metric}"])
            ).tolist()

        fig.update_yaxes(range=padded_range(all_metric_values, 0.20), row=row, col=col)

    fig.update_xaxes(title_text="r / R", range=[-0.05, 1.05])
    fig.update_layout(margin=dict(l=64, r=34, t=90, b=64))

    return style_fig(fig, height=580)


def chart_kde_histogram(
    values: np.ndarray,
    label: str,
    color: str,
    unit: str = "",
) -> go.Figure:
    fig = go.Figure()

    fig.add_trace(
        go.Histogram(
            x=values,
            nbinsx=30,
            marker=dict(color=color, line=dict(color=COLORS["bg_panel"], width=1)),
            opacity=0.55,
            name="Distribution",
        )
    )

    try:
        if len(np.unique(values)) > 4:
            kde = gaussian_kde(values)
            x_grid = np.linspace(values.min(), values.max(), 250)
            density = kde(x_grid)
            bin_width = (values.max() - values.min()) / 30
            density_scaled = density * len(values) * bin_width

            fig.add_trace(
                go.Scatter(
                    x=x_grid,
                    y=density_scaled,
                    mode="lines",
                    line=dict(color=COLORS["green_main"], width=2.5),
                    name="KDE",
                )
            )
    except Exception:
        pass

    fig.update_layout(
        showlegend=False,
        xaxis_title=f"{label} {unit}",
        yaxis_title="Count",
        bargap=0.04,
    )

    return style_fig(fig, height=260)


def chart_violin(df: pd.DataFrame) -> go.Figure:
    fig = make_subplots(
        rows=1,
        cols=3,
        subplot_titles=("Figure of Merit", "Thrust [N]", "Flight Time [s]"),
        horizontal_spacing=0.08,
    )

    metrics = [
        (1, "FOM", COLORS["violet"]),
        (2, "T", COLORS["green_main"]),
        (3, "flight_time_s", COLORS["orange"]),
    ]

    for col_idx, metric, color in metrics:
        fig.add_trace(
            go.Violin(
                y=df[metric],
                box_visible=True,
                meanline_visible=True,
                fillcolor=color,
                opacity=0.4,
                line_color=color,
                points="outliers",
                showlegend=False,
            ),
            row=1,
            col=col_idx,
        )

    return style_fig(fig, height=360)


def chart_thrust_power(df: pd.DataFrame) -> go.Figure:
    fig = go.Figure()

    fig.add_trace(
        go.Scattergl(
            x=df["Pshaft"],
            y=df["T"],
            mode="markers",
            marker=dict(
                size=4,
                color=df["FOM"],
                colorscale="Viridis",
                opacity=0.6,
                line=dict(width=0),
                colorbar=dict(title="FOM"),
                showscale=True,
            ),
            text=df["prop_id"],
            hovertemplate=(
                "prop_id %{text}<br>"
                "Pshaft=%{x:.2f} W<br>"
                "T=%{y:.3f} N<br>"
                "FOM=%{marker.color:.3f}<extra></extra>"
            ),
        )
    )

    fig.update_layout(
        xaxis_title="Shaft Power P [W]",
        yaxis_title="Thrust T [N]",
    )

    return style_fig(fig, height=420)


def chart_correlation_heatmap(df: pd.DataFrame) -> go.Figure:
    cols = [
        "radius",
        "blade_count",
        "inner_chord",
        "inner_thickness",
        "inner_camber",
        "mid_radial_pos",
        "mid_chord",
        "mid_angle",
        "outer_chord",
        "outer_angle",
        "outer_thickness",
        "outer_camber",
        "ring_height",
        "ring_thickness",
    ]

    cols = [c for c in cols if c in df.columns]

    corr = df[cols].corr(method="spearman").round(2)

    fig = go.Figure(
        data=go.Heatmap(
            z=corr.values,
            x=corr.columns,
            y=corr.columns,
            colorscale=[
                [0, COLORS["red"]],
                [0.4, COLORS["bg_panel_2"]],
                [0.5, COLORS["bg_panel"]],
                [0.6, COLORS["bg_panel_2"]],
                [1, COLORS["green_main"]],
            ],
            zmid=0,
            zmin=-1,
            zmax=1,
            colorbar=dict(title="ρ"),
            hovertemplate="%{y} vs %{x}<br>ρ=%{z}<extra></extra>",
            text=corr.values,
            texttemplate="%{text}",
            textfont=dict(size=9, color=COLORS["text_primary"]),
        )
    )

    fig.update_layout(height=520)
    fig.update_xaxes(side="bottom", tickangle=-45)

    return style_fig(fig)


def chart_testing_coverage_thrust_fom(full: pd.DataFrame, sel: pd.DataFrame) -> go.Figure:
    fig = go.Figure()

    fig.add_trace(
        go.Scattergl(
            x=full["FOM"],
            y=full["T"],
            mode="markers",
            marker=dict(
                size=5,
                color="rgba(47,125,50,0.20)",
                line=dict(width=0),
            ),
            name=f"Full dataset ({len(full):,})",
            text=full["prop_id"],
            hovertemplate=(
                "prop_id %{text}<br>"
                "FOM=%{x:.3f}<br>"
                "Thrust=%{y:.3f} N<extra></extra>"
            ),
        )
    )

    fig.add_trace(
        go.Scattergl(
            x=sel["FOM"],
            y=sel["T"],
            mode="markers",
            marker=dict(
                size=9,
                color=COLORS["orange"],
                line=dict(color="white", width=1),
            ),
            name=f"Testing set ({len(sel)})",
            text=sel["prop_id"],
            hovertemplate=(
                "TEST prop_id %{text}<br>"
                "FOM=%{x:.3f}<br>"
                "Thrust=%{y:.3f} N<extra></extra>"
            ),
        )
    )

    fig.update_layout(
        xaxis_title="Figure of Merit [-]",
        yaxis_title="Static Thrust [N]",
    )

    return style_fig(fig, height=430)


def chart_testing_coverage_mass_tw(full: pd.DataFrame, sel: pd.DataFrame) -> go.Figure:
    fig = go.Figure()

    fig.add_trace(
        go.Scattergl(
            x=full["m_total_g"],
            y=full["T_over_W"],
            mode="markers",
            marker=dict(
                size=5,
                color="rgba(47,125,50,0.20)",
                line=dict(width=0),
            ),
            name=f"Full dataset ({len(full):,})",
            text=full["prop_id"],
            hovertemplate=(
                "prop_id %{text}<br>"
                "Mass=%{x:.2f} g<br>"
                "T/W=%{y:.2f}<extra></extra>"
            ),
        )
    )

    fig.add_trace(
        go.Scattergl(
            x=sel["m_total_g"],
            y=sel["T_over_W"],
            mode="markers",
            marker=dict(
                size=9,
                color=COLORS["orange"],
                line=dict(color="white", width=1),
            ),
            name=f"Testing set ({len(sel)})",
            text=sel["prop_id"],
            hovertemplate=(
                "TEST prop_id %{text}<br>"
                "Mass=%{x:.2f} g<br>"
                "T/W=%{y:.2f}<extra></extra>"
            ),
        )
    )

    fig.update_layout(
        xaxis_title="Total Mass [g]",
        yaxis_title="Thrust / Weight [-]",
    )

    return style_fig(fig, height=430)


def _pca_2d_numpy(
    full: pd.DataFrame,
    sel: pd.DataFrame,
    cols: list[str],
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    X_full = full[cols].astype(float).to_numpy()
    X_sel = sel[cols].astype(float).to_numpy()

    mu = X_full.mean(axis=0)
    sigma = X_full.std(axis=0)
    sigma[sigma == 0] = 1.0

    X_full_scaled = (X_full - mu) / sigma
    X_sel_scaled = (X_sel - mu) / sigma

    _, singular_values, vt = np.linalg.svd(X_full_scaled, full_matrices=False)

    components = vt[:2].T

    full_scores = X_full_scaled @ components
    sel_scores = X_sel_scaled @ components

    explained_variance = singular_values**2 / (len(X_full_scaled) - 1)
    explained_ratio = explained_variance / explained_variance.sum()

    return full_scores, sel_scores, explained_ratio[:2]


def chart_testing_coverage_pca(full: pd.DataFrame, sel: pd.DataFrame) -> go.Figure:
    pca_cols = [
        "radius",
        "blade_count",
        "inner_chord",
        "inner_angle",
        "inner_thickness",
        "inner_camber",
        "mid_radial_pos",
        "mid_chord",
        "mid_angle",
        "outer_chord",
        "outer_angle",
        "outer_thickness",
        "outer_camber",
        "ring_height",
        "ring_thickness",
        "FOM",
        "T",
        "T_over_W",
        "m_total_g",
        "Pshaft",
    ]

    pca_cols = [c for c in pca_cols if c in full.columns and c in sel.columns]

    full_scores, sel_scores, explained_ratio = _pca_2d_numpy(full, sel, pca_cols)

    fig = go.Figure()

    fig.add_trace(
        go.Scattergl(
            x=full_scores[:, 0],
            y=full_scores[:, 1],
            mode="markers",
            marker=dict(
                size=5,
                color="rgba(47,125,50,0.18)",
                line=dict(width=0),
            ),
            name=f"Full dataset ({len(full):,})",
            text=full["prop_id"],
            hovertemplate=(
                "prop_id %{text}<br>"
                "PC1=%{x:.2f}<br>"
                "PC2=%{y:.2f}<extra></extra>"
            ),
        )
    )

    fig.add_trace(
        go.Scattergl(
            x=sel_scores[:, 0],
            y=sel_scores[:, 1],
            mode="markers",
            marker=dict(
                size=9,
                color=COLORS["orange"],
                line=dict(color="white", width=1),
            ),
            name=f"Testing set ({len(sel)})",
            text=sel["prop_id"],
            hovertemplate=(
                "TEST prop_id %{text}<br>"
                "PC1=%{x:.2f}<br>"
                "PC2=%{y:.2f}<extra></extra>"
            ),
        )
    )

    fig.update_layout(
        xaxis_title=f"PC1 [{explained_ratio[0] * 100:.1f}% variance]",
        yaxis_title=f"PC2 [{explained_ratio[1] * 100:.1f}% variance]",
    )

    return style_fig(fig, height=500)


def chart_3d_design_space(full: pd.DataFrame, sel: pd.DataFrame) -> go.Figure:
    not_sel = full[~full["is_selected"]]

    fig = go.Figure()

    fig.add_trace(
        go.Scatter3d(
            x=not_sel["FOM"],
            y=not_sel["T_over_W"],
            z=not_sel["m_total_g"],
            mode="markers",
            marker=dict(
                size=2,
                color=not_sel["FOM"],
                colorscale="Viridis",
                opacity=0.45,
                colorbar=dict(title="FOM"),
            ),
            name=f"Full fleet ({len(not_sel):,})",
            customdata=not_sel["prop_id"],
            hovertemplate=(
                "<b>prop_id %{customdata}</b><br>"
                "FOM=%{x:.3f}<br>"
                "T/W=%{y:.2f}<br>"
                "Mass=%{z:.2f} g<extra></extra>"
            ),
        )
    )

    fig.add_trace(
        go.Scatter3d(
            x=sel["FOM"],
            y=sel["T_over_W"],
            z=sel["m_total_g"],
            mode="markers",
            marker=dict(
                size=5,
                color=COLORS["orange"],
                line=dict(color="white", width=0.5),
                symbol="diamond",
            ),
            name=f"Testing set ({len(sel)})",
            customdata=sel["prop_id"],
            hovertemplate=(
                "<b>TEST prop_id %{customdata}</b><br>"
                "FOM=%{x:.3f}<br>"
                "T/W=%{y:.2f}<br>"
                "Mass=%{z:.2f} g<extra></extra>"
            ),
        )
    )

    axis_kw = dict(
        backgroundcolor=COLORS["bg_panel_2"],
        gridcolor=GRID_COLOR,
        showbackground=True,
        zerolinecolor=ZERO_COLOR,
        title_font=dict(family=PLOT_FONT, color=AXIS_COLOR),
        tickfont=dict(family=PLOT_FONT, color=AXIS_COLOR, size=10),
    )

    fig.update_layout(
        scene=dict(
            xaxis=dict(title="Figure of Merit", **axis_kw),
            yaxis=dict(title="Thrust / Weight [-]", **axis_kw),
            zaxis=dict(title="Total Mass [g]", **axis_kw),
            bgcolor=COLORS["bg_panel"],
            camera=dict(eye=dict(x=1.6, y=1.6, z=1.0)),
        ),
        height=620,
    )

    return style_fig(fig)


# ─────────────────────────────────────────────────────────────────────────────
# SINGLE-PROP CHARTS
# ─────────────────────────────────────────────────────────────────────────────
def chart_prop_radial(prop: pd.Series) -> go.Figure:
    fig = make_subplots(
        rows=2,
        cols=2,
        subplot_titles=("Chord [mm]", "Pitch [deg]", "Thickness [%]", "Camber [%]"),
        horizontal_spacing=0.12,
        vertical_spacing=0.24,
    )

    x = [0.0, float(prop["mid_radial_pos"]), 1.0]

    metrics = [
        (1, 1, "chord", COLORS["green_main"]),
        (1, 2, "angle", COLORS["orange"]),
        (2, 1, "thickness", COLORS["blue"]),
        (2, 2, "camber", COLORS["green"]),
    ]

    for row, col, metric, color in metrics:
        y = [
            float(prop[f"inner_{metric}"]),
            _station_value(prop, metric, "mid"),
            float(prop[f"outer_{metric}"]),
        ]

        fig.add_trace(
            go.Scatter(
                x=x,
                y=y,
                mode="lines+markers+text",
                line=dict(color=color, width=3, shape="spline"),
                marker=dict(size=12, color=color, line=dict(color="white", width=2)),
                text=[f"<b>{v:.1f}</b>" for v in y],
                textposition="top center",
                textfont=dict(family=PLOT_FONT, color=color, size=11),
                showlegend=False,
                cliponaxis=False,
            ),
            row=row,
            col=col,
        )

        fig.update_yaxes(range=padded_range(y, 0.28), row=row, col=col)

    fig.update_xaxes(title_text="r / R", range=[-0.06, 1.06])
    fig.update_layout(margin=dict(l=68, r=40, t=92, b=72))

    return style_fig(fig, height=560)


def chart_blade_planform(prop: pd.Series) -> go.Figure:
    R = float(prop["radius"])

    r_control = np.array([0.0, float(prop["mid_radial_pos"]), 1.0]) * R
    c_control = np.array(
        [
            float(prop["inner_chord"]),
            float(prop["mid_chord"]),
            float(prop["outer_chord"]),
        ],
        dtype=float,
    )

    sort_idx = np.argsort(r_control)
    r_control = r_control[sort_idx]
    c_control = c_control[sort_idx]

    spline = CubicSpline(r_control, c_control, bc_type="natural")

    r_smooth = np.linspace(r_control.min(), r_control.max(), 250)
    c_smooth = spline(r_smooth)
    c_smooth = np.maximum(c_smooth, 0.0)

    upper = c_smooth / 2.0
    lower = -c_smooth / 2.0

    fig = go.Figure()

    hub = 8.5
    theta = np.linspace(0, 2 * np.pi, 120)

    fig.add_trace(
        go.Scatter(
            x=hub * np.cos(theta),
            y=hub * np.sin(theta),
            mode="lines",
            line=dict(color=COLORS["text_muted"], width=1.2, dash="dot"),
            showlegend=False,
            hoverinfo="skip",
            name="Hub",
        )
    )

    fig.add_trace(
        go.Scatter(
            x=R * np.cos(theta),
            y=R * np.sin(theta),
            mode="lines",
            line=dict(color=COLORS["orange"], width=1.2, dash="dash"),
            showlegend=False,
            hoverinfo="skip",
            name="Tip radius",
        )
    )

    fig.add_trace(
        go.Scatter(
            x=np.concatenate([r_smooth, r_smooth[::-1]]),
            y=np.concatenate([upper, lower[::-1]]),
            fill="toself",
            fillcolor="rgba(47,125,50,0.20)",
            line=dict(color=COLORS["green_main"], width=2.4),
            name="Spline blade planform",
            hovertemplate="span=%{x:.1f} mm<br>half chord=%{y:.1f} mm<extra></extra>",
        )
    )

    fig.add_trace(
        go.Scatter(
            x=r_control,
            y=c_control / 2.0,
            mode="markers+text",
            marker=dict(size=9, color=COLORS["orange"], line=dict(color="white", width=1)),
            text=["Inner", "Mid", "Outer"],
            textposition="top center",
            name="Control stations",
            hovertemplate="%{text}<br>span=%{x:.1f} mm<extra></extra>",
            cliponaxis=False,
        )
    )

    max_extent = R + 4

    fig.update_layout(
        xaxis=dict(
            title="Span [mm]",
            range=[-2, max_extent],
            scaleanchor="y",
            scaleratio=1,
        ),
        yaxis=dict(
            title="Chord extent [mm]",
            range=[-max_extent / 2.2, max_extent / 2.2],
        ),
        height=360,
        showlegend=False,
    )

    return style_fig(fig)


def naca4_airfoil(
    camber_percent: float,
    thickness_percent: float,
    p: float = 0.4,
    n: int = 220,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    m = float(camber_percent) / 100.0
    t = float(thickness_percent) / 100.0

    beta = np.linspace(0.0, np.pi, n)
    x = 0.5 * (1.0 - np.cos(beta))

    yt = 5.0 * t * (
        0.2969 * np.sqrt(np.maximum(x, 1e-12))
        - 0.1260 * x
        - 0.3516 * x**2
        + 0.2843 * x**3
        - 0.1015 * x**4
    )

    yc = np.zeros_like(x)
    dyc_dx = np.zeros_like(x)

    if m > 0 and 0 < p < 1:
        left = x < p
        right = ~left

        yc[left] = m / (p**2) * (2 * p * x[left] - x[left] ** 2)
        yc[right] = m / ((1 - p) ** 2) * (
            (1 - 2 * p) + 2 * p * x[right] - x[right] ** 2
        )

        dyc_dx[left] = 2 * m / (p**2) * (p - x[left])
        dyc_dx[right] = 2 * m / ((1 - p) ** 2) * (p - x[right])

    theta = np.arctan(dyc_dx)

    xu = x - yt * np.sin(theta)
    yu = yc + yt * np.cos(theta)

    xl = x + yt * np.sin(theta)
    yl = yc - yt * np.cos(theta)

    return xu, yu, xl, yl


def rotate_xy(
    x: np.ndarray,
    y: np.ndarray,
    angle_deg: float,
    origin_x: float = 0.25,
    origin_y: float = 0.0,
) -> tuple[np.ndarray, np.ndarray]:
    angle = -np.deg2rad(angle_deg)

    x_shift = x - origin_x
    y_shift = y - origin_y

    x_rot = x_shift * np.cos(angle) - y_shift * np.sin(angle) + origin_x
    y_rot = x_shift * np.sin(angle) + y_shift * np.cos(angle) + origin_y

    return x_rot, y_rot


def chart_naca_stations_separated(prop: pd.Series) -> go.Figure:
    stations = [
        {
            "name": "Inner",
            "camber": float(prop["inner_camber"]),
            "thickness": float(prop["inner_thickness"]),
            "angle": float(prop["inner_angle"]),
            "color": COLORS["green_main"],
        },
        {
            "name": "Mid",
            "camber": _station_value(prop, "camber", "mid"),
            "thickness": _station_value(prop, "thickness", "mid"),
            "angle": float(prop["mid_angle"]),
            "color": COLORS["orange"],
        },
        {
            "name": "Outer",
            "camber": float(prop["outer_camber"]),
            "thickness": float(prop["outer_thickness"]),
            "angle": float(prop["outer_angle"]),
            "color": COLORS["blue"],
        },
    ]

    fig = make_subplots(
        rows=1,
        cols=3,
        subplot_titles=[
            f"{s['name']} · α = {s['angle']:.1f}° · t = {s['thickness']:.1f}% · c = {s['camber']:.1f}%"
            for s in stations
        ],
        horizontal_spacing=0.08,
    )

    for idx, station in enumerate(stations, start=1):
        xu, yu, xl, yl = naca4_airfoil(
            camber_percent=station["camber"],
            thickness_percent=station["thickness"],
            p=0.4,
            n=260,
        )

        x_profile = np.concatenate([xu, xl[::-1], [xu[0]]])
        y_profile = np.concatenate([yu, yl[::-1], [yu[0]]])

        x_rot, y_rot = rotate_xy(
            x=x_profile,
            y=y_profile,
            angle_deg=station["angle"],
            origin_x=0.25,
            origin_y=0.0,
        )

        chord_x = np.array([0.0, 1.0])
        chord_y = np.array([0.0, 0.0])
        chord_x_rot, chord_y_rot = rotate_xy(
            x=chord_x,
            y=chord_y,
            angle_deg=station["angle"],
            origin_x=0.25,
            origin_y=0.0,
        )

        fig.add_trace(
            go.Scatter(
                x=x_rot,
                y=y_rot,
                mode="lines",
                fill="toself",
                fillcolor="rgba(47,125,50,0.12)" if idx == 1 else "rgba(199,125,43,0.12)" if idx == 2 else "rgba(79,111,145,0.12)",
                line=dict(color=station["color"], width=2.6),
                name=station["name"],
                hovertemplate=(
                    f"{station['name']}<br>"
                    f"angle={station['angle']:.2f}°<br>"
                    f"camber={station['camber']:.2f}%<br>"
                    f"thickness={station['thickness']:.2f}%<extra></extra>"
                ),
                showlegend=False,
            ),
            row=1,
            col=idx,
        )

        fig.add_trace(
            go.Scatter(
                x=chord_x_rot,
                y=chord_y_rot,
                mode="lines+markers",
                line=dict(color=COLORS["text_muted"], width=1.4, dash="dash"),
                marker=dict(size=5, color=COLORS["text_muted"]),
                name=f"{station['name']} chord",
                hoverinfo="skip",
                showlegend=False,
            ),
            row=1,
            col=idx,
        )

        all_x = np.concatenate([x_rot, chord_x_rot])
        all_y = np.concatenate([y_rot, chord_y_rot])

        fig.update_xaxes(
            title_text="x / chord [-]",
            range=padded_range(all_x, 0.18),
            row=1,
            col=idx,
        )
        fig.update_yaxes(
            title_text="y / chord [-]",
            range=padded_range(all_y, 0.28),
            scaleanchor=f"x{idx}" if idx > 1 else "x",
            scaleratio=1,
            row=1,
            col=idx,
        )

    fig.update_layout(
        height=440,
        margin=dict(l=64, r=34, t=92, b=64),
    )

    return style_fig(fig)


# ─────────────────────────────────────────────────────────────────────────────
# DASHBOARD 1
# ─────────────────────────────────────────────────────────────────────────────
def render_dashboard_1(full: pd.DataFrame, sel: pd.DataFrame) -> None:
    section_label("Fleet Status")
    fleet_kpis(full)

    panel_header(
        "Radial Evolution Analysis",
        f"{min(280, len(full))} samples · 3-station geometry",
    )
    st.caption(
        "Geometric properties traced from hub through mid-span to blade tip. "
        "Bold lines show the fleet median."
    )
    st.plotly_chart(
        chart_radial_evolution(full),
        use_container_width=True,
        config={"displayModeBar": False},
    )

    c1, c2 = st.columns([1.1, 1])

    with c1:
        panel_header("Geometry Distributions", "Histogram + density estimate")

        sub_1, sub_2, sub_3 = st.columns(3)

        with sub_1:
            st.caption("Tip Radius R [mm]")
            st.plotly_chart(
                chart_kde_histogram(full["radius"].values, "Radius", COLORS["green_main"], "[mm]"),
                use_container_width=True,
                config={"displayModeBar": False},
            )

        with sub_2:
            st.caption("Blade Count")
            st.plotly_chart(
                chart_kde_histogram(full["blade_count"].values, "Blades", COLORS["violet"]),
                use_container_width=True,
                config={"displayModeBar": False},
            )

        with sub_3:
            st.caption("Mid Radial Position [r/R]")
            st.plotly_chart(
                chart_kde_histogram(
                    full["mid_radial_pos"].values,
                    "mid_radial_pos",
                    COLORS["orange"],
                ),
                use_container_width=True,
                config={"displayModeBar": False},
            )

    with c2:
        panel_header("Performance Benchmarks", "Violin / quartile / outliers")
        st.plotly_chart(
            chart_violin(full),
            use_container_width=True,
            config={"displayModeBar": False},
        )

    c3, c4 = st.columns([1, 1])

    with c3:
        panel_header("Aerodynamic Operating Map", "Thrust vs shaft power · color = FOM")
        st.caption("The upper-left edge represents configurations with strong thrust per watt.")
        st.plotly_chart(
            chart_thrust_power(full),
            use_container_width=True,
            config={"displayModeBar": False},
        )

    with c4:
        panel_header("Input Correlation Matrix", "Spearman ρ")
        st.caption(
            "Near-zero values indicate broad design-space coverage. "
            "Stronger values indicate geometric or parametric coupling."
        )
        st.plotly_chart(
            chart_correlation_heatmap(full),
            use_container_width=True,
            config={"displayModeBar": False},
        )

    section_label("Testing Set Coverage")

    cov1, cov2 = st.columns(2)

    with cov1:
        panel_header("Coverage: Thrust vs FOM", "Full dataset vs selected 100")
        st.caption(
            "This plot checks whether the selected propellers cover both low and high "
            "efficiency / thrust regions."
        )
        st.plotly_chart(
            chart_testing_coverage_thrust_fom(full, sel),
            use_container_width=True,
            config={"displayModeBar": False},
        )

    with cov2:
        panel_header("Coverage: Mass vs T/W", "Structural-performance coverage")
        st.caption(
            "This plot checks whether the selected propellers span both light and heavy "
            "designs and weak/strong thrust-to-weight configurations."
        )
        st.plotly_chart(
            chart_testing_coverage_mass_tw(full, sel),
            use_container_width=True,
            config={"displayModeBar": False},
        )

    panel_header(
        "Coverage: PCA Design Space",
        "PC1 vs PC2 projection using geometry + performance variables",
    )
    st.caption(
        "The PCA projection compresses the design space into two axes. "
        "A representative testing set should spread across the same region as the full dataset."
    )
    st.plotly_chart(
        chart_testing_coverage_pca(full, sel),
        use_container_width=True,
        config={"displayModeBar": False},
    )

    panel_header(
        "3D Design Space Span",
        "Trade-space: FOM × T/W × Mass",
    )
    st.caption(
        "Drag to rotate. Orange diamonds show the selected 100-propeller testing set."
    )
    st.plotly_chart(
        chart_3d_design_space(full, sel),
        use_container_width=True,
        config={"displayModeBar": True},
    )


# ─────────────────────────────────────────────────────────────────────────────
# DASHBOARD 2
# ─────────────────────────────────────────────────────────────────────────────
def render_prop_card(p: pd.Series, idx: int, in_print_set: bool) -> None:
    prop_id = int(p["prop_id"])

    badge_html = (
        '<span class="badge orange">Testing set</span>'
        if in_print_set
        else '<span class="badge cyan">Simulation</span>'
    )

    hover_badge = (
        '<span class="badge green">Hover capable</span>'
        if p["can_hover"]
        else '<span class="badge red">No hover</span>'
    )

    html = f"""
<a class="prop-card-link" href="?page=explorer&prop_id={prop_id}" target="_self">
<div class="prop-row-card">
<div>
<div class="prop-card-top">
<div>
<div class="prop-main-title">Propeller #{prop_id:04d}</div>
<div class="prop-subtitle">R = {int(p['radius'])} mm · {int(p['blade_count'])} blades · {p['m_total_g']:.1f} g</div>
</div>
<div class="prop-card-badges">
{badge_html}
{hover_badge}
</div>
</div>

<div class="prop-metric-grid">
<div class="prop-metric">
<div class="label">FOM</div>
<div class="value">{p['FOM']:.3f}</div>
</div>

<div class="prop-metric">
<div class="label">Thrust</div>
<div class="value">{p['T']:.3f} N</div>
</div>

<div class="prop-metric">
<div class="label">T/W</div>
<div class="value">{p['T_over_W']:.2f}</div>
</div>

<div class="prop-metric">
<div class="label">Power</div>
<div class="value">{p['Pshaft']:.2f} W</div>
</div>

<div class="prop-metric">
<div class="label">Hover</div>
<div class="value">{p['hover_time_s']:.1f} s</div>
</div>

<div class="prop-metric">
<div class="label">Endurance</div>
<div class="value">{p['flight_time_s']:.1f} s</div>
</div>

<div class="prop-metric">
<div class="label">Altitude</div>
<div class="value">{p['h_max_m']:.1f} m</div>
</div>

<div class="prop-metric">
<div class="label">RPM hover</div>
<div class="value">{p['RPM_hover_min']:.0f}</div>
</div>
</div>
</div>

<div>
<div class="prop-preview">
<span>Open propeller configuration</span>
</div>
</div>
</div>
</a>
"""
    st.markdown(html.strip(), unsafe_allow_html=True)


def render_experimental_validation(prop: pd.Series) -> None:
    section_label("Experimental Validation Input")

    panel_header(
        "Bench Test Comparator",
        "Enter measured values and compare against simulation",
    )

    st.caption(
        "Use this section after physical testing. By default, measured values equal the simulated reference, "
        "so all deviations start at zero."
    )

    sim_t = float(prop["T"])
    sim_p = float(prop["Pshaft"])
    sim_fom = float(prop["FOM"])

    val_l, val_r = st.columns(2)

    with val_l:
        st.markdown(
            """
<div style="font-size:12px;font-weight:700;color:#8a9a8d;text-transform:uppercase;margin-bottom:6px">
Measured input
</div>
""",
            unsafe_allow_html=True,
        )

        exp_t = st.number_input(
            "Experimental Thrust [N]",
            min_value=0.0,
            max_value=10.0,
            value=sim_t,
            step=0.001,
            format="%.4f",
            key=f"exp_t_{int(prop['prop_id'])}",
        )

        exp_p = st.number_input(
            "Experimental Shaft Power [W]",
            min_value=0.0,
            max_value=300.0,
            value=sim_p,
            step=0.01,
            format="%.3f",
            key=f"exp_p_{int(prop['prop_id'])}",
        )

    with val_r:
        html = f"""
<div style="font-size:12px;font-weight:700;color:#8a9a8d;text-transform:uppercase;margin-bottom:6px">
Simulated reference
</div>
<div class="kpi">
<div class="label">Sim Thrust</div>
<div class="value">{sim_t:.4f}<span class="unit">N</span></div>
<div class="sub">Model reference at design point</div>
</div>
<div style="height:8px"></div>
<div class="kpi">
<div class="label">Sim Power</div>
<div class="value">{sim_p:.3f}<span class="unit">W</span></div>
<div class="sub">Shaft input prediction</div>
</div>
"""
        st.markdown(html, unsafe_allow_html=True)

    err_t = ((exp_t - sim_t) / max(sim_t, 1e-9)) * 100.0
    err_p = ((exp_p - sim_p) / max(sim_p, 1e-9)) * 100.0

    if exp_p > 0 and sim_t > 0:
        fom_exp = sim_fom * ((exp_t / sim_t) ** 1.5) * (sim_p / exp_p)
    else:
        fom_exp = 0.0

    err_fom = ((fom_exp - sim_fom) / max(sim_fom, 1e-9)) * 100.0

    def status_color(err: float) -> tuple[str, str]:
        abs_err = abs(err)

        if abs_err < 5:
            return COLORS["green"], "Nominal"

        if abs_err < 15:
            return COLORS["yellow"], "Acceptable"

        return COLORS["red"], "Deviation"

    rcols = st.columns(3)

    results = [
        ("Thrust Δ", sim_t, exp_t, err_t, "N"),
        ("Power Δ", sim_p, exp_p, err_p, "W"),
        ("FOM Δ", sim_fom, fom_exp, err_fom, ""),
    ]

    for col, (label, sim, exp, err, unit) in zip(rcols, results):
        color, status = status_color(err)

        with col:
            html = f"""
<div class="kpi" style="border-left:4px solid {color}">
<div class="label">{label}</div>
<div class="value" style="color:{color}">{err:+.2f}<span class="unit">%</span></div>
<div class="sub" style="color:{color}">● {status}</div>
<div style="display:flex;justify-content:space-between;margin-top:8px;font-size:12px;color:#5f6f63">
<span>SIM <b style="color:#1f2933">{sim:.4f}{unit}</b></span>
<span>MEAS <b style="color:#1f2933">{exp:.4f}{unit}</b></span>
</div>
</div>
"""
            st.markdown(html, unsafe_allow_html=True)


def render_prop_detail(prop: pd.Series, full: pd.DataFrame) -> None:
    in_print = bool(prop["is_selected"])

    badge = (
        '<span class="badge orange">Testing set</span>'
        if in_print
        else '<span class="badge cyan">Simulation only</span>'
    )

    html = f"""
<div class="detail-panel">
<div style="display:flex;justify-content:space-between;align-items:center">
<div>
<div style="font-size:12px;font-weight:700;color:#8a9a8d;text-transform:uppercase;">
Propeller configuration
</div>
<div style="font-size:34px;font-weight:800;color:#1f2933;letter-spacing:-0.03em">
Propeller #{int(prop['prop_id']):04d}
</div>
<div style="color:#5f6f63;font-size:14px;">
R = {int(prop['radius'])} mm · {int(prop['blade_count'])} blades · {prop['m_total_g']:.2f} g
</div>
</div>
<div style="text-align:right">
{badge}
<div style="font-size:44px;color:#2f7d32;font-weight:800;line-height:1;margin-top:8px;">
{prop['FOM']:.3f}
</div>
<div style="font-size:11px;font-weight:700;color:#8a9a8d;text-transform:uppercase;">
Figure of merit
</div>
</div>
</div>
</div>
"""
    st.markdown(html, unsafe_allow_html=True)

    perf_cols = st.columns(6)

    perf_data = [
        ("Static Thrust", f"{prop['T']:.4f}", "N", TIPS["T"]),
        ("Shaft Power", f"{prop['Pshaft']:.3f}", "W", TIPS["Pshaft"]),
        ("T / W Ratio", f"{prop['T_over_W']:.2f}", "", TIPS["T_W"]),
        ("Hover Time", f"{prop['hover_time_s']:.2f}", "s", TIPS["hover_time_s"]),
        ("Max Altitude", f"{prop['h_max_m']:.1f}", "m", TIPS["h_max_m"]),
        ("Hover RPM", f"{prop['RPM_hover_min']:.0f}", "", TIPS["RPM_hover"]),
    ]

    for col, (lab, val, unit, tip) in zip(perf_cols, perf_data):
        with col:
            unit_html = f'<span class="unit">{unit}</span>' if unit else ""

            html = f"""
<div class="kpi" title="{tip}">
<div class="label">{lab}</div>
<div class="value">{val}{unit_html}</div>
<div class="sub" style="font-size:11px">{tip[:48]}{'…' if len(tip) > 48 else ''}</div>
</div>
"""
            st.markdown(html, unsafe_allow_html=True)

    render_geometric_parameters(prop)

    section_label("Geometric Profile")

    g1, g2 = st.columns([1.15, 1])

    with g1:
        panel_header("Radial Profile", "Chord / pitch / thickness / camber")
        st.plotly_chart(
            chart_prop_radial(prop),
            use_container_width=True,
            config={"displayModeBar": False},
        )

    with g2:
        panel_header("Blade Planform", "Top view · cubic spline chord distribution")
        st.plotly_chart(
            chart_blade_planform(prop),
            use_container_width=True,
            config={"displayModeBar": False},
        )

    panel_header(
        "NACA 4-Digit Airfoil Reconstruction",
        "Separated inner / mid / outer plots · local pitch angle included",
    )
    st.caption(
        "Each subplot uses NACA 4-digit equations and rotates the airfoil by its local pitch angle. "
        "The mid station uses the same interpolation rule as the generator: "
        "mid = inner + mid_radial_pos · (outer − inner). "
        "The position of maximum camber is fixed at p = 0.4 because it is not stored in the dataset."
    )
    st.plotly_chart(
        chart_naca_stations_separated(prop),
        use_container_width=True,
        config={"displayModeBar": False},
    )

    section_label("Mass Budget & Flight Envelope")

    m1, m2 = st.columns([1, 1.15])

    with m1:
        panel_header("Mass Budget", "Hub · blades · ring breakdown")

        masses = pd.DataFrame(
            {
                "Component": ["Hub", "Blades", "Ring"],
                "Mass [g]": [prop["m_hub_g"], prop["m_blades_g"], prop["m_ring_g"]],
            }
        )

        fig_mass = go.Figure(
            go.Bar(
                x=masses["Mass [g]"],
                y=masses["Component"],
                orientation="h",
                marker=dict(
                    color=[COLORS["blue"], COLORS["green_main"], COLORS["orange"]],
                    line=dict(color=COLORS["bg_panel"], width=1.5),
                ),
                text=[
                    f"{v:.2f} g · {100 * v / prop['m_total_g']:.1f}%"
                    for v in masses["Mass [g]"]
                ],
                textposition="outside",
                hovertemplate="%{y}: %{x:.2f} g<extra></extra>",
            )
        )

        fig_mass.update_layout(
            xaxis_title="Mass [g]",
            yaxis_title="",
            height=280,
            showlegend=False,
        )

        st.plotly_chart(
            style_fig(fig_mass),
            use_container_width=True,
            config={"displayModeBar": False},
        )

    with m2:
        panel_header(
            "Flight Envelope vs Fleet",
            f"Percentile rank of propeller #{int(prop['prop_id']):04d}",
        )

        rank_metrics = [
            ("FOM", prop["FOM"], full["FOM"]),
            ("Thrust [N]", prop["T"], full["T"]),
            ("T/W", prop["T_over_W"], full["T_over_W"]),
            ("Hover [s]", prop["hover_time_s"], full["hover_time_s"]),
            ("Endurance [s]", prop["flight_time_s"], full["flight_time_s"]),
            ("Max Alt [m]", prop["h_max_m"], full["h_max_m"]),
            ("V max [m/s]", prop["v_max_ms"], full["v_max_ms"]),
        ]

        labels = []
        values = []

        for label, v, series in rank_metrics:
            pct = (series < v).mean() * 100.0
            labels.append(label)
            values.append(pct)

        fig_rank = go.Figure()

        fig_rank.add_trace(
            go.Bar(
                x=values,
                y=labels,
                orientation="h",
                marker=dict(
                    color=values,
                    colorscale=[
                        [0, COLORS["red"]],
                        [0.5, COLORS["yellow"]],
                        [1, COLORS["green"]],
                    ],
                    cmin=0,
                    cmax=100,
                    line=dict(color=COLORS["bg_panel"], width=1.5),
                ),
                text=[f"{v:.0f} %ile" for v in values],
                textposition="inside",
                hovertemplate="%{y}<br>Better than %{x:.1f}% of fleet<extra></extra>",
            )
        )

        fig_rank.update_layout(
            xaxis=dict(title="Percentile rank within fleet", range=[0, 105]),
            yaxis=dict(autorange="reversed"),
            height=320,
            showlegend=False,
        )

        st.plotly_chart(
            style_fig(fig_rank),
            use_container_width=True,
            config={"displayModeBar": False},
        )

    render_experimental_validation(prop)


def render_dashboard_2(full: pd.DataFrame, sel: pd.DataFrame) -> None:
    if "visible_prop_cards" not in st.session_state:
        st.session_state["visible_prop_cards"] = 25

    query_params = st.query_params

    if "prop_id" in query_params:
        try:
            st.session_state["selected_prop_id"] = int(query_params["prop_id"])
        except ValueError:
            st.session_state["selected_prop_id"] = None

    with st.sidebar:
        st.markdown(
            '<div class="sidebar-title">Propeller filters</div>',
            unsafe_allow_html=True,
        )

        st.markdown(
            '<div class="sidebar-section">Source set</div>',
            unsafe_allow_html=True,
        )

        source = st.radio(
            "Source",
            options=["Full fleet", "Testing set (100)", "Hover-capable only"],
            label_visibility="collapsed",
            key="filter_source",
        )

        search_prop = st.text_input(
            "Search propeller ID",
            placeholder="Example: 42",
            key="filter_search_prop",
        )

        st.markdown(
            '<div class="sidebar-section">Geometry</div>',
            unsafe_allow_html=True,
        )

        radius_range = st.slider(
            "Radius [mm]",
            int(full["radius"].min()),
            int(full["radius"].max()),
            (int(full["radius"].min()), int(full["radius"].max())),
            help="Tip radius R of the propeller in millimetres.",
            key="filter_radius",
        )

        blade_choices = sorted(full["blade_count"].unique().tolist())

        blades_sel = st.multiselect(
            "Blade count",
            options=blade_choices,
            default=blade_choices,
            help=TIPS["blade_count"],
            key="filter_blades",
        )

        st.markdown(
            '<div class="sidebar-section">Performance</div>',
            unsafe_allow_html=True,
        )

        fom_range = st.slider(
            "Figure of Merit",
            0.0,
            1.0,
            (float(full["FOM"].quantile(0.25)), float(full["FOM"].max())),
            step=0.01,
            help=TIPS["FOM"],
            key="filter_fom",
        )

        thrust_range = st.slider(
            "Thrust [N]",
            0.0,
            float(full["T"].max() + 0.05),
            (0.0, float(full["T"].max() + 0.05)),
            step=0.05,
            help=TIPS["T"],
            key="filter_thrust",
        )

        st.markdown(
            '<div class="sidebar-section">Sort</div>',
            unsafe_allow_html=True,
        )

        sort_by = st.selectbox(
            "Sort by",
            [
                "FOM (high→low)",
                "Thrust (high→low)",
                "Mass (low→high)",
                "T/W (high→low)",
                "prop_id",
            ],
            key="filter_sort",
        )

    current_filter_state = (
        source,
        search_prop,
        tuple(radius_range),
        tuple(blades_sel),
        tuple(fom_range),
        tuple(thrust_range),
        sort_by,
    )

    if st.session_state.get("previous_filter_state") != current_filter_state:
        st.session_state["visible_prop_cards"] = 25
        st.session_state["previous_filter_state"] = current_filter_state

    if source == "Full fleet":
        df = full.copy()
    elif source == "Testing set (100)":
        df = full[full["is_selected"]].copy()
    else:
        df = full[full["can_hover"]].copy()

    df = df[
        (df["radius"].between(*radius_range))
        & (df["blade_count"].isin(blades_sel))
        & (df["FOM"].between(*fom_range))
        & (df["T"].between(*thrust_range))
    ]

    if search_prop.strip():
        try:
            searched_id = int(search_prop.strip())
            df = df[df["prop_id"] == searched_id]
        except ValueError:
            st.warning("Propeller ID search must be a number.")

    sort_map = {
        "FOM (high→low)": ("FOM", False),
        "Thrust (high→low)": ("T", False),
        "Mass (low→high)": ("m_total_g", True),
        "T/W (high→low)": ("T_over_W", False),
        "prop_id": ("prop_id", True),
    }

    sort_col, sort_asc = sort_map[sort_by]
    df = df.sort_values(sort_col, ascending=sort_asc).reset_index(drop=True)

    if (
        "selected_prop_id" in st.session_state
        and st.session_state["selected_prop_id"] is not None
    ):
        pid = int(st.session_state["selected_prop_id"])

        if len(full[full["prop_id"] == pid]) == 0:
            st.session_state["selected_prop_id"] = None
            st.query_params.clear()
            st.warning("Selected propeller was not found.")
            return

        prop = full[full["prop_id"] == pid].iloc[0]

        back_col, _ = st.columns([1.2, 6])

        with back_col:
            if st.button("Back to list", use_container_width=True):
                st.session_state["selected_prop_id"] = None
                st.query_params.clear()
                st.session_state["main_dashboard_section"] = "Propeller Configuration Explorer"
                st.rerun()

        render_prop_detail(prop, full)
        return

    section_label("Propeller Inventory")

    info_cols = st.columns([2, 1, 1, 1])

    with info_cols[0]:
        html = f"""
<div style="padding:14px 0">
<div style="color:#2f7d32;font-size:22px;font-weight:800;letter-spacing:-0.02em">
{len(df):,} propellers match active filters
</div>
<div style="color:#5f6f63;font-size:13px;margin-top:4px">
Sorted by <b style="color:#1f2933">{sort_by}</b>
</div>
</div>
"""
        st.markdown(html, unsafe_allow_html=True)

    with info_cols[1]:
        st.metric(
            "Mean FOM",
            f"{df['FOM'].mean():.3f}" if len(df) else "—",
            help=TIPS["FOM"],
        )

    with info_cols[2]:
        st.metric(
            "Mean Thrust",
            f"{df['T'].mean():.3f} N" if len(df) else "—",
            help=TIPS["T"],
        )

    with info_cols[3]:
        st.metric(
            "Mean Mass",
            f"{df['m_total_g'].mean():.1f} g" if len(df) else "—",
        )

    if len(df) == 0:
        st.warning("No propellers match the current filter set. Loosen constraints.")
        return

    visible_n = min(st.session_state["visible_prop_cards"], len(df))
    visible_df = df.head(visible_n)

    st.markdown(
        f"""
<div style="font-size:13px;color:#5f6f63;margin-bottom:12px;">
Showing <b>{visible_n}</b> of <b>{len(df):,}</b> matching propellers.
</div>
""",
        unsafe_allow_html=True,
    )

    with st.container(height=780, border=False):
        for idx, (_, p) in enumerate(visible_df.iterrows()):
            render_prop_card(
                p=p,
                idx=idx,
                in_print_set=bool(p["is_selected"]),
            )

    if visible_n < len(df):
        load_more_col, _ = st.columns([1, 4])

        with load_more_col:
            if st.button("Load more", use_container_width=True):
                st.session_state["visible_prop_cards"] += 25
                st.rerun()


# ─────────────────────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────────────────────
def main() -> None:
    inject_css()

    if "selected_prop_id" not in st.session_state:
        st.session_state["selected_prop_id"] = None

    full, sel = load_data()
    query_params = st.query_params

    page_options = [
        "Global Dataset Analytics",
        "Propeller Configuration Explorer",
    ]

    if "main_dashboard_section" not in st.session_state:
        if "prop_id" in query_params or query_params.get("page") == "explorer":
            st.session_state["main_dashboard_section"] = "Propeller Configuration Explorer"
        else:
            st.session_state["main_dashboard_section"] = "Global Dataset Analytics"

    if st.session_state["main_dashboard_section"] == "Propeller Configuration Explorer":
        if "prop_id" in query_params:
            try:
                st.session_state["selected_prop_id"] = int(query_params["prop_id"])
            except ValueError:
                st.session_state["selected_prop_id"] = None

    render_masthead(full, sel)

    nav_col, _ = st.columns([2, 5])

    with nav_col:
        page = st.radio(
            "Dashboard section",
            options=page_options,
            horizontal=True,
            label_visibility="collapsed",
            key="main_dashboard_section",
        )

    if page == "Global Dataset Analytics":
        st.session_state["selected_prop_id"] = None
        render_dashboard_1(full, sel)
    else:
        render_dashboard_2(full, sel)

    st.markdown(
        f"""
<div class="footer-ribbon">
<div><span class="blink"></span> System online · Dashboard ready</div>
<div>BEM + duct model · ρ = 1.225 kg/m³</div>
<div>{len(full):,} configs · {len(sel)} selected for testing</div>
<div>PROP·LAB v2.0</div>
</div>
""",
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()
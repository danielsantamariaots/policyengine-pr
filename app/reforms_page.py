"""Reformas: score reforms on the PRCS microdata (bill-tracker style).

Each row is a reform; columns are the revenue cost to Hacienda, the change
in PAN spending, the share of households better and worse off, and the
mean change in net income. Selecting a row shows the decile chart.
"""

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from policyengine_pr.analysis.scoring import score
from policyengine_pr.reforms.parametric import parametric_reform

BASELINE_COLOR = "#2a78d6"
REFORM_COLOR = "#eb6834"
MARKET_COLOR = "#9a9a94"

TEXT = {
    "title": (
        "Reformas · impacto en Puerto Rico",
        "Reforms · impact on Puerto Rico",
    ),
    "caption": (
        "Cada reforma se simula sobre la Encuesta sobre la Comunidad de Puerto "
        "Rico 2023 (PUMS, {:,.0f} hogares) con las reglas de 2025, con pesos "
        "calibrados a los totales oficiales de recaudo, Crédito por Trabajo y "
        "PAN (véase Calibración, al pie).",
        "Each reform is simulated on the 2023 Puerto Rico Community Survey "
        "(PUMS, {:,.0f} households) under 2025 rules, with weights calibrated "
        "to official totals for revenue, Crédito por Trabajo and PAN (see "
        "Calibration, at the foot).",
    ),
    "custom": ("Reforma de la barra lateral", "Sidebar reform"),
    "col_reform": ("Reforma", "Reform"),
    "col_cost": ("Costo para Hacienda", "Cost to Hacienda"),
    "col_cost_help": (
        "Contribución perdida más Crédito por Trabajo adicional, en millones",
        "Tax lost plus extra Crédito por Trabajo, in millions",
    ),
    "col_pan": ("Cambio en PAN", "PAN change"),
    "col_better": ("Hogares que ganan", "Households better off"),
    "col_worse": ("Hogares que pierden", "Households worse off"),
    "col_mean": ("Cambio medio por hogar", "Mean change per household"),
    "pick": ("Reforma a detallar", "Reform to detail"),
    "chart_title": (
        "Cambio medio en ingreso neto por decil de ingreso",
        "Mean change in net income by income decile",
    ),
    "x_axis": (
        "Decil de ingreso neto del hogar (1 = más bajo)",
        "Household net-income decile (1 = lowest)",
    ),
    "s_change": ("Cambio medio ($/año)", "Mean change ($/year)"),
    "share_title": (
        "Hogares que ganan y pierden por decil",
        "Households better and worse off by decile",
    ),
    "s_better": ("Ganan", "Better off"),
    "s_worse": ("Pierden", "Worse off"),
    "totals_title": (
        "Totales (millones de dólares al año)",
        "Totals ($ million a year)",
    ),
    "col_item": ("Partida", "Item"),
    "col_base": ("Ley vigente", "Current law"),
    "col_ref": ("Reforma", "Reform"),
    "col_change": ("Cambio", "Change"),
    "calibration_title": (
        "Calibración a totales oficiales",
        "Calibration to official totals",
    ),
    "calibration_intro": (
        "Los pesos de la encuesta se reponderan para reproducir estos totales "
        "administrativos (fuentes en docs/statutes/calibration/SOURCES.md). "
        "'Antes' es la encuesta sin calibrar; 'Después', la base que usa esta página.",
        "Survey weights are reweighted to reproduce these administrative totals "
        "(sources in docs/statutes/calibration/SOURCES.md). 'Before' is the "
        "uncalibrated survey; 'After' is the base this page uses.",
    ),
    "uncalibrated": (
        "Base sin calibrar: ejecute build_calibrated() para calibrar los pesos.",
        "Uncalibrated base: run build_calibrated() to calibrate the weights.",
    ),
    "col_target": ("Total", "Total"),
    "col_published": ("Publicado", "Published"),
    "col_before": ("Antes", "Before"),
    "col_after": ("Después", "After"),
    "no_data": (
        "No se encuentra el archivo de microdatos (data/prcs_2023.h5). "
        "Descargue los PUMS 2023 de Puerto Rico en data/raw/pums_2023/ y "
        "ejecute `python -c 'from policyengine_pr.data import build_prcs; "
        "build_prcs()'`.",
        "Microdata file not found (data/prcs_2023.h5). Download the 2023 "
        "Puerto Rico PUMS into data/raw/pums_2023/ and run "
        "`python -c 'from policyengine_pr.data import build_prcs; build_prcs()'`.",
    ),
    "note": (
        "Supuestos: unidades contributivas construidas desde la composición "
        "del hogar (jefe y cónyuge rinden en conjunto; otros adultos, "
        "individual); ingresos de 2023 sin ajustar a 2025; intereses, "
        "dividendos y rentas de la PUMS tratados como intereses bancarios; "
        "PAN al beneficio máximo para todo hogar elegible, sin prueba de "
        "recursos ni tasa de participación. Sin efectos de comportamiento.",
        "Assumptions: tax units built from household composition (head and "
        "spouse file jointly; other adults singly); 2023 incomes not uprated "
        "to 2025; PUMS interest, dividends and rent treated as bank interest; "
        "PAN at the maximum for every eligible household, no resources test "
        "or take-up rate. No behavioural responses.",
    ),
}


@st.cache_resource(show_spinner=False)
def _baseline():
    from policyengine_pr import Simulation
    from policyengine_pr.analysis.scoring import default_dataset

    return Simulation(dataset=default_dataset())


@st.cache_data(show_spinner=False)
def _calibration_report():
    from policyengine_pr import Simulation
    from policyengine_pr.data import PRCS, calibrate

    _, report = calibrate(Simulation(dataset=PRCS))
    return report


@st.cache_data(show_spinner=False)
def _score(changes: tuple):
    reform = parametric_reform(dict(changes)) if changes else None
    return score(reform, baseline_sim=_baseline())


def money_m(x):
    return f"{x / 1e6:,.0f} M"


def render(L, example_reforms, current_values, sidebar_changes, sidebar_name):
    def t(key, *args):
        s = TEXT[key][L]
        return s.format(*args) if args else s

    from policyengine_pr.data import PRCS

    if not PRCS.file_path.exists():
        st.title(t("title"))
        st.warning(t("no_data"))
        return

    reforms = []
    for key, es, en, changes in example_reforms:
        if key == "none":
            continue
        resolved = {
            path: (round(current_values[path] * 1.2) if v is None else v)
            for path, v in changes.items()
        }
        reforms.append(((es, en)[L], tuple(sorted(resolved.items()))))
    if sidebar_changes:
        reforms.append((sidebar_name, tuple(sorted(sidebar_changes.items()))))

    results = {name: _score(changes) for name, changes in reforms}
    households = (
        next(iter(results.values()))["summary"]["households"] if results else 0
    )

    st.title(t("title"))
    st.caption(t("caption", households))

    table = pd.DataFrame(
        [
            {
                t("col_reform"): name,
                t("col_cost"): r["summary"]["revenue_change"],
                t("col_pan"): r["summary"]["pan_change"],
                t("col_better"): r["summary"]["share_better_off"],
                t("col_worse"): r["summary"]["share_worse_off"],
                t("col_mean"): r["summary"]["net_income_change"] / households,
            }
            for name, r in results.items()
        ]
    )
    st.dataframe(
        table.style.format(
            {
                t("col_cost"): lambda x: f"${x / 1e6:,.0f} M",
                t("col_pan"): lambda x: f"${x / 1e6:+,.0f} M",
                t("col_better"): "{:.0%}",
                t("col_worse"): "{:.0%}",
                t("col_mean"): "${:,.0f}",
            }
        ),
        use_container_width=True,
        hide_index=True,
        column_config={
            t("col_cost"): st.column_config.TextColumn(help=t("col_cost_help"))
        },
    )

    pick = st.selectbox(t("pick"), list(results))
    r = results[pick]
    dec = r["deciles"]

    layout = dict(
        margin=dict(l=10, r=10, t=10, b=10),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        legend=dict(orientation="h", y=1.1, x=0),
        xaxis=dict(title=t("x_axis"), dtick=1, showgrid=False),
        yaxis=dict(
            title=None, gridcolor="rgba(128,128,128,0.18)", zeroline=False
        ),
    )
    st.subheader(t("chart_title"))
    fig = go.Figure(
        go.Bar(
            x=dec["decile"],
            y=dec["mean_change"],
            name=t("s_change"),
            marker=dict(
                color=[
                    REFORM_COLOR if v < 0 else BASELINE_COLOR
                    for v in dec["mean_change"]
                ]
            ),
            hovertemplate="%{y:$,.0f}<extra></extra>",
        )
    )
    fig.add_hline(y=0, line=dict(color=MARKET_COLOR, width=1))
    fig.update_layout(height=320, **layout)
    fig.update_yaxes(tickprefix="$", tickformat=",")
    st.plotly_chart(fig, use_container_width=True)

    st.subheader(t("share_title"))
    fig = go.Figure()
    fig.add_trace(
        go.Bar(
            x=dec["decile"],
            y=dec["share_better_off"],
            name=t("s_better"),
            marker=dict(color=BASELINE_COLOR),
            hovertemplate="%{y:.0%}<extra>" + t("s_better") + "</extra>",
        )
    )
    fig.add_trace(
        go.Bar(
            x=dec["decile"],
            y=-dec["share_worse_off"],
            name=t("s_worse"),
            marker=dict(color=REFORM_COLOR),
            hovertemplate="%{y:.0%}<extra>" + t("s_worse") + "</extra>",
        )
    )
    fig.add_hline(y=0, line=dict(color=MARKET_COLOR, width=1))
    fig.update_layout(height=280, barmode="relative", **layout)
    fig.update_yaxes(tickformat=".0%")
    st.plotly_chart(fig, use_container_width=True)

    st.subheader(t("totals_title"))
    tot = r["totals"]
    st.dataframe(
        pd.DataFrame(
            {
                t("col_item"): tot["label_es" if L == 0 else "label_en"],
                t("col_base"): tot["baseline"] / 1e6,
                t("col_ref"): tot["reform"] / 1e6,
                t("col_change"): tot["change"] / 1e6,
            }
        ).style.format(
            {
                t("col_base"): "{:,.0f}",
                t("col_ref"): "{:,.0f}",
                t("col_change"): "{:+,.0f}",
            }
        ),
        use_container_width=True,
        hide_index=True,
    )
    st.caption(t("note"))

    from policyengine_pr.analysis.scoring import default_dataset
    from policyengine_pr.data import PRCSCalibrated

    with st.expander(t("calibration_title")):
        if default_dataset() is PRCSCalibrated:
            st.markdown(t("calibration_intro"))
            rep = _calibration_report()
            st.dataframe(
                pd.DataFrame(
                    {
                        t("col_target"): rep["target"],
                        t("col_published"): rep["published"],
                        t("col_before"): rep["before"],
                        t("col_after"): rep["after"],
                    }
                ).style.format(
                    {
                        c: "{:,.0f}"
                        for c in (
                            t("col_published"),
                            t("col_before"),
                            t("col_after"),
                        )
                    }
                ),
                use_container_width=True,
                hide_index=True,
            )
        else:
            st.warning(t("uncalibrated"))

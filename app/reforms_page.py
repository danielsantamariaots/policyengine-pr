"""Reformas: score reforms on the PRCS microdata (bill-tracker style).

Each row is a reform; columns are the revenue cost to Hacienda, the change
in PAN spending, the share of households better and worse off, and the
mean change in net income. Selecting a row shows the decile chart.
"""

from pathlib import Path

import charts
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
    "chart_sub": (
        "Cambio anual medio en el ingreso neto de los hogares de cada decil, reforma menos ley vigente",
        "Mean annual change in household net income by decile, reform minus current law",
    ),
    "share_sub": (
        "Porcentaje de hogares de cada decil cuyo ingreso neto sube (arriba) o baja (abajo)",
        "Share of households in each decile whose net income rises (above) or falls (below)",
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
    "eti": ("Respuesta de comportamiento", "Behavioural response"),
    "eti_help": (
        "Elasticidad del ingreso tributable: cuánto cambian los salarios cuando cambia la "
        "tasa marginal neta. 0 = modelo estático; 0.25 es una estimación central habitual.",
        "Elasticity of taxable income: how much wages respond to the net-of-tax marginal "
        "rate. 0 = static; 0.25 is a common central estimate.",
    ),
    "eti_static": ("Ninguna (estático)", "None (static)"),
    "benefits_title": (
        "Créditos y beneficios por decil, ley vigente",
        "Credits and benefits by decile, current law",
    ),
    "benefits_sub": (
        "Promedio anual por hogar en cada decil, reciba o no el programa. Sección 8 se imputa a hogares arrendatarios dentro del límite de ingreso muy bajo (calibrado a 28,425 hogares; el subsidio total modelado es el 66% del de HUD).",
        "Annual average per household in each decile, recipients or not. Section 8 is imputed to renter households within the very low income limit (calibrated to 28,425 households; the modelled subsidy total is 66% of HUD's).",
    ),
    "benefits_y": ("Promedio anual por hogar", "Annual average per household"),
    "benefits_table": ("Ver tabla", "Table view"),
    "col_share": ("% de hogares con {}", "% of households with {}"),
    "col_mean": ("{} medio", "Mean {}"),
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
def _baseline_for(dataset_mtime: float):
    """Baseline simulation, cached per dataset file version so a redeployed
    data file never meets a baseline built from the previous one."""
    from policyengine_pr import Simulation
    from policyengine_pr.analysis.scoring import default_dataset

    return Simulation(dataset=default_dataset())


def _baseline():
    from policyengine_pr.analysis.scoring import default_dataset

    return _baseline_for(default_dataset().file_path.stat().st_mtime)


REPORT_CSV = (
    Path(__file__).resolve().parents[1] / "data" / "calibration_report.csv"
)


@st.cache_data(show_spinner=False)
def _calibration_report():
    if REPORT_CSV.exists():
        return pd.read_csv(REPORT_CSV)
    from policyengine_pr import Simulation
    from policyengine_pr.data import PRCS, calibrate

    _, report = calibrate(Simulation(dataset=PRCS))
    return report


@st.cache_data(show_spinner=False)
def _benefits_for(dataset_mtime: float):
    from policyengine_pr.analysis.scoring import benefits_by_decile

    return benefits_by_decile(_baseline())


def _benefits():
    from policyengine_pr.analysis.scoring import default_dataset

    return _benefits_for(default_dataset().file_path.stat().st_mtime)


@st.cache_data(show_spinner=False)
def _score_for(changes: tuple, eti: float, dataset_mtime: float):
    reform = parametric_reform(dict(changes)) if changes else None
    return score(reform, baseline_sim=_baseline(), eti=eti)


def _score(changes: tuple, eti: float = 0.0):
    from policyengine_pr.analysis.scoring import default_dataset

    return _score_for(
        changes, eti, default_dataset().file_path.stat().st_mtime
    )


def money_m(x):
    return f"{x / 1e6:,.0f} M"


def render(L, example_reforms, current_values, sidebar_changes, sidebar_name):
    def t(key, *args):
        s = TEXT[key][L]
        return s.format(*args) if args else s

    from policyengine_pr.analysis.scoring import default_dataset

    if not default_dataset().file_path.exists():
        st.title(t("title"))
        st.warning(t("no_data"))
        return

    reforms = []
    for key, es, en, changes in example_reforms:
        if key == "none":
            continue
        resolved = dict(changes)
        reforms.append(((es, en)[L], tuple(sorted(resolved.items()))))
    if sidebar_changes:
        reforms.append((sidebar_name, tuple(sorted(sidebar_changes.items()))))

    st.title(t("title"))
    eti = st.radio(
        t("eti"),
        [0.0, 0.25, 0.4],
        format_func=lambda v: t("eti_static") if v == 0 else f"ETI {v}",
        horizontal=True,
        help=t("eti_help"),
    )
    results = {name: _score(changes, eti) for name, changes in reforms}
    households = (
        next(iter(results.values()))["summary"]["households"] if results else 0
    )

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

    fig = charts.figure(
        t("chart_title"),
        t("chart_sub"),
        x_title=t("x_axis"),
        y_money=True,
        height=360,
    )
    fig.add_trace(
        go.Bar(
            x=dec["decile"],
            y=dec["mean_change"],
            name=t("s_change"),
            marker=dict(
                color=[
                    charts.SERIES["worse"]
                    if v < 0
                    else charts.SERIES["better"]
                    for v in dec["mean_change"]
                ],
                line=dict(width=0),
            ),
            text=[f"${v:+,.0f}" for v in dec["mean_change"]],
            textposition="outside",
            textfont=dict(size=11, color=charts.MUTED),
            cliponaxis=False,
            hovertemplate="%{y:$,.0f}<extra></extra>",
        )
    )
    charts.hline(fig, 0, color=charts.ZERO)
    fig.update_xaxes(dtick=1)
    fig.update_layout(showlegend=False, bargap=0.25)
    st.plotly_chart(fig, use_container_width=True, config=charts.CONFIG)

    fig = charts.figure(
        t("share_title"),
        t("share_sub"),
        x_title=t("x_axis"),
        y_percent=True,
        height=320,
    )
    charts.bars(
        fig,
        dec["decile"],
        dec["share_better_off"],
        t("s_better"),
        charts.SERIES["better"],
        money=False,
    )
    charts.bars(
        fig,
        dec["decile"],
        -dec["share_worse_off"],
        t("s_worse"),
        charts.SERIES["worse"],
        money=False,
    )
    charts.hline(fig, 0, color=charts.ZERO)
    fig.update_xaxes(dtick=1)
    fig.update_layout(barmode="relative", bargap=0.25)
    st.plotly_chart(fig, use_container_width=True, config=charts.CONFIG)

    from policyengine_pr.analysis.scoring import BENEFITS

    st.subheader(t("benefits_title"))
    ben = _benefits()
    fig = charts.figure(
        None,
        None,
        x_title=t("x_axis"),
        y_money=True,
        height=400,
    )
    series_keys = {
        "pr_eitc": "eitc",
        "federal_actc": "actc",
        "pan": "pan",
        "tanf": "tanf",
        "section8": "section8",
    }
    for var, es, en in BENEFITS:
        charts.bars(
            fig,
            ben["decile"],
            ben[f"{var}_mean"],
            (es, en)[L],
            charts.SERIES[series_keys[var]],
        )
    fig.update_layout(barmode="stack", bargap=0.25)
    fig.update_xaxes(dtick=1)
    fig.update_yaxes(title_text=t("benefits_y"))
    st.caption(t("benefits_sub"))
    st.plotly_chart(fig, use_container_width=True, config=charts.CONFIG)
    with st.expander(t("benefits_table")):
        table = pd.DataFrame({t("x_axis"): ben["decile"]})
        for var, es, en in BENEFITS:
            label = (es, en)[L]
            table[t("col_mean").format(label)] = ben[f"{var}_mean"]
            table[t("col_share").format(label)] = ben[f"{var}_share"]
        st.dataframe(
            table.style.format(
                {
                    c: "${:,.0f}"
                    for c in table.columns
                    if "medio" in c or "Mean" in c
                }
                | {c: "{:.0%}" for c in table.columns if "%" in c}
            ),
            use_container_width=True,
            hide_index=True,
        )

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

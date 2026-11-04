"""Reformas: score reforms on the PRCS microdata (bill-tracker style).

Each row is a reform; columns are the revenue cost to Hacienda, the change
in PAN spending, the share of households better and worse off, and the
mean change in net income. Selecting a row shows the decile chart.
"""

from pathlib import Path

import card
import charts
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
import ui

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
    "custom": (
        "Reforma contributiva de la barra lateral",
        "Sidebar tax reform",
    ),
    "col_reform": ("Reforma contributiva", "Tax reform"),
    "col_cost": ("Costo para Hacienda", "Cost to Hacienda"),
    "col_cost_help": (
        "Contribución perdida más Crédito por Trabajo adicional, en millones",
        "Tax lost plus extra Crédito por Trabajo, in millions",
    ),
    "col_pan": ("Cambio en PAN", "PAN change"),
    "col_better": ("Hogares que ganan", "Households better off"),
    "col_worse": ("Hogares que pierden", "Households worse off"),
    "col_mean": ("Cambio medio por hogar", "Mean change per household"),
    "pick": ("Reforma contributiva a detallar", "Tax reform to detail"),
    "chart_title": (
        "¿Quién gana con la reforma contributiva?",
        "Who gains from the tax reform?",
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
        "¿Cuántos ganan y cuántos pierden en cada decil?",
        "How many gain and how many lose in each decile?",
    ),
    "s_better": ("Ganan", "Better off"),
    "s_worse": ("Pierden", "Worse off"),
    "s_same": ("Sin cambio", "No change"),
    "decile_tick": ("Decil {}<br>{}", "Decile {}<br>{}"),
    "hover_change": (
        "Decil %{x}: %{y:$+,.0f} al año por hogar (%{customdata:+.1%} del ingreso neto medio)",
        "Decile %{x}: %{y:$+,.0f} a year per household (%{customdata:+.1%} of mean net income)",
    ),
    "hover_share": (
        "Decil %{x}: %{customdata[0]:.0%} ganan, %{customdata[1]:.0%} pierden, %{customdata[2]:.0%} sin cambio",
        "Decile %{x}: %{customdata[0]:.0%} better off, %{customdata[1]:.0%} worse off, %{customdata[2]:.0%} unchanged",
    ),
    "totals_title": (
        "Totales (millones de dólares al año)",
        "Totals ($ million a year)",
    ),
    "col_item": ("Partida", "Item"),
    "col_base": ("Ley vigente", "Current law"),
    "col_ref": ("Reforma contributiva", "Tax reform"),
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
    "col_ben_mean": ("{} medio", "Mean {}"),
    "download_card": ("Descargar tarjeta (PNG)", "Download card (PNG)"),
    "explain_change": (
        "Los hogares de Puerto Rico se ordenan por ingreso neto y se dividen en diez grupos iguales (deciles): el 1 es el 10% más pobre, el 10 el más rico; bajo cada decil está su ingreso neto medio. Cada barra es el cambio anual medio en el ingreso neto de los hogares de ese decil con la reforma, contando a todos (reciban algo o no). Verde: ganan; rojo: pierden. Al pasar el cursor se ve el cambio como porcentaje del ingreso del decil.",
        "Puerto Rico's households are ranked by net income and split into ten equal groups (deciles): 1 is the poorest tenth, 10 the richest; under each decile is its mean net income. Each bar is the mean annual change in net income for that decile under the reform, counting every household (whether it receives anything or not). Green: gain; red: loss. Hover shows the change as a share of the decile's income.",
    ),
    "explain_share": (
        "Para cada decil, qué parte de los hogares sale ganando (verde, hacia arriba), perdiendo (rojo, hacia abajo) o sin cambio apreciable (gris). Las tres partes suman el 100% del decil.",
        "For each decile, the share of households better off (green, upward), worse off (red, downward) or with no appreciable change (grey). The three parts add up to the whole decile.",
    ),
    "explain_benefits": (
        "Con la ley vigente, cuánto recibe de media un hogar de cada decil en cada crédito o ayuda, contando a todos los hogares del decil (los que no reciben cuentan como cero). Es la fotografía de partida sobre la que actúa cualquier reforma; *Ver tabla* añade qué parte de los hogares recibe cada programa.",
        "Under current law, how much a household in each decile receives on average from each credit or benefit, counting every household in the decile (non-recipients count as zero). It is the starting picture any reform acts on; *Table view* adds the share of households receiving each programme.",
    ),
    "card_sub": (
        "Reforma contributiva simulada sobre la Encuesta de la Comunidad de Puerto Rico 2023, reglas de 2025, pesos calibrados a totales oficiales.",
        "Tax reform simulated on the 2023 Puerto Rico Community Survey, 2025 rules, weights calibrated to official totals.",
    ),
    "card_cost": (
        "Costo anual para Hacienda: {}",
        "Annual cost to Hacienda: {}",
    ),
    "card_gain": (
        "Costo anual para Hacienda: {} (recaudo)",
        "Annual gain for Hacienda: {}",
    ),
    "card_b1": (
        "{:.0%} de los hogares salen ganando; {:.0%} perdiendo",
        "{:.0%} of households are better off; {:.0%} worse off",
    ),
    "card_b2": (
        "Cambio medio en ingreso neto: {} por hogar al año",
        "Mean change in net income: {} per household a year",
    ),
    "card_b3": (
        "Contribución sobre ingresos {}; Crédito por Trabajo {}; PAN {}",
        "Income tax {}; Crédito por Trabajo {}; PAN {}",
    ),
    "card_footer": (
        "Espacios Abiertos · policyengine-pr versión {} · policyengine-pr.streamlit.app",
        "Espacios Abiertos · policyengine-pr version {} · policyengine-pr.streamlit.app",
    ),
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
    s = r["summary"]
    households = s["households"]
    cost = s["revenue_change"]
    m = lambda x: f"${x / 1e6:,.0f} M"
    st.download_button(
        t("download_card"),
        card.reform_card(
            pick,
            t("card_sub"),
            t("card_cost" if cost >= 0 else "card_gain", m(abs(cost))),
            [
                t("card_b1", s["share_better_off"], s["share_worse_off"]),
                t("card_b2", f"${s['net_income_change'] / households:+,.0f}"),
                t(
                    "card_b3",
                    m(s["income_tax_change"]),
                    m(s["eitc_change"]),
                    m(s["pan_change"]),
                ),
            ],
            t("card_footer", ui.LAST_UPDATE.replace("-", ".")),
        ),
        "reforma_contributiva.png",
        "image/png",
        key="download_reform_card",
    )
    dec = r["deciles"]

    fig = charts.figure(
        t("chart_title"),
        t("chart_sub"),
        x_title=t("x_axis"),
        y_money=True,
        height=360,
    )
    ticks = [
        t("decile_tick", int(d), f"${m / 1e3:,.0f}k")
        for d, m in zip(dec["decile"], dec["mean_net_income"])
    ]
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
            customdata=dec["mean_change"] / dec["mean_net_income"],
            hovertemplate=t("hover_change") + "<extra></extra>",
        )
    )
    charts.hline(fig, 0, color=charts.ZERO)
    fig.update_xaxes(tickvals=list(dec["decile"]), ticktext=ticks)
    fig.update_layout(showlegend=False, bargap=0.25, hovermode="x")
    st.plotly_chart(fig, use_container_width=True, config=charts.CONFIG)
    charts.explain(L, t("explain_change"))

    fig = charts.figure(
        t("share_title"),
        t("share_sub"),
        x_title=t("x_axis"),
        y_percent=True,
        height=320,
    )
    same = 1 - dec["share_better_off"] - dec["share_worse_off"]
    shares = list(zip(dec["share_better_off"], dec["share_worse_off"], same))
    for values, label, colour in (
        (dec["share_better_off"], "s_better", charts.SERIES["better"]),
        (same, "s_same", charts.GRID),
        (-dec["share_worse_off"], "s_worse", charts.SERIES["worse"]),
    ):
        fig.add_trace(
            go.Bar(
                x=dec["decile"],
                y=values,
                name=t(label),
                marker=dict(color=colour, line=dict(width=0)),
                text=[
                    f"{abs(v):.0%}" if abs(v) >= 0.08 else "" for v in values
                ],
                textposition="inside",
                insidetextanchor="middle",
                textfont=dict(
                    size=11,
                    color="white" if label != "s_same" else charts.MUTED,
                ),
                customdata=shares,
                hovertemplate=t("hover_share") + "<extra></extra>",
            )
        )
    charts.hline(fig, 0, color=charts.ZERO)
    fig.update_xaxes(tickvals=list(dec["decile"]), ticktext=ticks)
    fig.update_yaxes(range=[-1.02, 1.02])
    fig.update_layout(barmode="relative", bargap=0.25, hovermode="x")
    st.plotly_chart(fig, use_container_width=True, config=charts.CONFIG)
    charts.explain(L, t("explain_share"))

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
    charts.explain(L, t("explain_benefits"))
    with st.expander(t("benefits_table")):
        table = pd.DataFrame({t("x_axis"): ben["decile"]})
        for var, es, en in BENEFITS:
            label = (es, en)[L]
            table[t("col_ben_mean").format(label)] = ben[f"{var}_mean"]
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

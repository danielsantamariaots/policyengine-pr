"""CliffWatch: how taxes, credits and net income change as earnings rise.

Modelled on PolicyEngine's CliffWatch (policyengine.org/us/cliffwatch).
The whole earnings range is one simulation, using policyengine-core axes on
the filer's employment income, so a $500 step is affordable.
"""

import charts
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from policyengine_pr import Simulation

YEAR = 2025
STEP = 500
MAX_WAGES = 150_000
HIGH_EMTR = (
    0.5  # a marginal rate at or above this is flagged as a high-rate zone
)
TAX_COLOR = "#2a78d6"
PAYROLL_COLOR = "#eb6834"
CREDIT_COLOR = "#1baf7a"
NET_COLOR = "#1f1f1f"
MARKET_COLOR = "#9a9a94"
CLIFF_COLOR = "#d6283c"
PAN_COLOR = "#c9a227"
TANF_COLOR = "#8e44ad"

TEXT = {
    "title": ("CliffWatch · Puerto Rico", "CliffWatch · Puerto Rico"),
    "caption": (
        "Cómo cambian las contribuciones, los créditos y el ingreso neto del "
        "hogar a medida que suben los salarios del contribuyente, en pasos de "
        "$500 hasta $150,000. Los demás datos del hogar son los de la barra "
        "lateral.",
        "How the household's taxes, credits and net income change as the "
        "filer's wages rise, in $500 steps up to $150,000. All other "
        "household inputs come from the sidebar.",
    ),
    "what_is_cliff": (
        "**Un precipicio** es un punto donde ganar $500 más deja al hogar con "
        "*menos* ingreso neto. **Una zona de tasa alta** es un tramo donde de "
        "cada $100 adicionales el hogar se queda con menos de $50, por la suma "
        "de contribuciones y créditos que se reducen.",
        "**A cliff** is a point where earning $500 more leaves the household "
        "with *less* net income. **A high-rate zone** is a range where the "
        "household keeps less than $50 of each additional $100, once taxes "
        "and withdrawn credits are added up.",
    ),
    "what_is_cliff_title": ("¿Qué es un precipicio?", "What is a cliff?"),
    "m_cliffs": ("Precipicios", "Cliffs"),
    "m_cliffs_help": (
        "Puntos donde $500 más de salario reducen el ingreso neto",
        "Points where $500 more in wages reduce net income",
    ),
    "m_worst": ("Mayor pérdida", "Largest loss"),
    "m_worst_help": (
        "Pérdida de ingreso neto en el peor precipicio",
        "Net income lost at the worst cliff",
    ),
    "m_high": ("Tramo con tasa ≥ 50%", "Range at ≥ 50%"),
    "m_high_help": (
        "Suma de los tramos de $500 con tasa marginal efectiva de 50% o más",
        "Sum of the $500 steps with an effective marginal rate of 50% or more",
    ),
    "m_emtr_here": ("Tasa marginal aquí", "Marginal rate here"),
    "m_emtr_here_help": (
        "De los próximos $500 de salario del contribuyente, cuánto se va en "
        "contribuciones y créditos perdidos",
        "Of the filer's next $500 in wages, how much goes to taxes and lost "
        "credits",
    ),
    "chart_net": (
        "Ingreso neto frente a ingreso de mercado",
        "Net income vs market income",
    ),
    "chart_components": (
        "Contribuciones y créditos por nivel de salarios",
        "Taxes and credits by wage level",
    ),
    "chart_emtr": ("Tasa marginal efectiva", "Effective marginal tax rate"),
    "s_market": ("Ingreso de mercado", "Market income"),
    "s_net": ("Ingreso neto", "Net income"),
    "s_net_reform": ("Ingreso neto (reforma)", "Net income (reform)"),
    "s_tax": ("Contribución sobre ingresos de PR", "PR income tax"),
    "s_payroll": ("Seguro Social y Medicare", "Social Security and Medicare"),
    "s_eitc": ("Crédito por Trabajo", "Crédito por Trabajo (PR EITC)"),
    "s_actc": ("Crédito federal por hijos", "Federal child credit (ACTC)"),
    "s_pan": ("PAN", "PAN (nutrition assistance)"),
    "s_tanf": ("TANF", "TANF (cash assistance)"),
    "s_section8": ("Sección 8", "Section 8 (housing voucher)"),
    "s_cliff": ("Precipicio", "Cliff"),
    "s_emtr": ("Ley vigente", "Current law"),
    "s_emtr_reform": ("Reforma", "Reform"),
    "x_axis": ("Salarios del contribuyente", "Filer wages"),
    "you": ("Su hogar", "Your household"),
    "chart_net_sub": (
        "Salarios del contribuyente de $0 a $150,000 en pasos de $500; las X rojas marcan precipicios",
        "Filer wages from $0 to $150,000 in $500 steps; red Xs mark cliffs",
    ),
    "chart_components_sub": (
        "Créditos y beneficios por encima de cero; contribuciones por debajo",
        "Credits and benefits above zero; taxes below",
    ),
    "chart_emtr_sub": (
        "De cada $100 adicionales de salario, la parte que se va en contribuciones y créditos perdidos; sombreado = 50% o más",
        "Of each additional $100 in wages, the share lost to taxes and withdrawn credits; shaded = 50% or more",
    ),
    "cliffs_title": ("Precipicios detectados", "Cliffs detected"),
    "no_cliffs": (
        "No hay precipicios para este hogar: el ingreso neto nunca baja al "
        "subir los salarios.",
        "No cliffs for this household: net income never falls as wages rise.",
    ),
    "zones_title": (
        "Zonas de tasa marginal alta (≥ 50%)",
        "High marginal-rate zones (≥ 50%)",
    ),
    "no_zones": (
        "Ningún tramo de salarios tiene una tasa marginal de 50% o más.",
        "No wage range has a marginal rate of 50% or more.",
    ),
    "col_wages": ("Salarios", "Wages"),
    "col_loss": ("Pérdida de ingreso neto", "Net income lost"),
    "col_cause": ("Causa principal", "Main cause"),
    "col_from": ("Desde", "From"),
    "col_to": ("Hasta", "To"),
    "col_emtr": ("Tasa marginal media", "Average marginal rate"),
    "col_width": ("Ancho", "Width"),
    "scenario": ("Escenario", "Scenario"),
    "current": ("Ley vigente", "Current law"),
    "reform": ("Reforma", "Reform"),
    "table_view": ("Ver tabla", "Table view"),
    "cause_eitc": (
        "Se pierde el Crédito por Trabajo",
        "Crédito por Trabajo lost",
    ),
    "cause_actc": (
        "Se reduce el crédito federal por hijos",
        "Federal child credit falls",
    ),
    "cause_tax": ("Sube la contribución de PR", "PR income tax rises"),
    "cause_payroll": ("Suben Seguro Social y Medicare", "Payroll taxes rise"),
    "cause_pan": ("Se pierde el PAN", "PAN lost"),
    "cause_tanf": ("Se reduce o se pierde el TANF", "TANF reduced or lost"),
    "cause_section8": (
        "Se reduce el subsidio de Sección 8",
        "Section 8 subsidy falls",
    ),
    "narr_none": (
        "Para este hogar no hay precipicios: el ingreso neto sube siempre que "
        "suben los salarios, y en ningún tramo se pierde la mitad o más de "
        "cada $100 adicionales.",
        "This household has no cliffs: net income always rises with wages, "
        "and no range loses half or more of each additional $100.",
    ),
    "narr_cliff": (
        "Para este hogar, el mayor precipicio está en **{}**: ganar $500 más "
        "reduce el ingreso neto en **{}** porque {}.",
        "For this household, the largest cliff is at **{}**: earning $500 "
        "more cuts net income by **{}** because {}.",
    ),
    "narr_more_cliffs": (
        " Hay {} precipicios en total.",
        " There are {} cliffs in all.",
    ),
    "narr_zone": (
        " Entre **{}** y **{}**, el hogar se queda con menos de ${:.0f} de "
        "cada $100 adicionales (tasa marginal media {:.0%}).",
        " Between **{}** and **{}**, the household keeps less than ${:.0f} of "
        "each additional $100 (average marginal rate {:.0%}).",
    ),
    "narr_more_zones": (
        " Hay otros {} tramos con tasa marginal de 50% o más.",
        " {} other ranges have a marginal rate of 50% or more.",
    ),
    "narr_no_zone": (
        " En ningún otro tramo se pierde la mitad o más de cada $100 adicionales.",
        " No other range loses half or more of each additional $100.",
    ),
    "narr_cause_eitc": (
        "se reduce o se pierde el Crédito por Trabajo",
        "the Crédito por Trabajo is reduced or lost",
    ),
    "narr_cause_actc": (
        "se reduce el crédito federal por hijos",
        "the federal child credit falls",
    ),
    "narr_cause_tax": (
        "la contribución de PR sube más que el salario adicional",
        "PR income tax rises by more than the extra wages",
    ),
    "narr_cause_payroll": (
        "suben el Seguro Social y Medicare",
        "payroll taxes rise",
    ),
    "narr_cause_pan": (
        "el hogar pierde el PAN al superar el límite de ingreso neto",
        "the household loses PAN by exceeding the net income limit",
    ),
    "narr_cause_tanf": (
        "se reduce o se pierde el TANF",
        "TANF is reduced or lost",
    ),
    "narr_cause_section8": (
        "se reduce el subsidio de Sección 8",
        "the Section 8 subsidy falls",
    ),
    "compare_title": (
        "Comparar con otro hogar",
        "Compare with another household",
    ),
    "compare_sub": (
        "Mismos salarios del contribuyente en el eje; el otro hogar se "
        "calcula con la misma ley (y la misma reforma, si hay una).",
        "Same filer wages on the axis; the other household is computed under "
        "the same law (and the same reform, if any).",
    ),
    "compare_pick": ("Comparar con", "Compare with"),
    "compare_none": ("Sin comparación", "No comparison"),
    "compare_unmarried": (
        "Los mismos adultos sin casarse (penalidad por matrimonio)",
        "The same adults unmarried (marriage penalty)",
    ),
    "compare_net": (
        "Ingreso neto de los dos hogares",
        "Net income of both households",
    ),
    "compare_emtr": (
        "Tasa marginal efectiva de los dos hogares",
        "Effective marginal rate of both households",
    ),
    "compare_this": ("Este hogar", "This household"),
    "m_compare_net": (
        "Ingreso neto del otro hogar, a sus salarios",
        "Other household's net income at your wages",
    ),
    "m_compare_diff": (
        "Diferencia frente a este hogar",
        "Difference from this household",
    ),
    "m_marriage": (
        "Penalidad por matrimonio, a sus salarios",
        "Marriage penalty at your wages",
    ),
    "m_marriage_help": (
        "Ingreso neto de la pareja casada menos la suma de los dos hogares "
        "por separado (el contribuyente con los hijos; el cónyuge solo). "
        "Negativo: casarse cuesta dinero; positivo: bono por matrimonio.",
        "Net income of the married couple minus the sum of the two separate "
        "households (filer with the children; spouse alone). Negative: "
        "marriage costs money; positive: a marriage bonus.",
    ),
    "narr_marriage_penalty": (
        "A sus salarios, casarse **cuesta {}** al año frente a vivir como dos "
        "hogares separados.",
        "At your wages, marriage **costs {}** a year compared with two "
        "separate households.",
    ),
    "narr_marriage_bonus": (
        "A sus salarios, casarse **rinde {}** más al año que vivir como dos "
        "hogares separados.",
        "At your wages, marriage **yields {}** more a year than two separate "
        "households.",
    ),
    "narr_marriage_none": (
        "A sus salarios no hay penalidad ni bono por matrimonio.",
        "At your wages there is neither a marriage penalty nor a bonus.",
    ),
    "note": (
        "La tasa marginal efectiva se calcula sobre pasos de $500. El PAN se "
        "modela con el beneficio máximo para todo hogar elegible, porque ADSEF "
        "no publica la tabla de beneficios por nivel de ingreso neto: el "
        "precipicio al superar el límite es, en parte, un artefacto de esa "
        "laguna. El TANF usa el máximo de una familia de tres ($584) para todo "
        "tamaño. La Sección 8 solo aparece si el hogar tiene vale y usa la "
        "renta justa de mercado de San Juan. Plan Vital se evalúa pero no "
        "tiene valor en dólares.",
        "The effective marginal rate is computed over $500 steps. PAN is "
        "modelled at the maximum benefit for every eligible household because "
        "ADSEF does not publish the benefit schedule by net income: the cliff "
        "at the limit is partly an artefact of that gap. TANF uses the "
        "three-person maximum ($584) for every size. Section 8 appears only if "
        "the household holds a voucher and uses the San Juan fair market "
        "rent. Plan Vital is assessed but carries no dollar value.",
    ),
}

VARS = {
    "wages": "employment_income",
    "market": "household_market_income",
    "net": "household_net_income",
    "tax": "pr_income_tax",
    "ss": "employee_social_security_tax",
    "medicare": "employee_medicare_tax",
    "se": "self_employment_tax",
    "eitc": "pr_eitc",
    "actc": "federal_actc",
    "pan": "pan",
    "tanf": "tanf",
    "section8": "section8",
}


def earnings_range(situation, reform=None):
    """One simulation over the filer's wages from $0 to MAX_WAGES."""
    situation = dict(situation)
    situation["axes"] = [
        [
            {
                "name": "employment_income",
                "count": MAX_WAGES // STEP + 1,
                "min": 0,
                "max": MAX_WAGES,
                "period": YEAR,
                "index": 0,  # the filer is the first person
            }
        ]
    ]
    sim = Simulation(situation=situation, reform=reform)
    n_people = len(situation["people"])
    out = {}
    for key, var in VARS.items():
        if key == "wages":  # person-level: keep the filer only
            values = sim.calculate(var, YEAR)[::n_people]
        else:  # sum person-level variables up to the household
            values = sim.calculate(var, YEAR, map_to="household")
        out[key] = np.asarray(values, dtype=float)
    df = pd.DataFrame(out)
    df["payroll"] = df["ss"] + df["medicare"] + df["se"]
    df["emtr"] = 1 - df["net"].diff() / df["wages"].diff()
    return df


def combined_range(parts, reform=None):
    """Net income over the wage axis for a household made of several
    simulated parts: (situation, None) rides the axis; (situation, wages)
    is held at those wages (an unmarried spouse on their own income)."""
    out = None
    for situation, fixed in parts:
        df = earnings_range(situation, reform)
        if out is None:
            out = df[["wages"]].copy()
            out["net"] = 0.0
        if fixed is None:
            out["net"] += df["net"].values
        else:
            out["net"] += df.loc[round(min(fixed, MAX_WAGES) / STEP), "net"]
    out["emtr"] = 1 - out["net"].diff() / out["wages"].diff()
    return out


def find_cliffs(df, L):
    """Steps where net income falls. Cause = component with the largest
    adverse change over that step."""
    rows = []
    d = df.diff()
    for i in np.flatnonzero(d["net"] < -0.5):
        adverse = {
            "cause_eitc": -d.loc[i, "eitc"],
            "cause_actc": -d.loc[i, "actc"],
            "cause_tax": d.loc[i, "tax"],
            "cause_payroll": d.loc[i, "payroll"],
            "cause_pan": -d.loc[i, "pan"],
            "cause_tanf": -d.loc[i, "tanf"],
            "cause_section8": -d.loc[i, "section8"],
        }
        cause = max(adverse, key=adverse.get)
        rows.append(
            {
                "wages": df.loc[i, "wages"],
                "loss": -d.loc[i, "net"],
                "cause": TEXT[cause][L],
                "cause_key": cause,
            }
        )
    return pd.DataFrame(rows, columns=["wages", "loss", "cause", "cause_key"])


def find_zones(df):
    """Contiguous wage ranges with EMTR >= HIGH_EMTR."""
    high = (df["emtr"] >= HIGH_EMTR).to_numpy()
    zones, start = [], None
    for i, flag in enumerate(high):
        if flag and start is None:
            start = i
        if (not flag or i == len(high) - 1) and start is not None:
            end = i if flag else i - 1
            zones.append(
                {
                    "from": df.loc[start - 1, "wages"],
                    "to": df.loc[end, "wages"],
                    "emtr": df.loc[start:end, "emtr"].mean(),
                }
            )
            start = None
    return pd.DataFrame(zones, columns=["from", "to", "emtr"])


def money(x):
    return f"${x:,.0f}"


def narrative(cliffs, zones, L):
    """One paragraph saying what the tables say."""

    def md(key, *args):
        return TEXT[key][L].format(*args).replace("$", "\\$")

    if not len(cliffs) and not len(zones):
        return md("narr_none")
    text = ""
    if len(cliffs):
        worst = cliffs.loc[cliffs["loss"].idxmax()]
        text += md(
            "narr_cliff",
            money(worst["wages"]),
            money(worst["loss"]),
            TEXT["narr_" + worst["cause_key"]][L],
        )
        if len(cliffs) > 1:
            text += md("narr_more_cliffs", len(cliffs))
    # zones wider than one step (a one-step zone is just a cliff)
    wide = zones[(zones["to"] - zones["from"]) > STEP]
    if len(wide):
        z = wide.loc[(wide["to"] - wide["from"]).idxmax()]
        text += md(
            "narr_zone",
            money(z["from"]),
            money(z["to"]),
            (1 - z["emtr"]) * 100,
            z["emtr"],
        )
        if len(wide) > 1:
            text += md("narr_more_zones", len(wide) - 1)
    elif len(cliffs):
        text += md("narr_no_zone")
    return text.strip()


def render(
    situation,
    filer_wages,
    reform,
    L,
    summary=None,
    reform_name=None,
    metric_row=None,
    reform_notice=None,
    compare=None,
):
    """compare: list of (key, label, parts) options for the comparison
    section; parts as in combined_range. key "unmarried" adds the marriage
    penalty reading."""

    def t(key):
        return TEXT[key][L]

    def md(key):
        # Streamlit renders "$...$" as LaTeX in markdown; escape the dollars.
        return TEXT[key][L].replace("$", "\\$")

    reform_name = reform_name or t("s_emtr_reform")
    assisted = bool(
        situation["households"]["household"]
        .get("housing_assisted", {})
        .get(YEAR, False)
    )
    st.title(t("title"))
    charts.mobile_hint(
        (
            "En el móvil, pulse » arriba a la izquierda para describir el hogar.",
            "On a phone, tap » at the top left to describe the household.",
        )[L]
    )
    st.caption(md("caption"))
    if summary:
        st.markdown(f"**{summary}**")
    if reform_notice:
        st.info(reform_notice)

    base = earnings_range(situation)
    ref = earnings_range(situation, reform) if reform else None
    shown = ref if ref is not None else base
    cliffs = find_cliffs(shown, L)
    zones = find_zones(shown)
    here = round(min(filer_wages, MAX_WAGES) / STEP)
    emtr_here = shown.loc[min(here + 1, len(shown) - 1), "emtr"]

    if metric_row:
        metric_row()
    st.markdown(narrative(cliffs, zones, L))
    with st.expander(t("what_is_cliff_title")):
        st.markdown(md("what_is_cliff"))

    c1, c2, c3, c4 = st.columns(4)
    c1.metric(t("m_cliffs"), len(cliffs), help=md("m_cliffs_help"))
    c2.metric(
        t("m_worst"),
        money(cliffs["loss"].max()) if len(cliffs) else "—",
        help=md("m_worst_help"),
    )
    c3.metric(
        t("m_high"),
        money((zones["to"] - zones["from"]).sum()) if len(zones) else "$0",
        help=md("m_high_help"),
    )
    c4.metric(
        t("m_emtr_here"), f"{emtr_here:.0%}", help=md("m_emtr_here_help")
    )

    def marker_lines(fig):
        fig.update_xaxes(tickprefix="$", tickformat=",")
        charts.vline(
            fig, filer_wages, color=charts.MUTED, dash="dot", label=t("you")
        )
        for w in cliffs["wages"]:
            charts.vline(fig, w, color=charts.SERIES["cliff"], dash="dash")

    # --- net income vs market income
    fig = charts.figure(
        t("chart_net"),
        t("chart_net_sub"),
        x_title=t("x_axis"),
        y_money=True,
        height=400,
    )
    charts.line(
        fig,
        base["wages"],
        base["market"],
        t("s_market"),
        charts.SERIES["market"],
        dash="dash",
    )
    if ref is None:
        charts.line(
            fig, base["wages"], base["net"], t("s_net"), charts.SERIES["net"]
        )
    else:
        charts.line(
            fig,
            base["wages"],
            base["net"],
            t("s_emtr"),
            charts.SERIES["baseline"],
        )
        charts.line(
            fig, ref["wages"], ref["net"], reform_name, charts.SERIES["reform"]
        )
    if len(cliffs):
        at = shown[shown["wages"].isin(cliffs["wages"])]
        fig.add_trace(
            go.Scatter(
                x=at["wages"],
                y=at["net"],
                name=t("s_cliff"),
                mode="markers",
                marker=dict(
                    color=charts.SERIES["cliff"],
                    size=10,
                    symbol="x",
                    line=dict(width=2),
                ),
                hovertemplate="%{y:$,.0f}<extra>" + t("s_cliff") + "</extra>",
            )
        )
    last = shown.iloc[-1]
    charts.end_label(
        fig,
        last["wages"],
        last["net"],
        money(last["net"]),
        charts.SERIES["net"] if ref is None else charts.SERIES["reform"],
    )
    marker_lines(fig)
    st.plotly_chart(fig, use_container_width=True, config=charts.CONFIG)

    # --- components: credits above zero, taxes below
    fig = charts.figure(
        t("chart_components"),
        t("chart_components_sub"),
        x_title=t("x_axis"),
        y_money=True,
        height=400,
    )
    for key, label, sign in (
        ("eitc", "s_eitc", 1),
        ("actc", "s_actc", 1),
        ("pan", "s_pan", 1),
        ("tanf", "s_tanf", 1),
        *([("section8", "s_section8", 1)] if assisted else []),
        ("tax", "s_tax", -1),
        ("payroll", "s_payroll", -1),
    ):
        charts.bars(
            fig,
            shown["wages"],
            sign * shown[key],
            t(label),
            charts.SERIES[key],
        )
    charts.hline(fig, 0, color=charts.ZERO)
    marker_lines(fig)
    fig.update_layout(barmode="relative", bargap=0.15)
    st.plotly_chart(fig, use_container_width=True, config=charts.CONFIG)

    # --- EMTR
    fig = charts.figure(
        t("chart_emtr"),
        t("chart_emtr_sub"),
        x_title=t("x_axis"),
        y_percent=True,
        height=360,
    )
    for _, z in zones.iterrows():
        fig.add_vrect(
            x0=z["from"],
            x1=z["to"],
            fillcolor=charts.SERIES["cliff"],
            opacity=0.08,
            line_width=0,
        )
    if ref is None:
        charts.line(
            fig,
            base["wages"],
            base["emtr"],
            t("s_emtr"),
            charts.SERIES["tax"],
            money=False,
            shape="hv",
        )
    else:
        charts.line(
            fig,
            base["wages"],
            base["emtr"],
            t("s_emtr"),
            charts.SERIES["baseline"],
            money=False,
            shape="hv",
        )
        charts.line(
            fig,
            ref["wages"],
            ref["emtr"],
            reform_name,
            charts.SERIES["reform"],
            money=False,
            shape="hv",
        )
    charts.hline(fig, HIGH_EMTR, color=charts.MUTED, dash="dot", label="50%")
    charts.hline(
        fig, 1, color=charts.SERIES["cliff"], dash="dot", label="100%"
    )
    marker_lines(fig)
    # cap the axis at 150%: a cliff's one-step rate can be several hundred
    # per cent and would flatten everything else (cliffs are listed below)
    fig.update_yaxes(range=[min(-0.1, shown["emtr"].min() - 0.05), 1.5])
    st.plotly_chart(fig, use_container_width=True, config=charts.CONFIG)

    # --- tables
    left, right = st.columns(2)
    with left:
        st.subheader(t("cliffs_title"))
        if len(cliffs):
            st.dataframe(
                cliffs.drop(columns="cause_key")
                .rename(
                    columns={
                        "wages": t("col_wages"),
                        "loss": t("col_loss"),
                        "cause": t("col_cause"),
                    }
                )
                .style.format(
                    {t("col_wages"): "${:,.0f}", t("col_loss"): "${:,.0f}"}
                ),
                use_container_width=True,
                hide_index=True,
            )
        else:
            st.success(md("no_cliffs"))
    with right:
        st.subheader(t("zones_title"))
        if len(zones):
            z = zones.assign(width=zones["to"] - zones["from"]).rename(
                columns={
                    "from": t("col_from"),
                    "to": t("col_to"),
                    "emtr": t("col_emtr"),
                    "width": t("col_width"),
                }
            )
            st.dataframe(
                z.style.format(
                    {
                        t("col_from"): "${:,.0f}",
                        t("col_to"): "${:,.0f}",
                        t("col_width"): "${:,.0f}",
                        t("col_emtr"): "{:.0%}",
                    }
                ),
                use_container_width=True,
                hide_index=True,
            )
        else:
            st.success(md("no_zones"))

    with st.expander(t("table_view")):
        table = shown[
            [
                "wages",
                "market",
                "tax",
                "payroll",
                "eitc",
                "actc",
                "pan",
                "tanf",
                *(["section8"] if assisted else []),
                "net",
                "emtr",
            ]
        ].rename(
            columns={
                "wages": t("col_wages"),
                "market": t("s_market"),
                "tax": t("s_tax"),
                "payroll": t("s_payroll"),
                "eitc": t("s_eitc"),
                "actc": t("s_actc"),
                "pan": t("s_pan"),
                "tanf": t("s_tanf"),
                "section8": t("s_section8"),
                "net": t("s_net"),
                "emtr": t("col_emtr"),
            }
        )
        st.dataframe(
            table.style.format(
                {c: "${:,.0f}" for c in table.columns if c != t("col_emtr")}
                | {t("col_emtr"): "{:.0%}"}
            ),
            use_container_width=True,
            hide_index=True,
            height=360,
        )
    if compare:
        st.subheader(t("compare_title"))
        st.caption(md("compare_sub"))
        keys = ["none"] + [k for k, *_ in compare]
        labels = {"none": t("compare_none")} | {
            k: lab for k, lab, _ in compare
        }
        pick = st.selectbox(
            t("compare_pick"),
            keys,
            format_func=lambda k: labels[k],
            key="compare_with",
        )
        if pick != "none":
            parts = next(parts for k, _, parts in compare if k == pick)
            other = combined_range(parts, reform)
            idx = min(here, len(other) - 1)
            net_here, other_here = shown.loc[idx, "net"], other.loc[idx, "net"]
            if pick == "unmarried":
                diff = net_here - other_here
                st.metric(
                    t("m_marriage"), money(diff), help=md("m_marriage_help")
                )
                if diff < -0.5:
                    st.markdown(
                        md("narr_marriage_penalty").format(
                            money(-diff).replace("$", "\\$")
                        )
                    )
                elif diff > 0.5:
                    st.markdown(
                        md("narr_marriage_bonus").format(
                            money(diff).replace("$", "\\$")
                        )
                    )
                else:
                    st.markdown(md("narr_marriage_none"))
            else:
                c1, c2 = st.columns(2)
                c1.metric(t("m_compare_net"), money(other_here))
                c2.metric(t("m_compare_diff"), money(other_here - net_here))
            fig = charts.figure(
                t("compare_net"), x_title=t("x_axis"), y_money=True, height=380
            )
            charts.line(
                fig,
                shown["wages"],
                shown["net"],
                t("compare_this"),
                charts.SERIES["net"],
            )
            charts.line(
                fig,
                other["wages"],
                other["net"],
                labels[pick],
                charts.SERIES["reform"],
            )
            charts.end_label(
                fig,
                shown.iloc[-1]["wages"],
                shown.iloc[-1]["net"],
                money(shown.iloc[-1]["net"]),
                charts.SERIES["net"],
            )
            charts.end_label(
                fig,
                other.iloc[-1]["wages"],
                other.iloc[-1]["net"],
                money(other.iloc[-1]["net"]),
                charts.SERIES["reform"],
            )
            marker_lines(fig)
            st.plotly_chart(
                fig, use_container_width=True, config=charts.CONFIG
            )
            fig = charts.figure(
                t("compare_emtr"),
                x_title=t("x_axis"),
                y_percent=True,
                height=340,
            )
            charts.line(
                fig,
                shown["wages"],
                shown["emtr"],
                t("compare_this"),
                charts.SERIES["net"],
                money=False,
                shape="hv",
            )
            charts.line(
                fig,
                other["wages"],
                other["emtr"],
                labels[pick],
                charts.SERIES["reform"],
                money=False,
                shape="hv",
            )
            charts.hline(
                fig, HIGH_EMTR, color=charts.MUTED, dash="dot", label="50%"
            )
            fig.update_yaxes(range=[-0.5, 1.5])
            marker_lines(fig)
            st.plotly_chart(
                fig, use_container_width=True, config=charts.CONFIG
            )
    st.caption(md("note"))

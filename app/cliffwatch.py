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
        "Cuántas veces, al subir el salario, el hogar acaba con menos dinero que antes porque pierde una ayuda de golpe: cada punto donde $500 más de salario reducen el ingreso neto.",
        "How many times, as wages rise, the household ends up with less money than before because it loses a benefit all at once: each point where $500 more in wages lowers net income.",
    ),
    "m_worst": ("Mayor pérdida", "Largest loss"),
    "m_worst_help": (
        "En el peor de esos puntos, cuánto ingreso neto pierde el hogar al año por ganar $500 más.",
        "At the worst of those points, how much net income a year the household loses by earning $500 more.",
    ),
    "m_high": ("Tramo con tasa ≥ 50%", "Range at ≥ 50%"),
    "m_high_help": (
        "Cuánto salario, sumando tramos de $500, está en zonas donde de cada $100 más el hogar se queda con $50 o menos (tasa marginal efectiva del 50% o más).",
        "How much wage range, adding up $500 steps, sits in zones where the household keeps $50 or less of each extra $100 (an effective marginal rate of 50% or more).",
    ),
    "m_emtr_here": (
        "Aquí, de cada $100 más se queda con",
        "Here, of each extra $100 it keeps",
    ),
    "m_emtr_here_help": (
        "Con el salario que usted puso: si el contribuyente ganara $100 más, cuántos dólares le quedarían al hogar después de más contribución y menos créditos y ayudas, medido sobre los próximos $500.",
        "At the wages you entered: if the filer earned $100 more, how many dollars the household would keep after more tax and fewer credits and benefits, measured over the next $500.",
    ),
    "chart_net": (
        "¿Dónde pierde al ganar más?",
        "Where does it lose by earning more?",
    ),
    "chart_components": (
        "¿Qué paga y qué recibe a cada nivel de salario?",
        "What does it pay and receive at each wage level?",
    ),
    "chart_emtr": (
        "¿Con cuánto se queda de cada $100 más?",
        "How much of each extra $100 does it keep?",
    ),
    "explain_net": (
        "La línea continua es el ingreso neto del hogar (lo que le queda tras contribuciones, créditos y ayudas) para cada nivel de salario del contribuyente; la línea de rayas son los ingresos del hogar antes de contribuciones y ayudas (salarios, pensiones, Seguro Social, intereses). Donde la línea continua baja al subir el salario hay un precipicio: ganar $500 más deja menos dinero. Cada etiqueta roja dice cuánto se pierde y por qué; la banda sombreada es un tramo donde el hogar se queda con $50 o menos de cada $100 adicionales.",
        "The solid line is the household's net income (what is left after taxes, credits and benefits) at each level of the filer's wages; the dashed line is the household's income before taxes and benefits (wages, pensions, Social Security, interest). Where the solid line drops as wages rise there is a cliff: earning $500 more leaves less money. Each red label says how much is lost and why; the shaded band is a range where the household keeps $50 or less of each extra $100.",
    ),
    "explain_components": (
        "Las franjas de arriba son lo que el hogar recibe a cada nivel de salario (Crédito por Trabajo, crédito federal por hijos, PAN, TANF y, si tiene vale, Sección 8); las de abajo, lo que paga (contribución de Puerto Rico, Seguro Social y Medicare). La altura de cada franja es su cantidad anual. Donde una franja de arriba se estrecha de golpe, esa ayuda se pierde.",
        "The bands above zero are what the household receives at each wage level (Crédito por Trabajo, federal child credit, PAN, TANF and, with a voucher, Section 8); the bands below are what it pays (Puerto Rico tax, Social Security and Medicare). Each band's height is its annual amount. Where a band above narrows abruptly, that benefit is lost.",
    ),
    "explain_kept": (
        "De cada $100 adicionales de salario, cuántos dólares se queda el hogar después de pagar más contribución y de perder parte de los créditos y ayudas. $100 significa que se queda con todo; $50 o menos (sombreado) es un tramo de tasa alta; un triángulo rojo en el suelo es un precipicio, con la pérdida de ese paso de $500.",
        "Of each extra $100 in wages, how many dollars the household keeps after paying more tax and losing part of its credits and benefits. $100 means it keeps everything; $50 or less (shaded) is a high-rate range; a red triangle at the floor is a cliff, with the loss over that $500 step.",
    ),
    "explain_compare_net": (
        "Ingreso neto de su hogar y del hogar elegido, con los mismos salarios del contribuyente en el eje. Si compara con *los mismos adultos sin casarse*, la segunda línea suma los dos hogares por separado; la diferencia entre líneas es la penalidad (o el bono) por matrimonio a cada nivel de salario.",
        "Net income of your household and of the chosen household, with the same filer wages on the axis. When comparing with *the same adults unmarried*, the second line adds the two separate households; the gap between the lines is the marriage penalty (or bonus) at each wage level.",
    ),
    "explain_compare_emtr": (
        "Tasa marginal efectiva de los dos hogares: de cada $100 adicionales, la parte que se pierde en contribuciones y ayudas reducidas. Por encima del 50% (línea punteada) el hogar se queda con menos de la mitad.",
        "Effective marginal rate of both households: of each extra $100, the share lost to taxes and reduced benefits. Above 50% (dotted line) the household keeps less than half.",
    ),
    "tables_expander": (
        "Ver precipicios y zonas en tabla",
        "See cliffs and zones as tables",
    ),
    "s_market": (
        "Ingresos antes de contribuciones y ayudas",
        "Income before taxes and benefits",
    ),
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
    "s_emtr_reform": ("Reforma contributiva", "Tax reform"),
    "x_axis": ("Salarios del contribuyente", "Filer wages"),
    "you": ("Su hogar", "Your household"),
    "chart_net_sub": (
        "Salarios del contribuyente de $0 a $150,000 en pasos de $500; cada etiqueta roja es un precipicio",
        "Filer wages from $0 to $150,000 in $500 steps; each red label is a cliff",
    ),
    "chart_components_sub": (
        "Créditos y beneficios por encima de cero; contribuciones por debajo",
        "Credits and benefits above zero; taxes below",
    ),
    "chart_emtr_sub": (
        "Sombreado: tramos donde se queda con $50 o menos; triángulos: precipicios, con su pérdida",
        "Shaded: ranges where it keeps $50 or less; triangles: cliffs, with their loss",
    ),
    "y_net": ("Ingreso neto anual", "Annual net income"),
    "y_components": ("Al año", "Per year"),
    "y_emtr": ("Se queda con", "Keeps"),
    "zone_label": ("Zona de tasa alta: {:.0%}", "High-rate zone: {:.0%}"),
    "hover_cliff": (
        "A {}: ganar $500 más baja el ingreso neto {} ({})",
        "At {}: earning $500 more lowers net income by {} ({})",
    ),
    "cliff_label": ("{} · {}", "{} · {}"),
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
    "reform": ("Reforma contributiva", "Tax reform"),
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
        "Cuánto gana o pierde esta pareja al año por estar casada y rendir una sola planilla: el ingreso neto de la pareja menos la suma de los dos hogares por separado (el contribuyente con los hijos; el cónyuge solo). Negativo es una penalidad por matrimonio; positivo, un bono.",
        "How much this couple gains or loses a year by being married and filing one return: the couple's net income minus the sum of the two separate households (filer with the children; spouse alone). Negative is a marriage penalty; positive, a bonus.",
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
    "section8_hint": (
        "La Sección 8 se dibuja solo si marca *El hogar tiene un vale de Sección 8* en Vivienda.",
        "Section 8 is drawn only if you tick *Household holds a Section 8 voucher* under Housing.",
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
        t("m_emtr_here"),
        money(100 - emtr_here * 100),
        help=md("m_emtr_here_help"),
    )

    def marker_lines(fig):
        fig.update_xaxes(tickformat="$,.3~s")
        charts.vline(
            fig, filer_wages, color=charts.MUTED, dash="dot", label=t("you")
        )
        for w in cliffs["wages"]:
            charts.vline(fig, w, color=charts.SERIES["cliff"], dash="dash")

    # --- net income vs income before taxes and benefits
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
    # explaining hover: a sentence at each cliff, the value elsewhere
    notes = {
        float(c["wages"]): TEXT["hover_cliff"][L].format(
            money(c["wages"]), money(c["loss"]), c["cause"].lower()
        )
        for _, c in cliffs.iterrows()
    }
    hover_text = [notes.get(float(w), "") for w in shown["wages"]]
    if ref is None:
        fig.add_trace(
            go.Scatter(
                x=base["wages"],
                y=base["net"],
                name=t("s_net"),
                mode="lines",
                line=dict(color=charts.SERIES["net"], width=2),
                customdata=hover_text,
                hovertemplate="%{y:$,.0f}<br><span style='color:"
                + charts.SERIES["cliff"]
                + "'>%{customdata}</span><extra>"
                + t("s_net")
                + "</extra>",
            )
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
    wide_zones = zones[(zones["to"] - zones["from"]) > STEP]
    for _, z in wide_zones.iterrows():
        fig.add_vrect(
            x0=z["from"],
            x1=z["to"],
            fillcolor=charts.SERIES["cliff"],
            opacity=0.06,
            line_width=0,
            annotation_text=TEXT["zone_label"][L].format(z["emtr"]),
            annotation_position="top left",
            annotation_font=dict(size=11, color=charts.MUTED),
        )
    if len(cliffs):
        at = shown[shown["wages"].isin(cliffs["wages"])]
        fig.add_trace(
            go.Scatter(
                x=at["wages"],
                y=at["net"],
                name=t("s_cliff"),
                mode="markers",
                marker=dict(color=charts.SERIES["cliff"], size=9),
                hovertemplate="%{y:$,.0f}<extra>" + t("s_cliff") + "</extra>",
            )
        )
        for i, (_, c) in enumerate(cliffs.iterrows()):
            y_at = float(
                shown.loc[shown["wages"] == c["wages"], "net"].iloc[0]
            )
            charts.annotate(
                fig,
                c["wages"],
                y_at,
                TEXT["cliff_label"][L].format(
                    "-" + money(c["loss"]), c["cause"]
                ),
                charts.SERIES["cliff"],
                above=(i % 2 == 0),
            )
    fig.update_yaxes(title_text=t("y_net"))
    last = shown.iloc[-1]
    # direct labels at the right end replace the legend
    charts.end_label(
        fig,
        last["wages"],
        last["market"],
        t("s_market"),
        charts.SERIES["market"],
    )
    if ref is None:
        charts.end_label(
            fig,
            last["wages"],
            last["net"],
            f"{t('s_net')} {money(last['net'])}",
            charts.SERIES["net"],
        )
    else:
        charts.end_label(
            fig,
            base.iloc[-1]["wages"],
            base.iloc[-1]["net"],
            t("s_emtr"),
            charts.SERIES["baseline"],
        )
        charts.end_label(
            fig,
            last["wages"],
            last["net"],
            f"{reform_name} {money(last['net'])}",
            charts.SERIES["reform"],
        )
    fig.update_layout(showlegend=False, margin=dict(r=170))
    marker_lines(fig)
    st.plotly_chart(fig, use_container_width=True, config=charts.CONFIG)
    charts.explain(L, t("explain_net"))

    # --- components and kept-share charts, full width, one after the other
    col_components, col_emtr = st.container(), st.container()
    with col_components:
        fig = charts.figure(
            t("chart_components"),
            t("chart_components_sub"),
            x_title=t("x_axis"),
            y_money=True,
            height=380,
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
            charts.area(
                fig,
                shown["wages"],
                sign * shown[key],
                t(label),
                charts.SERIES[key],
                "pos" if sign > 0 else "neg",
            )
        charts.hline(fig, 0, color=charts.ZERO)
        fig.update_yaxes(title_text=t("y_components"))
        marker_lines(fig)
        st.plotly_chart(fig, use_container_width=True, config=charts.CONFIG)
        if not assisted:
            st.caption(md("section8_hint"))
        charts.explain(L, t("explain_components"))
    with col_emtr:
        # --- kept share of each extra $100 (1 - EMTR), clipped at 0
        fig = charts.figure(
            t("chart_emtr"),
            t("chart_emtr_sub"),
            x_title=t("x_axis"),
            y_money=True,
            height=380,
        )
        for _, z in zones.iterrows():
            fig.add_vrect(
                x0=z["from"],
                x1=z["to"],
                fillcolor=charts.SERIES["cliff"],
                opacity=0.08,
                line_width=0,
            )

        # what the household keeps of each extra $100 (1 - EMTR), floored at
        # $0: a cliff's one-step rate can be several hundred per cent and would
        # flatten everything else; cliffs are marked at the bottom with their loss
        def kept(df):
            return np.clip((1 - df["emtr"]) * 100, 0, None)

        if ref is None:
            charts.line(
                fig,
                base["wages"],
                kept(base),
                t("s_emtr"),
                charts.SERIES["tax"],
                shape="hv",
            )
        else:
            charts.line(
                fig,
                base["wages"],
                kept(base),
                t("s_emtr"),
                charts.SERIES["baseline"],
                shape="hv",
            )
            charts.line(
                fig,
                ref["wages"],
                kept(ref),
                reform_name,
                charts.SERIES["reform"],
                shape="hv",
            )
        charts.hline(fig, 50, color=charts.MUTED, dash="dot", label="$50")
        if len(cliffs):
            fig.add_trace(
                go.Scatter(
                    x=cliffs["wages"],
                    y=[0] * len(cliffs),
                    name=t("s_cliff"),
                    mode="markers+text",
                    marker=dict(
                        color=charts.SERIES["cliff"],
                        size=10,
                        symbol="triangle-up",
                    ),
                    text=["-" + money(v) for v in cliffs["loss"]],
                    textposition="bottom center",
                    textfont=dict(size=11, color=charts.SERIES["cliff"]),
                    hovertemplate="%{text}<extra>" + t("s_cliff") + "</extra>",
                )
            )
        fig.update_yaxes(
            title_text=t("y_emtr"),
            range=[-14, max(110, float(kept(shown).max()) + 8)],
            tickformat="$,.0f",
        )
        if ref is None:
            fig.update_layout(showlegend=False)
        marker_lines(fig)
        st.plotly_chart(fig, use_container_width=True, config=charts.CONFIG)
        charts.explain(L, t("explain_kept"))

        # --- tables, folded
        tables = st.expander(t("tables_expander"))
    with tables:
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
            charts.explain(L, t("explain_compare_net"))
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
            charts.explain(L, t("explain_compare_emtr"))
    st.caption(md("note"))

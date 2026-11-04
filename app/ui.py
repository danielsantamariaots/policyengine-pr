"""Shared user-facing pieces for the app: presets, example reforms,
plain-language captions, the household summary line, the metric row, the
"not included" box, the assumptions expander and the tutorial.

Everything here is text and layout; the model lives in policyengine_pr.
"""

import pandas as pd
import streamlit as st

from policyengine_pr.reforms.parametric import LEVERS

YEAR = 2025
MINIMUM_WAGE_ANNUAL = 10.50 * 2080  # $10.50/hour, Ley 47-2021, from July 2024

# ---------------------------------------------------------------------------
# Default sidebar values. Every household widget has a key here so presets
# can overwrite them through st.session_state.
# ---------------------------------------------------------------------------
PERSON_VARS = [
    "self_employment_income",
    "pension_income",
    "social_security",
    "interest_income",
    "dividend_income",
    "long_term_capital_gains",
]
DEDUCTION_VARS = [
    "mortgage_interest",
    "medical_expenses",
    "charitable_contributions",
    "ira_contributions",
    "education_account_contributions",
    "student_loan_payments",
]
DEFAULTS = {
    "joint": False,
    "filer_age": 35,
    "filer_wages": 30_000,
    "filer_veteran": False,
    "spouse_age": 35,
    "spouse_wages": 0,
    "spouse_veteran": False,
    "n_children": 2,
    "other_deductions": 0,
    "abt_other_income": 0,
    "housing_assisted": False,
    "housing_rent": 0,
    "municipio": "San Juan",
    "pan_resources": 0,
    "pan_pays_dependent_care": False,
    "pan_recurrent_medical_expenses": False,
    **{f"c{i}": min(4 + 4 * i, 25) for i in range(8)},
    **{f"filer_{v}": 0 for v in PERSON_VARS},
    **{f"spouse_{v}": 0 for v in PERSON_VARS},
    **{f"d_{v}": 0 for v in DEDUCTION_VARS},
}

# (key, label es, label en, overrides)
PRESETS = [
    ("custom", "Hogar personalizado", "Custom household", {}),
    (
        "minwage",
        "Trabajador soltero con salario mínimo",
        "Single worker at the minimum wage",
        {
            "filer_age": 30,
            "filer_wages": round(MINIMUM_WAGE_ANNUAL),
            "n_children": 0,
        },
    ),
    (
        "single_parent",
        "Madre o padre con dos hijos, $30,000",
        "Single parent with two children, $30,000",
        {
            "filer_age": 32,
            "filer_wages": 30_000,
            "n_children": 2,
            "c0": 4,
            "c1": 8,
        },
    ),
    (
        "couple",
        "Pareja con dos salarios y dos hijos",
        "Two-earner couple with two children",
        {
            "joint": True,
            "filer_age": 38,
            "filer_wages": 45_000,
            "spouse_age": 36,
            "spouse_wages": 25_000,
            "n_children": 2,
            "c0": 6,
            "c1": 10,
        },
    ),
    (
        "retiree",
        "Pensionado de 65 años",
        "Retiree aged 65",
        {
            "filer_age": 65,
            "filer_wages": 0,
            "filer_pension_income": 24_000,
            "filer_social_security": 14_000,
            "n_children": 0,
        },
    ),
    (
        "voucher",
        "Madre o padre con un hijo y vale de Sección 8, $18,000",
        "Single parent with one child and a Section 8 voucher, $18,000",
        {
            "filer_age": 28,
            "filer_wages": 18_000,
            "n_children": 1,
            "c0": 3,
            "housing_assisted": True,
        },
    ),
    (
        "youth",
        "Joven de 22 años, $30,000",
        "Young worker aged 22, $30,000",
        {"filer_age": 22, "filer_wages": 30_000, "n_children": 0},
    ),
    (
        "self_employed",
        "Cuenta propia, $60,000 de ganancia",
        "Self-employed, $60,000 profit",
        {
            "filer_age": 45,
            "filer_wages": 0,
            "filer_self_employment_income": 60_000,
            "n_children": 1,
            "c0": 12,
        },
    ),
]


# Example reforms come from the YAML files in reforms/ (one file per reform:
# name, name_en, description, source, start, levers). Keys are file stems.
def _example_reforms():
    from policyengine_pr.reforms.files import REFORMS_DIR, load_reform

    rows = [("none", "Ninguna (ley vigente)", "None (current law)", {})]
    for path in sorted(REFORMS_DIR.glob("*.yaml")):
        meta, changes = load_reform(path)
        rows.append(
            (
                path.stem,
                meta["name"],
                meta.get("name_en", meta["name"]),
                changes,
            )
        )
    return rows


EXAMPLE_REFORMS = _example_reforms()

TEXT = {
    "nav": ("Página", "Page"),
    "nav_home": ("Inicio", "Home"),
    "nav_calc": ("Mi hogar", "My household"),
    "nav_cliff": ("¿Y si gano más?", "What if I earn more?"),
    "nav_reform": ("Reforma contributiva", "Tax reform"),
    "nav_method": ("Cómo funciona", "How it works"),
    "method_en_note": (
        "",
        "This page is in Spanish; the technical description in English is in the repository's ROADMAP.md and docs/statutes/.",
    ),
    "home_title": (
        "¿Cuánto paga su hogar en contribuciones y cuánto recibe en créditos y ayudas?",
        "How much does your household pay in taxes, and how much does it get in credits and benefits?",
    ),
    "home_intro": (
        "Descríbalo en un minuto y vea el resultado línea por línea, con cada "
        "regla citada a un documento oficial de Hacienda, el IRS, ADSEF o HUD. "
        "Año contributivo 2025.",
        "Describe it in a minute and see the result line by line, with every "
        "rule cited to an official Hacienda, IRS, ADSEF or HUD document. Tax "
        "year 2025.",
    ),
    "start": ("Empezar con un ejemplo", "Start with an example"),
    "start_help": (
        "Abre Mi hogar con una madre de 32 años, dos hijos y $30,000 de salario; cambie lo que quiera.",
        "Opens My household with a 32-year-old mother, two children and $30,000 in wages; change anything.",
    ),
    "home_more": (
        "O elija qué quiere saber:",
        "Or choose what you want to know:",
    ),
    "card_calc_title": (
        "¿Cuánto paga mi hogar?",
        "How much does my household pay?",
    ),
    "card_calc_body": (
        "Contribución, créditos e ingreso neto de un hogar, línea por línea "
        "según la planilla (Formulario 482). Pruebe una reforma contributiva "
        "y vea la diferencia.",
        "A household's tax, credits and net income, line by line as on the "
        "return (Formulario 482). Try a tax reform and see the difference.",
    ),
    "card_cliff_title": (
        "¿Dónde pierde mi hogar al ganar más?",
        "Where does my household lose by earning more?",
    ),
    "card_reform_title": (
        "¿Cuánto cuesta una reforma contributiva y a quién beneficia?",
        "What does a tax reform cost and who gains?",
    ),
    "card_reform_body": (
        "Cada reforma contributiva simulada sobre la Encuesta de la Comunidad "
        "de Puerto Rico: costo para Hacienda, hogares que ganan y pierden, "
        "cambio por decil de ingreso.",
        "Each tax reform simulated on the Puerto Rico Community Survey: cost "
        "to Hacienda, households better and worse off, change by income decile.",
    ),
    "card_cliff_body": (
        "Cómo cambian contribuciones y créditos a medida que suben los "
        "salarios, y en qué puntos ganar más deja menos ingreso neto.",
        "How taxes and credits change as wages rise, and where earning more "
        "leaves less net income.",
    ),
    "open": ("Abrir", "Open"),
    "home_disclaimer": (
        "Los resultados son estimaciones a partir de los formularios e "
        "instrucciones oficiales para 2025 y no sustituyen asesoría "
        "profesional.",
        "Results are estimates from the official 2025 forms and instructions "
        "and are not professional advice.",
    ),
    "preset": ("Hogar tipo", "Household preset"),
    "preset_help": (
        "Elija un hogar de ejemplo y ajuste lo que quiera debajo.",
        "Pick an example household, then adjust anything below.",
    ),
    "example_reform": ("Propuestas de ejemplo", "Example proposals"),
    "example_reform_help": (
        "Rellena los parámetros de abajo; puede editarlos después.",
        "Fills the levers below; you can edit them afterwards.",
    ),
    "reform_name": ("Nombre de la reforma contributiva", "Tax reform name"),
    "reform_default_name": ("Reforma contributiva", "Tax reform"),
    "summary_single": ("planilla individual", "single return"),
    "summary_joint": ("planilla conjunta", "joint return"),
    "summary_filer": ("contribuyente de {} años", "filer aged {}"),
    "summary_spouse": ("cónyuge de {} años", "spouse aged {}"),
    "summary_wages": ("salarios {}", "wages {}"),
    "summary_se": ("cuenta propia {}", "self-employment {}"),
    "summary_pension": ("pensión {}", "pension {}"),
    "summary_ss": ("Seguro Social {}", "Social Security {}"),
    "summary_voucher": ("vale de Sección 8 en {}", "Section 8 voucher in {}"),
    "summary_children_0": ("sin dependientes", "no dependents"),
    "summary_children_1": ("1 dependiente ({} años)", "1 dependent (age {})"),
    "summary_children_n": (
        "{} dependientes ({} años)",
        "{} dependents (ages {})",
    ),
    "m_tax": ("Contribución de PR", "PR income tax"),
    "m_tax_help": (
        "Línea 26 del Formulario 482: lo que el hogar debe a Hacienda antes "
        "de retenciones y créditos reembolsables.",
        "Formulario 482 line 26: what the household owes Hacienda before "
        "withholding and refundable credits.",
    ),
    "m_credits": ("Créditos", "Credits"),
    "m_credits_help": (
        "Crédito por Trabajo (línea 27C) más el crédito federal por hijos "
        "(línea 27D). Se pagan aunque no se deba contribución.",
        "Crédito por Trabajo (line 27C) plus the federal child credit (line "
        "27D). Paid even when no tax is owed.",
    ),
    "m_net": ("Ingreso neto", "Net income"),
    "m_net_help": (
        "Ingresos del hogar menos contribución de PR, Seguro Social y "
        "Medicare, más créditos reembolsables, PAN y TANF.",
        "Household income minus PR tax, Social Security and Medicare, plus "
        "refundable credits, PAN and TANF.",
    ),
    "m_rate": (
        "De cada $100 más, se queda con",
        "Of each extra $100, it keeps",
    ),
    "m_rate_help": (
        "100 menos la tasa contributiva neta: (ingreso de mercado − ingreso "
        "neto) / ingreso de mercado. Más de $100 cuando el hogar recibe más en "
        "créditos de lo que paga.",
        "Net tax rate: (market income − net income) / market income. "
        "Negative when the household receives more in credits than it pays.",
    ),
    "headline_sentence": (
        "Su hogar paga **{}** de contribución sobre ingresos, recibe **{}** en "
        "créditos reembolsables y se queda con **{}** de ingreso neto al año. ",
        "Your household pays **{}** in income tax, receives **{}** in "
        "refundable credits and keeps **{}** in net income a year. ",
    ),
    "rate_sentence_pos": (
        "De cada $100 adicionales que gane, se queda con **${:.0f}**; el "
        "resto se va en contribuciones y créditos que se reducen.",
        "Of each additional $100 it earns, it keeps **${:.0f}**; the rest "
        "goes to taxes and credits that shrink.",
    ),
    "rate_sentence_neg": (
        "De cada $100 adicionales que gane, se queda con **${:.0f}**: los "
        "créditos crecen más de lo que sube la contribución.",
        "Of each additional $100 it earns, it keeps **${:.0f}**: credits "
        "grow faster than the tax.",
    ),
    "rate_sentence_zero": (
        "Este hogar no tiene ingresos de mercado.",
        "This household has no market income.",
    ),
    "not_included_title": (
        "Qué cubre y qué no",
        "What is covered and what is not",
    ),
    "not_included": (
        "**Qué cubre y qué no.** La contribución sobre ingresos de 2025, el "
        "Crédito por Trabajo, el crédito federal por hijos, el Seguro Social y "
        "Medicare, el PAN, el TANF, la Sección 8 y la elegibilidad al Plan "
        "Vital, con cada regla citada a su fuente oficial.\n\n"
        "**No está incluido:** las columnas de 4% y 20% del Anejo A2 ni el "
        "arrastre de pérdidas de capital; los créditos por inversión del Anejo "
        "B; las categorías A, B, D, G y T del TANF; las respuestas de "
        "comportamiento (el modelo es estático).\n\n"
        "**Lea con cuidado:**\n"
        "- **PAN:** paga el beneficio máximo a todo núcleo elegible, porque "
        "ADSEF no publica la tabla que lo reduce con el ingreso; los límites "
        "para núcleos de 2 o más personas son los de octubre de 2021. El "
        "precipicio al superar el límite es, en parte, un efecto de esa laguna.\n"
        "- **TANF:** categoría C (madre o padre solo con hijos menores) con el "
        "máximo de una familia de tres ($584) para todo tamaño.\n"
        "- **Sección 8:** solo si marca que el hogar tiene un vale; usa las "
        "rentas justas de mercado y los límites de HUD del municipio elegido, "
        "no el estándar de pago que fija Vivienda.\n"
        "- **Plan Vital:** se informa quién es elegible; no tiene valor en "
        "dólares.\n"
        "- **Jóvenes:** la exención de la Ley 135-2014 se aplica sola entre "
        "los 16 y 26 años.\n\n"
        "Los resultados son estimaciones y no sustituyen asesoría profesional.",
        "**What is covered and what is not.** The 2025 income tax, the "
        "Crédito por Trabajo, the federal child credit, Social Security and "
        "Medicare, PAN, TANF, Section 8 and Plan Vital eligibility, each rule "
        "cited to its official source.\n\n"
        "**Not included:** the 4% and 20% columns of Anejo A2 and capital-loss "
        "carryovers; Anejo B investment credits; TANF categories A, B, D, G "
        "and T; behavioural responses (the model is static).\n\n"
        "**Read with care:**\n"
        "- **PAN:** pays the maximum benefit to every eligible núcleo, because "
        "ADSEF does not publish the schedule that reduces it with income; the "
        "limits for núcleos of 2 or more are the October 2021 ones. The cliff "
        "at the limit is partly an effect of that gap.\n"
        "- **TANF:** category C (single parent with minor children) with the "
        "three-person maximum ($584) for every size.\n"
        "- **Section 8:** only if you tick that the household holds a "
        "voucher; uses HUD's fair market rents and income limits for the "
        "chosen municipio, not the payment standard Vivienda sets.\n"
        "- **Plan Vital:** reports who is eligible; it carries no dollar "
        "value.\n"
        "- **Youth:** the Ley 135-2014 exemption applies by itself at ages 16 "
        "to 26.\n\n"
        "Results are estimates, not professional advice.",
    ),
    "why_title": ("¿Por qué estos números?", "Why these numbers?"),
    "why_tax": (
        "**Contribución:** su ingreso bruto ajustado es {}; tras {} de deducciones y exenciones queda {} sujeto a contribución. La tabla da {}, que la ley rebaja al 92% o 95% ({}), y la contribución básica alterna añade {}: total **{}**.",
        "**Tax:** your adjusted gross income is {}; after {} in deductions and exemptions, {} is subject to tax. The table gives {}, which the law reduces to 92% or 95% ({}), and the alternate basic tax adds {}: total **{}**.",
    ),
    "why_credits": (
        "**Créditos:** **{}** de Crédito por Trabajo (depende del ingreso ganado y de los dependientes) y **{}** de crédito federal por hijos (ACTC). Son reembolsables: se cobran aunque la contribución sea cero.",
        "**Credits:** **{}** Crédito por Trabajo (depends on earned income and dependents) and **{}** federal child credit (ACTC). Both are refundable: paid even when the tax is zero.",
    ),
    "why_net": (
        "**Ingreso neto:** ingresos de mercado {} menos contribución {} y Seguro Social y Medicare {}, más créditos {} y ayudas {} (PAN {}, TANF {}, Sección 8 {}) = **{}**.",
        "**Net income:** market income {} minus tax {} and Social Security and Medicare {}, plus credits {} and benefits {} (PAN {}, TANF {}, Section 8 {}) = **{}**.",
    ),
    "glossary_title": ("Glosario", "Glossary"),
    "examples_title": ("Hogares de ejemplo", "Example households"),
    "example_line": (
        "**{}** paga **{}** de contribución, recibe **{}** en créditos y se queda con **{}**.",
        "**{}** pays **{}** in tax, receives **{}** in credits and keeps **{}**.",
    ),
    "see": ("Ver", "See"),
    "assumptions_title": ("Ver supuestos", "See assumptions"),
    "assumptions_intro": (
        "Valores de ley vigente usados en el cálculo (año contributivo "
        "2025). Cada uno procede de un archivo de parámetros con su fuente "
        "oficial en `policyengine_pr/parameters/`.",
        "Current-law values used in the calculation (tax year 2025). Each "
        "comes from a parameter file with its official source in "
        "`policyengine_pr/parameters/`.",
    ),
    "col_param": ("Parámetro", "Parameter"),
    "col_current": ("Ley vigente", "Current law"),
    "col_reform": ("Reforma contributiva", "Tax reform"),
    "col_source": ("Archivo", "File"),
    "share_title": ("Compartir", "Share"),
    "share_help": (
        "La dirección de esta página incluye el hogar, la reforma y la "
        "página abierta. Copie el enlace para compartir exactamente lo que ve.",
        "This page's address includes the household, the reform and the open "
        "page. Copy the link to share exactly what you see.",
    ),
    "tutorial_title": ("Cómo usar estas páginas", "How to use these pages"),
    "tab_calc": ("Calculadora", "Calculator"),
    "tab_cliff": ("CliffWatch", "CliffWatch"),
    "tab_reform": ("Reformas", "Reforms"),
}

TUTORIAL_CALC = (
    """
**1. Describa el hogar** en la barra lateral, o elija un *hogar tipo* y
ajuste lo que quiera: estado civil, edades, salarios y dependientes. Otros
ingresos (cuenta propia, pensiones, Seguro Social) y las deducciones del
Anejo A tienen su propia sección; la calculadora aplica los límites de ley.

**2. Lea los resultados.** Arriba, cuatro cifras: contribución, créditos
reembolsables, ingreso neto y lo que se va de cada \\$100. Debajo, una frase
en lenguaje llano. A la derecha, *Línea por línea* sigue el orden del
Formulario 482 con una explicación breve de cada partida. A la izquierda,
cómo cambiarían contribuciones y créditos si los salarios del contribuyente
fueran de \\$0 a \\$150,000.
""",
    """
**1. Describe the household** in the sidebar, or pick a *household preset*
and adjust: filing status, ages, wages and dependents. Other income
(self-employment, pensions, Social Security) and Anejo A deductions have
their own sections; the calculator applies the statutory limits.

**2. Read the results.** At the top, four figures: tax, refundable credits,
net income and what goes out of every \\$100. Below, a plain-language
sentence. On the right, *Line by line* follows Formulario 482 with a short
explanation of each item. On the left, how taxes and credits would change
if the filer's wages ran from \\$0 to \\$150,000.
""",
)
TUTORIAL_CLIFF = (
    """
**CliffWatch** toma el mismo hogar y sube los salarios del contribuyente en
pasos de \\$500 hasta \\$150,000.

- **Un precipicio** es un punto donde ganar \\$500 más deja al hogar con
  *menos* ingreso neto. Se marca con una X roja y se explica en la tabla
  *Precipicios detectados* (salarios, pérdida y causa principal).
- **Una zona de tasa alta** es un tramo donde de cada \\$100 adicionales el
  hogar se queda con menos de \\$50. Se sombrea en la gráfica de tasa
  marginal.
- El párrafo bajo el título resume lo anterior en palabras.

Con una reforma activa se dibujan las dos curvas y los precipicios se
calculan sobre la reforma. Al final, *Comparar con* superpone otro hogar
tipo; para una planilla conjunta, *Los mismos adultos sin casarse* calcula
la penalidad o el bono por matrimonio.
""",
    """
**CliffWatch** takes the same household and raises the filer's wages in
\\$500 steps to \\$150,000.

- **A cliff** is a point where earning \\$500 more leaves the household with
  *less* net income. It is marked with a red X and explained in the
  *Cliffs detected* table (wages, loss, main cause).
- **A high-rate zone** is a range where the household keeps less than \\$50
  of each additional \\$100. It is shaded in the marginal-rate chart.
- The paragraph under the title says the same in words.

With a reform active, both curves are drawn and cliffs are computed on the
reform. At the bottom, *Compare with* overlays another preset household;
for a joint return, *The same adults unmarried* gives the marriage penalty
or bonus.
""",
)
TUTORIAL_REFORM = (
    """
Al final de la barra lateral, elija una **reforma de ejemplo** o cambie
cualquier parámetro (tramos y tasas, exenciones, factor 92%/95%, Crédito
por Trabajo, exención para jóvenes). Dé un nombre a la reforma: aparecerá en
las gráficas. Las dos páginas pasan a modo de comparación: cada cifra
muestra su diferencia frente a la ley vigente (verde = mejora para el
hogar). Para volver a la ley vigente, elija *Ninguna* o restaure los
valores.
""",
    """
At the bottom of the sidebar, pick an **example reform** or change any
lever (brackets and rates, exemptions, the 92%/95% factor, the Crédito por
Trabajo, the youth exemption). Name the reform: it appears in the charts.
Both pages switch to comparison mode: every figure shows its difference
from current law (green = better for the household). To return to current
law, choose *None* or restore the values.
""",
)


def t(key, L, *args):
    s = TEXT[key][L]
    return s.format(*args) if args else s


def md(key, L, *args):
    """Markdown text with dollar signs escaped (Streamlit treats $…$ as LaTeX)."""
    return t(key, L, *args).replace("$", "\\$")


def money(x):
    return f"${x:,.0f}"


# ---------------------------------------------------------------------------
# Session-state helpers for presets and example reforms
# ---------------------------------------------------------------------------
def hh_from_state(state):
    """The household dict the calculator builds from the sidebar, from any
    mapping with the sidebar's keys (session state or DEFAULTS + overrides)."""
    g = state.get
    hh = {
        "joint": bool(g("joint", False)),
        "filer_age": g("filer_age", 35),
        "filer_veteran": bool(g("filer_veteran", False)),
        "filer": {v: g(f"filer_{v}", 0) for v in PERSON_VARS},
        "spouse_age": g("spouse_age", 35),
        "spouse_wages": g("spouse_wages", 0),
        "spouse_veteran": bool(g("spouse_veteran", False)),
        "spouse": {v: g(f"spouse_{v}", 0) for v in PERSON_VARS},
        "child_ages": [g(f"c{i}", 0) for i in range(int(g("n_children", 0)))],
        "deductions": {v: g(f"d_{v}", 0) for v in DEDUCTION_VARS},
        "other_deductions": g("other_deductions", 0),
        "abt_other_income": g("abt_other_income", 0),
        "housing_assisted": bool(g("housing_assisted", False)),
        "housing_rent": g("housing_rent", 0),
        "municipio": g("municipio", "San Juan"),
        "pan_resources": g("pan_resources", 0),
        "pan_pays_dependent_care": bool(g("pan_pays_dependent_care", False)),
        "pan_recurrent_medical_expenses": bool(
            g("pan_recurrent_medical_expenses", False)
        ),
    }
    if not hh["joint"]:
        hh["spouse_wages"], hh["spouse"] = 0, {}
    return hh, g("filer_wages", 0)


def preset_hh(key):
    """(hh, filer_wages) for a preset household."""
    row = _lookup(PRESETS, key)
    return hh_from_state({**DEFAULTS, **(row[3] if row else {})})


def unmarried_split(hh):
    """The same two adults as two unmarried households: the filer keeps the
    children, deductions and housing; the spouse lives alone on their own
    wages and other income. Returns (hh_filer, hh_spouse)."""
    a = dict(hh, joint=False, spouse_wages=0, spouse={})
    b, _ = hh_from_state(
        {
            **DEFAULTS,
            "filer_age": hh["spouse_age"],
            "filer_veteran": hh["spouse_veteran"],
            "n_children": 0,
            **{f"filer_{v}": hh["spouse"].get(v, 0) for v in PERSON_VARS},
        }
    )
    return a, b


SHARED_KEYS = ("view", "lang", "reform_name", "compare_with", "show_levers")


def _coerce(value, like):
    if isinstance(like, bool):
        return value in ("1", "true", "True")
    if isinstance(like, int):
        return int(float(value))
    if isinstance(like, float):
        return float(value)
    return value


def apply_query_params(lever_defaults):
    """Load a shared link (?filer_wages=30000&joint=1&r.gov...=12000) into
    the session state, once, before the widgets are created."""
    if st.session_state.get("_qp_applied"):
        return
    st.session_state["_qp_applied"] = True
    for k, v in st.query_params.to_dict().items():
        try:
            if k.startswith("r."):
                path = k[2:]
                if path in lever_defaults:
                    st.session_state[f"r_{path}"] = float(v)
            elif k in DEFAULTS:
                st.session_state[k] = _coerce(v, DEFAULTS[k])
            elif k == "show_levers":
                st.session_state[k] = v in ("1", "true", "True")
            elif k == "reform":
                row = _lookup(EXAMPLE_REFORMS, v)
                if row is not None:
                    st.session_state["example_reform"] = row[0]
                    apply_example_reform(lever_defaults)
            elif k in SHARED_KEYS:
                st.session_state[k] = v
        except (TypeError, ValueError):
            continue


def sync_query_params(lever_defaults):
    """Write every non-default input to the URL so the page can be shared.
    Call after the sidebar has been built."""
    s = st.session_state
    out = {}
    for k, default in DEFAULTS.items():
        v = s.get(k, default)
        if v != default:
            out[k] = str(int(v)) if isinstance(v, bool) else str(v)
    levers = {}
    for path, default in lever_defaults.items():
        v = s.get(f"r_{path}", default)
        if abs(float(v) - float(default)) > 1e-9:
            levers[f"r.{path}"] = f"{v:g}"
    # a reform file whose levers match exactly travels as ?reform=<key>
    alias = next(
        (
            key
            for key, _, _, changes in EXAMPLE_REFORMS
            if changes
            and len(changes) == len(levers)
            and all(
                abs(
                    float(s.get(f"r_{p}", lever_defaults.get(p, 0)))
                    - float(val)
                )
                < 1e-6
                for p, val in changes.items()
            )
        ),
        None,
    )
    if alias:
        out["reform"] = alias
    else:
        out.update(levers)
    for k in SHARED_KEYS:
        v = s.get(k)
        if v is True:
            out[k] = "1"
        elif v and v is not False and v not in ("home", "none", "Español"):
            out[k] = str(v)
    if st.query_params.to_dict() != out:
        st.query_params.from_dict(out)


def share_link():
    """The full URL of the current page, from st.context when available."""
    try:
        url = st.context.url
    except Exception:
        return None
    if not url:
        return None
    url = str(url)
    query = "&".join(f"{k}={v}" for k, v in st.query_params.to_dict().items())
    base = url.split("?")[0]
    return f"{base}?{query}" if query else base


def init_state(lever_defaults):
    for k, v in DEFAULTS.items():
        st.session_state.setdefault(k, v)
    for path, v in lever_defaults.items():
        st.session_state.setdefault(f"r_{path}", v)
    st.session_state.setdefault("view", "home")
    st.session_state.setdefault("lang", "Español")
    st.session_state.setdefault("reform_name", "")
    st.session_state.setdefault("show_levers", False)
    apply_query_params(lever_defaults)


def _lookup(table, value):
    """Find a preset/reform by key or by either label; None if unknown
    (a stale widget value after a reload must not crash the page)."""
    for row in table:
        if value in (row[0], row[1], row[2]):
            return row
    return None


def apply_preset():
    row = _lookup(PRESETS, st.session_state.get("preset"))
    if row is None or row[0] == "custom":
        return
    for k, v in {**DEFAULTS, **row[3]}.items():
        st.session_state[k] = v


def apply_example_reform(lever_defaults):
    row = _lookup(EXAMPLE_REFORMS, st.session_state.get("example_reform"))
    if row is None:
        return
    key, changes = row[0], row[3]
    for path, base in lever_defaults.items():
        st.session_state[f"r_{path}"] = base
    for path, value in changes.items():
        st.session_state[f"r_{path}"] = float(value)
    name = next(
        r[1 + st.session_state.get("L", 0)]
        for r in EXAMPLE_REFORMS
        if r[0] == key
    )
    st.session_state["reform_name"] = "" if key == "none" else name


# ---------------------------------------------------------------------------
# Components
# ---------------------------------------------------------------------------
def household_summary(hh, filer_wages, L):
    parts = [
        t("summary_filer", L, hh["filer_age"]),
        t("summary_joint" if hh["joint"] else "summary_single", L),
    ]
    if hh["joint"]:
        parts.append(t("summary_spouse", L, hh["spouse_age"]))
    ages = hh["child_ages"]
    if not ages:
        parts.append(t("summary_children_0", L))
    elif len(ages) == 1:
        parts.append(t("summary_children_1", L, ages[0]))
    else:
        parts.append(
            t(
                "summary_children_n",
                L,
                len(ages),
                ", ".join(str(a) for a in ages),
            )
        )
    wages = filer_wages + (hh["spouse_wages"] if hh["joint"] else 0)
    parts.append(t("summary_wages", L, money(wages)))
    for var, key in (
        ("self_employment_income", "summary_se"),
        ("pension_income", "summary_pension"),
        ("social_security", "summary_ss"),
    ):
        total = hh["filer"][var] + (
            hh["spouse"].get(var, 0) if hh["joint"] else 0
        )
        if total:
            parts.append(t(key, L, money(total)))
    if hh.get("housing_assisted"):
        parts.append(t("summary_voucher", L, hh.get("municipio", "San Juan")))
    text = "; ".join(parts)
    # shown with st.markdown, where "$…$" would be read as LaTeX
    return (text[0].upper() + text[1:] + ".").replace("$", "\\$")


def metric_row(base, ref, L):
    """The four headline figures, identical on both pages."""
    shown = ref or base

    def metric(col, label, key, help_key, tile, lower_is_better=False):
        delta = money(ref[key] - base[key]) if ref else None
        with col, st.container(key=f"tile_{tile}"):
            st.metric(
                t(label, L),
                money(shown[key]),
                delta=delta,
                help=md(help_key, L),
                delta_color="inverse" if lower_is_better else "normal",
            )

    c1, c2, c3, c4 = st.columns(4)
    metric(c1, "m_tax", "pr_income_tax", "m_tax_help", "pays", True)
    metric(c2, "m_credits", "pr_refundable_credits", "m_credits_help", "gets")
    metric(c3, "m_net", "household_net_income", "m_net_help", "net")
    market = shown["household_market_income"]
    rate = (market - shown["household_net_income"]) / market if market else 0.0
    delta = None
    if ref and base["household_market_income"]:
        base_rate = (
            base["household_market_income"] - base["household_net_income"]
        ) / base["household_market_income"]
        delta = f"{(rate - base_rate) * 100:+.1f} pp"
    with c4, st.container(key="tile_rate"):
        st.metric(
            t("m_rate", L),
            money(100 - rate * 100),
            delta=f"{-(rate - base_rate) * 100:+.1f} pp" if delta else None,
            delta_color="normal",
            help=md("m_rate_help", L),
        )
    head = md(
        "headline_sentence",
        L,
        money(shown["pr_income_tax"]),
        money(shown["pr_refundable_credits"]),
        money(shown["household_net_income"]),
    )
    if not market:
        st.markdown(head + md("rate_sentence_zero", L))
    elif rate >= 0:
        st.markdown(head + md("rate_sentence_pos", L, 100 - rate * 100))
    else:
        st.markdown(head + md("rate_sentence_neg", L, 100 - rate * 100))


VALIDATED_RETURNS = (
    None  # set to the number of returns matched after the CPA validation
)
LAST_UPDATE = "2026-11-04"

ABOUT = (
    "**Sobre este modelo.** Hecho por [Espacios Abiertos](https://espaciosabiertos.org) "
    "sobre [PolicyEngine](https://policyengine.org); código y fuentes abiertos en "
    "[GitHub](https://github.com/danielsantamariaots/policyengine-pr). Reglas del año "
    "contributivo 2025. Versión del modelo: {}. ¿Un error o una duda? "
    "[Escríbanos](https://github.com/danielsantamariaots/policyengine-pr/issues/new). "
    "Licencia AGPL-3.0.",
    "**About this model.** Built by [Espacios Abiertos](https://espaciosabiertos.org) "
    "on [PolicyEngine](https://policyengine.org); code and sources open on "
    "[GitHub](https://github.com/danielsantamariaots/policyengine-pr). Tax year 2025 "
    "rules. Model version: {}. An error or a question? "
    "[Write to us](https://github.com/danielsantamariaots/policyengine-pr/issues/new). "
    "AGPL-3.0 licence.",
)
VALIDATED = (
    " Comprobado contra {} planillas reales de 2025 revisadas por un CPA.",
    " Checked against {} real 2025 returns reviewed by a CPA.",
)


def footer(L):
    text = ABOUT[L].format(LAST_UPDATE)
    if VALIDATED_RETURNS:
        text += VALIDATED[L].format(VALIDATED_RETURNS)
    st.divider()
    st.caption(text)


def card_tiles(base, ref, L):
    shown = ref or base
    market = shown["household_market_income"]
    rate = (market - shown["household_net_income"]) / market if market else 0.0
    return [
        (t("m_tax", L), money(shown["pr_income_tax"]), "pays"),
        (t("m_credits", L), money(shown["pr_refundable_credits"]), "gets"),
        (t("m_net", L), money(shown["household_net_income"]), "net"),
        (t("m_rate", L), money(100 - rate * 100), "rate"),
    ]


def headline_text(shown, L):
    """The headline sentence as plain text (no markdown) for the card."""
    market = shown["household_market_income"]
    rate = (market - shown["household_net_income"]) / market if market else 0.0
    head = t(
        "headline_sentence",
        L,
        money(shown["pr_income_tax"]),
        money(shown["pr_refundable_credits"]),
        money(shown["household_net_income"]),
    )
    if not market:
        tail = t("rate_sentence_zero", L)
    elif rate >= 0:
        tail = t("rate_sentence_pos", L, 100 - rate * 100)
    else:
        tail = t("rate_sentence_neg", L, 100 - rate * 100)
    return (head + tail).replace("**", "")


def not_included(L, short=False):
    """short=True keeps only the 'Lea con cuidado' bullets and the disclaimer
    (household pages); the full box goes on the home and reform pages."""
    text = md("not_included", L)
    if short:
        marker = "**Lea con cuidado:**" if L == 0 else "**Read with care:**"
        text = text[text.index(marker) :]
    st.warning(text)


def why(base, shown, L):
    """Three sentences, built from the computed values, that explain the
    headline numbers in words."""
    with st.expander(t("why_title", L)):
        x = shown
        ded = x["pr_deductions"] + x["pr_exemptions"]
        pct = "92%" if x["pr_taxable_gross_income"] <= 100_000 else "95%"
        st.markdown(
            md(
                "why_tax",
                L,
                money(x["pr_taxable_gross_income"]),
                money(ded),
                money(x["pr_net_taxable_income"]),
                money(x["pr_regular_tax"]),
                pct,
                money(x["pr_abt_excess"]),
                money(x["pr_income_tax"]),
            )
        )
        st.markdown(
            md("why_credits", L, money(x["pr_eitc"]), money(x["federal_actc"]))
        )
        payroll = (
            x["employee_social_security_tax"]
            + x["employee_medicare_tax"]
            + x["self_employment_tax"]
        )
        benefits = x["pan"] + x["tanf"] + x["section8"]
        st.markdown(
            md(
                "why_net",
                L,
                money(x["household_market_income"]),
                money(x["pr_income_tax"]),
                money(payroll),
                money(x["pr_refundable_credits"]),
                money(benefits),
                money(x["pan"]),
                money(x["tanf"]),
                money(x["section8"]),
                money(x["household_net_income"]),
            )
        )


GLOSSARY = [
    (
        "Ingreso bruto ajustado",
        "Adjusted gross income",
        "Todo lo que gana el hogar y que Hacienda cuenta: salarios, cuenta propia, pensiones tributables, intereses y dividendos (línea 5 de la planilla).",
        "Everything the household earns that Hacienda counts: wages, self-employment, taxable pensions, interest and dividends (line 5 of the return).",
    ),
    (
        "Deducciones",
        "Deductions",
        "Gastos que la ley permite restar antes de calcular la contribución: hipoteca, gastos médicos, donativos, IRA, educación, préstamos de estudio (Anejo A).",
        "Expenses the law lets you subtract before the tax is computed: mortgage, medical, donations, IRA, education, student loans (Anejo A).",
    ),
    (
        "Exenciones",
        "Exemptions",
        "Cantidades fijas que se restan por cada contribuyente ($3,500), dependiente ($2,500) y veterano ($1,500).",
        "Fixed amounts subtracted per filer ($3,500), dependent ($2,500) and veteran ($1,500).",
    ),
    (
        "Ingreso neto sujeto a contribución",
        "Net taxable income",
        "Lo que queda tras deducciones y exenciones; es la cantidad a la que se aplica la tabla de tasas.",
        "What is left after deductions and exemptions; the rate table applies to it.",
    ),
    (
        "Tabla de tasas (tramos)",
        "Rate table (brackets)",
        "0% hasta $9,000; 7% hasta $25,000; 14% hasta $41,500; 25% hasta $61,500; 33% después. Cada tasa se aplica solo a la parte del ingreso dentro de su tramo.",
        "0% to $9,000; 7% to $25,000; 14% to $41,500; 25% to $61,500; 33% above. Each rate applies only to the income within its bracket.",
    ),
    (
        "Ajuste gradual",
        "Gradual adjustment",
        "Recargo que quita el beneficio del tramo de 0% y de las exenciones a quienes ganan más de $500,000.",
        "Surcharge that removes the benefit of the 0% bracket and the exemptions above $500,000 of income.",
    ),
    (
        "Contribución básica alterna",
        "Alternate basic tax",
        "Un cálculo paralelo con menos deducciones; se paga la mayor de las dos contribuciones. Aplica desde $25,000 de ingreso neto alterno.",
        "A parallel computation with fewer deductions; the higher of the two taxes is paid. Applies from $25,000 of alternate net income.",
    ),
    (
        "Crédito reembolsable",
        "Refundable credit",
        "Crédito que Hacienda paga aunque la contribución sea cero. El Crédito por Trabajo y el crédito federal por hijos lo son.",
        "A credit Hacienda pays even when the tax is zero. The Crédito por Trabajo and the federal child credit are refundable.",
    ),
    (
        "Crédito por Trabajo",
        "Crédito por Trabajo (PR EITC)",
        "Crédito para quien trabaja: sube con el ingreso ganado hasta un máximo (según el número de dependientes) y luego baja hasta desaparecer.",
        "Credit for workers: rises with earned income up to a maximum (by number of dependents) and then falls to zero.",
    ),
    (
        "Crédito federal por hijos (ACTC)",
        "Federal child credit (ACTC)",
        "Parte reembolsable del crédito federal por hijos que los residentes de Puerto Rico reclaman al IRS: hasta $1,700 por hijo en 2025, 15% del ingreso ganado sobre $2,500.",
        "Refundable part of the federal child credit that Puerto Rico residents claim from the IRS: up to $1,700 per child in 2025, 15% of earned income above $2,500.",
    ),
    (
        "Tasa marginal efectiva",
        "Effective marginal rate",
        "De cada $100 adicionales que gana el hogar, la parte que se va en más contribuciones y en créditos y ayudas que se reducen.",
        "Of each additional $100 the household earns, the part that goes to more tax and to credits and benefits that shrink.",
    ),
    (
        "Precipicio",
        "Cliff",
        "Punto en el que ganar un poco más deja al hogar con menos ingreso neto, porque se pierde una ayuda de golpe (por ejemplo, el PAN al superar su límite).",
        "A point where earning slightly more leaves the household with less net income, because a benefit is lost all at once (for example PAN above its limit).",
    ),
    (
        "Núcleo de servicio (PAN)",
        "Núcleo de servicio (PAN)",
        "La unidad a la que ADSEF da el PAN: quienes compran y preparan la comida juntos. Una persona de 60 años o más puede ser su propio núcleo.",
        "The unit ADSEF pays PAN to: those who buy and prepare food together. A person aged 60 or over may be a núcleo of their own.",
    ),
    (
        "Vale de Sección 8",
        "Section 8 voucher",
        "Ayuda federal para el alquiler, administrada por Vivienda: cubre la diferencia entre la renta justa de mercado y el 30% del ingreso ajustado del hogar.",
        "Federal rent assistance run by Vivienda: covers the gap between the fair market rent and 30% of the household's adjusted income.",
    ),
    (
        "Ley vigente",
        "Current law",
        "Las reglas de 2025 tal como están en los formularios e instrucciones oficiales; la reforma contributiva se compara contra ellas.",
        "The 2025 rules as they stand in the official forms and instructions; a tax reform is compared against them.",
    ),
]


def glossary(L):
    with st.expander(t("glossary_title", L)):
        for es, en, des, den in GLOSSARY:
            st.markdown(
                f"**{(es, en)[L]}.** {(des, den)[L]}".replace("$", "\\$")
            )


def example_household(examples, L):
    """Named households with a one-line result; each 'Ver' loads its preset."""
    st.subheader(t("examples_title", L))
    for key, name, tax, credits, net in examples:
        c1, c2 = st.columns([6, 1])
        c1.markdown(
            md("example_line", L, name, money(tax), money(credits), money(net))
        )
        c2.button(
            t("see", L),
            key=f"example_{key}",
            on_click=lambda k=key: (
                st.session_state.update(preset=k),
                apply_preset(),
                st.session_state.update(view="calc"),
            ),
        )


def assumptions(current_values, changes, L, labels):
    with st.expander(t("assumptions_title", L)):
        st.markdown(md("assumptions_intro", L))
        rows = []
        for path, label_en, kind in LEVERS:
            base = current_values[path]
            new = changes.get(path, base)
            fmt = (lambda v: f"{v:.2%}") if kind == "rate" else money
            rows.append(
                {
                    t("col_param", L): labels.get(label_en, label_en)
                    if L == 0
                    else label_en,
                    t("col_current", L): fmt(base),
                    t("col_reform", L): fmt(new) if changes else "—",
                    t("col_source", L): "parameters/"
                    + path.split("[")[0].replace(".", "/")
                    + ".yaml",
                }
            )
        st.dataframe(
            pd.DataFrame(rows), use_container_width=True, hide_index=True
        )


def tutorial(L):
    with st.expander(t("tutorial_title", L)):
        tabs = st.tabs(
            [t("tab_calc", L), t("tab_cliff", L), t("tab_reform", L)]
        )
        for tab, text in zip(
            tabs, (TUTORIAL_CALC, TUTORIAL_CLIFF, TUTORIAL_REFORM)
        ):
            with tab:
                st.markdown(text[L])


def start_example():
    st.session_state["preset"] = "single_parent"
    apply_preset()
    st.session_state["view"] = "calc"


def home(L, examples=None):
    st.title(t("home_title", L))
    st.markdown(t("home_intro", L))
    st.button(
        t("start", L),
        key="start_example",
        type="primary",
        help=t("start_help", L),
        on_click=start_example,
    )
    if examples:
        example_household(examples, L)
    st.markdown(t("home_more", L))
    c1, c2, c3 = st.columns(3)
    for col, title, body, view in (
        (c1, "card_calc_title", "card_calc_body", "calc"),
        (c2, "card_cliff_title", "card_cliff_body", "cliff"),
        (c3, "card_reform_title", "card_reform_body", "reform"),
    ):
        with col, st.container(border=True):
            st.subheader(t(title, L))
            st.markdown(md(body, L))
            st.button(
                t("open", L),
                key=f"open_{view}",
                type="primary",
                on_click=lambda v=view: st.session_state.update(view=v),
            )
    tutorial(L)
    not_included(L)
    st.caption(t("home_disclaimer", L))

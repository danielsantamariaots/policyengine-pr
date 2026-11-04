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
    "nav_calc": ("Calculadora", "Calculator"),
    "nav_cliff": ("CliffWatch", "CliffWatch"),
    "nav_reform": ("Reformas", "Reforms"),
    "home_title": (
        "Modelo contributivo de Puerto Rico",
        "Puerto Rico tax model",
    ),
    "home_intro": (
        "Un modelo abierto del sistema contributivo de individuos de Puerto "
        "Rico (año contributivo 2025), construido sobre PolicyEngine. Cada "
        "regla está citada a un formulario o instrucción oficial de Hacienda "
        "o del IRS. Elija qué quiere saber:",
        "An open model of Puerto Rico's individual tax system (tax year "
        "2025), built on PolicyEngine. Every rule is cited to an official "
        "Hacienda or IRS form or instruction. Choose what you want to know:",
    ),
    "card_calc_title": (
        "¿Cuánto paga mi hogar?",
        "How much does my household pay?",
    ),
    "card_calc_body": (
        "Contribución, créditos e ingreso neto de un hogar, línea por línea "
        "según la planilla (Formulario 482). Pruebe una reforma y vea la "
        "diferencia.",
        "A household's tax, credits and net income, line by line as on the "
        "return (Formulario 482). Try a reform and see the difference.",
    ),
    "card_cliff_title": (
        "¿Dónde pierde mi hogar al ganar más?",
        "Where does my household lose by earning more?",
    ),
    "card_reform_title": (
        "¿Cuánto cuesta una reforma y a quién beneficia?",
        "What does a reform cost and who gains?",
    ),
    "card_reform_body": (
        "Cada reforma simulada sobre la Encuesta de la Comunidad de Puerto "
        "Rico: costo para Hacienda, hogares que ganan y pierden, cambio por "
        "decil de ingreso.",
        "Each reform simulated on the Puerto Rico Community Survey: cost to "
        "Hacienda, households better and worse off, change by income decile.",
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
        "profesional. Código y fuentes: github.com/danielsantamariaots/"
        "policyengine-pr.",
        "Results are estimates from the official 2025 forms and instructions "
        "and are not professional advice. Code and sources: "
        "github.com/danielsantamariaots/policyengine-pr.",
    ),
    "preset": ("Hogar tipo", "Household preset"),
    "preset_help": (
        "Elija un hogar de ejemplo y ajuste lo que quiera debajo.",
        "Pick an example household, then adjust anything below.",
    ),
    "example_reform": ("Reformas de ejemplo", "Example reforms"),
    "example_reform_help": (
        "Rellena los parámetros de abajo; puede editarlos después.",
        "Fills the levers below; you can edit them afterwards.",
    ),
    "reform_name": ("Nombre de la reforma", "Reform name"),
    "reform_default_name": ("Reforma", "Reform"),
    "summary_single": ("planilla individual", "single return"),
    "summary_joint": ("planilla conjunta", "joint return"),
    "summary_filer": ("contribuyente de {} años", "filer aged {}"),
    "summary_spouse": ("cónyuge de {} años", "spouse aged {}"),
    "summary_wages": ("salarios {}", "wages {}"),
    "summary_se": ("cuenta propia {}", "self-employment {}"),
    "summary_pension": ("pensión {}", "pension {}"),
    "summary_ss": ("Seguro Social {}", "Social Security {}"),
    "summary_voucher": ("vale de Sección 8", "Section 8 voucher"),
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
    "m_rate": ("Se va de cada $100", "Out of each $100"),
    "m_rate_help": (
        "Tasa contributiva neta: (ingreso de mercado − ingreso neto) / "
        "ingreso de mercado. Negativa cuando el hogar recibe más en créditos "
        "de lo que paga.",
        "Net tax rate: (market income − net income) / market income. "
        "Negative when the household receives more in credits than it pays.",
    ),
    "rate_sentence_pos": (
        "De cada $100 que gana este hogar, **${:.0f}** se van en "
        "contribuciones netas de créditos.",
        "Out of every $100 this household earns, **${:.0f}** goes to taxes "
        "net of credits.",
    ),
    "rate_sentence_neg": (
        "Este hogar recibe **${:.0f}** en créditos netos por cada $100 que "
        "gana: los créditos superan lo que paga en contribuciones.",
        "This household receives **${:.0f}** in net credits for every $100 "
        "it earns: credits exceed what it pays in taxes.",
    ),
    "rate_sentence_zero": (
        "Este hogar no tiene ingresos de mercado.",
        "This household has no market income.",
    ),
    "not_included_title": ("Qué no incluye", "What is not included"),
    "not_included": (
        "**No incluido:** tasas preferenciales distintas del 10% y 15% "
        "(columnas de 4% y 20% del Anejo A2) y arrastre de pérdidas de "
        "capital; créditos por inversión (Anejo B); categorías A, B, D, G y T "
        "del TANF; efectos de comportamiento. "
        "**Incluido con salvedades:** el PAN paga el beneficio máximo a todo "
        "hogar elegible, porque ADSEF no publica la tabla que lo reduce según "
        "el ingreso neto, usa los límites de octubre de 2021 para hogares de 2 "
        "o más personas y no aplica prueba de recursos; el TANF (categoría C, "
        "madre o padre solo con hijos menores) usa el máximo de una familia de "
        "tres ($584) para todo tamaño; la Sección 8 solo se calcula si usted "
        "indica que el hogar tiene un vale, con los límites y rentas justas "
        "de mercado de San Juan-Guaynabo para toda la isla; el Plan Vital se "
        "evalúa como elegibilidad, sin valor en dólares. La exención para jóvenes (Ley "
        "135-2014) se aplica automáticamente entre los 16 y 26 años.",
        "**Not included:** preferential rates other than 10% and 15% (Anejo "
        "A2 columns at 4% and 20%) and capital-loss carryovers; investment "
        "credits (Anejo B); TANF categories A, B, D, G and T; behavioural "
        "responses. **Included with caveats:** PAN pays the "
        "maximum benefit to every eligible household because ADSEF does not "
        "publish the schedule that reduces it with net income, uses the "
        "October 2021 limits for households of 2 or more, and applies no "
        "resources test; TANF (category C, single parent with minor "
        "children) uses the three-person maximum ($584) for every size; "
        "Section 8 is computed only if you say the household holds a voucher, "
        "with the San Juan-Guaynabo income limits and fair market rents applied "
        "island-wide; Plan Vital is assessed as eligibility only, with no "
        "dollar value. The "
        "youth exemption (Ley 135-2014) applies automatically at ages 16–26.",
    ),
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
    "col_reform": ("Reforma", "Reform"),
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


SHARED_KEYS = ("view", "lang", "reform_name", "compare_with")


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
    for path, default in lever_defaults.items():
        v = s.get(f"r_{path}", default)
        if abs(float(v) - float(default)) > 1e-9:
            out[f"r.{path}"] = f"{v:g}"
    for k in SHARED_KEYS:
        v = s.get(k)
        if v and v not in ("home", "none", "Español"):
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
        parts.append(t("summary_voucher", L))
    text = "; ".join(parts)
    # shown with st.markdown, where "$…$" would be read as LaTeX
    return (text[0].upper() + text[1:] + ".").replace("$", "\\$")


def metric_row(base, ref, L):
    """The four headline figures, identical on both pages."""
    shown = ref or base

    def metric(col, label, key, help_key, lower_is_better=False):
        delta = money(ref[key] - base[key]) if ref else None
        col.metric(
            t(label, L),
            money(shown[key]),
            delta=delta,
            help=md(help_key, L),
            delta_color="inverse" if lower_is_better else "normal",
        )

    c1, c2, c3, c4 = st.columns(4)
    metric(c1, "m_tax", "pr_income_tax", "m_tax_help", lower_is_better=True)
    metric(c2, "m_credits", "pr_refundable_credits", "m_credits_help")
    metric(c3, "m_net", "household_net_income", "m_net_help")
    market = shown["household_market_income"]
    rate = (market - shown["household_net_income"]) / market if market else 0.0
    delta = None
    if ref and base["household_market_income"]:
        base_rate = (
            base["household_market_income"] - base["household_net_income"]
        ) / base["household_market_income"]
        delta = f"{(rate - base_rate) * 100:+.1f} pp"
    c4.metric(
        t("m_rate", L),
        f"-${-rate * 100:,.0f}" if rate < 0 else money(rate * 100),
        delta=delta,
        delta_color="inverse",
        help=md("m_rate_help", L),
    )
    if not market:
        st.caption(md("rate_sentence_zero", L))
    elif rate >= 0:
        st.caption(md("rate_sentence_pos", L, rate * 100))
    else:
        st.caption(md("rate_sentence_neg", L, -rate * 100))


def not_included(L):
    st.warning(md("not_included", L))


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


def home(L):
    st.title(t("home_title", L))
    st.markdown(t("home_intro", L))
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

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

# Example reforms: (key, name es, name en, {lever path: value})
EXAMPLE_REFORMS = [
    ("none", "Ninguna (ley vigente)", "None (current law)", {}),
    (
        "zero_bracket",
        "Ampliar el tramo de 0% a $12,000",
        "Widen the 0% bracket to $12,000",
        {"gov.hacienda.income.rates[1].threshold": 12_000.0},
    ),
    (
        "eitc_up",
        "Subir 20% el Crédito por Trabajo máximo",
        "Raise the maximum Crédito por Trabajo 20%",
        {
            f"gov.hacienda.credits.eitc.max.{n}": None  # filled from current law
            for n in range(4)
        },
    ),
    (
        "no_notch",
        "Eliminar el salto del 92% al 95%",
        "Remove the 92%→95% jump",
        {"gov.hacienda.income.tax_determination.rate.standard": 0.92},
    ),
    (
        "exemption_up",
        "Exención personal a $5,000 / $10,000",
        "Personal exemption to $5,000 / $10,000",
        {
            "gov.hacienda.income.exemptions.personal.SINGLE": 5_000.0,
            "gov.hacienda.income.exemptions.personal.JOINT": 10_000.0,
        },
    ),
]

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
    "summary_children_0": ("sin dependientes", "no dependents"),
    "summary_children_1": ("1 dependiente ({} años)", "1 dependent (age {})"),
    "summary_children_n": (
        "{} dependientes ({} años)",
        "{} dependents (ages {})",
    ),
    "m_tax": ("Contribución sobre ingresos de PR", "PR income tax"),
    "m_tax_help": (
        "Línea 26 del Formulario 482: lo que el hogar debe a Hacienda antes "
        "de retenciones y créditos reembolsables.",
        "Formulario 482 line 26: what the household owes Hacienda before "
        "withholding and refundable credits.",
    ),
    "m_credits": ("Créditos reembolsables", "Refundable credits"),
    "m_credits_help": (
        "Crédito por Trabajo (línea 27C) más el crédito federal por hijos "
        "(línea 27D). Se pagan aunque no se deba contribución.",
        "Crédito por Trabajo (line 27C) plus the federal child credit (line "
        "27D). Paid even when no tax is owed.",
    ),
    "m_net": ("Ingreso neto", "Net income"),
    "m_net_help": (
        "Ingresos del hogar menos contribución de PR, Seguro Social y "
        "Medicare, más créditos reembolsables y PAN.",
        "Household income minus PR tax, Social Security and Medicare, plus "
        "refundable credits and PAN.",
    ),
    "m_rate": ("Lo que se va de cada $100", "Out of every $100"),
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
        "Tasas preferenciales distintas del 10% y 15% (columnas de 4% y 20% "
        "del Anejo A2); créditos por inversión (Anejo B); Medicaid/Vital, TANF "
        "y Sección 8. El PAN está incluido con el beneficio máximo por tamaño "
        "del hogar, pero ADSEF no publica la tabla que reduce el beneficio "
        "según el ingreso neto, ni los límites vigentes para hogares de 2 o "
        "más personas (se usan los de octubre de 2021); efectos de "
        "comportamiento. La "
        "exención para jóvenes (Ley 135-2014) se aplica automáticamente "
        "entre los 16 y 26 años.",
        "Preferential rates other than 10% and 15% (Anejo A2 columns at 4% "
        "and 20%); investment credits (Anejo B); Medicaid/Vital, TANF and "
        "Section 8. PAN is included at the maximum benefit by household size, "
        "but ADSEF does not publish the schedule that reduces the benefit "
        "with net income, nor the current limits for households of 2 or more "
        "(October 2021 values are used); behavioural responses. The youth "
        "exemption (Ley 135-2014) applies automatically at ages 16–26.",
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
calculan sobre la reforma.
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
reform.
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
def init_state(lever_defaults):
    for k, v in DEFAULTS.items():
        st.session_state.setdefault(k, v)
    for path, v in lever_defaults.items():
        st.session_state.setdefault(f"r_{path}", v)
    st.session_state.setdefault("view", "home")
    st.session_state.setdefault("reform_name", "")


def apply_preset():
    key = st.session_state["preset"]
    overrides = next(p[3] for p in PRESETS if p[0] == key)
    if key == "custom":
        return
    for k, v in {**DEFAULTS, **overrides}.items():
        st.session_state[k] = v


def apply_example_reform(lever_defaults):
    key = st.session_state["example_reform"]
    changes = next(r[3] for r in EXAMPLE_REFORMS if r[0] == key)
    for path, base in lever_defaults.items():
        st.session_state[f"r_{path}"] = base
    for path, value in changes.items():
        if value is None:  # relative change: +20% on the current value
            value = round(lever_defaults[path] * 1.2)
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
    st.warning(f"**{t('not_included_title', L)}.** {t('not_included', L)}")


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

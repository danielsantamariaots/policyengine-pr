"""Household calculator prototype on top of policyengine-pr.

Run with:  streamlit run app/calculator.py
"""

import cliffwatch
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from policyengine_pr import Simulation, system
from policyengine_pr.reforms.parametric import LEVERS, parametric_reform

YEAR = 2025
BASELINE_COLOR = "#2a78d6"
REFORM_COLOR = "#eb6834"
CREDIT_COLOR = "#1baf7a"

# ---------------------------------------------------------------------------
# Text in both languages. Spanish is the default; English is one toggle away.
# ---------------------------------------------------------------------------
TEXT = {
    "title": (
        "Calculadora contributiva de hogares de Puerto Rico",
        "Puerto Rico household tax calculator",
    ),
    "caption": (
        "Prototipo sobre policyengine-pr · año contributivo 2025 · "
        "cada regla citada a un documento oficial de Hacienda o del "
        "IRS en docs/statutes/",
        "Prototype on policyengine-pr · tax year 2025 · every rule "
        "cited to a Hacienda or IRS document in docs/statutes/",
    ),
    "language": ("Idioma / Language", "Idioma / Language"),
    "view": ("Página", "Page"),
    "view_calc": ("Calculadora", "Calculator"),
    "view_cliff": ("CliffWatch", "CliffWatch"),
    "household": ("Hogar", "Household"),
    "joint": (
        "Casados que rinden planilla conjunta",
        "Married filing jointly",
    ),
    "filer_age": ("Edad del contribuyente", "Filer age"),
    "filer_wages": ("Salarios del contribuyente ($)", "Filer wages ($)"),
    "filer_veteran": ("El contribuyente es veterano", "Filer is a veteran"),
    "spouse_age": ("Edad del cónyuge", "Spouse age"),
    "spouse_wages": ("Salarios del cónyuge ($)", "Spouse wages ($)"),
    "spouse_veteran": ("El cónyuge es veterano", "Spouse is a veteran"),
    "filer": ("Contribuyente", "Filer"),
    "spouse": ("Cónyuge", "Spouse"),
    "other_income": ("{}: otros ingresos", "{} other income"),
    "children": ("Dependientes (hijos)", "Dependent children"),
    "child_age": ("Edad del hijo {}", "Child {} age"),
    "deductions": ("Deducciones (Anejo A)", "Deductions (Anejo A)"),
    "other_deductions": ("Otras deducciones ($)", "Other deductions ($)"),
    "other_deductions_help": (
        "Pérdidas por causas fortuitas y partidas no calculadas",
        "Casualty losses and items not computed",
    ),
    "advanced": ("Avanzado", "Advanced"),
    "abt_other": (
        "Otros ingresos sujetos a contribución básica alterna ($)",
        "Other income subject to alternate basic tax ($)",
    ),
    "abt_other_help": (
        "Partidas de entidades conducto y exentas no modeladas; los "
        "salarios nunca están sujetos (instrucciones 2025, p. 82).",
        "Pass-through and exempt items not modelled; wages are never "
        "subject (2025 instructions, p. 82).",
    ),
    "reform": ("Reforma", "Reform"),
    "reform_caption": (
        "Edite cualquier parámetro; los demás mantienen la ley vigente.",
        "Edit any lever; unchanged levers keep current law.",
    ),
    "reform_active": (
        "Reforma activa: {} parámetro(s) cambiado(s). Las diferencias "
        "son reforma menos ley vigente.",
        "Reform active: {} lever(s) changed. Deltas are reform minus "
        "current law.",
    ),
    "m_tax": ("Contribución sobre ingresos de PR", "PR income tax"),
    "m_credits": ("Créditos reembolsables", "Refundable credits"),
    "m_credits_help": (
        "Crédito por Trabajo + ACTC federal",
        "Crédito por Trabajo + federal ACTC",
    ),
    "m_net": ("Ingreso neto", "Net income"),
    "m_rate": ("Tasa contributiva neta", "Net tax rate"),
    "m_rate_help": (
        "(ingreso de mercado − ingreso neto) / ingreso de mercado; "
        "negativo significa una transferencia neta al hogar",
        "(market income − net income) / market income; negative means "
        "a net transfer",
    ),
    "range_title": (
        "A lo largo de la escala de ingresos",
        "Across the income range",
    ),
    "range_caption": (
        "Mismo hogar; salarios del contribuyente de $0 a $150,000.",
        "Same household; filer wages varied from $0 to $150,000.",
    ),
    "x_axis": ("Salarios del contribuyente", "Filer wages"),
    "s_tax": ("Contribución sobre ingresos de PR", "PR income tax"),
    "s_payroll": ("Contribuciones de nómina", "Payroll taxes"),
    "s_credits": ("Créditos reembolsables", "Refundable credits"),
    "s_net": ("Ingreso neto", "Net income"),
    "s_net_reform": ("Ingreso neto (reforma)", "Net income (reform)"),
    "s_change": ("Cambio en ingreso neto", "Change in net income"),
    "s_net_current": ("Ingreso neto, ley vigente", "Net income, current law"),
    "s_net_ref": ("Ingreso neto, reforma", "Net income, reform"),
    "change_caption": (
        "Positivo significa que el hogar sale ganando con la reforma.",
        "Positive means the household is better off under the reform.",
    ),
    "table_view": ("Ver tabla", "Table view"),
    "marginal": ("Tasa marginal", "Marginal rate"),
    "line_by_line": ("Línea por línea", "Line by line"),
    "col_item": ("Partida", "Item"),
    "col_amount": ("Cantidad", "Amount"),
    "col_current": ("Ley vigente", "Current law"),
    "col_reform": ("Reforma", "Reform"),
    "col_change": ("Cambio", "Change"),
    "not_modelled": (
        "**Todavía no modelado:** intereses, dividendos y ganancias de "
        "capital a tasas preferenciales; créditos no reembolsables por "
        "inversión (Anejo B); beneficios (PAN, Medicaid). La exención "
        "para jóvenes (Ley 135-2014) se aplica automáticamente entre los "
        "16 y 26 años.",
        "**Not yet modelled:** interest, dividends and capital gains at "
        "preferential rates; nonrefundable investment credits (Anejo B); "
        "benefits (PAN, Medicaid). Youth exemption (Ley 135-2014) applies "
        "automatically for ages 16–26.",
    ),
    "tutorial_title": (
        "Cómo usar esta calculadora",
        "How to use this calculator",
    ),
}

OUTPUTS = [
    (
        "pr_taxable_gross_income",
        "Ingreso bruto ajustado (línea 5)",
        "Adjusted gross income (line 5)",
    ),
    (
        "pr_deductions",
        "Deducciones, Anejo A (línea 6)",
        "Deductions, Anejo A (line 6)",
    ),
    (
        "pr_exemptions",
        "Exenciones personal, por veterano y por dependientes",
        "Personal, veteran and dependent exemptions",
    ),
    (
        "pr_net_taxable_income",
        "Ingreso neto sujeto a contribución (línea 13)",
        "Net taxable income (line 13)",
    ),
    (
        "pr_regular_tax",
        "Contribución según tabla, Sec. 1021.01 (línea 14)",
        "Tax per table, Sec. 1021.01 (line 14)",
    ),
    (
        "pr_gradual_adjustment",
        "Ajuste gradual (línea 15)",
        "Gradual adjustment (line 15)",
    ),
    (
        "pr_regular_tax_before_credits",
        "Contribución regular tras 92%/95% (línea 17)",
        "Regular tax after 92%/95% (line 17)",
    ),
    (
        "pr_abt_excess",
        "Exceso de contribución básica alterna (línea 20)",
        "Alternate basic tax excess (line 20)",
    ),
    (
        "pr_income_tax",
        "Contribución sobre ingresos de PR (línea 26)",
        "PR income tax (line 26)",
    ),
    (
        "pr_eitc",
        "Crédito por Trabajo (línea 27C)",
        "Crédito por Trabajo (line 27C)",
    ),
    (
        "federal_actc",
        "Crédito tributario adicional por hijos, federal (línea 27D)",
        "Federal additional child tax credit (line 27D)",
    ),
    (
        "employee_social_security_tax",
        "Seguro Social retenido",
        "Social Security tax withheld",
    ),
    ("employee_medicare_tax", "Medicare retenido", "Medicare tax withheld"),
    (
        "self_employment_tax",
        "Contribución por trabajo por cuenta propia (Schedule SE)",
        "Self-employment tax (Schedule SE)",
    ),
    ("household_net_income", "Ingreso neto del hogar", "Household net income"),
]
RANGE_VARS = [
    "pr_income_tax",
    "employee_social_security_tax",
    "employee_medicare_tax",
    "self_employment_tax",
    "pr_refundable_credits",
    "household_net_income",
]
PERSON_INPUTS = [
    # (variable, label es, label en, step, help es, help en)
    (
        "self_employment_income",
        "Ganancia neta por cuenta propia ($)",
        "Self-employment net profit ($)",
        1_000,
        "Anejo M, Parte IV, línea 9",
        "Anejo M, Parte IV, línea 9",
    ),
    (
        "pension_income",
        "Pensión de un plan cualificado ($)",
        "Pension from a qualified plan ($)",
        1_000,
        "Anejo H; $11,000 / $15,000 exentos según la edad",
        "Anejo H; $11,000 / $15,000 exempt by age",
    ),
    (
        "social_security",
        "Beneficios del Seguro Social ($)",
        "Social Security benefits ($)",
        1_000,
        "No tributan en Puerto Rico",
        "Not taxed in Puerto Rico",
    ),
]
DEDUCTION_INPUTS = [
    (
        "mortgage_interest",
        "Intereses hipotecarios ($)",
        "Home mortgage interest ($)",
        500,
        "El menor entre lo pagado, 30% del ingreso y $35,000",
        "Lesser of paid, 30% of income, $35,000",
    ),
    (
        "medical_expenses",
        "Gastos médicos ($)",
        "Medical expenses ($)",
        500,
        "Deducibles en exceso del 6% del ingreso bruto ajustado",
        "Deductible above 6% of AGI",
    ),
    (
        "charitable_contributions",
        "Donativos ($)",
        "Charitable contributions ($)",
        500,
        "Hasta 50% del ingreso bruto ajustado",
        "Up to 50% of AGI",
    ),
    (
        "ira_contributions",
        "Aportaciones a IRA ($)",
        "IRA contributions ($)",
        500,
        "Hasta $7,000 por persona, limitado por ingresos ganados",
        "Up to $7,000 per person, limited by earnings",
    ),
    (
        "education_account_contributions",
        "Cuentas de aportación educativa ($)",
        "Education accounts ($)",
        100,
        "Hasta $1,000 por beneficiario",
        "Up to $1,000 per beneficiary",
    ),
    (
        "student_loan_payments",
        "Pagos de préstamos estudiantiles ($)",
        "Student loan payments ($)",
        100,
        "Intereses y principal, nivel universitario",
        "Interest and principal, university level",
    ),
]
LEVER_LABELS_ES = {
    "Bracket 2 starts (7%)": "Inicio del tramo 2 (7%)",
    "Bracket 2 rate": "Tasa del tramo 2",
    "Bracket 3 starts (14%)": "Inicio del tramo 3 (14%)",
    "Bracket 3 rate": "Tasa del tramo 3",
    "Bracket 4 starts (25%)": "Inicio del tramo 4 (25%)",
    "Bracket 4 rate": "Tasa del tramo 4",
    "Top bracket starts (33%)": "Inicio del tramo superior (33%)",
    "Top bracket rate": "Tasa del tramo superior",
    "Personal exemption, single": "Exención personal, individual",
    "Personal exemption, joint": "Exención personal, conjunta",
    "Exemption per dependent": "Exención por dependiente",
    "Tax factor, gross income ≤ threshold": "Factor (92%) si ingreso bruto ≤ umbral",
    "Tax factor, above threshold": "Factor (95%) sobre el umbral",
    "Tax factor income threshold": "Umbral de ingreso bruto del factor",
    "EITC maximum, no children": "Crédito por Trabajo máximo, sin dependientes",
    "EITC maximum, 1 child": "Crédito por Trabajo máximo, 1 dependiente",
    "EITC maximum, 2 children": "Crédito por Trabajo máximo, 2 dependientes",
    "EITC maximum, 3+ children": "Crédito por Trabajo máximo, 3+ dependientes",
    "EITC phase-out start, 2 children, single": "Inicio de reducción del crédito, 2 dep., individual",
    "EITC phase-out start, 2 children, joint": "Inicio de reducción del crédito, 2 dep., conjunta",
    "EITC income limit, 2 children, single": "Límite de ingreso del crédito, 2 dep., individual",
    "EITC income limit, 2 children, joint": "Límite de ingreso del crédito, 2 dep., conjunta",
    "Youth exemption (Ley 135)": "Exención para jóvenes (Ley 135)",
    "Youth exemption maximum age": "Edad máxima de la exención para jóvenes",
}

TUTORIAL = {
    "es": """
**1. Describa el hogar** en la barra lateral: estado civil, edades, salarios y
dependientes. Para ingresos que no sean salarios (trabajo por cuenta propia,
pensiones, Seguro Social) abra *Contribuyente: otros ingresos*. Las
deducciones del Anejo A van en su propia sección; la calculadora aplica los
límites de ley (por ejemplo, gastos médicos solo sobre el 6% del ingreso).

**2. Lea los resultados.** Arriba: contribución, créditos reembolsables,
ingreso neto y la tasa neta (negativa cuando el hogar recibe más en créditos
de lo que paga). A la derecha, *Línea por línea* sigue el orden de la
planilla (Formulario 482). A la izquierda, la gráfica muestra cómo cambian
contribuciones y créditos si los salarios del contribuyente variaran de $0 a
$150,000; la línea punteada marca el hogar actual. *Ver tabla* añade la
tasa marginal efectiva en cada tramo.

**3. Pruebe una reforma.** Al final de la barra lateral, cambie cualquier
parámetro (tramos, exenciones, factor 92%/95%, Crédito por Trabajo, exención
para jóvenes). La página pasa a modo de comparación: cada cifra muestra la
diferencia frente a la ley vigente y aparece una gráfica de *Cambio en
ingreso neto*. Para volver a la ley vigente, restaure el valor original.

**4. CliffWatch.** Arriba de la barra lateral, cambie *Calculadora* por
*CliffWatch* para ver, con el mismo hogar, cómo cambian contribuciones,
créditos e ingreso neto en pasos de $500 hasta $150,000, la tasa marginal
efectiva en cada paso, y una lista de los *precipicios* (puntos donde ganar
$500 más deja al hogar con menos ingreso neto) y de las zonas donde la tasa
marginal llega al 50% o más. Con una reforma activa se comparan las dos curvas.

**Ejemplos para empezar:** edad 22 y salarios $30,000 (exención para jóvenes:
contribución cero); dos dependientes y salarios de $44,000 frente a $45,000
(se pierde todo el Crédito por Trabajo); *Inicio del tramo 2* en $12,000
(ampliar el tramo de 0%).

**Qué no está incluido todavía:** intereses, dividendos y ganancias de
capital a tasas preferenciales; créditos por inversión del Anejo B;
beneficios como PAN y Medicaid. Los resultados son estimaciones a partir de
los formularios e instrucciones de Hacienda y del IRS para 2025; no
sustituyen asesoría profesional.
""",
    "en": """
**1. Describe the household** in the sidebar: filing status, ages, wages and
dependents. Non-wage income (self-employment, pensions, Social Security) is
under *Filer other income*. Anejo A deductions have their own section; the
calculator applies the statutory limits (for example, medical expenses only
above 6% of income).

**2. Read the results.** At the top: tax, refundable credits, net income and
the net rate (negative when the household receives more in credits than it
pays). On the right, *Line by line* follows the order of the return
(Formulario 482). On the left, the chart shows how taxes and credits would
change if the filer's wages ran from $0 to $150,000; the dotted line marks
the current household. *Table view* adds the effective marginal rate at each
step.

**3. Try a reform.** At the bottom of the sidebar, change any lever (brackets,
exemptions, the 92%/95% factor, the Crédito por Trabajo, the youth
exemption). The page switches to comparison mode: every figure shows its
difference from current law and a *Change in net income* chart appears. To
return to current law, restore the original value.

**4. CliffWatch.** At the top of the sidebar, switch *Calculator* to
*CliffWatch* to see, for the same household, how taxes, credits and net
income change in $500 steps up to $150,000, the effective marginal rate at
each step, and a list of *cliffs* (points where earning $500 more leaves the
household with less net income) and of zones where the marginal rate reaches
50% or more. With a reform active, both curves are compared.

**Examples to start with:** age 22 and $30,000 wages (youth exemption: zero
tax); two dependents at $44,000 vs $45,000 wages (the whole Crédito por
Trabajo is lost); *Bracket 2 starts* at $12,000 (a wider 0% bracket).

**Not included yet:** interest, dividends and capital gains at preferential
rates; Anejo B investment credits; benefits such as PAN and Medicaid. Results
are estimates from Hacienda's and the IRS's 2025 forms and instructions and
are not professional advice.
""",
}


def current_value(path):
    """Current-law value of a lever at the start of YEAR."""
    node = system.parameters
    for name in path.split("."):
        if "[" in name:
            name, index = name.split("[")
            node = node.children[name].brackets[int(index[:-1])]
        else:
            node = node.children[name]
    return float(node(f"{YEAR}-01-01"))


def build_situation(hh, filer_wages):
    """hh: dict of household inputs; filer_wages varied separately."""
    filer = {
        "age": {YEAR: hh["filer_age"]},
        "employment_income": {YEAR: filer_wages},
        "is_veteran": {YEAR: hh["filer_veteran"]},
    }
    for var, *_ in PERSON_INPUTS:
        filer[var] = {YEAR: hh["filer"][var]}
    for var, *_ in DEDUCTION_INPUTS:
        filer[var] = {YEAR: hh["deductions"][var]}
    people = {"filer": filer}
    if hh["joint"]:
        spouse = {
            "age": {YEAR: hh["spouse_age"]},
            "employment_income": {YEAR: hh["spouse_wages"]},
            "is_veteran": {YEAR: hh["spouse_veteran"]},
        }
        for var, *_ in PERSON_INPUTS:
            spouse[var] = {YEAR: hh["spouse"][var]}
        people["spouse"] = spouse
    for i, age in enumerate(hh["child_ages"]):
        people[f"child_{i}"] = {
            "age": {YEAR: age},
            "is_tax_unit_dependent": {YEAR: True},
        }
    members = list(people)
    tax_unit = {
        "members": members,
        "pr_filing_status": {YEAR: "JOINT" if hh["joint"] else "SINGLE"},
        "pr_other_deductions": {YEAR: hh["other_deductions"]},
        "pr_abt_other_income": {YEAR: hh["abt_other_income"]},
    }
    return {
        "people": people,
        "tax_units": {"tax_unit": tax_unit},
        "households": {"household": {"members": members}},
    }


def compute(situation, variables, reform=None):
    sim = Simulation(situation=situation, reform=reform)
    return {v: float(sim.calculate(v, YEAR)[0]) for v in variables}


def money(x):
    return f"${x:,.0f}"


st.set_page_config(page_title="Calculadora contributiva PR", layout="wide")

with st.sidebar:
    lang = st.radio(
        TEXT["language"][0],
        ["Español", "English"],
        horizontal=True,
        label_visibility="collapsed",
    )
L = 0 if lang == "Español" else 1


def t(key, *args):
    s = TEXT[key][L]
    return s.format(*args) if args else s


with st.sidebar:
    view = st.radio(
        t("view"),
        [t("view_calc"), t("view_cliff")],
        horizontal=True,
        label_visibility="collapsed",
    )
show_cliffwatch = view == t("view_cliff")


def person_inputs(prefix_key):
    with st.expander(t("other_income", t(prefix_key))):
        return {
            var: st.number_input(
                (es, en)[L],
                0,
                5_000_000,
                0,
                step=step,
                help=(hes, hen)[L],
                key=f"{prefix_key}_{var}",
            )
            for var, es, en, step, hes, hen in PERSON_INPUTS
        }


if not show_cliffwatch:
    st.title(t("title"))
    st.caption(t("caption"))
    with st.expander(t("tutorial_title"), expanded=False):
        st.markdown(TUTORIAL["es" if L == 0 else "en"])

hh = {}
with st.sidebar:
    st.header(t("household"))
    hh["joint"] = st.toggle(t("joint"), value=False)
    hh["filer_age"] = st.number_input(t("filer_age"), 16, 100, 35)
    filer_wages = st.number_input(
        t("filer_wages"), 0, 2_000_000, 30_000, step=1_000
    )
    hh["filer_veteran"] = st.checkbox(t("filer_veteran"), value=False)
    hh["filer"] = person_inputs("filer")
    hh["spouse_age"], hh["spouse_wages"] = 35, 0
    hh["spouse_veteran"], hh["spouse"] = False, {}
    if hh["joint"]:
        hh["spouse_age"] = st.number_input(t("spouse_age"), 16, 100, 35)
        hh["spouse_wages"] = st.number_input(
            t("spouse_wages"), 0, 2_000_000, 0, step=1_000
        )
        hh["spouse_veteran"] = st.checkbox(t("spouse_veteran"), value=False)
        hh["spouse"] = person_inputs("spouse")
    n_children = st.number_input(t("children"), 0, 8, 2)
    hh["child_ages"] = [
        st.number_input(
            t("child_age", i + 1), 0, 25, min(4 + 4 * i, 25), key=f"c{i}"
        )
        for i in range(n_children)
    ]
    with st.expander(t("deductions")):
        hh["deductions"] = {
            var: st.number_input(
                (es, en)[L],
                0,
                1_000_000,
                0,
                step=step,
                help=(hes, hen)[L],
                key=f"d_{var}",
            )
            for var, es, en, step, hes, hen in DEDUCTION_INPUTS
        }
        hh["other_deductions"] = st.number_input(
            t("other_deductions"),
            0,
            1_000_000,
            0,
            step=500,
            help=t("other_deductions_help"),
        )
    with st.expander(t("advanced")):
        hh["abt_other_income"] = st.number_input(
            t("abt_other"),
            0,
            5_000_000,
            0,
            step=1_000,
            help=t("abt_other_help"),
        )

    st.header(t("reform"))
    st.caption(t("reform_caption"))
    changes = {}
    for path, label_en, kind in LEVERS:
        label = LEVER_LABELS_ES.get(label_en, label_en) if L == 0 else label_en
        base_value = current_value(path)
        if kind == "rate":
            new = st.number_input(
                label,
                0.0,
                1.0,
                base_value,
                step=0.01,
                format="%.4f",
                key=f"r_{path}",
            )
        else:
            new = st.number_input(
                label,
                0.0,
                5_000_000.0,
                base_value,
                step=500.0,
                format="%.0f",
                key=f"r_{path}",
            )
        if abs(new - base_value) > 1e-9:
            changes[path] = new
    reform = parametric_reform(changes) if changes else None

if show_cliffwatch:
    if reform:
        st.info(t("reform_active", len(changes)))
    cliffwatch.render(build_situation(hh, 0), filer_wages, reform, L)
    st.stop()

situation = build_situation(hh, filer_wages)
extra = ["pr_refundable_credits", "household_market_income", "household_tax"]
variables = [v for v, *_ in OUTPUTS] + extra
base = compute(situation, variables)
ref = compute(situation, variables, reform) if reform else None
shown = ref or base
market = base["household_market_income"]

if reform:
    st.info(t("reform_active", len(changes)))


def metric(col, label, key, help_=None, lower_is_better=False):
    delta = money(ref[key] - base[key]) if ref else None
    col.metric(
        label,
        money(shown[key]),
        delta=delta,
        help=help_,
        delta_color="inverse" if lower_is_better else "normal",
    )


c1, c2, c3, c4 = st.columns(4)
metric(c1, t("m_tax"), "pr_income_tax", lower_is_better=True)
metric(c2, t("m_credits"), "pr_refundable_credits", t("m_credits_help"))
metric(c3, t("m_net"), "household_net_income")
net_rate = (market - shown["household_net_income"]) / market if market else 0.0
c4.metric(t("m_rate"), f"{net_rate:.1%}", help=t("m_rate_help"))

left, right = st.columns([3, 2])

with left:
    st.subheader(t("range_title"))
    st.caption(t("range_caption"))
    rows = []
    for w in range(0, 150_001, 2_500):
        s = build_situation(hh, w)
        x = compute(s, RANGE_VARS)
        row = {
            t("x_axis"): w,
            t("s_tax"): x["pr_income_tax"],
            t("s_payroll"): x["employee_social_security_tax"]
            + x["employee_medicare_tax"]
            + x["self_employment_tax"],
            t("s_credits"): x["pr_refundable_credits"],
            t("s_net"): x["household_net_income"],
        }
        if reform:
            y = compute(s, RANGE_VARS, reform)
            row[t("s_net_reform")] = y["household_net_income"]
            row[t("s_change")] = (
                y["household_net_income"] - x["household_net_income"]
            )
        rows.append(row)
    df = pd.DataFrame(rows)
    xcol = t("x_axis")

    layout = dict(
        margin=dict(l=10, r=10, t=10, b=10),
        hovermode="x unified",
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        legend=dict(orientation="h", y=1.08, x=0),
        xaxis=dict(title=xcol, tickprefix="$", tickformat=",", showgrid=False),
        yaxis=dict(
            title=None,
            tickprefix="$",
            tickformat=",",
            gridcolor="rgba(128,128,128,0.18)",
            zeroline=False,
        ),
    )

    def line(fig, col, color):
        fig.add_trace(
            go.Scatter(
                x=df[xcol],
                y=df[col],
                name=col,
                mode="lines",
                line=dict(color=color, width=2),
                hovertemplate="%{y:$,.0f}<extra>" + col + "</extra>",
            )
        )

    if reform:
        fig = go.Figure()
        line(fig, t("s_change"), REFORM_COLOR)
        fig.add_hline(y=0, line=dict(color="#9a9a94", width=1))
        fig.add_vline(
            x=filer_wages, line=dict(color="#9a9a94", width=1, dash="dot")
        )
        fig.update_layout(height=300, **layout)
        st.plotly_chart(fig, use_container_width=True)
        st.caption(t("change_caption"))

    fig = go.Figure()
    if reform:
        df[t("s_net_current")] = df[t("s_net")]
        line(fig, t("s_net_current"), BASELINE_COLOR)
        df[t("s_net_ref")] = df[t("s_net_reform")]
        line(fig, t("s_net_ref"), REFORM_COLOR)
    else:
        line(fig, t("s_tax"), BASELINE_COLOR)
        line(fig, t("s_payroll"), REFORM_COLOR)
        line(fig, t("s_credits"), CREDIT_COLOR)
    fig.add_vline(
        x=filer_wages, line=dict(color="#9a9a94", width=1, dash="dot")
    )
    fig.update_layout(height=380, **layout)
    st.plotly_chart(fig, use_container_width=True)

    df[t("marginal")] = 1 - df[t("s_net")].diff() / df[xcol].diff()
    show = [
        c for c in df.columns if c not in (t("s_net_current"), t("s_net_ref"))
    ]
    with st.expander(t("table_view")):
        st.dataframe(
            df[show].style.format(
                {c: "${:,.0f}" for c in show if c != t("marginal")}
                | {t("marginal"): "{:.0%}"}
            ),
            use_container_width=True,
            hide_index=True,
            height=320,
        )

with right:
    st.subheader(t("line_by_line"))
    if reform:
        table = pd.DataFrame(
            [
                ((es, en)[L], base[v], ref[v], ref[v] - base[v])
                for v, es, en in OUTPUTS
            ],
            columns=[
                t("col_item"),
                t("col_current"),
                t("col_reform"),
                t("col_change"),
            ],
        )
        fmt = {
            t("col_current"): "${:,.0f}",
            t("col_reform"): "${:,.0f}",
            t("col_change"): "{:+,.0f}",
        }
    else:
        table = pd.DataFrame(
            [((es, en)[L], base[v]) for v, es, en in OUTPUTS],
            columns=[t("col_item"), t("col_amount")],
        )
        fmt = {t("col_amount"): "${:,.2f}"}
    st.dataframe(
        table.style.format(fmt),
        use_container_width=True,
        hide_index=True,
        height=560,
    )

st.divider()
st.markdown(t("not_modelled"))

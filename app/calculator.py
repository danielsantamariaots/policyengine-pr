"""Household calculator prototype on top of policyengine-pr.

Run with:  streamlit run app/calculator.py

Three pages share one sidebar: Inicio (choose a page), Calculadora
(line-by-line result for one household) and CliffWatch (taxes, credits and
net income as wages rise). Shared text and layout live in ui.py.
"""

import sys
from pathlib import Path

# Import policyengine_pr from this checkout, not from a package installed at
# first deploy (Streamlit Community Cloud keeps that install across pushes).
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import charts  # noqa: E402
import cliffwatch  # noqa: E402
import pandas as pd  # noqa: E402
import reforms_page
import streamlit as st
import ui

from policyengine_pr import Simulation, system
from policyengine_pr.data.hud_areas import MUNICIPIOS
from policyengine_pr.reforms.parametric import LEVERS, parametric_reform

YEAR = 2025
BASELINE_COLOR = "#2a78d6"
REFORM_COLOR = "#eb6834"
CREDIT_COLOR = "#1baf7a"
PAN_COLOR = "#c9a227"
TANF_COLOR = "#8e44ad"

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
    "pan_inputs": ("PAN: recursos y gastos", "PAN: resources and expenses"),
    "pan_resources": (
        "Recursos contables del hogar ($)",
        "Household countable resources ($)",
    ),
    "pan_resources_help": (
        "Cuentas bancarias y otros bienes contables (Reglamento 8684, Arts. 46-48). Límite de $5,000, o $15,000 si hay una persona de 60 años o más.",
        "Bank balances and other countable assets (Reglamento 8684, Arts. 46-48). Limit $5,000, or $15,000 with a member aged 60+.",
    ),
    "pan_care": (
        "Paga cuido de niños para poder trabajar",
        "Pays child care in order to work",
    ),
    "pan_care_help": (
        "Deducción de $225 al mes por niño de 2 años o menos y $200 por niño mayor (Art. 45.D).",
        "Deduction of $225 a month per child aged 2 or under and $200 per older child (Art. 45.D).",
    ),
    "pan_medical": (
        "Gastos médicos recurrentes (60+ o menores)",
        "Recurrent medical expenses (60+ or children)",
    ),
    "pan_medical_help": (
        "Deducción de $100 al mes (Art. 45.C).",
        "Deduction of $100 a month (Art. 45.C).",
    ),
    "housing": ("Vivienda (Sección 8)", "Housing (Section 8)"),
    "housing_assisted": (
        "El hogar tiene un vale de Sección 8",
        "Household holds a Section 8 voucher",
    ),
    "housing_assisted_help": (
        "Vale de elección de vivienda del Departamento de la Vivienda. El "
        "subsidio es la renta justa de mercado de San Juan menos el 30% del "
        "ingreso ajustado (24 CFR 982.505).",
        "Housing Choice Voucher from the Departamento de la Vivienda. The "
        "subsidy is the San Juan fair market rent less 30% of adjusted "
        "income (24 CFR 982.505).",
    ),
    "municipio": ("Municipio", "Municipio"),
    "municipio_help": (
        "Fija el área de HUD: límites de ingreso y renta justa de mercado (FY2025) del vale.",
        "Sets the HUD area: the voucher's income limits and fair market rent (FY2025).",
    ),
    "housing_rent": (
        "Renta mensual, con utilidades ($)",
        "Monthly rent incl. utilities ($)",
    ),
    "housing_rent_help": (
        "Tope del subsidio. Deje 0 si la renta iguala la renta justa de mercado.",
        "Caps the subsidy. Leave 0 if the rent equals the fair market rent.",
    ),
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
        "**{}** activa: {} parámetro(s) cambiado(s). Las diferencias "
        "son reforma menos ley vigente.",
        "**{}** active: {} lever(s) changed. Deltas are reform minus "
        "current law.",
    ),
    "range_title": (
        "A lo largo de la escala de ingresos",
        "Across the income range",
    ),
    "you": ("Su hogar", "Your household"),
    "section8_hint": (
        "La Sección 8 se dibuja solo si marca *El hogar tiene un vale de Sección 8* en Vivienda.",
        "Section 8 is drawn only if you tick *Household holds a Section 8 voucher* under Housing.",
    ),
    "range_caption": (
        "Mismo hogar; salarios del contribuyente de $0 a $150,000. Para "
        "precipicios y tasas marginales, vea CliffWatch.",
        "Same household; filer wages varied from $0 to $150,000. For cliffs "
        "and marginal rates, see CliffWatch.",
    ),
    "mobile_hint": (
        "En el móvil, pulse » arriba a la izquierda para describir el hogar y la reforma.",
        "On a phone, tap » at the top left to describe the household and the reform.",
    ),
    "x_axis": ("Salarios del contribuyente", "Filer wages"),
    "s_tax": ("Contribución sobre ingresos de PR", "PR income tax"),
    "s_payroll": ("Seguro Social y Medicare", "Social Security and Medicare"),
    "s_eitc": ("Crédito por Trabajo", "Crédito por Trabajo (PR EITC)"),
    "s_actc": ("Crédito federal por hijos", "Federal child credit (ACTC)"),
    "s_pan": ("PAN", "PAN"),
    "s_tanf": ("TANF", "TANF"),
    "s_section8": ("Sección 8", "Section 8"),
    "section8_off": (
        "No se calcula: marque *El hogar tiene un vale de Sección 8* en "
        "Vivienda",
        "Not computed: tick *Household holds a Section 8 voucher* under "
        "Housing",
    ),
    "section8_zero": (
        "Sin subsidio: el 30% del ingreso ajustado (${:,.0f} al mes) supera "
        "el estándar de pago de ${:,.0f} ({} dormitorios)",
        "No subsidy: 30% of adjusted income (${:,.0f} a month) exceeds the "
        "${:,.0f} payment standard ({} bedrooms)",
    ),
    "section8_on": (
        "Vale de vivienda: estándar de pago de ${:,.0f} ({} dormitorios) "
        "menos ${:,.0f} al mes de pago del inquilino (30% del ingreso "
        "ajustado), por 12",
        "Housing voucher: ${:,.0f} payment standard ({} bedrooms) less the "
        "${:,.0f} monthly tenant payment (30% of adjusted income), times 12",
    ),
    "s_net": ("Ingreso neto", "Net income"),
    "s_change": ("Cambio en ingreso neto", "Change in net income"),
    "s_net_current": ("Ingreso neto, ley vigente", "Net income, current law"),
    "change_caption": (
        "Positivo significa que el hogar sale ganando con la reforma.",
        "Positive means the household is better off under the reform.",
    ),
    "table_view": ("Ver tabla", "Table view"),
    "marginal": ("Pierde de cada $100 adicionales", "Lost per extra $100"),
    "line_by_line": ("Línea por línea", "Line by line"),
    "col_item": ("Partida", "Item"),
    "col_what": ("Qué es", "What it is"),
    "col_amount": ("Cantidad", "Amount"),
    "col_current": ("Ley vigente", "Current law"),
    "col_reform": ("Reforma", "Reform"),
    "col_change": ("Cambio", "Change"),
}

# (variable, label es, label en, gloss es, gloss en)
OUTPUTS = [
    (
        "pr_taxable_gross_income",
        "Ingreso bruto ajustado (línea 5)",
        "Adjusted gross income (line 5)",
        "Salarios, cuenta propia y pensiones tributables, antes de deducciones",
        "Taxable wages, self-employment and pensions, before deductions",
    ),
    (
        "pr_preferential_income",
        "Ingresos a tasas preferenciales (Anejo A2, línea 5)",
        "Income at preferential rates (Anejo A2, line 5)",
        "Intereses bancarios (10%), dividendos y ganancias de capital (15%); ya incluidos en la línea 5",
        "Bank interest (10%), dividends and capital gains (15%); already inside line 5",
    ),
    (
        "pr_deductions",
        "Deducciones, Anejo A (línea 6)",
        "Deductions, Anejo A (line 6)",
        "Hipoteca, gastos médicos, donativos, IRA, educación, préstamos",
        "Mortgage, medical, charity, IRA, education, student loans",
    ),
    (
        "pr_exemptions",
        "Exenciones (líneas 7 a 9)",
        "Exemptions (lines 7 to 9)",
        "$3,500 por contribuyente ($7,000 en conjunta), $2,500 por dependiente, $1,500 por veterano",
        "$3,500 per filer ($7,000 joint), $2,500 per dependent, $1,500 per veteran",
    ),
    (
        "pr_net_taxable_income",
        "Ingreso neto sujeto a contribución (línea 13)",
        "Net taxable income (line 13)",
        "Lo que queda tras deducciones y exenciones; sobre esto se aplica la tabla",
        "What is left after deductions and exemptions; the rate table applies to it",
    ),
    (
        "pr_regular_tax",
        "Contribución según tabla (línea 14)",
        "Tax per table (line 14)",
        "0% hasta $9,000; 7% hasta $25,000; 14% hasta $41,500; 25% hasta $61,500; 33% después",
        "0% to $9,000; 7% to $25,000; 14% to $41,500; 25% to $61,500; 33% above",
    ),
    (
        "pr_gradual_adjustment",
        "Ajuste gradual (línea 15)",
        "Gradual adjustment (line 15)",
        "Recargo de 5% sobre ingreso neto mayor de $500,000",
        "5% surcharge on net income above $500,000",
    ),
    (
        "pr_regular_tax_before_credits",
        "Contribución regular tras 92%/95% (línea 17)",
        "Regular tax after 92%/95% (line 17)",
        "Se paga el 92% de la tabla si el ingreso bruto no pasa de $100,000; el 95% si lo pasa. Con ingresos a tasas preferenciales, el menor entre el Anejo A2 y las tasas ordinarias",
        "92% of the table if gross income is at most $100,000; 95% above. With preferential income, the lower of Anejo A2 and the ordinary rates",
    ),
    (
        "pr_abt_excess",
        "Exceso de contribución básica alterna (línea 20)",
        "Alternate basic tax excess (line 20)",
        "Impuesto mínimo sobre ingresos distintos de salarios; cero para la mayoría",
        "Minimum tax on non-wage income; zero for most households",
    ),
    (
        "pr_income_tax",
        "Contribución sobre ingresos de PR (línea 26)",
        "PR income tax (line 26)",
        "Lo que el hogar debe a Hacienda por el año",
        "What the household owes Hacienda for the year",
    ),
    (
        "pr_eitc",
        "Crédito por Trabajo (línea 27C)",
        "Crédito por Trabajo (line 27C)",
        "Crédito reembolsable para trabajadores; sube con los salarios y luego baja hasta cero",
        "Refundable credit for workers; rises with wages, then phases out to zero",
    ),
    (
        "federal_actc",
        "Crédito federal por hijos (línea 27D)",
        "Federal child credit (line 27D)",
        "Hasta $1,700 por hijo menor de 17, limitado por el Seguro Social y Medicare pagados",
        "Up to $1,700 per child under 17, limited by Social Security and Medicare paid",
    ),
    (
        "employee_social_security_tax",
        "Seguro Social retenido",
        "Social Security tax withheld",
        "6.2% de los salarios hasta $176,100 (federal)",
        "6.2% of wages up to $176,100 (federal)",
    ),
    (
        "employee_medicare_tax",
        "Medicare retenido",
        "Medicare tax withheld",
        "1.45% de los salarios (federal)",
        "1.45% of wages (federal)",
    ),
    (
        "self_employment_tax",
        "Contribución por cuenta propia (Schedule SE)",
        "Self-employment tax (Schedule SE)",
        "15.3% sobre el 92.35% de la ganancia neta (federal)",
        "15.3% of 92.35% of net profit (federal)",
    ),
    (
        "pan",
        "PAN, beneficio anual (ADSEF)",
        "PAN, annual benefit (ADSEF)",
        "Asistencia nutricional: beneficio máximo según tamaño del hogar si el ingreso neto mensual no supera el límite",
        "Nutrition assistance: maximum benefit by household size if monthly net income is within the limit",
    ),
    (
        "tanf",
        "TANF, beneficio anual (ADSEF, categoría C)",
        "TANF, annual benefit (ADSEF, category C)",
        "Ayuda en efectivo a madres o padres solos con hijos menores: $584 al mes menos el ingreso contable",
        "Cash aid to single parents with minor children: $584 a month less countable income",
    ),
    (
        "section8",
        "Sección 8, subsidio anual (Vivienda)",
        "Section 8, annual subsidy (Vivienda)",
        "Vale de vivienda: renta justa de mercado de San Juan menos el 30% del ingreso ajustado; solo si el hogar indica que tiene vale",
        "Housing voucher: San Juan fair market rent less 30% of adjusted income; only if the household says it holds a voucher",
    ),
    (
        "vital_eligible_count",
        "Plan Vital: miembros elegibles",
        "Plan Vital: eligible members",
        "Personas del hogar con derecho a Medicaid o CHIP según el ingreso mensual (sin valor en dólares)",
        "Household members eligible for Medicaid or CHIP by monthly income (no dollar value assigned)",
    ),
    (
        "household_net_income",
        "Ingreso neto del hogar",
        "Household net income",
        "Ingresos menos contribuciones más créditos reembolsables, PAN, TANF y Sección 8",
        "Income minus taxes plus refundable credits, PAN, TANF and Section 8",
    ),
]
RANGE_VARS = [
    "pr_income_tax",
    "employee_social_security_tax",
    "employee_medicare_tax",
    "self_employment_tax",
    "pr_eitc",
    "federal_actc",
    "pan",
    "tanf",
    "section8",
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
    (
        "interest_income",
        "Intereses de depósitos bancarios en PR ($)",
        "Interest on PR bank deposits ($)",
        500,
        "Anejo FF; primeros $100 ($200 conjunta) exentos; 10% o tasas ordinarias",
        "Anejo FF; first $100 ($200 joint) exempt; 10% or ordinary rates",
    ),
    (
        "dividend_income",
        "Dividendos de corporaciones de PR ($)",
        "Dividends from PR corporations ($)",
        500,
        "Anejo FF, Parte II; 15% (Sección 1023.06)",
        "Anejo FF, Part II; 15% (Sección 1023.06)",
    ),
    (
        "long_term_capital_gains",
        "Ganancia neta de capital a largo plazo ($)",
        "Net long-term capital gain ($)",
        1_000,
        "Anejo D; 15% o tasas ordinarias si resultan menores (Sección 1023.02)",
        "Anejo D; 15% or ordinary rates if lower (Sección 1023.02)",
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
        "households": {
            "household": {
                "members": members,
                "housing_assisted": {YEAR: hh["housing_assisted"]},
                "housing_rent": {YEAR: hh["housing_rent"]},
                "hud_area": {YEAR: MUNICIPIOS[hh["municipio"]][1]},
                "pan_resources": {YEAR: hh["pan_resources"]},
                "pan_pays_dependent_care": {
                    YEAR: hh["pan_pays_dependent_care"]
                },
                "pan_recurrent_medical_expenses": {
                    YEAR: hh["pan_recurrent_medical_expenses"]
                },
            }
        },
    }


def compute(situation, variables, reform=None):
    sim = Simulation(situation=situation, reform=reform)
    return {v: float(sim.calculate(v, YEAR)[0]) for v in variables}


money = ui.money

# ---------------------------------------------------------------------------
# Sidebar: language, page, household, reform
# ---------------------------------------------------------------------------
st.set_page_config(page_title="Modelo contributivo PR", layout="wide")
charts.inject_css()

CURRENT = {path: current_value(path) for path, _, _ in LEVERS}
ui.init_state(CURRENT)

with st.sidebar:
    lang = st.radio(
        TEXT["language"][0],
        ["Español", "English"],
        horizontal=True,
        label_visibility="collapsed",
        key="lang",
    )
L = 0 if lang == "Español" else 1
st.session_state["L"] = L


def t(key, *args):
    s = TEXT[key][L]
    return s.format(*args) if args else s


VIEWS = {
    "home": "nav_home",
    "calc": "nav_calc",
    "cliff": "nav_cliff",
    "reform": "nav_reform",
}
with st.sidebar:
    view = st.radio(
        ui.t("nav", L),
        list(VIEWS),
        format_func=lambda v: ui.t(VIEWS[v], L),
        horizontal=True,
        label_visibility="collapsed",
        key="view",
    )


def person_inputs(prefix_key):
    with st.expander(t("other_income", t(prefix_key))):
        return {
            var: st.number_input(
                (es, en)[L],
                0,
                5_000_000,
                step=step,
                help=(hes, hen)[L],
                key=f"{prefix_key}_{var}",
            )
            for var, es, en, step, hes, hen in PERSON_INPUTS
        }


hh = {}
with st.sidebar:
    st.header(t("household"))
    st.selectbox(
        ui.t("preset", L),
        [p[0] for p in ui.PRESETS],
        format_func=lambda k: next(p[1 + L] for p in ui.PRESETS if p[0] == k),
        key="preset",
        on_change=ui.apply_preset,
        help=ui.t("preset_help", L),
    )
    hh["joint"] = st.toggle(t("joint"), key="joint")
    hh["filer_age"] = st.number_input(t("filer_age"), 16, 100, key="filer_age")
    filer_wages = st.number_input(
        t("filer_wages"), 0, 2_000_000, step=1_000, key="filer_wages"
    )
    hh["filer_veteran"] = st.checkbox(t("filer_veteran"), key="filer_veteran")
    hh["filer"] = person_inputs("filer")
    hh["spouse_age"], hh["spouse_wages"] = 35, 0
    hh["spouse_veteran"], hh["spouse"] = False, {}
    if hh["joint"]:
        hh["spouse_age"] = st.number_input(
            t("spouse_age"), 16, 100, key="spouse_age"
        )
        hh["spouse_wages"] = st.number_input(
            t("spouse_wages"), 0, 2_000_000, step=1_000, key="spouse_wages"
        )
        hh["spouse_veteran"] = st.checkbox(
            t("spouse_veteran"), key="spouse_veteran"
        )
        hh["spouse"] = person_inputs("spouse")
    n_children = st.number_input(t("children"), 0, 8, key="n_children")
    hh["child_ages"] = [
        st.number_input(t("child_age", i + 1), 0, 25, key=f"c{i}")
        for i in range(n_children)
    ]
    with st.expander(t("deductions")):
        hh["deductions"] = {
            var: st.number_input(
                (es, en)[L],
                0,
                1_000_000,
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
            step=500,
            help=t("other_deductions_help"),
            key="other_deductions",
        )
    with st.expander(t("pan_inputs")):
        hh["pan_resources"] = st.number_input(
            t("pan_resources"),
            0,
            1_000_000,
            step=500,
            key="pan_resources",
            help=t("pan_resources_help"),
        )
        hh["pan_pays_dependent_care"] = st.checkbox(
            t("pan_care"),
            key="pan_pays_dependent_care",
            help=t("pan_care_help"),
        )
        hh["pan_recurrent_medical_expenses"] = st.checkbox(
            t("pan_medical"),
            key="pan_recurrent_medical_expenses",
            help=t("pan_medical_help"),
        )
    with st.expander(t("housing")):
        hh["housing_assisted"] = st.checkbox(
            t("housing_assisted"),
            key="housing_assisted",
            help=t("housing_assisted_help"),
        )
        hh["municipio"] = st.selectbox(
            t("municipio"),
            list(MUNICIPIOS),
            key="municipio",
            help=t("municipio_help"),
        )
        hh["housing_rent"] = st.number_input(
            t("housing_rent"),
            0,
            10_000,
            step=50,
            key="housing_rent",
            help=t("housing_rent_help"),
        )
    with st.expander(t("advanced")):
        hh["abt_other_income"] = st.number_input(
            t("abt_other"),
            0,
            5_000_000,
            step=1_000,
            help=t("abt_other_help"),
            key="abt_other_income",
        )

    st.header(t("reform"))
    st.selectbox(
        ui.t("example_reform", L),
        [r[0] for r in ui.EXAMPLE_REFORMS],
        format_func=lambda k: next(
            r[1 + L] for r in ui.EXAMPLE_REFORMS if r[0] == k
        ),
        key="example_reform",
        on_change=ui.apply_example_reform,
        args=(CURRENT,),
        help=ui.t("example_reform_help", L),
    )
    st.text_input(
        ui.t("reform_name", L),
        key="reform_name",
        placeholder=ui.t("reform_default_name", L),
    )
    st.caption(t("reform_caption"))
    changes = {}
    for path, label_en, kind in LEVERS:
        label = LEVER_LABELS_ES.get(label_en, label_en) if L == 0 else label_en
        base_value = CURRENT[path]
        if kind == "rate":
            new = st.number_input(
                label, 0.0, 1.0, step=0.01, format="%.4f", key=f"r_{path}"
            )
        else:
            new = st.number_input(
                label,
                0.0,
                5_000_000.0,
                step=500.0,
                format="%.0f",
                key=f"r_{path}",
            )
        if abs(new - base_value) > 1e-9:
            changes[path] = new
    reform = parametric_reform(changes) if changes else None
    reform_name = st.session_state["reform_name"] or ui.t(
        "reform_default_name", L
    )
    ui.sync_query_params(CURRENT)
    with st.expander(ui.t("share_title", L)):
        st.caption(ui.t("share_help", L))
        link = ui.share_link()
        if link:
            st.code(link, language=None, wrap_lines=True)

# ---------------------------------------------------------------------------
# Pages
# ---------------------------------------------------------------------------
if view == "home":
    ui.home(L)
    st.stop()

if view == "reform":
    reforms_page.render(L, ui.EXAMPLE_REFORMS, CURRENT, changes, reform_name)
    ui.not_included(L)
    ui.tutorial(L)
    st.stop()

situation = build_situation(hh, filer_wages)
extra = [
    "pr_refundable_credits",
    "household_market_income",
    "household_tax",
    "section8_total_tenant_payment",
    "section8_payment_standard",
    "section8_bedrooms",
]
variables = [v for v, *_ in OUTPUTS] + extra
base = compute(situation, variables)
ref = compute(situation, variables, reform) if reform else None
shown = ref or base

if view == "cliff":
    compare = []
    if hh["joint"]:
        a, b = ui.unmarried_split(hh)
        compare.append(
            (
                "unmarried",
                cliffwatch.TEXT["compare_unmarried"][L],
                [
                    (build_situation(a, 0), None),
                    (build_situation(b, 0), hh["spouse_wages"]),
                ],
            )
        )
    for key, es, en, _ in ui.PRESETS:
        if key != "custom":
            p_hh, p_wages = ui.preset_hh(key)
            compare.append(
                (key, (es, en)[L], [(build_situation(p_hh, 0), None)])
            )
    cliffwatch.render(
        build_situation(hh, 0),
        filer_wages,
        reform,
        L,
        summary=ui.household_summary(hh, filer_wages, L),
        reform_name=reform_name,
        metric_row=lambda: ui.metric_row(base, ref, L),
        reform_notice=t("reform_active", reform_name, len(changes))
        if reform
        else None,
        compare=compare,
    )
    ui.not_included(L)
    ui.assumptions(CURRENT, changes, L, LEVER_LABELS_ES)
    ui.tutorial(L)
    st.stop()

st.title(t("title"))
charts.mobile_hint(t("mobile_hint"))
st.caption(t("caption"))
st.markdown(f"**{ui.household_summary(hh, filer_wages, L)}**")
if reform:
    st.info(t("reform_active", reform_name, len(changes)))

ui.metric_row(base, ref, L)

# chart full width, line-by-line table underneath
left, right = st.container(), st.container()

with left:
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
            t("s_eitc"): x["pr_eitc"],
            t("s_actc"): x["federal_actc"],
            t("s_pan"): x["pan"],
            t("s_tanf"): x["tanf"],
            **(
                {t("s_section8"): x["section8"]}
                if hh["housing_assisted"]
                else {}
            ),
            t("s_net"): x["household_net_income"],
        }
        if reform:
            y = compute(s, RANGE_VARS, reform)
            row[reform_name] = y["household_net_income"]
            row[t("s_change")] = (
                y["household_net_income"] - x["household_net_income"]
            )
        rows.append(row)
    df = pd.DataFrame(rows)
    xcol = t("x_axis")

    if reform:
        fig = charts.figure(
            t("s_change"),
            t("change_caption"),
            x_title=xcol,
            y_money=True,
            height=320,
        )
        charts.line(
            fig,
            df[xcol],
            df[t("s_change")],
            t("s_change"),
            charts.SERIES["reform"],
        )
        charts.hline(fig, 0, color=charts.ZERO)
        charts.vline(
            fig, filer_wages, color=charts.MUTED, dash="dot", label=t("you")
        )
        fig.update_layout(showlegend=False)
        fig.update_xaxes(tickprefix="$", tickformat=",")
        st.plotly_chart(fig, use_container_width=True, config=charts.CONFIG)

    fig = charts.figure(
        t("range_title"),
        t("range_caption"),
        x_title=xcol,
        y_money=True,
        height=460,
    )
    if reform:
        charts.line(
            fig,
            df[xcol],
            df[t("s_net")],
            t("s_net_current"),
            charts.SERIES["baseline"],
        )
        charts.line(
            fig,
            df[xcol],
            df[reform_name],
            reform_name,
            charts.SERIES["reform"],
        )
    else:
        for col, key in (
            ("s_tax", "tax"),
            ("s_payroll", "payroll"),
            ("s_eitc", "eitc"),
            ("s_actc", "actc"),
            ("s_pan", "pan"),
            ("s_tanf", "tanf"),
            ("s_section8", "section8"),
        ):
            if t(col) in df:
                charts.line(
                    fig, df[xcol], df[t(col)], t(col), charts.SERIES[key]
                )
    charts.vline(
        fig, filer_wages, color=charts.MUTED, dash="dot", label=t("you")
    )
    st.plotly_chart(fig, use_container_width=True, config=charts.CONFIG)
    if not reform and not hh["housing_assisted"]:
        st.caption(t("section8_hint"))

    df[t("marginal")] = (1 - df[t("s_net")].diff() / df[xcol].diff()) * 100
    with st.expander(t("table_view")):
        st.dataframe(
            df.style.format(
                {c: "${:,.0f}" for c in df.columns if c != t("marginal")}
                | {t("marginal"): "${:,.0f}"}
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
                ((es, en)[L], base[v], ref[v], ref[v] - base[v], (ges, gen)[L])
                for v, es, en, ges, gen in OUTPUTS
            ],
            columns=[
                t("col_item"),
                t("col_current"),
                t("col_reform"),
                t("col_change"),
                t("col_what"),
            ],
        )
        fmt = {
            t("col_current"): "${:,.0f}",
            t("col_reform"): "${:,.0f}",
            t("col_change"): "{:+,.0f}",
        }
    else:
        table = pd.DataFrame(
            [
                ((es, en)[L], base[v], (ges, gen)[L])
                for v, es, en, ges, gen in OUTPUTS
            ],
            columns=[t("col_item"), t("col_amount"), t("col_what")],
        )
        fmt = {t("col_amount"): "${:,.2f}"}
        table.loc[
            table[t("col_item")].str.startswith("Plan Vital"), t("col_amount")
        ] = base["vital_eligible_count"]
    s8 = table[t("col_item")].str.startswith(("Sección 8", "Section 8"))
    if not hh["housing_assisted"]:
        table.loc[s8, t("col_what")] = t("section8_off")
    elif shown["section8"] <= 0:
        table.loc[s8, t("col_what")] = t(
            "section8_zero",
            shown["section8_total_tenant_payment"],
            shown["section8_payment_standard"],
            int(shown["section8_bedrooms"]),
        )
    else:
        table.loc[s8, t("col_what")] = t(
            "section8_on",
            shown["section8_payment_standard"],
            int(shown["section8_bedrooms"]),
            shown["section8_total_tenant_payment"],
        )
    st.dataframe(
        table.style.format(fmt),
        use_container_width=True,
        hide_index=True,
        height=600,
        column_config={
            t("col_item"): st.column_config.TextColumn(width="medium"),
            t("col_what"): st.column_config.TextColumn(width="large"),
        },
    )

st.divider()
ui.not_included(L)
ui.assumptions(CURRENT, changes, L, LEVER_LABELS_ES)
ui.tutorial(L)

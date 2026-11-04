"""Build the CPA validation workbook: test households with every line the
model produces, and blank columns for a preparer to enter the figures from
a real return or from Hacienda's software.

    python -m policyengine_pr.analysis.validation_workbook docs/validacion/casos_validacion_2025.xlsx
"""

import sys
from pathlib import Path

from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill
from openpyxl.utils import get_column_letter

from policyengine_pr import Simulation

YEAR = 2025

# (variable, label, Formulario 482 line)
LINES = [
    ("pr_taxable_gross_income", "Ingreso bruto ajustado", "5"),
    (
        "pr_preferential_income",
        "Ingresos a tasas preferenciales (Anejo A2)",
        "A2-5",
    ),
    ("pr_deductions", "Total de deducciones (Anejo A)", "6"),
    ("pr_exemptions", "Exenciones personal, dependientes, veterano", "7-9"),
    ("pr_net_taxable_income", "Ingreso neto sujeto a contribución", "13"),
    ("pr_regular_tax", "Contribución según tabla", "14"),
    ("pr_gradual_adjustment", "Ajuste gradual", "15"),
    (
        "pr_regular_tax_before_credits",
        "Contribución regular (tras 92%/95% o Anejo A2)",
        "17",
    ),
    ("pr_abt_excess", "Exceso de contribución básica alterna", "20"),
    ("pr_income_tax", "Contribución sobre ingresos de PR", "26"),
    ("pr_eitc", "Crédito por Trabajo", "27C"),
    ("federal_actc", "Crédito federal por hijos (ACTC, 1040-SS)", "27D"),
    (
        "employee_social_security_tax",
        "Seguro Social retenido (empleado)",
        "W-2",
    ),
    ("employee_medicare_tax", "Medicare retenido (empleado)", "W-2"),
    (
        "self_employment_tax",
        "Contribución por cuenta propia (Schedule SE)",
        "1040-SS",
    ),
    ("pan", "PAN anual (ADSEF)", "—"),
    ("tanf", "TANF anual (ADSEF)", "—"),
    ("household_net_income", "Ingreso neto del hogar", "—"),
]

# Test households: id, description, people (dict), filing status, extras
CASES = [
    (
        "C01",
        "Soltero, salarios $21,840 (salario mínimo)",
        {"p": dict(age=30, employment_income=21_840)},
        "SINGLE",
        {},
    ),
    (
        "C02",
        "Soltera, 2 hijos (4 y 8), salarios $30,000",
        {
            "p": dict(age=32, employment_income=30_000),
            "c1": dict(age=4),
            "c2": dict(age=8),
        },
        "SINGLE",
        {},
    ),
    (
        "C03",
        "Casados conjunta, 2 hijos, salarios $45,000 + $25,000",
        {
            "p": dict(age=38, employment_income=45_000),
            "s": dict(age=36, employment_income=25_000),
            "c1": dict(age=6),
            "c2": dict(age=10),
        },
        "JOINT",
        {},
    ),
    (
        "C04",
        "Pensionado 65, pensión $24,000, Seguro Social $14,000",
        {"p": dict(age=65, pension_income=24_000, social_security=14_000)},
        "SINGLE",
        {},
    ),
    (
        "C05",
        "Joven 22, salarios $30,000 (Ley 135)",
        {"p": dict(age=22, employment_income=30_000)},
        "SINGLE",
        {},
    ),
    (
        "C06",
        "Cuenta propia $60,000, 1 hijo (12)",
        {"p": dict(age=45, self_employment_income=60_000), "c1": dict(age=12)},
        "SINGLE",
        {},
    ),
    (
        "C07",
        "Soltero, salarios $95,000 (≤ $100k, factor 92%)",
        {"p": dict(age=40, employment_income=95_000)},
        "SINGLE",
        {},
    ),
    (
        "C08",
        "Soltero, salarios $105,000 (> $100k, factor 95%)",
        {"p": dict(age=40, employment_income=105_000)},
        "SINGLE",
        {},
    ),
    (
        "C09",
        "Soltero, salarios $50,000 + ganancia de capital $10,000",
        {
            "p": dict(
                age=40,
                employment_income=50_000,
                long_term_capital_gains=10_000,
            )
        },
        "SINGLE",
        {},
    ),
    (
        "C10",
        "Soltero, salarios $40,000 + dividendos $30,000, hipoteca $10,000",
        {
            "p": dict(
                age=40,
                employment_income=40_000,
                dividend_income=30_000,
                mortgage_interest=10_000,
            )
        },
        "SINGLE",
        {},
    ),
    (
        "C11",
        "Casados conjunta, salarios $600,000 (ajuste gradual)",
        {"p": dict(age=50, employment_income=600_000), "s": dict(age=50)},
        "JOINT",
        {},
    ),
    (
        "C12",
        "Veterano soltero, salarios $35,000, IRA $7,000, médicos $5,000",
        {
            "p": dict(
                age=45,
                employment_income=35_000,
                is_veteran=True,
                ira_contributions=7_000,
                medical_expenses=5_000,
            )
        },
        "SINGLE",
        {},
    ),
    (
        "C13",
        "Soltera, 1 hijo (3), salarios $7,200 (TANF)",
        {"p": dict(age=28, employment_income=7_200), "c1": dict(age=3)},
        "SINGLE",
        {},
    ),
    (
        "C14",
        "Casados conjunta, 3 hijos, salarios $44,000 (límite CT)",
        {
            "p": dict(age=35, employment_income=44_000),
            "s": dict(age=34),
            "c1": dict(age=2),
            "c2": dict(age=5),
            "c3": dict(age=9),
        },
        "JOINT",
        {},
    ),
]

INPUT_FIELDS = [
    "age",
    "employment_income",
    "self_employment_income",
    "pension_income",
    "social_security",
    "interest_income",
    "dividend_income",
    "long_term_capital_gains",
    "mortgage_interest",
    "medical_expenses",
    "charitable_contributions",
    "ira_contributions",
    "is_veteran",
]


def situation(people, status):
    sit_people = {}
    for name, attrs in people.items():
        person = {k: {YEAR: v} for k, v in attrs.items()}
        if name.startswith("c"):
            person["is_tax_unit_dependent"] = {YEAR: True}
        sit_people[name] = person
    members = list(sit_people)
    return {
        "people": sit_people,
        "tax_units": {
            "t": {"members": members, "pr_filing_status": {YEAR: status}}
        },
        "households": {"h": {"members": members}},
    }


def build(out: Path):
    wb = Workbook()
    ws = wb.active
    ws.title = "Léame"
    for i, line in enumerate(
        [
            "Casos de validación · policyengine-pr · año contributivo 2025",
            "",
            "Propósito: que un(a) preparador(a) compute cada caso con el Formulario 482 de 2025 (o con el programa de",
            "Hacienda) y anote sus cifras en las columnas 'CPA'. Las columnas 'Modelo' son la salida de policyengine-pr.",
            "La columna 'Diferencia' se calcula sola. Cualquier diferencia distinta de cero merece una nota.",
            "",
            "Supuestos comunes: residentes de Puerto Rico todo el año; ingresos del año; salarios de W-2PR sin",
            "retención considerada; dependientes cualificados hijos del contribuyente; sin otras deducciones ni créditos.",
            "PAN y TANF son beneficios de ADSEF (no líneas de la planilla) y pueden ignorarse en la validación contributiva.",
            "",
            "Hoja 'Entradas': los datos de cada caso. Hoja 'Resultados': una fila por línea y caso.",
        ],
        1,
    ):
        ws.cell(row=i, column=1, value=line)
    ws["A1"].font = Font(bold=True, size=13)
    ws.column_dimensions["A"].width = 120

    head = Font(bold=True)
    fill = PatternFill("solid", fgColor="DDEBF7")
    cpa = PatternFill("solid", fgColor="FFF2CC")
    inp = wb.create_sheet("Entradas")
    cols = ["Caso", "Descripción", "Estado personal", "Persona"] + INPUT_FIELDS
    for j, c in enumerate(cols, 1):
        cell = inp.cell(row=1, column=j, value=c)
        cell.font, cell.fill = head, fill
    r = 2
    results = {}
    for cid, desc, people, status, _ in CASES:
        for name, attrs in people.items():
            row = [cid, desc, status, name] + [
                attrs.get(f, "") for f in INPUT_FIELDS
            ]
            for j, v in enumerate(row, 1):
                inp.cell(row=r, column=j, value=v)
            r += 1
        sim = Simulation(situation=situation(people, status))
        results[cid] = {v: float(sim.calculate(v, YEAR)[0]) for v, *_ in LINES}
    for j in range(1, len(cols) + 1):
        inp.column_dimensions[get_column_letter(j)].width = 16
    inp.column_dimensions["B"].width = 48

    res = wb.create_sheet("Resultados")
    cols = [
        "Caso",
        "Descripción",
        "Línea 482",
        "Partida",
        "Modelo",
        "CPA",
        "Diferencia",
        "Nota",
    ]
    for j, c in enumerate(cols, 1):
        cell = res.cell(row=1, column=j, value=c)
        cell.font, cell.fill = head, fill
    r = 2
    for cid, desc, *_ in CASES:
        for v, label, line in LINES:
            res.cell(row=r, column=1, value=cid)
            res.cell(row=r, column=2, value=desc)
            res.cell(row=r, column=3, value=line)
            res.cell(row=r, column=4, value=label)
            res.cell(
                row=r, column=5, value=round(results[cid][v], 2)
            ).number_format = "#,##0.00"
            res.cell(row=r, column=6).fill = cpa
            res.cell(row=r, column=6).number_format = "#,##0.00"
            res.cell(
                row=r, column=7, value=f'=IF(F{r}="","",F{r}-E{r})'
            ).number_format = "#,##0.00"
            res.cell(row=r, column=8).fill = cpa
            r += 1
        r += 1
    for j, w in zip(range(1, 9), (8, 48, 10, 46, 14, 14, 14, 40)):
        res.column_dimensions[get_column_letter(j)].width = w
    res.freeze_panes = "A2"
    out.parent.mkdir(parents=True, exist_ok=True)
    wb.save(out)
    return out


if __name__ == "__main__":
    print(
        build(
            Path(
                sys.argv[1]
                if len(sys.argv) > 1
                else "docs/validacion/casos_validacion_2025.xlsx"
            )
        )
    )

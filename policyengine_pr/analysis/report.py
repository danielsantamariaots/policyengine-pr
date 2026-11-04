"""Two-page reform report (Markdown; .docx via docs/hacienda/fuentes_documentos/md2docx.js).

    from policyengine_pr.analysis.report import write_report
    write_report({"gov.hacienda.income.rates[1].threshold": 12_000.0},
                 "Ampliar el tramo de 0% a $12,000", Path("docs/informes/ejemplo.md"))

Sections: headline numbers, totals table, change by decile, three example
households, assumptions and sources. Figures come from scoring.score; the
household examples from single-household simulations.
"""

from datetime import date
from pathlib import Path

from policyengine_pr import Simulation
from policyengine_pr.analysis.scoring import score
from policyengine_pr.reforms.parametric import (
    LEVER_LABELS_ES,
    LEVERS,
    parametric_reform,
)

YEAR = 2025
HOUSEHOLDS = [
    (
        "Trabajador soltero, salario mínimo ($21,840)",
        {"p": dict(age=30, employment_income=21_840)},
        "SINGLE",
    ),
    (
        "Madre con dos hijos, $30,000",
        {
            "p": dict(age=32, employment_income=30_000),
            "c1": dict(age=4),
            "c2": dict(age=8),
        },
        "SINGLE",
    ),
    (
        "Pareja con dos hijos, $45,000 + $25,000",
        {
            "p": dict(age=38, employment_income=45_000),
            "s": dict(age=36, employment_income=25_000),
            "c1": dict(age=6),
            "c2": dict(age=10),
        },
        "JOINT",
    ),
    (
        "Soltero, $95,000",
        {"p": dict(age=40, employment_income=95_000)},
        "SINGLE",
    ),
]
LABELS = {path: LEVER_LABELS_ES.get(label, label) for path, label, _ in LEVERS}


def _situation(people, status):
    sp = {}
    for name, attrs in people.items():
        person = {k: {YEAR: v} for k, v in attrs.items()}
        if name.startswith("c"):
            person["is_tax_unit_dependent"] = {YEAR: True}
        sp[name] = person
    members = list(sp)
    return {
        "people": sp,
        "tax_units": {
            "t": {"members": members, "pr_filing_status": {YEAR: status}}
        },
        "households": {"h": {"members": members}},
    }


def m(x):
    return f"${x / 1e6:,.0f} M"


def write_report(
    changes: dict, name: str, out: Path, eti: float = 0.0
) -> Path:
    reform = parametric_reform(changes)
    r = score(reform, eti=eti)
    s, tot, dec = r["summary"], r["totals"], r["deciles"]
    cost = s["revenue_change"]
    lines = [
        f"# {name}",
        "",
        f"*Estimación de policyengine-pr · Espacios Abiertos · {date.today():%d/%m/%Y} · año contributivo {YEAR}*",
        "",
        "## En una línea",
        "",
        f"La reforma {'cuesta' if cost > 0 else 'aporta'} a Hacienda **{m(abs(cost))} al año** "
        f"(contribución sobre ingresos {m(s['income_tax_change'])}, Crédito por Trabajo {m(s['eitc_change'])}); "
        f"**{s['share_better_off']:.0%}** de los hogares salen ganando y **{s['share_worse_off']:.0%}** perdiendo; "
        f"el cambio medio es de **${s['net_income_change'] / s['households']:,.0f}** por hogar al año.",
        "",
        "## Qué cambia",
        "",
        "| Parámetro | Valor |",
        "|---|---|",
    ]
    for path, value in changes.items():
        lines.append(f"| {LABELS.get(path, path)} | {value:,.4g} |")
    lines += [
        "",
        "## Totales (millones de dólares al año)",
        "",
        "| Partida | Ley vigente | Reforma | Cambio |",
        "|---|---|---|---|",
    ]
    for _, row in tot.iterrows():
        lines.append(
            f"| {row['label_es']} | {row['baseline'] / 1e6:,.0f} | {row['reform'] / 1e6:,.0f} | {row['change'] / 1e6:+,.0f} |"
        )
    lines += [
        "",
        "## Por decil de ingreso neto del hogar",
        "",
        "| Decil | Ingreso neto medio | Cambio medio | Ganan | Pierden |",
        "|---|---|---|---|---|",
    ]
    for _, row in dec.iterrows():
        lines.append(
            f"| {int(row['decile'])} | ${row['mean_net_income']:,.0f} | ${row['mean_change']:+,.0f} | {row['share_better_off']:.0%} | {row['share_worse_off']:.0%} |"
        )
    lines += [
        "",
        "## Hogares de ejemplo",
        "",
        "| Hogar | Contribución (vigente → reforma) | Créditos y beneficios | Ingreso neto (cambio) |",
        "|---|---|---|---|",
    ]
    vars_ = [
        "pr_income_tax",
        "pr_refundable_credits",
        "household_benefits",
        "household_net_income",
    ]
    for label, people, status in HOUSEHOLDS:
        sit = _situation(people, status)
        b = {
            v: float(Simulation(situation=sit).calculate(v, YEAR)[0])
            for v in vars_
        }
        f = {
            v: float(
                Simulation(situation=sit, reform=reform).calculate(v, YEAR)[0]
            )
            for v in vars_
        }
        lines.append(
            f"| {label} | ${b['pr_income_tax']:,.0f} → ${f['pr_income_tax']:,.0f} | "
            f"${b['pr_refundable_credits'] + b['household_benefits']:,.0f} → ${f['pr_refundable_credits'] + f['household_benefits']:,.0f} | "
            f"${f['household_net_income']:,.0f} ({f['household_net_income'] - b['household_net_income']:+,.0f}) |"
        )
    lines += [
        "",
        "## Supuestos y fuentes",
        "",
        "- Reglas del año contributivo 2025 codificadas desde los formularios e instrucciones de Hacienda, el IRS, ADSEF y CMS; cada parámetro cita su fuente (repositorio policyengine-pr).",
        "- Microdatos: Encuesta sobre la Comunidad de Puerto Rico 2023 (PUMS), 1.28 millones de hogares ponderados, con pesos calibrados a los totales oficiales de recaudo (Hacienda, AF2023-24), Crédito por Trabajo (año contributivo 2023) y PAN (USDA FNS, AF2024).",
        "- Unidades contributivas construidas desde la composición del hogar; ingresos de 2023 ajustados a 2025 por el salario medio anual de Puerto Rico (BLS QCEW, ×1.0815). La contribución sobre ingresos se muestra antes del Crédito por Trabajo; el recaudo neto calibrado es la diferencia entre ambas filas.",
        f"- Respuesta de comportamiento: {'ninguna (modelo estático)' if eti == 0 else f'elasticidad del ingreso tributable de {eti} aplicada al cambio en la tasa marginal neta de los salarios'}.",
        "- PAN con el beneficio máximo para todo hogar elegible (ADSEF no publica la tabla de reducción); TANF con el máximo de una familia de tres para todo tamaño.",
        "- Los niveles están calibrados a totales agregados; los cambios son la cifra principal. Estimaciones, no asesoría profesional.",
    ]
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(lines) + "\n")
    return out


def write_report_from_file(reform_file, out: Path, eti: float = 0.0) -> Path:
    """Report for a reforms/*.yaml file; the file's name becomes the title."""
    from policyengine_pr.reforms.files import load_reform

    meta, changes = load_reform(reform_file)
    return write_report(changes, meta["name"], out, eti=eti)


if __name__ == "__main__":
    import sys

    reform_file, out = sys.argv[1], Path(sys.argv[2])
    eti = float(sys.argv[3]) if len(sys.argv) > 3 else 0.0
    print(write_report_from_file(reform_file, out, eti))

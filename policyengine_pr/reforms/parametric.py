"""Parametric reforms: change parameter values without touching formulas.

A reform is a mapping from a parameter path (dotted, with ``brackets[i]``
for scale brackets) to its new value. Only values can change; a reform
that needs new formulas belongs in its own module.

Example::

    reform = parametric_reform({
        "gov.hacienda.income.rates[1].threshold": 12_000,
        "gov.hacienda.income.exemptions.personal.SINGLE": 5_000,
    })
    Simulation(situation=..., reform=reform)
"""

from policyengine_core.reforms import Reform, set_parameter


def parametric_reform(changes: dict, start: str = "2025-01-01") -> type:
    """Build a Reform class applying every change from ``start`` onward."""
    modifiers = [
        set_parameter(path, value, start=start, return_modifier=True)
        for path, value in changes.items()
    ]

    class reform(Reform):
        name = "Parametric reform"

        def apply(self):
            for modifier in modifiers:
                self.modify_parameters(modifier)

    return reform


# Levers a tax reform proposal is likely to move, with labels for the app.
# (path, label, kind) where kind is "dollars" or "rate".
LEVERS = [
    (
        "gov.hacienda.income.rates[1].threshold",
        "Bracket 2 starts (7%)",
        "dollars",
    ),
    ("gov.hacienda.income.rates[1].rate", "Bracket 2 rate", "rate"),
    (
        "gov.hacienda.income.rates[2].threshold",
        "Bracket 3 starts (14%)",
        "dollars",
    ),
    ("gov.hacienda.income.rates[2].rate", "Bracket 3 rate", "rate"),
    (
        "gov.hacienda.income.rates[3].threshold",
        "Bracket 4 starts (25%)",
        "dollars",
    ),
    ("gov.hacienda.income.rates[3].rate", "Bracket 4 rate", "rate"),
    (
        "gov.hacienda.income.rates[4].threshold",
        "Top bracket starts (33%)",
        "dollars",
    ),
    ("gov.hacienda.income.rates[4].rate", "Top bracket rate", "rate"),
    (
        "gov.hacienda.income.exemptions.personal.SINGLE",
        "Personal exemption, single",
        "dollars",
    ),
    (
        "gov.hacienda.income.exemptions.personal.JOINT",
        "Personal exemption, joint",
        "dollars",
    ),
    (
        "gov.hacienda.income.exemptions.dependent",
        "Exemption per dependent",
        "dollars",
    ),
    (
        "gov.hacienda.income.tax_determination.rate.reduced",
        "Tax factor, gross income ≤ threshold",
        "rate",
    ),
    (
        "gov.hacienda.income.tax_determination.rate.standard",
        "Tax factor, above threshold",
        "rate",
    ),
    (
        "gov.hacienda.income.tax_determination.rate.gross_income_threshold",
        "Tax factor income threshold",
        "dollars",
    ),
    (
        "gov.hacienda.credits.eitc.max.0",
        "EITC maximum, no children",
        "dollars",
    ),
    ("gov.hacienda.credits.eitc.max.1", "EITC maximum, 1 child", "dollars"),
    ("gov.hacienda.credits.eitc.max.2", "EITC maximum, 2 children", "dollars"),
    (
        "gov.hacienda.credits.eitc.max.3",
        "EITC maximum, 3+ children",
        "dollars",
    ),
    (
        "gov.hacienda.credits.eitc.phase_out_start.2.SINGLE",
        "EITC phase-out start, 2 children, single",
        "dollars",
    ),
    (
        "gov.hacienda.credits.eitc.phase_out_start.2.JOINT",
        "EITC phase-out start, 2 children, joint",
        "dollars",
    ),
    (
        "gov.hacienda.credits.eitc.earned_income_limit.2.SINGLE",
        "EITC income limit, 2 children, single",
        "dollars",
    ),
    (
        "gov.hacienda.credits.eitc.earned_income_limit.2.JOINT",
        "EITC income limit, 2 children, joint",
        "dollars",
    ),
    (
        "gov.hacienda.income.exempt.youth.amount",
        "Youth exemption (Ley 135)",
        "dollars",
    ),
    (
        "gov.hacienda.income.exempt.youth.max_age",
        "Youth exemption maximum age",
        "dollars",
    ),
]

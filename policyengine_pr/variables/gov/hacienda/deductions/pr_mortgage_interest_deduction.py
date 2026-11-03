from policyengine_pr.model_api import *


class pr_mortgage_interest_deduction(Variable):
    value_type = float
    entity = TaxUnit
    label = "PR home mortgage interest deduction"
    documentation = (
        "Anejo A, Parte I, línea 1i: the lesser of interest paid, 30% of "
        "adjusted gross income plus exempt income, and $35,000. The "
        "three-prior-year alternative test is not modelled."
    )
    unit = USD
    definition_period = YEAR

    def formula(tax_unit, period, parameters):
        p = parameters(period).gov.hacienda.deductions.mortgage_interest
        interest = add(tax_unit, period, ["mortgage_interest"])
        income = tax_unit("pr_gross_income", period)
        return min_(interest, min_(p.income_share * income, p.cap))

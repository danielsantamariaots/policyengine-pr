from policyengine_pr.model_api import *


class pr_regular_tax_before_credits(Variable):
    value_type = float
    entity = TaxUnit
    label = "PR regular tax before credits"
    documentation = (
        "Return Part 3, line 17. Gradual adjustment (Schedule P, net "
        "taxable income over $500,000) is not yet modelled."
    )
    unit = USD
    definition_period = YEAR

    def formula(tax_unit, period, parameters):
        p = parameters(period).gov.hacienda.income.tax_determination.rate
        tax = tax_unit("pr_regular_tax", period)
        gross_income = tax_unit("pr_gross_income", period)
        factor = where(
            gross_income <= p.gross_income_threshold, p.reduced, p.standard
        )
        return tax * factor

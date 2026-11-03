from policyengine_pr.model_api import *


class pr_regular_tax_before_credits(Variable):
    value_type = float
    entity = TaxUnit
    label = "PR regular tax before credits"
    documentation = "Return Part 3, line 17: the determination factor applied to table tax plus gradual adjustment."
    unit = USD
    definition_period = YEAR

    def formula(tax_unit, period, parameters):
        p = parameters(period).gov.hacienda.income.tax_determination.rate
        tax = tax_unit("pr_regular_tax", period)
        adjustment = tax_unit("pr_gradual_adjustment", period)
        gross_income = tax_unit("pr_gross_income", period)
        factor = where(
            gross_income <= p.gross_income_threshold, p.reduced, p.standard
        )
        return (tax + adjustment) * factor

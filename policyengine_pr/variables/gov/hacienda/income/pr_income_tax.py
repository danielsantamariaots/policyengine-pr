from policyengine_pr.model_api import *


class pr_income_tax(Variable):
    value_type = float
    entity = TaxUnit
    label = "PR income tax liability"
    documentation = (
        "Return Part 3, line 26: total tax determined less nonrefundable "
        "credits, floored at zero. Optional tax (line 23) and recapture "
        "(line 24) not modelled."
    )
    unit = USD
    definition_period = YEAR

    def formula(tax_unit, period, parameters):
        determined = tax_unit("pr_total_tax_determined", period)
        credits = tax_unit("pr_nonrefundable_credits", period)
        return max_(0, determined - credits)

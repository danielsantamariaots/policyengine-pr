from policyengine_pr.model_api import *


class pr_net_taxable_income(Variable):
    value_type = float
    entity = TaxUnit
    label = "PR net taxable income"
    documentation = "Return Part 2, line 13."
    unit = USD
    definition_period = YEAR

    def formula(tax_unit, period, parameters):
        income = tax_unit("pr_taxable_gross_income", period)
        deductions = tax_unit("pr_deductions", period)
        exemptions = tax_unit("pr_exemptions", period)
        return max_(0, income - deductions - exemptions)

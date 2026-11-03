from policyengine_pr.model_api import *


class pr_regular_tax(Variable):
    value_type = float
    entity = TaxUnit
    label = "PR regular tax per table"
    documentation = "Return Part 3, line 14 (Oval 1, Tax Computation Table)."
    unit = USD
    definition_period = YEAR

    def formula(tax_unit, period, parameters):
        income = tax_unit("pr_net_taxable_income", period)
        return parameters(period).gov.hacienda.income.rates.calc(income)

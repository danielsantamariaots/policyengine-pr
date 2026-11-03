from policyengine_pr.model_api import *


class pr_abt_net_income(Variable):
    value_type = float
    entity = TaxUnit
    label = "PR net income subject to alternate basic tax"
    documentation = "Anejo O Individuo, Parte I, línea 18."
    unit = USD
    definition_period = YEAR

    def formula(tax_unit, period, parameters):
        income = tax_unit("pr_abt_income", period)
        deductions = tax_unit("pr_deductions", period)
        exemptions = tax_unit("pr_exemptions", period)
        return max_(0, income - deductions - exemptions)

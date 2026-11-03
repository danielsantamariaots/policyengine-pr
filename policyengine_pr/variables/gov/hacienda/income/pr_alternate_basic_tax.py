from policyengine_pr.model_api import *


class pr_alternate_basic_tax(Variable):
    value_type = float
    entity = TaxUnit
    label = "PR alternate basic tax"
    documentation = (
        "Anejo O Individuo, Parte II, línea 4. The bracket's rate applies "
        "to the whole net income subject to ABT (a cliff, not a marginal "
        "schedule)."
    )
    unit = USD
    definition_period = YEAR

    def formula(tax_unit, period, parameters):
        p = parameters(period).gov.hacienda.income.alternate_basic_tax
        income = tax_unit("pr_abt_net_income", period)
        rate = p.rates.marginal_rates(income)
        return where(income > p.threshold, income * rate, 0)

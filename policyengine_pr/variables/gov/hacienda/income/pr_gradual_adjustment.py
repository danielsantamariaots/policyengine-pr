from policyengine_pr.model_api import *


class pr_gradual_adjustment(Variable):
    value_type = float
    entity = TaxUnit
    label = "PR gradual adjustment"
    documentation = (
        "Anejo P Individuo, línea 7. Phases out the benefit of the lower "
        "brackets and exemptions above the threshold. The limit's "
        "exemption component should also include the additional veteran "
        "exemption, not yet modelled."
    )
    unit = USD
    definition_period = YEAR

    def formula(tax_unit, period, parameters):
        p = parameters(period).gov.hacienda.income.gradual_adjustment
        income = tax_unit("pr_net_taxable_income", period)
        excess = max_(0, income - p.threshold)
        adjustment = p.rate * excess
        exemptions = tax_unit("pr_exemptions", period)
        limit = p.limit_base + p.limit_exemption_rate * exemptions
        return min_(adjustment, limit)

from policyengine_pr.model_api import *


class pr_abt_excess(Variable):
    value_type = float
    entity = TaxUnit
    label = "PR excess of net alternate basic tax over net regular tax"
    documentation = (
        "Anejo O Individuo, Parte II, línea 7; return Part 3, line 20. "
        "Foreign tax credits (Schedule C) not yet modelled."
    )
    unit = USD
    definition_period = YEAR

    def formula(tax_unit, period, parameters):
        abt = tax_unit("pr_alternate_basic_tax", period)
        regular = tax_unit("pr_regular_tax_before_credits", period)
        return max_(0, abt - regular)

from policyengine_pr.model_api import *


class pr_abt_other_income(Variable):
    value_type = float
    entity = TaxUnit
    label = "Other income subject to alternate basic tax"
    documentation = "Pass-through, exempt and other Anejo O Parte I items not yet modelled."
    unit = USD
    definition_period = YEAR

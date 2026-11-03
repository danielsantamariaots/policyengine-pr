from policyengine_pr.model_api import *


class pr_nonrefundable_credits(Variable):
    value_type = float
    entity = TaxUnit
    label = "PR nonrefundable tax credits"
    documentation = "Return Part 3, line 25 (Anejo B Individuo, Parte II, línea 28). Input until modelled."
    unit = USD
    definition_period = YEAR

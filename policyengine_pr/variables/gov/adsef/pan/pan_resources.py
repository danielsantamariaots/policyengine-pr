from policyengine_pr.model_api import *


class pan_resources(Variable):
    value_type = float
    entity = PANUnit
    label = "PAN countable resources"
    documentation = "Input: countable resources of the household (bank balances, vehicles above the exclusions, other property), Reglamento 8684 Art. 46-48. SSA disability, TANF and government disability pensions are not counted. Zero by default (not in the microdata)."
    unit = USD
    definition_period = YEAR
    default_value = 0

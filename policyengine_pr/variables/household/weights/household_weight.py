from policyengine_pr.model_api import *


class household_weight(Variable):
    value_type = float
    entity = Household
    label = "Household weight"
    documentation = "Survey weight of the household (PRCS WGTP)."
    definition_period = YEAR

from policyengine_pr.model_api import *


class household_market_income(Variable):
    value_type = float
    entity = Household
    label = "Household market income"
    documentation = "Phase 1: wages only."
    unit = USD
    definition_period = YEAR
    adds = ["employment_income"]

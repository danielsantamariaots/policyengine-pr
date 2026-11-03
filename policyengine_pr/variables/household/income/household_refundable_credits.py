from policyengine_pr.model_api import *


class household_refundable_credits(Variable):
    value_type = float
    entity = Household
    label = "Household refundable credits"
    unit = USD
    definition_period = YEAR
    adds = ["pr_refundable_credits"]

from policyengine_pr.model_api import *


class household_net_income(Variable):
    value_type = float
    entity = Household
    label = "Household net income"
    documentation = (
        "Market income less taxes plus refundable credits and benefits (PAN)."
    )
    unit = USD
    definition_period = YEAR
    adds = [
        "household_market_income",
        "household_refundable_credits",
        "household_benefits",
    ]
    subtracts = ["household_tax"]

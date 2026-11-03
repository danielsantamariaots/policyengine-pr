from policyengine_pr.model_api import *


class household_market_income(Variable):
    value_type = float
    entity = Household
    label = "Household market income"
    documentation = (
        "Wages, self-employment profit, pensions and Social Security benefits."
    )
    unit = USD
    definition_period = YEAR
    adds = [
        "employment_income",
        "self_employment_income",
        "pension_income",
        "social_security",
    ]

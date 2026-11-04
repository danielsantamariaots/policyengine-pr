from policyengine_pr.model_api import *


class pan_earned_income(Variable):
    value_type = float
    entity = Household
    label = "PAN earned income (annual)"
    documentation = "Wages and self-employment profit counted in full (Reglamento 8684, Art. 45.A; SPO FY2022 p. 26). Losses are not netted."
    unit = USD
    definition_period = YEAR

    def formula(household, period, parameters):
        wages = add(household, period, ["employment_income"])
        profit = household.sum(
            max_(0, household.members("self_employment_income", period))
        )
        return wages + profit

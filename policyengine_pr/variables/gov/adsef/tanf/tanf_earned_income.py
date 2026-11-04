from policyengine_pr.model_api import *


class tanf_earned_income(Variable):
    value_type = float
    entity = Household
    label = "TANF earned income (annual)"
    documentation = "Wages and self-employment profit of all members (Reglamento 7653, Sec. 4.18)."
    unit = USD
    definition_period = YEAR

    def formula(household, period, parameters):
        wages = add(household, period, ["employment_income"])
        profit = household.sum(
            max_(0, household.members("self_employment_income", period))
        )
        return wages + profit

from policyengine_pr.model_api import *


class pan_earned_income(Variable):
    value_type = float
    entity = PANUnit
    label = "PAN earned income (annual)"
    documentation = "Wages and self-employment profit counted in full (Reglamento 8684, Art. 45.A; SPO FY2022 p. 26). Losses are not netted."
    unit = USD
    definition_period = YEAR

    def formula(pan_unit, period, parameters):
        wages = add(pan_unit, period, ["employment_income"])
        profit = pan_unit.sum(
            max_(0, pan_unit.members("self_employment_income", period))
        )
        return wages + profit

from policyengine_pr.model_api import *


class section8_adjusted_income(Variable):
    value_type = float
    entity = Household
    label = "Section 8 adjusted income"
    documentation = "Annual income less $480 per dependent (member under 18) and $525 for an elderly family (any member aged 62+), 24 CFR 5.611(a). Medical, disability-assistance and child-care deductions not modelled."
    unit = USD
    definition_period = YEAR

    def formula(household, period, parameters):
        p = parameters(period).gov.hud.section8
        age = household.members("age", period)
        dependents = household.sum(age < 18)
        elderly = household.any(age >= p.elderly_age)
        deductions = p.deductions.dependent * dependents + where(
            elderly, p.deductions.elderly_disabled, 0
        )
        return max_(
            0, household("section8_annual_income", period) - deductions
        )

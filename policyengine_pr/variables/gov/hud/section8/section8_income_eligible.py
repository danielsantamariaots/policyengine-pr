from policyengine_pr.model_api import *


class section8_income_eligible(Variable):
    value_type = bool
    entity = Household
    label = "Income-eligible for admission to Section 8"
    documentation = "Annual income at or below the very low income limit for the household size (24 CFR 982.201(b)) in the household's HUD area. Admission only: a participating family keeps its voucher until the subsidy has been zero for 180 days (982.455), so this flag does not switch the subsidy off."
    definition_period = YEAR

    def formula(household, period, parameters):
        p = parameters(period).gov.hud.section8
        size = clip(household.nb_persons(), 1, 8).astype(str)
        area = household("hud_area", period).decode_to_str()
        return (
            household("section8_annual_income", period)
            <= p.income_limit.very_low[area][size]
        )

from policyengine_pr.model_api import *


class section8_bedrooms(Variable):
    value_type = int
    entity = Household
    label = "Section 8 voucher bedroom size"
    documentation = "Household size divided by the persons-per-bedroom subsidy standard, rounded up (24 CFR 982.402); capped at five bedrooms, the largest FMR published."

    definition_period = YEAR

    def formula(household, period, parameters):
        p = parameters(period).gov.hud.section8
        size = household.nb_persons()
        bedrooms = -(-size // p.persons_per_bedroom)  # ceiling division
        return clip(bedrooms, 0, 5)

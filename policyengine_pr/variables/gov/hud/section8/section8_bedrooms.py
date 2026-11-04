from policyengine_pr.model_api import *


class section8_bedrooms(Variable):
    value_type = int
    entity = Household
    label = "Section 8 voucher bedroom size"
    documentation = "PRPHA occupancy standard (Administrative Plan, June 2025, Sec. VI.B): the head of household and spouse get their own bedroom, every other member shares at two per bedroom, and a one-person family gets a one-bedroom voucher; capped at five bedrooms, the largest FMR published. The same-sex children six years apart rule is not modelled."

    definition_period = YEAR

    def formula(household, period, parameters):
        p = parameters(period).gov.hud.section8
        age = household.members("age", period)
        dependent = household.members("is_tax_unit_dependent", period)
        couple = clip(household.sum((age >= 18) & ~dependent), 1, 2)
        others = household.nb_persons() - couple
        bedrooms = 1 + -(-others // p.persons_per_bedroom)  # ceiling division
        return clip(bedrooms, 1, 5)

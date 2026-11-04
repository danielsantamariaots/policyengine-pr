from policyengine_pr.model_api import *


class pan_max_benefit(Variable):
    value_type = float
    entity = Household
    label = "PAN maximum monthly benefit"
    documentation = "SPO FY2022 p. 28 by household size, plus the elderly bonus per member aged 60+ (Reglamento 8684, Art. 51.C). Vieques and Culebra supplement not modelled."
    unit = USD
    definition_period = YEAR

    def formula(household, period, parameters):
        p = parameters(period).gov.adsef.pan
        size = min_(household("pan_household_size", period), 18).astype(str)
        return p.max_benefit[size] + p.elderly_bonus * household(
            "pan_elderly_count", period
        )

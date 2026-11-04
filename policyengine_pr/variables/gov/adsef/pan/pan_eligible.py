from policyengine_pr.model_api import *


class pan_eligible(Variable):
    value_type = bool
    entity = PANUnit
    label = "Eligible for PAN"
    documentation = "Monthly net income at or below the limit for the household size (SPO FY2022 p. 28; FNS: no gross income test) and countable resources within the limit. Citizenship, work registration and student rules not modelled."
    definition_period = YEAR

    def formula(pan_unit, period, parameters):
        p = parameters(period).gov.adsef.pan
        size = clip(pan_unit("pan_household_size", period), 1, 18).astype(str)
        net = pan_unit("pan_net_income", period) / MONTHS_IN_YEAR
        return (net <= p.net_income_limit[size]) & pan_unit(
            "pan_resources_eligible", period
        )

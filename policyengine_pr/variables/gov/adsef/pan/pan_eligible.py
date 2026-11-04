from policyengine_pr.model_api import *


class pan_eligible(Variable):
    value_type = bool
    entity = Household
    label = "Eligible for PAN"
    documentation = "Monthly net income at or below the limit for the household size (SPO FY2022 p. 28; FNS: no gross income test). Resources, citizenship, work registration and student rules not modelled."
    definition_period = YEAR

    def formula(household, period, parameters):
        p = parameters(period).gov.adsef.pan
        size = min_(household("pan_household_size", period), 18).astype(str)
        net = household("pan_net_income", period) / MONTHS_IN_YEAR
        return net <= p.net_income_limit[size]

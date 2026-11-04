from policyengine_pr.model_api import *


class pan_elderly_count(Variable):
    value_type = int
    entity = Household
    label = "PAN members aged 60 or over"
    documentation = "Reglamento 8684, Arts. 45.C.1 and 51.C."
    definition_period = YEAR

    def formula(household, period, parameters):
        p = parameters(period).gov.adsef.pan
        age = household.members("age", period)
        return household.sum(age >= p.elderly_age)

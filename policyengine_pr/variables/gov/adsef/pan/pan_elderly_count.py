from policyengine_pr.model_api import *


class pan_elderly_count(Variable):
    value_type = int
    entity = PANUnit
    label = "PAN members aged 60 or over"
    documentation = "Reglamento 8684, Arts. 45.C.1 and 51.C."
    definition_period = YEAR

    def formula(pan_unit, period, parameters):
        p = parameters(period).gov.adsef.pan
        age = pan_unit.members("age", period)
        return pan_unit.sum(age >= p.elderly_age)

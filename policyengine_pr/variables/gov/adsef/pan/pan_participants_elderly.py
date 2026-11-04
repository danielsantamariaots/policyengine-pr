from policyengine_pr.model_api import *


class pan_participants_elderly(Variable):
    value_type = float
    entity = Household
    label = "PAN participants aged 60+"
    documentation = "Persons aged 60 or over in núcleos with a positive PAN benefit (ADSEF '60+')."
    definition_period = YEAR

    def formula(household, period, parameters):
        members = household.members
        receiving = members.pan_unit("pan_benefit", period) > 0
        age = members("age", period)
        return household.sum(receiving & (age >= 60))

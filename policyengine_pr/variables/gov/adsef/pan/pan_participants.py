from policyengine_pr.model_api import *


class pan_participants(Variable):
    value_type = float
    entity = Household
    label = "PAN participants in the household"
    documentation = "Persons in núcleos with a positive PAN benefit (ADSEF 'participantes')."
    definition_period = YEAR

    def formula(household, period, parameters):
        members = household.members
        receiving = members.pan_unit("pan_benefit", period) > 0
        return household.sum(receiving)

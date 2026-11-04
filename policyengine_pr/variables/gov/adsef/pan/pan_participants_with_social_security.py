from policyengine_pr.model_api import *


class pan_participants_with_social_security(Variable):
    value_type = float
    entity = Household
    label = "PAN participants with Social Security"
    documentation = "Persons with Social Security benefits in núcleos with a positive PAN benefit (ADSEF 'SEGUROSOCIAL')."
    definition_period = YEAR

    def formula(household, period, parameters):
        members = household.members
        receiving = members.pan_unit("pan_benefit", period) > 0
        ss = members("social_security", period)
        return household.sum(receiving & (ss > 0))

from policyengine_pr.model_api import *


class pan_participants_with_wages(Variable):
    value_type = float
    entity = Household
    label = "PAN participants with wages"
    documentation = "Persons with wages in núcleos with a positive PAN benefit (ADSEF 'SALARIOS')."
    definition_period = YEAR

    def formula(household, period, parameters):
        members = household.members
        receiving = members.pan_unit("pan_benefit", period) > 0
        wages = members("employment_income", period)
        return household.sum(receiving & (wages > 0))

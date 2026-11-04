from policyengine_pr.model_api import *


class pan_units_without_income(Variable):
    value_type = float
    entity = Household
    label = "PAN núcleos with no income"
    documentation = "Núcleos with a positive PAN benefit and no earned or other countable income (ADSEF 'FAMSININGRESO')."
    definition_period = YEAR

    def formula(household, period, parameters):
        members = household.members
        receiving = members.pan_unit("pan_benefit", period) > 0
        gross = members.pan_unit("pan_gross_income", period)
        size = members.pan_unit("pan_household_size", period)
        return household.sum((receiving & (gross <= 0)) / size)

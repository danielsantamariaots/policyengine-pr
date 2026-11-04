from policyengine_pr.model_api import *


class pan_units_receiving(Variable):
    value_type = float
    entity = Household
    label = "PAN núcleos receiving a benefit"
    documentation = "Number of núcleos de servicio in the household with a positive PAN benefit; summed over households it is the participating-households count ADSEF and FNS publish (which counts núcleos)."
    definition_period = YEAR

    def formula(household, period, parameters):
        members = household.members
        receiving = members.pan_unit("pan_benefit", period) > 0
        size = members.pan_unit("pan_household_size", period)
        return household.sum(receiving / size)

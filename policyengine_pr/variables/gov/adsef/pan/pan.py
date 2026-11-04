from policyengine_pr.model_api import *


class pan(Variable):
    value_type = float
    entity = Household
    label = "PAN benefit (annual)"
    documentation = "Sum of the PAN benefits of the household's núcleos de servicio (pan_benefit)."
    unit = USD
    definition_period = YEAR

    def formula(household, period, parameters):
        members = household.members
        per_person = members.pan_unit(
            "pan_benefit", period
        ) / members.pan_unit("pan_household_size", period)
        return household.sum(per_person)

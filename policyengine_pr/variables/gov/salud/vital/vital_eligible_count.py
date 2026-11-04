from policyengine_pr.model_api import *


class vital_eligible_count(Variable):
    value_type = int
    entity = Household
    label = "Household members eligible for Plan Vital"
    documentation = "Count of members for whom is_vital_eligible is true."
    definition_period = YEAR

    def formula(household, period, parameters):
        return household.sum(household.members("is_vital_eligible", period))

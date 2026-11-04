from policyengine_pr.model_api import *


class pan_household_size(Variable):
    value_type = int
    entity = Household
    label = "PAN household size"
    documentation = "Members of the núcleo de servicio (Reglamento 8684, Art. 5). The model treats the whole household as one PAN unit."
    definition_period = YEAR

    def formula(household, period, parameters):
        return household.nb_persons()

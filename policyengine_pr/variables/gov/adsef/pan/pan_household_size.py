from policyengine_pr.model_api import *


class pan_household_size(Variable):
    value_type = int
    entity = PANUnit
    label = "PAN household size"
    documentation = "Members of the núcleo de servicio (Reglamento 8684, Art. 5). The model treats the whole household as one PAN unit."
    definition_period = YEAR

    def formula(pan_unit, period, parameters):
        return pan_unit.nb_persons()

from policyengine_pr.model_api import *


class pan_pays_dependent_care(Variable):
    value_type = bool
    entity = Household
    label = "Pays dependent care in order to work or train"
    documentation = "Input: the household pays for the care of its children so that an adult can work, look for work or train (Reglamento 8684, Art. 45.D). Not in the microdata."
    definition_period = YEAR
    default_value = False

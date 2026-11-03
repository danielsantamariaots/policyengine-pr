from policyengine_pr.model_api import *


class is_veteran(Variable):
    value_type = bool
    entity = Person
    label = "Is a veteran of the United States Armed Forces"
    definition_period = YEAR

from policyengine_pr.model_api import *


class person_weight(Variable):
    value_type = float
    entity = Person
    label = "Person weight"
    documentation = "Survey weight of the person (PRCS PWGTP)."
    definition_period = YEAR

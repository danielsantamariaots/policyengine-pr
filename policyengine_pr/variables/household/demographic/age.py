from policyengine_pr.model_api import *


class age(Variable):
    value_type = int
    entity = Person
    label = "Age"
    unit = "year"
    definition_period = YEAR

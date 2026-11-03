from policyengine_pr.model_api import *


class is_full_time_student(Variable):
    value_type = bool
    entity = Person
    label = "Is a full-time student"
    definition_period = YEAR

from policyengine_pr.model_api import *


class is_tax_unit_dependent(Variable):
    value_type = bool
    entity = Person
    label = "Is a dependent claimed in full on the tax unit's return"
    definition_period = YEAR

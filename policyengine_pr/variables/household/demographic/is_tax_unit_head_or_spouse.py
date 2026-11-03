from policyengine_pr.model_api import *


class is_tax_unit_head_or_spouse(Variable):
    value_type = bool
    entity = Person
    label = "Is the taxpayer or spouse on the return"
    definition_period = YEAR

    def formula(person, period, parameters):
        return ~person("is_tax_unit_dependent", period)

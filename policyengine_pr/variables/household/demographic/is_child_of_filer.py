from policyengine_pr.model_api import *


class is_child_of_filer(Variable):
    value_type = bool
    entity = Person
    label = "Is a child of the taxpayer or spouse"
    documentation = (
        "Only children (not other dependents) qualify for the PR EITC."
    )
    definition_period = YEAR
    default_value = True

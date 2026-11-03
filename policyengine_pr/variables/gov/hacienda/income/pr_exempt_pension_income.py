from policyengine_pr.model_api import *


class pr_exempt_pension_income(Variable):
    value_type = float
    entity = Person
    label = "Exempt pension income"
    unit = USD
    definition_period = YEAR

    def formula(person, period, parameters):
        return person("pension_income", period) - person(
            "pr_taxable_pension_income", period
        )

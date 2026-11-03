from policyengine_pr.model_api import *


class pr_taxable_employment_income(Variable):
    value_type = float
    entity = Person
    label = "Employment income subject to PR income tax"
    documentation = (
        "Return Part 1, line 1: wages less exempt wages (Anejo IE)."
    )
    unit = USD
    definition_period = YEAR

    def formula(person, period, parameters):
        return person("employment_income", period) - person(
            "pr_youth_exempt_income", period
        )

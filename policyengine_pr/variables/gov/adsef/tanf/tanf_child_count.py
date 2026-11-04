from policyengine_pr.model_api import *


class tanf_child_count(Variable):
    value_type = int
    entity = Household
    label = "Children under 18 in the household"
    documentation = (
        "Reglamento 7653, Category C: needy families with minor children."
    )
    definition_period = YEAR

    def formula(household, period, parameters):
        p = parameters(period).gov.adsef.tanf
        return household.sum(
            household.members("age", period) < p.child_max_age
        )

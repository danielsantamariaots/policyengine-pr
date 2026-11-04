from policyengine_pr.model_api import *


class tanf_adult_count(Variable):
    value_type = int
    entity = Household
    label = "Adults (18+) in the household"
    documentation = "Used for the single-parent rule: Puerto Rico does not serve two-parent units without a disabled parent (Welfare Rules Databook 2023, fn. 47)."
    definition_period = YEAR

    def formula(household, period, parameters):
        p = parameters(period).gov.adsef.tanf
        return household.sum(
            household.members("age", period) >= p.child_max_age
        )

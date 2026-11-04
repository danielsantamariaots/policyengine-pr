from policyengine_pr.model_api import *


class tanf_eligible(Variable):
    value_type = bool
    entity = Household
    label = "Eligible for TANF Category C"
    documentation = "A single adult with at least one child under 18 (two-parent units without a disabled parent are not served), with monthly gross earnings at or below the initial-eligibility ceiling and countable income below the maximum benefit. Resources, citizenship, work requirements and the 60-month limit not modelled."
    definition_period = YEAR

    def formula(household, period, parameters):
        p = parameters(period).gov.adsef.tanf
        single_parent = (household("tanf_adult_count", period) == 1) & (
            household("tanf_child_count", period) > 0
        )
        earnings = household("tanf_earned_income", period) / MONTHS_IN_YEAR
        countable = household("tanf_countable_income", period) / MONTHS_IN_YEAR
        return (
            single_parent
            & (earnings <= p.max_initial_earnings)
            & (countable < p.max_benefit)
        )

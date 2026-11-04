from policyengine_pr.model_api import *


class tanf_countable_income(Variable):
    value_type = float
    entity = Household
    label = "TANF countable income (annual)"
    documentation = "Earned income less the $90 work expense deduction per earner (Sec. 4.20.C.2), plus unearned income. New-job exemptions (Sec. 4.20) and child care deductions not modelled."
    unit = USD
    definition_period = YEAR

    def formula(household, period, parameters):
        p = parameters(period).gov.adsef.tanf
        earners = household.sum(
            (household.members("employment_income", period) > 0)
            | (household.members("self_employment_income", period) > 0)
        )
        earned = max_(
            0,
            household("tanf_earned_income", period)
            - p.work_expense_deduction * MONTHS_IN_YEAR * earners,
        )
        return earned + household("tanf_unearned_income", period)

from policyengine_pr.model_api import *


class tanf(Variable):
    value_type = float
    entity = Household
    label = "TANF benefit (annual)"
    documentation = "Maximum benefit less countable income, monthly, times 12; nothing is paid below the $10 minimum (Sec. 4.22.D). GAP: the three-person maximum ($584) is used for every family size."
    unit = USD
    definition_period = YEAR

    def formula(household, period, parameters):
        p = parameters(period).gov.adsef.tanf
        countable = household("tanf_countable_income", period) / MONTHS_IN_YEAR
        monthly = max_(0, p.max_benefit - countable)
        monthly = where(monthly < p.minimum_payment, 0, monthly)
        return where(
            household("tanf_eligible", period), monthly * MONTHS_IN_YEAR, 0
        )

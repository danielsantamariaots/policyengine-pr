from policyengine_pr.model_api import *


class section8(Variable):
    value_type = float
    entity = Household
    label = "Section 8 housing assistance payment (annual)"
    documentation = "For a household holding a voucher: the lower of the payment standard and the gross rent, less the total tenant payment, monthly, times 12 (24 CFR 982.505(b)); never below zero."
    unit = USD
    definition_period = YEAR

    def formula(household, period, parameters):
        standard = household("section8_payment_standard", period)
        rent = household("housing_rent", period)
        cap = where(rent > 0, min_(standard, rent), standard)
        hap = max_(0, cap - household("section8_total_tenant_payment", period))
        return where(
            household("housing_assisted", period), hap * MONTHS_IN_YEAR, 0
        )

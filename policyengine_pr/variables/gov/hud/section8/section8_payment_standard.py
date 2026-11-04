from policyengine_pr.model_api import *


class section8_payment_standard(Variable):
    value_type = float
    entity = Household
    label = "Section 8 payment standard (monthly)"
    documentation = "Payment standard for the voucher bedroom size (24 CFR 982.503), 100% of the FY2025 FMR of the household's HUD area (GAP: PRPHA's dollar schedule)."
    unit = USD
    definition_period = YEAR

    def formula(household, period, parameters):
        p = parameters(period).gov.hud.section8
        bedrooms = household("section8_bedrooms", period).astype(str)
        area = household("hud_area", period).decode_to_str()
        return p.payment_standard[area][bedrooms]

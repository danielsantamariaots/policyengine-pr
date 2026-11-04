from policyengine_pr.model_api import *


class section8_total_tenant_payment(Variable):
    value_type = float
    entity = Household
    label = "Section 8 total tenant payment (monthly)"
    documentation = "Highest of 30% of monthly adjusted income, 10% of monthly income and the minimum rent (24 CFR 5.628). Welfare rent does not apply in Puerto Rico."
    unit = USD
    definition_period = YEAR

    def formula(household, period, parameters):
        p = parameters(period).gov.hud.section8
        adjusted = (
            household("section8_adjusted_income", period) / MONTHS_IN_YEAR
        )
        gross = household("section8_annual_income", period) / MONTHS_IN_YEAR
        return max_(
            max_(
                p.total_tenant_payment_rate * adjusted,
                p.gross_income_rate * gross,
            ),
            p.minimum_rent,
        )

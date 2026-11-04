from policyengine_pr.model_api import *


class pan_other_income(Variable):
    value_type = float
    entity = Household
    label = "PAN other income counted (annual)"
    documentation = "Pensions and Social Security at the share counted since September 2018 (SPO FY2022 p. 26), plus interest, dividends and capital gains in full. Child support, unemployment and help from relatives are not modelled."
    unit = USD
    definition_period = YEAR

    def formula(household, period, parameters):
        p = parameters(period).gov.adsef.pan
        retirement = add(
            household, period, ["pension_income", "social_security"]
        )
        other = add(
            household,
            period,
            ["interest_income", "dividend_income", "long_term_capital_gains"],
        )
        return p.retirement_income_share * retirement + other

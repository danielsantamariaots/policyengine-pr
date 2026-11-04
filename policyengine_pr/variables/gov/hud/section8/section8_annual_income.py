from policyengine_pr.model_api import *


class section8_annual_income(Variable):
    value_type = float
    entity = Household
    label = "Section 8 annual income"
    documentation = "Annual income of all members (24 CFR 5.609(a)): wages, net self-employment income, pensions, Social Security, interest, dividends and TANF cash assistance. PAN is excluded (5.609(b)(5))."
    unit = USD
    definition_period = YEAR

    def formula(household, period, parameters):
        income = add(
            household,
            period,
            [
                "employment_income",
                "pension_income",
                "social_security",
                "interest_income",
                "dividend_income",
            ],
        )
        profit = household.sum(
            max_(0, household.members("self_employment_income", period))
        )
        return income + profit + household("tanf", period)

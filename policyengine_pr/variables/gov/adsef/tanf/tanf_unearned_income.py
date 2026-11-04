from policyengine_pr.model_api import *


class tanf_unearned_income(Variable):
    value_type = float
    entity = Household
    label = "TANF unearned income (annual)"
    documentation = "Pensions, Social Security, interest, dividends and capital gains (Reglamento 7653, Sec. 4.17: pensions and benefits are verified and counted)."
    unit = USD
    definition_period = YEAR
    adds = [
        "pension_income",
        "social_security",
        "interest_income",
        "dividend_income",
        "long_term_capital_gains",
    ]

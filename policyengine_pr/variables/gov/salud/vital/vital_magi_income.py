from policyengine_pr.model_api import *


class vital_magi_income(Variable):
    value_type = float
    entity = Household
    label = "Household MAGI for Plan Vital (annual)"
    documentation = "Wages, self-employment, pensions, Social Security, interest, dividends and capital gains of all members. CMS: eligibility is MAGI-based; Social Security counts in MAGI."
    unit = USD
    definition_period = YEAR
    adds = [
        "employment_income",
        "self_employment_income",
        "pension_income",
        "social_security",
        "interest_income",
        "dividend_income",
        "long_term_capital_gains",
    ]

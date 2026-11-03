from policyengine_pr.model_api import *


class household_tax(Variable):
    value_type = float
    entity = Household
    label = "Household taxes"
    documentation = "PR income tax, employee Social Security and Medicare taxes, and self-employment tax."
    unit = USD
    definition_period = YEAR
    adds = [
        "pr_income_tax",
        "employee_social_security_tax",
        "employee_medicare_tax",
        "self_employment_tax",
    ]

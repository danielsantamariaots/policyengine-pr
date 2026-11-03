from policyengine_pr.model_api import *


class tax_unit_payroll_taxes(Variable):
    value_type = float
    entity = TaxUnit
    label = "Social Security and Medicare taxes counted for the ACTC limit"
    documentation = (
        "Form 1040-SS, Part II, line 18: one-half of self-employment tax "
        "(line 12a) plus employee withholding on wages (line 13a)."
    )
    unit = USD
    definition_period = YEAR
    adds = [
        "self_employment_tax_deductible",
        "employee_social_security_tax",
        "employee_medicare_tax",
    ]

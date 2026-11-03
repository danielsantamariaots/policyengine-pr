from policyengine_pr.model_api import *


class tax_unit_payroll_taxes(Variable):
    value_type = float
    entity = TaxUnit
    label = "Social Security and Medicare taxes paid by the tax unit"
    documentation = (
        "Form 1040-SS, Part II, line 18. Phase 1: employee withholding on "
        "wages only; self-employment tax (line 12) not yet modelled."
    )
    unit = USD
    definition_period = YEAR
    adds = ["employee_social_security_tax", "employee_medicare_tax"]

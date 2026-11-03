from policyengine_pr.model_api import *


class pr_student_loan_deduction(Variable):
    value_type = float
    entity = TaxUnit
    label = "PR student loan deduction"
    documentation = "Anejo A, Parte I, línea 9: interest and principal paid on university-level student loans; no cap stated in the 2025 instructions."
    unit = USD
    definition_period = YEAR
    adds = ["student_loan_payments"]

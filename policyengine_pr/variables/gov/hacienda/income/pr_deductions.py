from policyengine_pr.model_api import *


class pr_deductions(Variable):
    value_type = float
    entity = TaxUnit
    label = "PR total deductions"
    documentation = (
        "Anejo A Individuo, Parte I, línea 11; return Part 2, line 6."
    )
    unit = USD
    definition_period = YEAR
    adds = [
        "pr_mortgage_interest_deduction",
        "pr_medical_expense_deduction",
        "pr_charitable_deduction",
        "pr_ira_deduction",
        "pr_education_account_deduction",
        "pr_student_loan_deduction",
        "pr_other_deductions",
    ]

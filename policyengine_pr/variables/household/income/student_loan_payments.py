from policyengine_pr.model_api import *


class student_loan_payments(Variable):
    value_type = float
    entity = Person
    label = "Ustudent loan payments"
    documentation = "Interest and principal paid on university-level student loans (Anejo A, Parte I, línea 9)"
    unit = USD
    definition_period = YEAR

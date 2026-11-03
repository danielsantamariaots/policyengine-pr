from policyengine_pr.model_api import *


class medical_expenses(Variable):
    value_type = float
    entity = Person
    label = "Umedical expenses"
    documentation = "Medical expenses not compensated by insurance (Anejo A, Parte III, Columna A)"
    unit = USD
    definition_period = YEAR

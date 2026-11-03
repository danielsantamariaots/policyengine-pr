from policyengine_pr.model_api import *


class pension_income(Variable):
    value_type = float
    entity = Person
    label = "Pension or annuity income from a qualified plan"
    documentation = "Periodic payments from a qualified or government plan (Anejo H Individuo, Parte II, línea 7)."
    unit = USD
    definition_period = YEAR

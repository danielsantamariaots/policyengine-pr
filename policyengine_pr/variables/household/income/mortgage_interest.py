from policyengine_pr.model_api import *


class mortgage_interest(Variable):
    value_type = float
    entity = Person
    label = "Umortgage interest"
    documentation = "Home mortgage interest paid on a qualified residence (Anejo A, Parte I, línea 1g)"
    unit = USD
    definition_period = YEAR

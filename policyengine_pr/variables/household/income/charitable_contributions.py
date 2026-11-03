from policyengine_pr.model_api import *


class charitable_contributions(Variable):
    value_type = float
    entity = Person
    label = "Ucharitable contributions"
    documentation = "Charitable contributions to eligible nonprofit organizations (Anejo A, Parte III, Columna B)"
    unit = USD
    definition_period = YEAR

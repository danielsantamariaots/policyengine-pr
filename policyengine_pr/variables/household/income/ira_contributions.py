from policyengine_pr.model_api import *


class ira_contributions(Variable):
    value_type = float
    entity = Person
    label = "Uira contributions"
    documentation = "Contributions to a Puerto Rico individual retirement account (Anejo A, Parte I, línea 7)"
    unit = USD
    definition_period = YEAR

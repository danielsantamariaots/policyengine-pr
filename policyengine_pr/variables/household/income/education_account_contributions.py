from policyengine_pr.model_api import *


class education_account_contributions(Variable):
    value_type = float
    entity = Person
    label = "Ueducation account contributions"
    documentation = "Cash contributions to educational contribution or My Future accounts (Anejo A, Parte I, línea 8)"
    unit = USD
    definition_period = YEAR

from policyengine_pr.model_api import *


class employment_income(Variable):
    value_type = float
    entity = Person
    label = "Employment income"
    documentation = (
        "Wages, salaries and other compensation for services (salarios)."
    )
    unit = USD
    definition_period = YEAR

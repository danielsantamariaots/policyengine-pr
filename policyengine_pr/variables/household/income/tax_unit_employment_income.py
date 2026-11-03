from policyengine_pr.model_api import *


class tax_unit_employment_income(Variable):
    value_type = float
    entity = TaxUnit
    label = "Tax unit employment income"
    unit = USD
    definition_period = YEAR
    adds = ["employment_income"]

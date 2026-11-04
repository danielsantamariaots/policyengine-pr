from policyengine_pr.model_api import *


class household_benefits(Variable):
    value_type = float
    entity = Household
    label = "Household benefits"
    documentation = "In-kind and cash benefits modelled: PAN."
    unit = USD
    definition_period = YEAR
    adds = ["pan"]

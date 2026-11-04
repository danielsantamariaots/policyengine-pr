from policyengine_pr.model_api import *


class household_benefits(Variable):
    value_type = float
    entity = Household
    label = "Household benefits"
    documentation = "Cash and in-kind benefits modelled: PAN and TANF (Plan Vital eligibility is reported but carries no cash value)."
    unit = USD
    definition_period = YEAR
    adds = ["pan", "tanf"]

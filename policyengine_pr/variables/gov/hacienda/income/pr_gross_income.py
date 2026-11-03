from policyengine_pr.model_api import *


class pr_gross_income(Variable):
    value_type = float
    entity = TaxUnit
    label = "PR gross income"
    documentation = (
        "Phase 1: wage income only. Used for the 1021.01(c) gross income test."
    )
    unit = USD
    definition_period = YEAR
    adds = ["employment_income"]

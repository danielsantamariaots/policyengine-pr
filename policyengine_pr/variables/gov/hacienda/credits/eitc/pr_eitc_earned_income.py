from policyengine_pr.model_api import *


class pr_eitc_earned_income(Variable):
    value_type = float
    entity = TaxUnit
    label = "PR EITC earned income"
    documentation = (
        "Anejo CT, Parte II, línea 1D: wages, pensions and self-employment "
        "income. Phase 1: wages only."
    )
    unit = USD
    definition_period = YEAR
    adds = ["employment_income"]

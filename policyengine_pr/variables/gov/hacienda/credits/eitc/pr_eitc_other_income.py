from policyengine_pr.model_api import *


class pr_eitc_other_income(Variable):
    value_type = float
    entity = TaxUnit
    label = "PR EITC net income from other sources"
    documentation = (
        "Anejo CT, Parte II, línea 2D. Input in phase 1 since non-wage "
        "income is not yet modelled."
    )
    unit = USD
    definition_period = YEAR

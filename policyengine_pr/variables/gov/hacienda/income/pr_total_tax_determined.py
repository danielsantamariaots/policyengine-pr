from policyengine_pr.model_api import *


class pr_total_tax_determined(Variable):
    value_type = float
    entity = TaxUnit
    label = "PR total tax determined"
    documentation = (
        "Return Part 3, line 22: net regular tax plus the excess of the "
        "alternate basic tax. Foreign tax credit (line 18) and the ABT "
        "credit (line 21) not yet modelled."
    )
    unit = USD
    definition_period = YEAR
    adds = ["pr_regular_tax_before_credits", "pr_abt_excess"]

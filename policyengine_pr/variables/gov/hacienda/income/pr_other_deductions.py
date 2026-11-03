from policyengine_pr.model_api import *


class pr_other_deductions(Variable):
    value_type = float
    entity = TaxUnit
    label = "Other PR deductions not modelled"
    documentation = (
        "Casualty losses and any other Anejo A item not computed from inputs."
    )
    unit = USD
    definition_period = YEAR

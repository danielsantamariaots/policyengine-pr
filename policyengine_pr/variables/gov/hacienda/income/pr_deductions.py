from policyengine_pr.model_api import *


class pr_deductions(Variable):
    value_type = float
    entity = TaxUnit
    label = "PR total deductions"
    documentation = "Schedule A Individual, Part I, line 11. Input until itemized deductions are modelled."
    unit = USD
    definition_period = YEAR

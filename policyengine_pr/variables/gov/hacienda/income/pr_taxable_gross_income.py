from policyengine_pr.model_api import *


class pr_taxable_gross_income(Variable):
    value_type = float
    entity = TaxUnit
    label = "PR gross income subject to tax"
    documentation = "Return Part 1, line 5, after exclusions on Anejo IE. Phase 1: wages only."
    unit = USD
    definition_period = YEAR
    adds = ["pr_taxable_employment_income"]

from policyengine_pr.model_api import *


class pr_taxable_gross_income(Variable):
    value_type = float
    entity = TaxUnit
    label = "PR adjusted gross income"
    documentation = "Return Part 1, line 5: wages after exempt wages, self-employment profit and taxable pensions. Alimony paid (line 4) not modelled."
    unit = USD
    definition_period = YEAR
    adds = [
        "pr_taxable_employment_income",
        "self_employment_income",
        "pr_taxable_pension_income",
    ]

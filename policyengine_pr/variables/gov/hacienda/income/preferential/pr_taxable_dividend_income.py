from policyengine_pr.model_api import *


class pr_taxable_dividend_income(Variable):
    value_type = float
    entity = TaxUnit
    label = "PR taxable dividends"
    documentation = "Anejo FF Individuo, Parte II, line 3 (return line 2D)."
    unit = USD
    definition_period = YEAR
    adds = ["dividend_income"]

from policyengine_pr.model_api import *


class pr_preferential_income(Variable):
    value_type = float
    entity = TaxUnit
    label = "PR income subject to preferential rates"
    documentation = "Anejo A2 Individuo, line 5: total of lines 4(a)-4(l). Modelled: long-term capital gains (4(a)), bank deposit interest (4(b)-4(d)), dividends (4(f))."
    unit = USD
    definition_period = YEAR
    adds = [
        "pr_taxable_capital_gains",
        "pr_taxable_interest_income",
        "pr_taxable_dividend_income",
    ]

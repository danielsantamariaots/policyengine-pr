from policyengine_pr.model_api import *


class pr_eitc_other_income(Variable):
    value_type = float
    entity = TaxUnit
    label = "PR EITC net income from other sources"
    documentation = "Anejo CT, Parte II, line 2D: interest, dividends and capital gains (return lines 2B-2D) plus other items entered as pr_eitc_unmodelled_other_income. Above $10,000 the credit is denied."
    unit = USD
    definition_period = YEAR
    adds = [
        "pr_taxable_interest_income",
        "pr_taxable_dividend_income",
        "pr_taxable_capital_gains",
        "pr_eitc_unmodelled_other_income",
    ]

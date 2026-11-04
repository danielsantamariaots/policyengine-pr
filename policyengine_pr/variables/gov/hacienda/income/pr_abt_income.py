from policyengine_pr.model_api import *


class pr_abt_income(Variable):
    value_type = float
    entity = TaxUnit
    label = "PR income subject to alternate basic tax before exemptions"
    documentation = (
        "Anejo O Individuo, Parte I, línea 16: business profit (lines 1-5) "
        "and other income (line 6: return lines 2A-2O, so taxable pensions, "
        "interest, dividends and capital gains), plus any "
        "amount entered in pr_abt_other_income. Wages are excluded "
        "(2025 instructions, p. 82)."
    )
    unit = USD
    definition_period = YEAR
    adds = [
        "self_employment_income",
        "pr_taxable_pension_income",
        "pr_taxable_interest_income",
        "pr_taxable_dividend_income",
        "pr_taxable_capital_gains",
        "pr_abt_other_income",
    ]

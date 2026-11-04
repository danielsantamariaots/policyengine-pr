from policyengine_pr.model_api import *


class pr_exempt_interest_income(Variable):
    value_type = float
    entity = TaxUnit
    label = "PR exempt bank deposit interest"
    documentation = "Anejo FF Individuo, Parte I, line 3: up to $100 ($200 joint) of interest from Puerto Rico financial institutions, Sección 1031.02(a)(3)(K)."
    unit = USD
    definition_period = YEAR

    def formula(tax_unit, period, parameters):
        p = parameters(period).gov.hacienda.income.preferential.bank_interest
        interest = add(tax_unit, period, ["interest_income"])
        status = tax_unit("pr_filing_status", period)
        return min_(interest, p.exemption[status])

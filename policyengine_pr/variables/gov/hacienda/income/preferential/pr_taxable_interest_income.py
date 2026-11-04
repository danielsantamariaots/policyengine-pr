from policyengine_pr.model_api import *


class pr_taxable_interest_income(Variable):
    value_type = float
    entity = TaxUnit
    label = "PR taxable bank deposit interest"
    documentation = "Anejo FF Individuo, Parte I, line 4 (return line 2C): interest after the exclusion, subject to the 10% rate."
    unit = USD
    definition_period = YEAR

    def formula(tax_unit, period, parameters):
        interest = add(tax_unit, period, ["interest_income"])
        return interest - tax_unit("pr_exempt_interest_income", period)

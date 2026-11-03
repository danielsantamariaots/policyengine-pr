from policyengine_pr.model_api import *


class pr_charitable_deduction(Variable):
    value_type = float
    entity = TaxUnit
    label = "PR charitable contribution deduction"
    documentation = "Anejo A, Parte I, línea 4: contributions up to 50% of adjusted gross income."
    unit = USD
    definition_period = YEAR

    def formula(tax_unit, period, parameters):
        p = parameters(period).gov.hacienda.deductions.charitable
        contributions = add(tax_unit, period, ["charitable_contributions"])
        agi = tax_unit("pr_taxable_gross_income", period)
        return min_(contributions, p.agi_share_limit * agi)

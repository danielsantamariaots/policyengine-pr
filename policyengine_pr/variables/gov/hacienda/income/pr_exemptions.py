from policyengine_pr.model_api import *


class pr_exemptions(Variable):
    value_type = float
    entity = TaxUnit
    label = "PR personal and dependent exemptions"
    unit = USD
    definition_period = YEAR

    def formula(tax_unit, period, parameters):
        p = parameters(period).gov.hacienda.income.exemptions
        filing_status = tax_unit("pr_filing_status", period)
        dependents = tax_unit.sum(
            tax_unit.members("is_tax_unit_dependent", period)
        )
        return p.personal[filing_status] + dependents * p.dependent

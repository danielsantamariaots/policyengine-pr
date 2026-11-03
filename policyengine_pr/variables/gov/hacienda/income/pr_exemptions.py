from policyengine_pr.model_api import *


class pr_exemptions(Variable):
    value_type = float
    entity = TaxUnit
    label = "PR personal, veteran and dependent exemptions"
    documentation = "Return Part 2, lines 7-9."
    unit = USD
    definition_period = YEAR

    def formula(tax_unit, period, parameters):
        p = parameters(period).gov.hacienda.income.exemptions
        filing_status = tax_unit("pr_filing_status", period)
        person = tax_unit.members
        dependents = tax_unit.sum(person("is_tax_unit_dependent", period))
        veterans = tax_unit.sum(
            person("is_veteran", period)
            & person("is_tax_unit_head_or_spouse", period)
        )
        return (
            p.personal[filing_status]
            + dependents * p.dependent
            + veterans * p.veteran
        )

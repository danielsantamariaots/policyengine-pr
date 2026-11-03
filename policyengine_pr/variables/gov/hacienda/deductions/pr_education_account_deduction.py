from policyengine_pr.model_api import *


class pr_education_account_deduction(Variable):
    value_type = float
    entity = TaxUnit
    label = "PR educational contribution account deduction"
    documentation = "Anejo A, Parte I, línea 8: up to $1,000 per beneficiary; beneficiaries approximated by dependents under 26."
    unit = USD
    definition_period = YEAR

    def formula(tax_unit, period, parameters):
        p = parameters(period).gov.hacienda.deductions
        contributions = add(
            tax_unit, period, ["education_account_contributions"]
        )
        person = tax_unit.members
        beneficiaries = tax_unit.sum(
            person("is_tax_unit_dependent", period)
            & (person("age", period) < 26)
        )
        return min_(
            contributions, p.education_account_per_beneficiary * beneficiaries
        )

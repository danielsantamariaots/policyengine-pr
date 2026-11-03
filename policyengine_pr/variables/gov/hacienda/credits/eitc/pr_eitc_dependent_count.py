from policyengine_pr.model_api import *


class pr_eitc_dependent_count(Variable):
    value_type = int
    entity = TaxUnit
    label = "Number of qualifying dependents for the PR EITC"
    documentation = "Anejo CT, Parte II, línea 4."
    definition_period = YEAR

    def formula(tax_unit, period, parameters):
        return tax_unit.sum(
            tax_unit.members("pr_eitc_eligible_dependent", period)
        )

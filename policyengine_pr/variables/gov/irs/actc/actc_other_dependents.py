from policyengine_pr.model_api import *


class actc_other_dependents(Variable):
    value_type = int
    entity = TaxUnit
    label = "Number of other dependents for the credit for other dependents"
    documentation = "Form 1040-SS, Part II, line 8: dependents who are not qualifying children."
    definition_period = YEAR

    def formula(tax_unit, period, parameters):
        person = tax_unit.members
        other = person("is_tax_unit_dependent", period) & ~person(
            "is_actc_qualifying_child", period
        )
        return tax_unit.sum(other)

from policyengine_pr.model_api import *


class actc_qualifying_children(Variable):
    value_type = int
    entity = TaxUnit
    label = "Number of ACTC qualifying children"
    documentation = "Form 1040-SS, Part II, line 2."
    definition_period = YEAR

    def formula(tax_unit, period, parameters):
        return tax_unit.sum(
            tax_unit.members("is_actc_qualifying_child", period)
        )

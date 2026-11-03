from policyengine_pr.model_api import *


class pr_eitc_earned_income(Variable):
    value_type = float
    entity = TaxUnit
    label = "PR EITC earned income"
    documentation = "Anejo CT, Parte II, línea 1D: wages (including exempt youth wages), taxable pensions and self-employment profit."
    unit = USD
    definition_period = YEAR

    def formula(tax_unit, period, parameters):
        wages = add(tax_unit, period, ["employment_income"])
        pensions = add(tax_unit, period, ["pr_taxable_pension_income"])
        profit = tax_unit.sum(
            max_(0, tax_unit.members("self_employment_income", period))
        )
        return wages + pensions + profit

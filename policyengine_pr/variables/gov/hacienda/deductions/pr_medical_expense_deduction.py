from policyengine_pr.model_api import *


class pr_medical_expense_deduction(Variable):
    value_type = float
    entity = TaxUnit
    label = "PR medical expense deduction"
    documentation = "Anejo A, Parte I, línea 3: expenses in excess of 6% of adjusted gross income."
    unit = USD
    definition_period = YEAR

    def formula(tax_unit, period, parameters):
        p = parameters(period).gov.hacienda.deductions
        expenses = add(tax_unit, period, ["medical_expenses"])
        agi = tax_unit("pr_taxable_gross_income", period)
        return max_(0, expenses - p.medical_agi_threshold * agi)

from policyengine_pr.model_api import *


class pr_taxable_capital_gains(Variable):
    value_type = float
    entity = TaxUnit
    label = "PR net long-term capital gain"
    documentation = "Anejo D Individuo, Parte VII, line 7 (return line 2B). Net losses are not deducted here (Sección 1034.01 loss limits not modelled)."
    unit = USD
    definition_period = YEAR

    def formula(tax_unit, period, parameters):
        return max_(0, add(tax_unit, period, ["long_term_capital_gains"]))

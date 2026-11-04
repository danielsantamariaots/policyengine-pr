from policyengine_pr.model_api import *


class pr_tax_at_regular_rates(Variable):
    value_type = float
    entity = TaxUnit
    label = "PR tax on all income at the regular rates"
    documentation = "Anejo A2 Individuo, line 16(d) (and return line 17 when there is no preferential income): table tax plus gradual adjustment, times the Sección 1021.01(c) factor."
    unit = USD
    definition_period = YEAR

    def formula(tax_unit, period, parameters):
        p = parameters(period).gov.hacienda.income.tax_determination.rate
        tax = tax_unit("pr_regular_tax", period)
        adjustment = tax_unit("pr_gradual_adjustment", period)
        gross_income = tax_unit("pr_gross_income", period)
        factor = where(
            gross_income <= p.gross_income_threshold, p.reduced, p.standard
        )
        return (tax + adjustment) * factor

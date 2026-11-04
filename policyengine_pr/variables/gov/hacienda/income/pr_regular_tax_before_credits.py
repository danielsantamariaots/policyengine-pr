from policyengine_pr.model_api import *


class pr_regular_tax_before_credits(Variable):
    value_type = float
    entity = TaxUnit
    label = "PR regular tax before credits"
    documentation = (
        "Return Part 3, line 17. Without preferential income: table tax plus "
        "gradual adjustment times the determination factor. With it, Anejo A2 "
        "line 17: the smaller of the tax with preferential rates (line 14) "
        "and the tax on all income at the regular rates (line 16(d)); the "
        "factor and the gradual adjustment are already inside both."
    )
    unit = USD
    definition_period = YEAR

    def formula(tax_unit, period, parameters):
        regular = tax_unit("pr_tax_at_regular_rates", period)
        with_preferential = tax_unit("pr_tax_with_preferential_rates", period)
        has_preferential = tax_unit("pr_preferential_income", period) > 0
        return where(
            has_preferential, min_(regular, with_preferential), regular
        )

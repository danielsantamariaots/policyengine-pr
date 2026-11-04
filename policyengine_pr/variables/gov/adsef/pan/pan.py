from policyengine_pr.model_api import *


class pan(Variable):
    value_type = float
    entity = Household
    label = "PAN benefit (annual)"
    documentation = (
        "Maximum benefit less the reduction rate times monthly net income, times 12, for eligible households. "
        "GAP: ADSEF's Tabla de Beneficios is not published; with the default reduction rate of 0 every eligible household receives the maximum (see gov/adsef/pan/benefit_reduction_rate.yaml)."
    )
    unit = USD
    definition_period = YEAR

    def formula(household, period, parameters):
        p = parameters(period).gov.adsef.pan
        net = household("pan_net_income", period) / MONTHS_IN_YEAR
        monthly = max_(
            0,
            household("pan_max_benefit", period)
            - p.benefit_reduction_rate * net,
        )
        return where(
            household("pan_eligible", period), monthly * MONTHS_IN_YEAR, 0
        )

from policyengine_pr.model_api import *


class pan_max_benefit(Variable):
    value_type = float
    entity = PANUnit
    label = "PAN maximum monthly benefit"
    documentation = "SPO FY2022 p. 28 by household size, plus the elderly bonus per member aged 60+ (Reglamento 8684, Art. 51.C). Sizes 2+ are the October 2021 table times the published one-person growth (estimate), and every amount is scaled to ADSEF's issuance per participant (estimate). Vieques and Culebra supplement not modelled."
    unit = USD
    definition_period = YEAR

    def formula(pan_unit, period, parameters):
        p = parameters(period).gov.adsef.pan
        n = clip(pan_unit("pan_household_size", period), 1, 18)
        base = p.max_benefit[n.astype(str)]
        # one-person values are published; larger núcleos use the 2021 table
        # times the one-person growth (ESTIMATE, see family_benefit_uprating)
        base = where(n >= 2, base * p.family_benefit_uprating, base)
        bonus = p.elderly_bonus * pan_unit("pan_elderly_count", period)
        return (base + bonus) * p.issuance_adjustment

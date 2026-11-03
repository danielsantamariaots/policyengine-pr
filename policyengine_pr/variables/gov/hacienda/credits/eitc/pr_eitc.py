from policyengine_pr.model_api import *


class pr_eitc(Variable):
    value_type = float
    entity = TaxUnit
    label = "PR earned income credit (Crédito por Trabajo)"
    documentation = (
        "Anejo CT, Parte III; return Part 3, line 27C. Phase-in rate times "
        "earned income up to the maximum, then reduced by the phase-out "
        "rate on earned income above the phase-out start."
    )
    unit = USD
    definition_period = YEAR

    def formula(tax_unit, period, parameters):
        p = parameters(period).gov.hacienda.credits.eitc
        eligible = tax_unit("pr_eitc_eligible", period)
        earned = tax_unit("pr_eitc_earned_income", period)
        status = tax_unit("pr_filing_status", period)
        joint = status == status.possible_values.JOINT
        n = min_(tax_unit("pr_eitc_dependent_count", period), 3)
        keys = n.astype(str)
        limit_status = where(joint, "JOINT", "SINGLE")
        phase_in = p.phase_in_rate[keys]
        maximum = p.max[keys]
        phase_out = p.phase_out_rate[keys]
        start = p.phase_out_start[keys][limit_status]
        phased_in = min_(phase_in * earned, maximum)
        reduction = phase_out * max_(0, earned - start)
        credit = max_(0, phased_in - reduction)
        return where(eligible, credit, 0)

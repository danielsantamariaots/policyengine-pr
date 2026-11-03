from policyengine_pr.model_api import *


class federal_actc(Variable):
    value_type = float
    entity = TaxUnit
    label = "Federal additional child tax credit (bona fide PR residents)"
    documentation = (
        "Form 1040-SS, Part II, line 19; reported on the PR return at Part "
        "3, line 27D. The refundable amount per child, limited by the "
        "phased-out CTC/ODC and by Social Security and Medicare taxes paid."
    )
    unit = USD
    definition_period = YEAR

    def formula(tax_unit, period, parameters):
        p = parameters(period).gov.irs.actc
        children = tax_unit("actc_qualifying_children", period)
        others = tax_unit("actc_other_dependents", period)
        # Line 2
        refundable = children * p.refundable_max
        # Lines 3-6: phase-out on excess MAGI rounded up to the increment.
        magi = tax_unit("federal_modified_agi", period)
        status = tax_unit("pr_filing_status", period)
        threshold = p.phase_out.threshold[status]
        excess = max_(0, magi - threshold)
        rounded = (
            np.ceil(excess / p.phase_out.increment) * p.phase_out.increment
        )
        reduction = p.phase_out.rate * rounded
        # Lines 7-11
        total_credit = (
            children * p.child_amount + others * p.other_dependent_amount
        )
        after_phase_out = max_(0, total_credit - reduction)
        line_11 = min_(refundable, after_phase_out)
        # Lines 12-18
        payroll = tax_unit("tax_unit_payroll_taxes", period)
        return where(children > 0, min_(line_11, payroll), 0)

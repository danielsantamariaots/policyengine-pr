from policyengine_pr.model_api import *


class pan_deductions(Variable):
    value_type = float
    entity = Household
    label = "PAN deductions (annual)"
    documentation = (
        "Reglamento 8684, Art. 45; amounts from the SPO FY2022 pp. 26-27 and the 2024 amendment. "
        "Earned-income deduction (50% up to the cap, minimum $100) or, for households with no earnings, the fixed other-income deduction; "
        "$100 per member aged 60+; standard deduction. Not modelled: disabled, student, terminally ill, medical and dependent-care deductions (no inputs yet)."
    )
    unit = USD
    definition_period = YEAR

    def formula(household, period, parameters):
        p = parameters(period).gov.adsef.pan.deductions
        earned = household("pan_earned_income", period) / MONTHS_IN_YEAR
        other = household("pan_other_income", period) / MONTHS_IN_YEAR
        earned_deduction = where(
            earned > 0,
            max_(
                min_(p.earned_income_share * earned, p.earned_income_cap),
                p.earned_income_minimum,
            ),
            0,
        )
        other_deduction = where(
            (earned <= 0) & (other > 0), p.other_income_fixed, 0
        )
        elderly = parameters(
            period
        ).gov.adsef.pan.deductions.elderly * household(
            "pan_elderly_count", period
        )
        monthly = earned_deduction + other_deduction + elderly + p.standard
        return monthly * MONTHS_IN_YEAR

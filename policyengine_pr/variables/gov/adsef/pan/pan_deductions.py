from policyengine_pr.model_api import *


class pan_deductions(Variable):
    value_type = float
    entity = Household
    label = "PAN deductions (annual)"
    documentation = (
        "Reglamento 8684, Art. 45; amounts from the SPO FY2022 pp. 26-27 and the 2024 amendment. "
        "Earned-income deduction (50% up to the cap, minimum $100) or, for households with no earnings, the fixed other-income deduction; "
        "$100 per member aged 60+ and per student; dependent care ($225 per child aged 2 or under, $200 per older child) when the household pays it to work; $100 recurrent medical expenses when reported; standard deduction. Not modelled: disabled and terminally ill deductions (no inputs), and the agriculture deduction."
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
        age = household.members("age", period)
        students = household.sum(
            household.members("is_full_time_student", period)
        )
        young_max = parameters(
            period
        ).gov.adsef.pan.dependent_care_max_age_young
        care = where(
            household("pan_pays_dependent_care", period),
            p.dependent_care_young * household.sum(age <= young_max)
            + p.dependent_care_older
            * household.sum((age > young_max) & (age < 18)),
            0,
        )
        medical = where(
            household("pan_recurrent_medical_expenses", period)
            & household.any(
                (age >= parameters(period).gov.adsef.pan.elderly_age)
                | (age < 18)
            ),
            p.medical,
            0,
        )
        monthly = (
            earned_deduction
            + other_deduction
            + elderly
            + p.student * students
            + care
            + medical
            + p.standard
        )
        return monthly * MONTHS_IN_YEAR

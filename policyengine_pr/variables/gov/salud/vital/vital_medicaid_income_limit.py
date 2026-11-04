from policyengine_pr.model_api import *


class vital_medicaid_income_limit(Variable):
    value_type = float
    entity = Household
    label = "Vital Medicaid monthly income limit for the household"
    documentation = "CMS 2026 table: one-person limit plus the increment per additional member."
    unit = USD
    definition_period = YEAR

    def formula(household, period, parameters):
        p = parameters(period).gov.salud.vital
        size = household("pan_household_size", period)
        return (
            p.medicaid_income_limit
            + p.medicaid_income_limit_per_additional_person * (size - 1)
        )

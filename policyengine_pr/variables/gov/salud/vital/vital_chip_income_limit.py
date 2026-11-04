from policyengine_pr.model_api import *


class vital_chip_income_limit(Variable):
    value_type = float
    entity = Household
    label = "Vital CHIP monthly income limit for the household"
    documentation = "CMS 2026 table, CHIP column: one-person limit plus the increment per additional member."
    unit = USD
    definition_period = YEAR

    def formula(household, period, parameters):
        p = parameters(period).gov.salud.vital
        size = household("household_size", period)
        return (
            p.chip_income_limit
            + p.chip_income_limit_per_additional_person * (size - 1)
        )

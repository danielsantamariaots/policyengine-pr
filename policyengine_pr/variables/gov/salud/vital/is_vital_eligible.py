from policyengine_pr.model_api import *


class is_vital_eligible(Variable):
    value_type = bool
    entity = Person
    label = "Eligible for Plan Vital (Medicaid or CHIP)"
    documentation = "Household monthly MAGI at or below the Medicaid limit for the household size; children under the CHIP age qualify up to the CHIP limit. Non-MAGI groups, resources and immigration status not modelled."
    definition_period = YEAR

    def formula(person, period, parameters):
        p = parameters(period).gov.salud.vital
        household = person.household
        monthly = household("vital_magi_income", period) / MONTHS_IN_YEAR
        medicaid = monthly <= household("vital_medicaid_income_limit", period)
        chip = monthly <= household("vital_chip_income_limit", period)
        child = person("age", period) < p.chip_max_age
        return medicaid | (child & chip)

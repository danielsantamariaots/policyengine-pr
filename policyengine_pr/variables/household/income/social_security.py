from policyengine_pr.model_api import *


class social_security(Variable):
    value_type = float
    entity = Person
    label = "Social Security benefits"
    documentation = "Not taxable in Puerto Rico (2025 instructions, Schedule H Individual); counted in market income only."
    unit = USD
    definition_period = YEAR

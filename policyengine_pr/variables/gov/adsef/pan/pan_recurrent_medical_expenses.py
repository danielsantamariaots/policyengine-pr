from policyengine_pr.model_api import *


class pan_recurrent_medical_expenses(Variable):
    value_type = bool
    entity = Household
    label = "Has recurrent medical expenses for an elderly, disabled member or child"
    documentation = "Input: the household has recurrent medical expenses for a member aged 60+, totally disabled or under 18 (Reglamento 8684, Art. 45.C; SPO FY2022 p. 27). Not in the microdata."
    definition_period = YEAR
    default_value = False

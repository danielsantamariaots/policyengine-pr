from policyengine_pr.model_api import *


class pan_gross_income(Variable):
    value_type = float
    entity = PANUnit
    label = "PAN gross income (annual)"
    documentation = "Reglamento 8684, Art. 42: income converted to a monthly base; here annual amounts divided by 12 in the deductions and benefit formulas."
    unit = USD
    definition_period = YEAR
    adds = ["pan_earned_income", "pan_other_income"]

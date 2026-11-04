from policyengine_pr.model_api import *


class pan_net_income(Variable):
    value_type = float
    entity = Household
    label = "PAN net income (annual)"
    documentation = "Reglamento 8684, Art. 5 def. 31: gross income less deductions, compared with the Tabla."
    unit = USD
    definition_period = YEAR

    def formula(household, period, parameters):
        return max_(
            0,
            household("pan_gross_income", period)
            - household("pan_deductions", period),
        )

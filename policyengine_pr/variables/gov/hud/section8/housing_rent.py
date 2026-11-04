from policyengine_pr.model_api import *


class housing_rent(Variable):
    value_type = float
    entity = Household
    label = "Monthly gross rent (rent plus utilities)"
    documentation = "Input: the unit's gross rent, used to cap the voucher subsidy (24 CFR 982.505(b): the subsidy is the lower of the payment standard and the gross rent, less the total tenant payment). Zero means the rent equals the payment standard."
    unit = USD
    definition_period = YEAR
    default_value = 0

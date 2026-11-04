from policyengine_pr.model_api import *


class housing_assisted(Variable):
    value_type = bool
    entity = Household
    label = "Holds a Section 8 housing choice voucher"
    documentation = "Input: the household rents with a Housing Choice Voucher (Sección 8) administered by the Departamento de la Vivienda. In the PRCS microdata receipt is imputed to renter households within the very low income limit, calibrated to HUD's 28,425 vouchers in use (policyengine_pr/data/prcs.py); in the app it is an input."
    definition_period = YEAR
    default_value = False

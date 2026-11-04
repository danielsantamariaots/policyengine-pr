from policyengine_pr.model_api import *


class housing_assisted(Variable):
    value_type = bool
    entity = Household
    label = "Holds a Section 8 housing choice voucher"
    documentation = "Input: the household rents with a Housing Choice Voucher (Sección 8) administered by the Departamento de la Vivienda. Participation is not imputed in the microdata; the subsidy is computed only for households flagged here."
    definition_period = YEAR
    default_value = False

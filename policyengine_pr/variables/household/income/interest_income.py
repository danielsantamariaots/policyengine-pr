from policyengine_pr.model_api import *


class interest_income(Variable):
    value_type = float
    entity = Person
    label = "Interest on deposits in Puerto Rico financial institutions"
    documentation = "Anejo FF Individuo, Parte I, Columns B-D (Formulario 480.6A/480.6B). Gross, before the Sección 1031.02(a)(3)(K) exclusion. Taxed at the Sección 1023.04 rate."
    unit = USD
    definition_period = YEAR

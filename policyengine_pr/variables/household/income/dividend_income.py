from policyengine_pr.model_api import *


class dividend_income(Variable):
    value_type = float
    entity = Person
    label = "Eligible dividends from Puerto Rico corporations"
    documentation = "Anejo FF Individuo, Parte II (line 2D of the return). Taxed at the Sección 1023.06 rate."
    unit = USD
    definition_period = YEAR

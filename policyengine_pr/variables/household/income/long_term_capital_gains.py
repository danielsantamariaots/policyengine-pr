from policyengine_pr.model_api import *


class long_term_capital_gains(Variable):
    value_type = float
    entity = Person
    label = "Net long-term capital gain"
    documentation = "Anejo D Individuo, Parte VII, line 7 (line 2B of the return). Taxed at the Sección 1023.02 rate or, if lower, the regular rates."
    unit = USD
    definition_period = YEAR

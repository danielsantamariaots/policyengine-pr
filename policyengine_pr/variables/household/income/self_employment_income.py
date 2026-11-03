from policyengine_pr.model_api import *


class self_employment_income(Variable):
    value_type = float
    entity = Person
    label = "Self-employment net profit"
    documentation = "Net gain from services rendered or trade or business (Anejo M Individuo, Parte IV, línea 9; return Part 1, lines 2P-2S)."
    unit = USD
    definition_period = YEAR

from policyengine_pr.model_api import *


class pr_abt_income(Variable):
    value_type = float
    entity = TaxUnit
    label = "PR income subject to alternate basic tax before exemptions"
    documentation = (
        "Anejo O Individuo, Parte I, línea 16. Input in phase 1: per the "
        "2025 instructions (p. 82), taxpayers with wage income only are not "
        "subject to the ABT, and the business, pass-through and exempt "
        "income items that feed this line are not yet modelled."
    )
    unit = USD
    definition_period = YEAR

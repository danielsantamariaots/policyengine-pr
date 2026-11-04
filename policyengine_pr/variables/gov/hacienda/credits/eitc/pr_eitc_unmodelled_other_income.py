from policyengine_pr.model_api import *


class pr_eitc_unmodelled_other_income(Variable):
    value_type = float
    entity = TaxUnit
    label = "PR EITC other income not modelled elsewhere"
    documentation = "Anejo CT, Parte II, lines 2A-2B items the model does not compute (rents, prizes, pass-through income, other exempt income). Input."
    unit = USD
    definition_period = YEAR

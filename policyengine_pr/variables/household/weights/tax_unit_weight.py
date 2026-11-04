from policyengine_pr.model_api import *


class tax_unit_weight(Variable):
    value_type = float
    entity = TaxUnit
    label = "Tax unit weight"
    documentation = "Weight of the tax unit: the household weight."
    definition_period = YEAR

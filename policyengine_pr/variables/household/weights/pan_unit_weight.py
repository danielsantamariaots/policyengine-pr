from policyengine_pr.model_api import *


class pan_unit_weight(Variable):
    value_type = float
    entity = PANUnit
    label = "Tax unit weight"
    documentation = "Weight of the PAN núcleo: the household weight."
    definition_period = YEAR

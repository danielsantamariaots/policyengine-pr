from policyengine_pr.model_api import *


class federal_modified_agi(Variable):
    value_type = float
    entity = TaxUnit
    label = "Modified AGI for the federal ACTC"
    documentation = (
        "Form 1040-SS, Part II, line 3: all income including Puerto Rico "
        "source income excluded under IRC §933. Phase 1: wages only."
    )
    unit = USD
    definition_period = YEAR
    adds = ["employment_income"]

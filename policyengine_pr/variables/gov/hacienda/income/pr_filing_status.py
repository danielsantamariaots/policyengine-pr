from policyengine_pr.model_api import *


class PRFilingStatus(Enum):
    SINGLE = "Individual taxpayer"
    JOINT = "Married living with spouse, filing jointly"
    SEPARATE = "Married filing separately"


class pr_filing_status(Variable):
    value_type = Enum
    possible_values = PRFilingStatus
    default_value = PRFilingStatus.SINGLE
    entity = TaxUnit
    label = "Filing status"
    definition_period = YEAR

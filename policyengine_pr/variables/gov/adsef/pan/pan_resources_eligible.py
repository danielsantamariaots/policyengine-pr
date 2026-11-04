from policyengine_pr.model_api import *


class pan_resources_eligible(Variable):
    value_type = bool
    entity = Household
    label = "Within the PAN resource limit"
    documentation = "Countable resources at or below $5,000, or $15,000 when a member is aged 60 or over (SPO FY2022 p. 28). Disability is not an input."
    definition_period = YEAR

    def formula(household, period, parameters):
        p = parameters(period).gov.adsef.pan
        elderly = household("pan_elderly_count", period) > 0
        limit = where(elderly, p.resource_limit_elderly, p.resource_limit)
        return household("pan_resources", period) <= limit

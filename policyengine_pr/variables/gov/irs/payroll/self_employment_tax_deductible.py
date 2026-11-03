from policyengine_pr.model_api import *


class self_employment_tax_deductible(Variable):
    value_type = float
    entity = Person
    label = "One-half of self-employment tax"
    documentation = "Schedule SE line 13; Form 1040-SS Part II line 12a."
    unit = USD
    definition_period = YEAR

    def formula(person, period, parameters):
        p = parameters(period).gov.irs.payroll.self_employment
        return p.deductible_share * person("self_employment_tax", period)

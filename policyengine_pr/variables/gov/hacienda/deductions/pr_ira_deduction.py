from policyengine_pr.model_api import *


class pr_ira_deduction(Variable):
    value_type = float
    entity = TaxUnit
    label = "PR IRA contribution deduction"
    documentation = (
        "Anejo A, Parte I, línea 7: per person, the lesser of contributions "
        "and \$7,000, limited by wages and self-employment earnings, and not "
        "allowed from age 75. The \$22,000 combined limit with employer plan "
        "contributions is not modelled."
    )
    unit = USD
    definition_period = YEAR

    def formula(tax_unit, period, parameters):
        p = parameters(period).gov.hacienda.deductions.ira
        person = tax_unit.members
        contributions = person("ira_contributions", period)
        earned = person("employment_income", period) + max_(
            0, person("self_employment_income", period)
        )
        eligible = person("age", period) < p.max_age
        per_person = where(
            eligible, min_(contributions, min_(p.per_person, earned)), 0
        )
        return tax_unit.sum(per_person)

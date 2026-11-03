from policyengine_pr.model_api import *


class pr_eitc_eligible(Variable):
    value_type = bool
    entity = TaxUnit
    label = "Eligible for the PR EITC"
    documentation = (
        "Anejo CT, Parte I and Parte II: earned income, taxpayer and spouse "
        "aged 19+, not married filing separately, other income within "
        "limit, earned income within the limit for the dependent count."
    )
    definition_period = YEAR

    def formula(tax_unit, period, parameters):
        p = parameters(period).gov.hacienda.credits.eitc
        earned = tax_unit("pr_eitc_earned_income", period)
        other = tax_unit("pr_eitc_other_income", period)
        status = tax_unit("pr_filing_status", period)
        statuses = status.possible_values
        n = min_(tax_unit("pr_eitc_dependent_count", period), 3)
        person = tax_unit.members
        adult_age = person("age", period)
        head_or_spouse = person("is_tax_unit_head_or_spouse", period)
        under_age = head_or_spouse & (adult_age < p.min_age)
        any_under_age = tax_unit.any(under_age)
        joint = status == statuses.JOINT
        limit_status = where(joint, "JOINT", "SINGLE")
        keys = n.astype(str)
        earned_limit = p.earned_income_limit[keys][limit_status]
        return (
            (earned > 0)
            & ~any_under_age
            & (status != statuses.SEPARATE)
            & (other <= p.other_income_limit)
            & (earned <= earned_limit)
        )

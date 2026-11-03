from policyengine_pr.model_api import *


class pr_eitc_eligible_dependent(Variable):
    value_type = bool
    entity = Person
    label = "Is a qualifying dependent for the PR EITC"
    documentation = (
        "Anejo CT, Parte I, requisito 4: a child of the taxpayer or spouse, "
        "claimed as a dependent, aged 18 or under (25 if a full-time "
        "student). PR residency and SSN requirements are assumed met."
    )
    definition_period = YEAR

    def formula(person, period, parameters):
        p = parameters(period).gov.hacienda.credits.eitc.dependent_max_age
        age = person("age", period)
        student = person("is_full_time_student", period)
        max_age = where(student, p.student, p.default)
        return (
            person("is_tax_unit_dependent", period)
            & person("is_child_of_filer", period)
            & (age <= max_age)
        )

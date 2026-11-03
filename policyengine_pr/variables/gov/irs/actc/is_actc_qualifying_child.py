from policyengine_pr.model_api import *


class is_actc_qualifying_child(Variable):
    value_type = bool
    entity = Person
    label = "Is a qualifying child for the federal ACTC"
    documentation = (
        "Form 1040-SS instructions, Part II, Qualifying child: a dependent "
        "child under 17 at year end. Valid SSN, relationship, residency and "
        "support tests are assumed met."
    )
    definition_period = YEAR

    def formula(person, period, parameters):
        p = parameters(period).gov.irs.actc
        return person("is_tax_unit_dependent", period) & (
            person("age", period) < p.child_max_age
        )

from policyengine_pr.model_api import *


class pr_youth_exempt_income(Variable):
    value_type = float
    entity = Person
    label = "Youth exempt income (Ley 135-2014)"
    documentation = (
        "Anejo IE Individuo, línea 31A: the first \$40,000 of wages of an "
        "individual aged 16 to 26 at the end of the taxable year. Applied "
        "per person; self-employment and services income not yet modelled."
    )
    unit = USD
    definition_period = YEAR

    def formula(person, period, parameters):
        p = parameters(period).gov.hacienda.income.exempt.youth
        age = person("age", period)
        eligible = (age >= p.min_age) & (age <= p.max_age)
        wages = person("employment_income", period)
        return where(eligible, min_(wages, p.amount), 0)

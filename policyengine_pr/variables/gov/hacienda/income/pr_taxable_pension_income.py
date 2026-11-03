from policyengine_pr.model_api import *


class pr_taxable_pension_income(Variable):
    value_type = float
    entity = Person
    label = "Pension income after the Sección 1031.02(a)(13) exemption"
    documentation = "Anejo H Individuo, Parte II, líneas 7-8: $11,000 exempt (under 60) or $15,000 (60 or older), not exceeding the pension."
    unit = USD
    definition_period = YEAR

    def formula(person, period, parameters):
        p = parameters(period).gov.hacienda.income.exempt.pension
        pension = person("pension_income", period)
        age = person("age", period)
        exempt = where(
            age >= p.age_threshold, p.amount.age_60_or_older, p.amount.under_60
        )
        return max_(0, pension - exempt)

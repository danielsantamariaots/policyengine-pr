from policyengine_pr.model_api import *


class employee_social_security_tax(Variable):
    value_type = float
    entity = Person
    label = "Employee Social Security tax withheld"
    documentation = "Formulario 499R-2/W-2PR, box 21."
    unit = USD
    definition_period = YEAR

    def formula(person, period, parameters):
        p = parameters(period).gov.irs.payroll.social_security
        wages = person("employment_income", period)
        return p.rate * min_(wages, p.wage_base)

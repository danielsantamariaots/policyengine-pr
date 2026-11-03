from policyengine_pr.model_api import *


class employee_medicare_tax(Variable):
    value_type = float
    entity = Person
    label = "Employee Medicare tax withheld"
    documentation = "Formulario 499R-2/W-2PR, box 23."
    unit = USD
    definition_period = YEAR

    def formula(person, period, parameters):
        p = parameters(period).gov.irs.payroll.medicare
        return p.rate * person("employment_income", period)

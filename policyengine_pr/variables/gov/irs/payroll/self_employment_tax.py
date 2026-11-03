from policyengine_pr.model_api import *


class self_employment_tax(Variable):
    value_type = float
    entity = Person
    label = "Self-employment tax"
    documentation = "Schedule SE lines 3-12: Social Security on net earnings up to the wage base less wages, plus Medicare on all net earnings."
    unit = USD
    definition_period = YEAR

    def formula(person, period, parameters):
        p = parameters(period).gov.irs.payroll
        profit = person("self_employment_income", period)
        net_earnings = max_(0, profit) * p.self_employment.net_earnings_share
        owes = net_earnings >= p.self_employment.minimum_net_earnings
        wages = person("employment_income", period)
        ss_room = max_(0, p.social_security.wage_base - wages)
        ss_tax = p.self_employment.social_security_rate * min_(
            net_earnings, ss_room
        )
        medicare_tax = p.self_employment.medicare_rate * net_earnings
        return where(owes, ss_tax + medicare_tax, 0)

from policyengine_pr.model_api import *


class pr_refundable_credits(Variable):
    value_type = float
    entity = TaxUnit
    label = "Refundable credits on the PR return"
    documentation = "Return Part 3, lines 27C (Crédito por Trabajo) and 27D (federal ACTC)."
    unit = USD
    definition_period = YEAR
    adds = ["pr_eitc", "federal_actc"]

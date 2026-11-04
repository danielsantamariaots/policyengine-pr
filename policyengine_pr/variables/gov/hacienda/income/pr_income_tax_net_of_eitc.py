from policyengine_pr.model_api import *


class pr_income_tax_net_of_eitc(Variable):
    value_type = float
    entity = TaxUnit
    label = "PR income tax net of the Crédito por Trabajo"
    documentation = "Income tax determined (line 26) less the refundable Crédito por Trabajo (line 27C): the model analogue of Hacienda's net individual income tax collections, which are net of refunds. Used for calibration only."
    unit = USD
    definition_period = YEAR
    adds = ["pr_income_tax"]
    subtracts = ["pr_eitc"]

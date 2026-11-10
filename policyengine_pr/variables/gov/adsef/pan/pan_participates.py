from policyengine_pr.model_api import *


class pan_participates(Variable):
    value_type = bool
    entity = PANUnit
    label = "Núcleo participates in PAN when eligible"
    documentation = "Take-up. True in the household calculator (an eligible núcleo is shown its benefit). In the PRCS microdata it is imputed so that participating núcleos reproduce ADSEF's casos, participants, participants aged 60+, with wages and with Social Security (policyengine_pr/data/pan_takeup.py): not every eligible núcleo applies."
    definition_period = YEAR
    default_value = True

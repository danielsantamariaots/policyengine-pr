from policyengine_pr.model_api import *


class pr_gross_income(Variable):
    value_type = float
    entity = TaxUnit
    label = "PR gross income including exempt income"
    documentation = (
        "Sum used for the Sección 1021.01(c) $100,000 test (instructions "
        "p. 20): adjusted gross income plus exempt wages and pensions."
    )
    unit = USD
    definition_period = YEAR
    adds = ["employment_income", "self_employment_income", "pension_income"]

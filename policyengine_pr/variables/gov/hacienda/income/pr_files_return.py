from policyengine_pr.model_api import *


class pr_files_return(Variable):
    value_type = bool
    entity = TaxUnit
    label = "Files a Puerto Rico income tax return"
    documentation = (
        "2025 instructions, 'Who must file', (a): every resident whose gross "
        "income net of exemptions is more than zero must file, unless the tax "
        "was fully withheld at source (withholding is not modelled, so such "
        "units are counted as filers); (d): net income subject to alternate "
        "basic tax of $25,000 or more. Units claiming the Crédito por Trabajo "
        "file to receive it. Used for the returns count only."
    )
    definition_period = YEAR

    def formula(tax_unit, period, parameters):
        p = parameters(period).gov.hacienda.income.alternate_basic_tax
        must = tax_unit("pr_taxable_gross_income", period) > tax_unit(
            "pr_exemptions", period
        )
        abt = tax_unit("pr_abt_net_income", period) >= p.threshold
        claims = tax_unit("pr_eitc", period) > 0
        return must | abt | claims

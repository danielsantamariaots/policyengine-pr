from policyengine_pr.model_api import *


class pr_tax_with_preferential_rates(Variable):
    value_type = float
    entity = TaxUnit
    label = "PR tax with preferential rates (Anejo A2)"
    documentation = (
        "Anejo A2 Individuo, line 14: regular tax on income not subject to "
        "preferential rates (line 12(d), with the gradual adjustment and the "
        "Sección 1021.01(c) factor) plus each preferential income times its "
        "rate (line 13). When preferential income is $20,000 or more, the "
        "Anejo A deductions are prorated by the whole-percent share of each "
        "income in adjusted gross income (Sección 1033.20; lines 7-8). "
        "Exemptions reduce regular income only (line 8(c)-(e))."
    )
    unit = USD
    definition_period = YEAR

    def formula(tax_unit, period, parameters):
        p = parameters(period).gov.hacienda.income
        agi = tax_unit("pr_taxable_gross_income", period)
        deductions = tax_unit("pr_deductions", period)
        exemptions = tax_unit("pr_exemptions", period)
        columns = [
            (
                tax_unit("pr_taxable_capital_gains", period),
                p.preferential.capital_gains_rate,
            ),
            (
                tax_unit("pr_taxable_interest_income", period),
                p.preferential.bank_interest.rate,
            ),
            (
                tax_unit("pr_taxable_dividend_income", period),
                p.preferential.dividends_rate,
            ),
        ]
        preferential = tax_unit("pr_preferential_income", period)
        regular_income = agi - preferential  # line 6
        prorate = (
            preferential >= p.preferential.deduction_limit_threshold
        ) & (agi > 0)
        safe_agi = where(agi > 0, agi, 1)

        def share(income):  # line 7: whole-percent share of AGI
            pct = np.round(income / safe_agi * 100) / 100
            return where(prorate, pct, 0)

        # Column A (line 11): regular income less its share of deductions and all exemptions
        regular_share = where(prorate, share(regular_income), 1)
        column_a = max_(
            0, regular_income - deductions * regular_share - exemptions
        )
        regular_tax = p.rates.calc(column_a)  # line 12(a)
        g = p.gradual_adjustment  # line 12(b), Anejo P on column A
        gradual = min_(
            g.rate * max_(0, column_a - g.threshold),
            g.limit_base + g.limit_exemption_rate * exemptions,
        )
        r = p.tax_determination.rate  # line 12(d)
        factor = where(
            tax_unit("pr_gross_income", period) <= r.gross_income_threshold,
            r.reduced,
            r.standard,
        )
        tax = (regular_tax + gradual) * factor
        for income, rate in columns:  # columns B-H, lines 11 and 13
            net = max_(0, income - deductions * share(income))
            tax = tax + net * rate
        return tax

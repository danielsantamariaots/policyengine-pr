# Roadmap to a March–April 2027 launch

Goal: when a PR tax reform proposal is published, produce within days
(1) a household calculator showing who gains and loses, and (2) static
estimates of revenue cost and distributional impact, credibly validated.

The exact proposal is unknown, so the model must cover every likely lever
as a parameter: brackets and rates, exemptions and deductions, the gradual
adjustment, alternate basic tax, PR EITC, child credits, youth exemption.

| Window | Deliverable | Critical inputs |
|---|---|---|
| Nov 2026 | Current-law individual income tax (tax year 2025): filing status, brackets, exemptions, deductions, gradual adjustment, ABT. Tests from planilla instructions. | Compiled Código text; 2025 planilla instructions and worksheets |
| Dec 2026 | PR EITC, PR child credit, federal CTC for PR residents, payroll taxes, Ley 135 youth exemption. | Same; IRS guidance for PR residents |
| Jan 2027 | Microdata: PRCS PUMS → tax units, imputations, reweighting to Hacienda aggregates. Baseline revenue / EITC cost reconciled to published figures. | PRCS PUMS (IPUMS); Hacienda filing statistics (request NOW — longest lead time) |
| Feb 2027 | Reform engine + app: parametric reforms, prebuilt scenarios for likely proposals, web app (household calculator + aggregate/distributional charts). | Hosting decision; Spanish/English copy |
| Mar 2027 | Validation report, private beta (legislative staff, press, academics), rapid-response playbook. Launch. | Reviewers lined up |
| Mar–Apr 2027 | Score the proposal within 48–72h of publication. | — |

Biggest risks: microdata calibration (start the Hacienda data request
immediately) and statute availability for 2025 amendments. Cut line if
late: ship the household calculator first; aggregate estimates follow.

## Scope notes (2026-11-03)

- **Nonrefundable credits (Anejo B, Parte II).** All 2025 lines are
  investment and incentive credits (housing infrastructure, affordable
  rental housing, urban centre construction, conservation easements,
  tourism, film, opportunity zones, purchased credits). None is a
  household credit, so `pr_nonrefundable_credits` stays an input; a
  reform affecting these is a business-incentive reform, out of scope.
- **Preferential rates (Anejo A2).** Interest, dividends and capital
  gains at 10%/15% are not modelled; such income is currently absent
  rather than mistaxed at ordinary rates. Next income item to add.

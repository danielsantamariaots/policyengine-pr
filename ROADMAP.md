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
- **Preferential rates (Anejo A2).** Modelled since 2026-11-04: bank
  deposit interest (10%, $100/$200 exclusion), dividends (15%) and
  long-term capital gains (15%), with the Sección 1033.20 deduction
  proration and the line-17 choice of the lower tax. Not modelled: the
  4%/20% columns (special acts, pension lump sums), capital-loss
  carryovers, and interest from outside Puerto Rico (taxed at ordinary
  rates; enter it as self-employment income only as a stopgap).
- **PAN (ADSEF).** Modelled since 2026-11-04 from Reglamento 8684 and the
  NAP State Plan FY2022 (`docs/statutes/pan/`): counted income (50% of
  pensions and Social Security), earned-income, other-income, elderly and
  standard deductions, net-income limits and maximum benefits by household
  size, elderly bonus. Gaps, each flagged in the parameter file: the Tabla
  de Beneficios schedule is not published (`benefit_reduction_rate` = 0
  pays the maximum to every eligible household); limits for sizes 2–18 are
  the October 2021 values; no resources test, dependent-care, disability,
  student or medical deductions, or Vieques/Culebra supplement. Ask ADSEF
  for the current Tabla and the FY2026 plan.
- **Microdata (PRCS 2023 PUMS).** Since 2026-11-04 `policyengine_pr/data/prcs.py`
  builds `data/prcs_2023.h5` from the Census PUMS person and housing files
  (download into `data/raw/pums_2023/`; `data/` is git-ignored). Tax units
  are built from household composition (head + spouse joint, their
  children as dependents, other adults single). `policyengine_pr/analysis/
  scoring.py` scores a reform (revenue, PAN, deciles, winners/losers) in
  about 0.1 s; the app's *Reformas* page shows it. Uncalibrated: baseline
  income tax (\$4.8 bn) and PAN households (835k vs 597k reporting PAN in
  the PRCS) exceed administrative totals; 2023 incomes are not uprated.
  Calibration to Hacienda's Tabla A and ADSEF's counts is the next data
  step once those tabulations arrive.

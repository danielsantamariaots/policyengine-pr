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
  for the current Tabla and the FY2026 plan. **Since 2026-11-04** the
  resources test ($5,000 / $15,000 with a member 60+) and the student,
  dependent-care ($225 / $200) and medical ($100) deductions are modelled
  from app inputs (`pan_resources`, `pan_pays_dependent_care`,
  `pan_recurrent_medical_expenses`); zero/false in the microdata.
- **Plan Vital and TANF.** Modelled since 2026-11-04 (`docs/statutes/vital/`,
  `docs/statutes/tanf/`). Vital: household MAGI against the CMS Puerto Rico
  Medicaid/CHIP levels (April 2026 table applied to 2025); eligibility
  only, no cash value. TANF Category C: single parent with a child under
  18, Reglamento 7653 deductions and minimum payment, Welfare Rules
  Database 2023 figures for a family of three ($584 maximum, $1,620
  earnings ceiling) applied to every size (GAP: ADSEF's standard-of-need
  table). Not modelled: categories A/B/D/G/T, new-job exemptions, child
  care deduction, resources, time limits, non-MAGI Medicaid, Sección 8.
- **Microdata (PRCS 2023 PUMS).** Since 2026-11-04 `policyengine_pr/data/prcs.py`
  builds `data/prcs_2023.h5` from the Census PUMS person and housing files
  (download into `data/raw/pums_2023/`; `data/` is git-ignored). Tax units
  are built from household composition (head + spouse joint, their
  children as dependents, other adults single). `policyengine_pr/analysis/
  scoring.py` scores a reform (revenue, PAN, deciles, winners/losers) in
  about 0.1 s; the app's *Reformas* page shows it. Uncalibrated: baseline
  income tax (\$4.8 bn) and PAN households (835k vs 597k reporting PAN in
  the PRCS) exceed administrative totals; 2023 incomes are not uprated.
  **Calibrated since 2026-11-04** (`policyengine_pr/data/calibration.py`,
  targets in `calibration_targets.yaml`, sources in
  `docs/statutes/calibration/`): entropy reweighting of household weights
  to seven published totals — households and persons (PRCS), net
  individual income tax FY2023-24 ($2,615.5 M, Hacienda), Crédito por
  Trabajo total and claimants TY2023 ($1,303 M, ~700k, Hacienda), PAN
  households and benefits FY2024 (738,510, $2,929 M, USDA FNS Keydata).
  All met exactly; weight ratios 0.07–4.45. Scoring and the Reformas page
  use `prcs_2023_calibrated.h5` when built. Distributional targets from
  Hacienda's Tabla A will replace these aggregates when they arrive.

- **Reform files, uprating, filing rule, app tests (2026-11-04).** A reform
  is a YAML file in `reforms/` (name, description, source, start, levers;
  values absolute or "+20%" relative to current law), loaded by
  `policyengine_pr/reforms/files.py`; the app's example reforms and the
  report CLI (`python -m policyengine_pr.analysis.report reforms/x.yaml
  out.md`) read them. PRCS incomes are uprated 2023 → 2025 by BLS QCEW
  average annual pay (×1.0815, `docs/statutes/uprating/`); a single factor
  for every income source is a simplification. `pr_files_return` applies
  the "who must file" rule (gross income net of exemptions > 0, ABT net
  income ≥ $25,000, or a Crédito por Trabajo claim); the calibration
  report shows the implied returns count (926k) against Hacienda's 1.2 M
  projection as a check, not a constraint. `tests/test_app.py` renders
  every page headlessly (Streamlit AppTest) in both languages.

- **Sección 8, comparison, shareable links (2026-11-04).** Housing Choice
  Vouchers are modelled under `gov/hud/section8/` from 24 CFR parts 5 and
  982 and HUD's FY2025 Puerto Rico tables (`docs/statutes/hud/`): annual and
  adjusted income (HOTMA $480 dependent / $525 elderly deductions), total
  tenant payment (30% adjusted, 10% gross floor), subsidy = min(payment
  standard, gross rent) − TTP, bedrooms at two per room. Only households
  flagged `housing_assisted` (an app input; the "voucher" preset) receive it,
  so Section 8 is not in reform scoring. PRPHA's Administrative Plan (June
  2025, avp.pr.gov) supplies the occupancy standard (head/spouse own
  bedroom, two per bedroom otherwise) and the $0 minimum rent. GAPS: San
  Juan-Guaynabo income limits and FMRs applied island-wide; the dollar
  payment-standard schedule and utility allowances unpublished (plan gives
  only the 90–110% band); no medical, disability or child-care deductions;
  HUD's Picture of Subsidized Households 2024 (PHA table, saved as
  `docs/statutes/hud/psh_2024_pr_vouchers.csv`): 33,948 vouchers across 75
  PHAs (PRPHA 12,437), average HAP $632 a month, average household income
  $7,183. **Imputed since 2026-11-04**: renter households within the very
  low income limit are drawn by stratum (member 62+, extremely low income)
  to HUD's shares and the weights are calibrated to 28,425 voucher
  households; the HAP total ($155 M) is 72% of HUD's $216 M (check only).
  Section 8 now enters reform scoring through household net income. CliffWatch gains a two-household comparison
  (presets, or the same adults unmarried → marriage penalty). The URL
  carries every non-default input and lever (`ui.sync_query_params`), so a
  calculator or CliffWatch view can be shared as a link.

## Launch checklist (target: March–April 2027)

| When | Step | Status |
|---|---|---|
| Nov 2026 | Send the four data requests (Hacienda, ADSEF, Salud, Vivienda) | letters drafted (Vivienda 4 Nov 2026) |
| Nov 2026 | Host the app (Streamlit Community Cloud, custom domain) | live at https://policyengine-pr.streamlit.app (4 Nov 2026); custom domain pending |
| Nov 2026 | CI, CONTRIBUTING guide, licence, public repo | CI green, guide done, repo public (4 Nov 2026); AGPL-3.0 (4 Nov 2026) |
| Nov–Dec 2026 | CPA validation of 10–15 real anonymised 2025 returns | workbook prepared |
| Dec 2026 | Calibration review (weights, tax-unit construction) | first pass 4 Nov 2026: 90% of weight ratios within 0.44–2.4, 0.1% of weight above 3 (large PAN households with EITC); PAN-only households scaled to 0.68, EITC households to 1.27. Tax-unit rules reviewed (spouse codes 21/23 joint, partners 22/24 separate, dependents <21 or student <26); re-check against Hacienda's tables |
| Dec 2026 | Reform report template, dry-run on a dummy reform | dry run 4 Nov 2026: EITC +20% with ETI 0.25, 2.3 s to Markdown, 0.1 s to Word; stale "not uprated" line fixed |
| Jan 2027 | Section 8 (HUD income limits, rent input); PAN resources test | both done 4 Nov 2026 (Section 8 with San Juan tables; PAN resources and care/student/medical deductions as inputs) |
| Jan 2027 | Behavioural response switch (ETI) on top brackets | done |
| Jan 2027 | Mobile layout and accessibility pass | first pass 4 Nov 2026: two-column metrics, smaller headings, wrapped chart subtitles, sidebar hint; every chart has a table view |
| Feb–Mar 2027 | Tax year 2026 parameters (instructions + BI RI EITC adjustment) | waits on Hacienda |
| Mar 2027 | Replace aggregate calibration with Hacienda's distributional tables | waits on Hacienda |
| Mar–Apr 2027 | Launch; score the reform proposal within days of release | — |

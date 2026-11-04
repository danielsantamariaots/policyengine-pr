# Sección 8 (Housing Choice Vouchers, HUD) — sources (2026-11-04)

Puerto Rico's vouchers are administered by the Administración de Vivienda
Pública (PRPHA, HUD code RQ005; 12,896 vouchers through nine regional
offices per the 2026 Annual Plan) and 74 municipal PHAs with another
21,500 vouchers (HUD Picture of Subsidized Households 2024: 33,948 in all,
about 2.7% of households). The federal
rules in 24 CFR parts 5 and 982 set the formula; PRPHA's Administrative
Plan (June 2025, on avp.pr.gov/reglamentacion) gives the subsidy standard
and the $0 minimum rent. Still unpublished: the dollar payment-standard
schedule (the plan only states the 90–110% of FMR band) and the utility
allowance schedule; both are flagged `gap:` in
`policyengine_pr/parameters/gov/hud/section8/`.

| File | Source | What it gives |
|---|---|---|
| HOME_IncomeLmts_State_PR_2025.pdf / .txt | https://www.hudexchange.info/resource/reportmanage/manage/?filter_Year=2025&filter_Scope=State&filter_State=PR&group=IncomeLmts&program=HOME | HUD FY2025 income limits (effective 1 April 2025) for every Puerto Rico FMR area, sizes 1–8: 30% limits, very low income (50%), 60% and low income (80%). San Juan-Guaynabo VERY LOW INCOME: 13,650 / 15,600 / 17,550 / 19,450 / 21,050 / 22,600 / 24,150 / 25,700. The Section 8 limits HUD publishes separately use the same VLI and ELI rows. |
| HOME_RentLimits_State_PR_2025.pdf / .txt | https://www.hudexchange.info/resource/reportmanage/manage/?filter_Year=2025&filter_Scope=State&filter_State=PR&group=RentLimits&program=HOME | HUD FY2025 HOME rents with the FY2025 **Fair Market Rent** row per area. San Juan-Guaynabo FMR: efficiency $552, 1 BR $569, 2 BR $656, 3 BR $861, 4 BR $1,033, 5 BR $1,188. (HUD's FMR dataset downloads returned empty responses to scripted requests; the HOME table is the saved copy.) |
| 24 CFR part 5, subpart F | https://www.ecfr.gov/current/title-24/subtitle-A/part-5/subpart-F | §5.403 elderly family (62+); §5.609 annual income (wages, net business income, pensions, Social Security, interest, dividends, welfare assistance; food benefits excluded); §5.611 deductions ($480 per dependent, $525 elderly/disabled family, as amended by HOTMA, 88 FR 9600); §5.628 total tenant payment (highest of 30% adjusted, 10% gross, welfare rent, minimum rent); §5.630 minimum rent $0–$50. |
| 24 CFR part 982 | https://www.ecfr.gov/current/title-24/subtitle-B/chapter-IX/part-982 | §982.201 admission limited to very low-income families (75% extremely low); §982.402 subsidy standard, at most two persons per bedroom; §982.503 payment standard 90–110% of FMR; §982.505 HAP = lower of payment standard and gross rent, less TTP; §982.455 voucher ends 180 days after HAP reaches zero. |
| PRPHA_Administrative_Plan_Section8_June2025.pdf / .txt | https://docs.pr.gov/files/Vivienda/avp.pr.gov/Reglamentaci%C3%B3n/PRPHA_Administrative_Plan_SECTION_8_AMENDMENT_JUNE%20_2025.pdf (avp.pr.gov → Reglamentación) | PRPHA Housing Choice Voucher Administrative Plan, amended 20 June 2025, 159 pp. Sec. VI.A payment standards 90–110% of FMR, set annually, hold harmless; VI.B occupancy standards (two per bedroom, head/spouse separate bedroom, one-person family → 1 BR, table 0–6 BR); VI.D family share (highest of 10% gross, 30% adjusted, **minimum rent $0**); VI.E / Sec. on adjusted income ($480 dependent, $400 elderly in the plan text, i.e. pre-HOTMA; child care, medical > 3%, disability expenses); Sec. XIV HOTMA chapter. |
| PRPHA_Annual_Plan_2026.pdf / .txt | https://docs.pr.gov/files/Vivienda/avp.pr.gov/Reglamentaci%C3%B3n/Plan_2026/PHA_Annual_Plan_2026_Final.pdf | PHA Annual Plan 2026: 12,863 HCVs on the HUD form (12,896 in the text), nine regional offices with their municipalities. No HAP totals. |
| psh_2024_pr_vouchers.csv (from PHA_2024_2020census.xlsx, kept in data/raw/hud/, git-ignored) | https://www.huduser.gov/portal/datasets/assthsg.html → Data → 2024 → Public Housing Agency (downloaded in a browser 2026-11-04; a 2025 file also exists) | HUD Picture of Subsidized Households, extract of 31 Dec 2024, Housing Choice Voucher rows for the 75 Puerto Rico PHAs. **33,948 vouchers in all**: PRPHA RQ005 12,437 (90% occupied), San Juan RQ006 4,715, Bayamón RQ011 2,225, Ponce 1,580, Caguas 1,405, Arecibo 933, Mayagüez 848, Carolina 808, and 67 smaller municipal PHAs. Unit-weighted averages: HAP **$632 a month**, tenant rent $170, household income **$7,183 a year**; 61–75% of households below 30% of area median; main income source wages 28% (PRPHA), welfare 6%, other (SS, pensions) 63%; head aged 62+ 34% (PRPHA); one-adult households 36%; bedroom mix PRPHA 35% 1 BR, 23% 2 BR, 42% 3+ BR. |
| HUD FY2025 FMR Documentation System (one page per municipio, read in a browser 4 Nov 2026; e.g. fips=7212799999 for San Juan) | https://www.huduser.gov/portal/datasets/fmr/fmrs/FY2025_code/2025summary.odn?fips=7212799999&year=2025&selection_type=county&data=2025 | FY2025 FMRs by bedroom and the municipios in each of the 11 FMR areas: San Juan-Guaynabo HMFA (28 municipios), Caguas (5), Fajardo (3), Barranquitas-Aibonito (4), Aguadilla-Isabela MSA (9, incl. Lares and Utuado), Arecibo (4), Guayama (3), Mayagüez (3, incl. Las Marías), San Germán (4), Ponce (4, incl. Adjuntas), Yauco (4); the other 7 municipios (Coamo, Culebra, Jayuya, Maricao, Salinas, Santa Isabel, Vieques) are the Nonmetro area. Income limits carve Adjuntas, Lares-Utuado and Las Marías out as exception areas (HOME table). Encoded in `policyengine_pr/data/hud_areas.py`. |
| psh_2025_pr_vouchers.csv (from PHA_2025_2020census.xlsx, git-ignored) | same HUD page, 2025 row (downloaded 4 Nov 2026) | Extract of 31 Dec 2025: 74 PHAs, 33,883 vouchers, 27,948 in use (82.5%), HAP $634 a month, household income $7,634, 27.5% head 62+, 62.6% below 30% of median, wages the main income for 31%. The 2025 file splits tenant-based (29,893) and project-based (3,946) vouchers; the CSV keeps the all-voucher row per PHA. |
| 89 FR 27377 (17 Apr 2024) | https://www.govinfo.gov/content/pkg/FR-2024-04-17/html/2024-08133.htm | HUD methodology for the annual inflation adjustment of the HOTMA amounts; 2024 dependent deduction $480. |
| Arizona Dept. of Housing IB-67-24 (Oct 2024) | https://housing.az.gov/sites/default/files/2024-10/IB-67-24-HOTMA-Implementation-Date-Extended.pdf | Secondary source: 2025 amounts unchanged, $480 dependent and $525 elderly/disabled. HUD's 2025 notice not yet saved. |

## What the model does

- Only households flagged `housing_assisted` get a subsidy. In the app it
  is an input; in the PRCS microdata it is imputed (since 2026-11-04) to
  renter households within the very low income limit, drawn at random
  within four strata (member 62+, income below the extremely low limit) to
  HUD's shares, and calibrated to 28,425 voucher households in use. The
  modelled HAP total ($142 M) is 66% of HUD's $216 M (28,425 × $632 × 12),
  consistent with PRPHA paying above 100% of the San Juan FMR or with
  lower incomes among actual voucher holders; reported as a check in
  `data/calibration_report.csv`.
- Annual income = wages + net self-employment profit + pensions + Social
  Security + interest + dividends + TANF. Adjusted income subtracts $480
  per member under 18 and $525 if any member is 62 or over.
- `hud_area` (input; 15 areas) selects the income limits and FMRs; the app
  offers a municipio list, the PRCS assigns it from the PUMA (PUMAs that
  span areas take the majority area).
- Bedrooms = 1 for the head/spouse plus ceil(others / 2) (PRPHA Sec. VI.B),
  capped at 5; payment standard = the area's FMR
  for that size; TTP = max(30% adjusted, 10% gross, $0); HAP = (min(payment
  standard, gross rent) − TTP) × 12, never negative. `housing_rent` = 0
  means the rent equals the payment standard.
- `section8_income_eligible` reports the admission test against the San
  Juan very low income limit; it does not switch the subsidy off (982.455).

## Gaps to close with Vivienda

1. Payment-standard dollar schedule by bedroom size and FMR area (982.503);
   the plan states only the 90–110% band.
2. Utility allowance schedule (gross rent = rent + allowance).
3. Share of vouchers by regional office / FMR area (HUD's Picture of
   Subsidized Households gives PHA totals, which the municipal PHAs map
   to municipios; PRPHA's 12,400 are island-wide).
4. Medical, disability-assistance and child-care deductions (§5.611(a)(3)–(4)):
   amounts are household-specific, so they need inputs rather than data.
5. Whether PRPHA applies the HOTMA $525 elderly deduction (the June 2025
   plan text still says $400).

The data request letter for these gaps is `docs/solicitud_datos_vivienda.md` (.docx alongside).

## Official statistics sources for Sección 8 in Puerto Rico (surveyed 2026-11-04)

| Source | What it gives | Access |
|---|---|---|
| HUD, Picture of Subsidized Households (huduser.gov/portal/datasets/assthsg.html) | Annual (2024 latest), by PHA / county / place / tract: subsidized units, people, average HUD expenditure per unit per month, average household income, income as % of area median, household composition, race, age of head, months on assistance. Separate rows for HCV, public housing, PBRA. | Public .xlsx; the server refuses scripted requests, download in a browser (`PHA_2024_2020census.xlsx`). |
| HUD PIH, Housing Choice Voucher Data Dashboard (hud.gov/helping-americans/public-indian-housing-hcv-dashboard) | Monthly, from the Voucher Management System: vouchers authorised and leased, HAP expenditure, per-unit cost, reserves, leasing potential, admissions and attrition; drill-down to state and PHA (RQ005 PRPHA, RQ006 San Juan, …). Two-month lag. | Tableau dashboard; data dictionary PDF (HCVDashboard_User_Guide_Data_Dictionary.pdf). |
| HUD PIH, Resident Characteristics Report (PIC/IMS) | Household income distribution, income sources, family type and bedroom size for HCV and public housing residents by PHA. | Public query page on hud.gov (PIH data systems); confirm current URL. |
| HUD, HCV funding and renewal tables (PIH Notices, annual "HCV Funding Awards" by PHA) | Annual budget authority and administrative fees per PHA. | Public spreadsheets on hud.gov. |
| HUD, FMRs and income limits (huduser.gov datasets) | Fair market rents (FY2025 PR areas) and Section 8 income limits by FMR area and size. | Public; the HOME tables saved here carry the same rows. |
| PRPHA, PHA Annual Plan (avp.pr.gov → Reglamentación) | Vouchers under ACC (12,863 on the 2026 form; 12,896 in the text), regional offices, PBV projects, goals. | Public PDF (PRPHA_Annual_Plan_2026.pdf). |
| PRPHA, Administrative Plan (June 2025) | Rules: occupancy standard, payment-standard band, minimum rent, deductions, preferences. | Public PDF (saved here). |
| AVP, Informe de Transición 2024, Sección 8 (transicion2024.pr.gov) | HUD-authorised vouchers 12,332; new vouchers issued 2021–2024 (636, 1,072, 523, 478); 104 Mainstream and 203 Emergency Housing Vouchers; landlord incentive programme (2,072 landlords, $4.0 M); 12 PBV elderly projects. | Public PDF (AVP_Informe_Transicion_2024_Seccion8.pdf, saved here). |
| Press (Primera Hora, AVP administrator) | 12,875 vouchers, 11,431 contracts; most contracts in San Juan, Bayamón and Carolina. | Secondary; date to be confirmed. |
| Not found | Instituto de Estadísticas de PR, Junta de Planificación and Oficina del Contralor publish nothing specific to the voucher programme; the Contralor's audits of AVP cover public housing. | — |

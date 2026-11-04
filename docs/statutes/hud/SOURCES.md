# Sección 8 (Housing Choice Vouchers, HUD) — sources (2026-11-04)

Puerto Rico's vouchers are administered by the Administración de Vivienda
Pública (PRPHA, HUD code RQ005; 12,896 vouchers through nine regional
offices per the 2026 Annual Plan) and a few municipal PHAs. The federal
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
| (not downloaded) HUD Picture of Subsidized Households 2024 | https://www.huduser.gov/portal/datasets/assthsg.html → PHA_2024_2020census.xlsx | PHA-level 2024 table with subsidized units, average HUD expenditure per month, household income and composition for RQ005 and the municipal PHAs. Public; the download needs a browser (scripted requests are refused). Use it to calibrate voucher counts and average HAP. |
| 89 FR 27377 (17 Apr 2024) | https://www.govinfo.gov/content/pkg/FR-2024-04-17/html/2024-08133.htm | HUD methodology for the annual inflation adjustment of the HOTMA amounts; 2024 dependent deduction $480. |
| Arizona Dept. of Housing IB-67-24 (Oct 2024) | https://housing.az.gov/sites/default/files/2024-10/IB-67-24-HOTMA-Implementation-Date-Extended.pdf | Secondary source: 2025 amounts unchanged, $480 dependent and $525 elderly/disabled. HUD's 2025 notice not yet saved. |

## What the model does

- Only households flagged `housing_assisted` (an app input) get a subsidy;
  voucher receipt is not imputed in the PRCS microdata, so Section 8 does
  not enter reform scoring.
- Annual income = wages + net self-employment profit + pensions + Social
  Security + interest + dividends + TANF. Adjusted income subtracts $480
  per member under 18 and $525 if any member is 62 or over.
- Bedrooms = 1 for the head/spouse plus ceil(others / 2) (PRPHA Sec. VI.B),
  capped at 5; payment standard = San Juan FMR
  for that size; TTP = max(30% adjusted, 10% gross, $0); HAP = (min(payment
  standard, gross rent) − TTP) × 12, never negative. `housing_rent` = 0
  means the rent equals the payment standard.
- `section8_income_eligible` reports the admission test against the San
  Juan very low income limit; it does not switch the subsidy off (982.455).

## Gaps to close with Vivienda

1. Payment-standard dollar schedule by bedroom size and FMR area (982.503);
   the plan states only the 90–110% band.
2. Utility allowance schedule (gross rent = rent + allowance).
3. Share of vouchers by regional office / FMR area, to apply the other
   seven areas' income limits and FMRs (HUD's Picture of Subsidized
   Households gives PHA totals, not areas).
4. Medical, disability-assistance and child-care deductions (§5.611(a)(3)–(4)):
   amounts are household-specific, so they need inputs rather than data.
5. Whether PRPHA applies the HOTMA $525 elderly deduction (the June 2025
   plan text still says $400).

The data request letter for these gaps is `docs/solicitud_datos_vivienda.md` (.docx alongside).

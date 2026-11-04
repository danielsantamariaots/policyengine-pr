# Calibration targets — sources (downloaded 2026-11-04)

Administrative totals used to reweight the PRCS 2023 PUMS households
(`policyengine_pr/data/calibration_targets.yaml`, method in
`policyengine_pr/data/calibration.py`).

| File | Source | What it gives |
|---|---|---|
| hacienda_recaudos_cierre_af2023-2024.pdf / .txt | https://hacienda.pr.gov/sites/default/files/comunicado_de_prensa_de_recaudos_cierre_af2023-2024_rev.pdf | Hacienda press release, preliminary close of FY2023-24 General Fund net revenue. "Individuos" $2,615.5 M (FY2022-23: $2,883.3 M; projection $2,604.0 M). The release attributes the $268 M fall to "la distribución del Incentivo Reintegrable" in FY2023-24, i.e. the figure is net of refundable-credit refunds. |
| hacienda_ingresos_netos_fondo_general_mayo_fy25.pdf / .txt | https://hacienda.pr.gov/sites/default/files/ingresos_netos_al_fondo_general_may_fy25_07.01.2025_r.pdf | Monthly net-revenue table, FY2024-25 through May (thousands): Individuos actual July–May $2,499,275 (FY2023-24 same months: $2,804,767); FY2024-25 projection through May $2,585,394. Kept for the FY2025 update of the net-tax target. |
| hacienda_comunicado_credito_por_trabajo_2024.html / .txt | https://hacienda.pr.gov/sobre-hacienda/sala-de-prensa-virtual/comunicados-de-prensa/secretario-de-hacienda-anuncia-aumento-en-el-credito-por-trabajo-para-el-ano-contributivo-2024 | Hacienda press release, 26 Dec 2024: ciclo contributivo 2023 (tax year 2023) "cerca de $1,303 millones en Crédito por Trabajo, beneficiando a cerca de 700,000 familias"; tax year 2024 estimate $1,432 M. |
| fns_keydata_feb2025.pdf / .txt | https://fns-prod.azureedge.us/sites/default/files/data-files/keydata-feb2025.pdf | USDA FNS Program Information Report (Keydata), Table 2b "Nutrition Assistance Program – Puerto Rico": FY2024 average 738,510 households, 1,274,983 persons, $2,928,990,448 benefits (food cost); FY2025 Oct–Jan 730,260 households, 1,249,567 persons. |

Not yet used:
- Number of individual returns: Hacienda reported 1,038,899 returns filed a week before the 15 April 2024 deadline and projected 1.2 million for the cycle (press release "Más de un millón de planillas radicadas…"). The model's tax units are every adult, not filers, so a filer count needs a filing rule first.
- Hacienda's statistical tabulations by AGI bracket (the data request in docs/solicitud_datos_hacienda.docx) would replace these aggregate targets with distributional ones.

## Method

Entropy (minimum-discrimination) reweighting of household weights: minimise
Σ w log(w/w₀) subject to the seven aggregate constraints, solved by Newton
iterations on the dual. Person and tax-unit weights are scaled by the same
household ratio. After calibration all targets are met exactly; the ratio
of calibrated to survey weights ranges from 0.07 to 4.45 (5th–95th
percentile 0.59–1.95).

## Caveats

- Net income tax: the model's `pr_income_tax − pr_eitc` is matched to a
  fiscal-year cash figure (withholding on 2024 incomes, refunds for tax year
  2023); timing and other refunds are ignored.
- PAN: the model pays the maximum benefit to every eligible household (no
  take-up, no resources test); matching the caseload therefore lowers the
  weight of eligible households rather than modelling non-participation.
- EITC claimants: the survey finds 550k eligible units against 700k
  claimants, so the calibration raises the weight of EITC-eligible units;
  part of the gap is the tax-unit construction (other adults filing
  singly) and under-reported self-employment income in the PRCS.

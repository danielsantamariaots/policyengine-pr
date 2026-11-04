# Uprating — sources (downloaded 2026-11-04)

The PRCS 2023 incomes are expressed in 2023 dollars (PUMS ADJINC). To
simulate the 2025 tax year they are uprated by the growth of average
annual pay in Puerto Rico from the BLS Quarterly Census of Employment and
Wages (all ownerships, all industries, statewide area 72000).

| File | Source | Figure |
|---|---|---|
| qcew_pr_2023_annual.csv | https://data.bls.gov/cew/data/api/2023/a/area/72000.csv | average annual pay $33,673; 938,018 employed; total wages $31.59 bn |
| qcew_pr_2024_annual.csv | https://data.bls.gov/cew/data/api/2024/a/area/72000.csv | $35,285; 947,908; $33.45 bn |
| qcew_pr_2025_annual.csv | https://data.bls.gov/cew/data/api/2025/a/area/72000.csv | $36,419; 947,557; $34.51 bn |

Factor 2023 → 2025: 36,419 / 33,673 = 1.0815. Applied to every money
input (wages, self-employment, pensions, Social Security, interest). A
single factor is a simplification: Social Security benefits rose by the
COLA (3.2% for 2024, 2.5% for 2025 = 1.058), pensions by less; a per-source
index is a later refinement. Parameter: `gov/data/uprating/average_annual_pay.yaml`.

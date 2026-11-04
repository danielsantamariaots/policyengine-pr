# data/

- `prcs_2023_calibrated.h5` — the model dataset: PRCS 2023 PUMS households
  for Puerto Rico with weights calibrated to administrative totals
  (`policyengine_pr/data/`). Committed (2.8 MB) so the hosted app can score
  reforms without the raw files. Rebuild with `build_prcs(); build_calibrated()`.
- `raw/` and `prcs_2023.h5` — not in git. Raw PUMS files are public:
  https://www2.census.gov/programs-surveys/acs/data/pums/2023/1-Year/

- `raw/hud/PHA_2024_2020census.xlsx`: HUD Picture of Subsidized Households 2024, PHA table (downloaded from huduser.gov in a browser). The Puerto Rico voucher rows are committed as `docs/statutes/hud/psh_2024_pr_vouchers.csv`.

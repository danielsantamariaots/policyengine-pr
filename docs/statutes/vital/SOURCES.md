# Plan Vital (Medicaid / CHIP in Puerto Rico) — sources (2026-11-04)

| File | Source | What it gives |
|---|---|---|
| medicaid_gov_puerto_rico_2026_table.md | https://www.medicaid.gov/state-overviews/puerto-rico.html (read in the browser; the page is JavaScript-rendered) | CMS, "Medicaid and CHIP Standard Monthly Income Eligibility Levels effective April 1, 2026 to April 2027": Medicaid $1,835 (1), $2,489 (2), $3,142 (3), $3,795 (4); CHIP $3,604 (1), $4,887 (2), $6,170 (3), $7,453 (4). Eligibility is MAGI-based; 1.3 million enrolled in January 2026. |
| medicaid_gov_puerto_rico_2026.html / .txt | same URL, raw download | Page shell without the table (kept for provenance). |
| medicaid_pr_cms_20.bin | https://medicaid.pr.gov/CMS/20 (cited by CMS as the source) | Estadísticas page of the Programa Medicaid, Departamento de Salud; no table in the HTML. |
| requisitos_medicaid.pdf / .txt | https://www.medicaid.pr.gov/CMS/DOCUMENTO/430 | Programa Medicaid, "Documentos necesarios para evaluar su solicitud": documentary requirements only. |

## What the levels are

The Medicaid column equals 138% of the 2026 HHS poverty guideline
($15,960 + $5,680 per additional person): 1.38 × 15,960 / 12 = $1,835.40;
increment $653.44. The CHIP column equals 271% (266% + the 5-point MAGI
disregard): $3,604.30; increment $1,282.73. These percentages are our
reading of the table; CMS's text says only that Puerto Rico "uses the
federal poverty level". Household sizes above 4 extend by the increment.

## Rules modelled

- Household MAGI (wages, self-employment, pensions, Social Security,
  interest, dividends, capital gains; monthly = annual / 12) compared with
  the limit for the household size.
- Adults and children: Medicaid limit. Children under 19: CHIP limit when
  above the Medicaid limit.
- No cash value is assigned to coverage; the model reports eligibility
  (persons covered) only.

## Open items

1. The April 2025 – March 2026 levels (the model applies the 2026 table to
   the 2025 tax year; the derived 2025 values — $1,799.75 and $3,534.29 —
   are noted in the table file but not used).
2. Non-MAGI groups (aged, blind, disabled; SSI-like), the medically needy
   pathway, resource tests, and the Puerto Rico-specific income deductions
   that third-party guides mention (medical, child care, housing) — not
   found in an official source.
3. Enrollment targets for calibration: CMS enrollment reports for Puerto
   Rico (1.3 million, January 2026).

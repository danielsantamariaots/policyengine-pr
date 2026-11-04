# Programa de Asistencia Nutricional (PAN / NAP) — sources (downloaded 2026-11-04)

PAN is Puerto Rico's block-grant replacement for SNAP (Food and Nutrition
Act of 2008, Section 19). ADSEF (Departamento de la Familia) sets the rules
in Reglamento 8684 and the dollar amounts in an annual **NAP State Plan of
Operations (SPO)** approved by USDA FNS. The dollar amounts are NOT in the
reglamento, which refers to "la Tabla" (Art. 5, definition 69) for both the
income limits and the benefit by net income.

| File | Source | Notes |
|---|---|---|
| reglamento_8684_pan_2015.pdf / .txt | https://docs.pr.gov/files/Familia/Reglamentos/Reglamento%208684%20-%20Reglamento%20para%20establecer%20las%20normas%20de%20elegibilidad%20del%20programa%20de%20asistencia%20nutricional%20(PAN).pdf | Reglamento 8684 of 28 Dec 2015, scanned with embedded OCR (garbled accents; ".txt" is `pdftotext -layout`). Rules, not amounts. |
| adsef_reglamento_pan_8684_copia_adsef.pdf | https://serviciosenlinea.adsef.pr.gov/documents/1.ReglamentoPAN.pdf | ADSEF's own copy, 127 pp., image-only. Same page count as above. |
| adsef_reglamento_tanf_7653.pdf | https://serviciosenlinea.adsef.pr.gov/documents/2.ReglamentoTANF.pdf | TANF reglamento 7653, for the later TANF provision. Image-only. |
| nap_state_plan_fy2023_adsef.pdf | https://serviciosenlinea.adsef.pr.gov/documents/NAP-STATE-PLAN-FIRMADO.pdf | Linked by ADSEF as "PR NAP STATE PLAN 2023" but the cover reads **"NAP State Plan of Operations FY 2022"**; 86 pp., scanned, no text layer (the .txt is empty). Pages read visually: 1–6 (contents), 24–32 (section VII, criteria). |
| adsef_ponencia_transicion_2024-10-30.pdf / .txt | https://transicion2024.pr.gov/Agencias/127/Ponencias/PONENCIA%20ADSEF%20PDF.pdf | ADSEF's statement to the 2024 transition committee. Official 2021–2024 one-person figures (p. 6) and the list of 2024 amendments. |
| adsef_pan_requisitos.pdf / .txt | https://serviciosenlinea.adsef.pr.gov/adsefdigital/Pdf/PAN%20Requisitos.pdf | Documentary requirements, not rules. |
| reglamento_9574_podes_2024.pdf | https://aldia.microjuris.com/wp-content/uploads/2024/07/Numeric_9000_9574.pdf | Reglamento 9574 (July 2024) is for PODES, not PAN; kept because it states that PAN income limits are "la tabla de beneficios del PAN vigente". |

## Rules (Reglamento 8684, 2015; SPO FY2022 section VII)

- **Unit:** "núcleo de servicio", the people who buy and prepare food
  together.
- **Gross income:** all members' monthly income (Art. 42 conversions:
  weekly × 4.3, biweekly × 2.15, semimonthly × 2). Self-employment net of
  production costs (Art. 44). Since September 2018 (FNS approval August
  2018) only **50% of retirement, veterans' and Social Security income**
  is counted (SPO p. 26); the 2024 amendment extended the 50% treatment to
  unemployment income (ADSEF statement p. 5).
- **Deductions** (Art. 45; SPO pp. 26–27; FY2022 amounts):
  - earned income (wages, training, self-employment): 50% up to a cap
    ($700 from October 2021; $600 in 2021 per the ADSEF table; $900 in
    2022, $1,100 in 2023, $1,400 from August 2024), or a fixed $100 if 50%
    is below $100;
  - other income (pensions, child support, SS, unemployment, help from
    relatives): fixed $100, not combinable with the earned-income
    deduction;
  - agriculture (bona fide farmers and farm workers): $760 (2021–2023),
    $903 (2024); approved harvest products: 100% exempt;
  - special: $100 per student, $100 per person 60+, $100 per totally
    disabled person (not both), $100 recurrent medical expenses
    (elderly/disabled/children), $100 terminally ill;
  - dependent care when needed to work/train: $225 per child aged 2 or
    under, $200 per child/adult over 2;
  - standard deduction for every household: $100 (2021), $184 (2022),
    $198 (2023), $279 (from August 2024).
- **Eligibility:** net income ≤ the limit for the household size. **No
  gross income test** (FNS summary, https://www.fns.usda.gov/nap/pr/summary,
  2026-03-30).
- **Resources:** $5,000; $15,000 if a member is 60+ (SPO p. 28) or
  totally disabled (2024 amendment). SSA disability, TANF and government
  disability pensions are not counted.
- **Benefit:** read from the Tabla by household size and net income; the
  maximum applies at zero income and the benefit falls as net income
  rises (SPO p. 29; Art. 51.A). Benefits may vary with available funds
  (Art. 51.B); ADSEF also distributes carry-overs as a monthly percentage
  adjustment (SPO p. 30).
- **Elderly bonus:** each person 60+ adds 20% of the one-person zero-income
  quota (Art. 51.C): $28 (2021), $33 (2022), $37 (2023–2024).
- **Vieques and Culebra:** higher maximum benefit ($219 vs $183 for one
  person in 2023–2024).
- **Family Markets:** 4% of benefits reserved for local produce (SPO p. 30).
- **New-job exemption:** gross earnings of a participant who starts a job
  exempt 100% months 1–6, 66% months 7–12, 33% months 13–18 (SPO p. 29);
  extended in 2024 to 12 months at 100%, 6 at 66%, then 33% to month 24.

## Maximum monthly net income and maximum benefit by household size

SPO FY2022, p. 28, "effective date October 2021". Maximum benefits reflect
the 23% increase approved by USDA in 2021.

| Size | Net income limit | Max benefit | Size | Net income limit | Max benefit |
|---|---|---|---|---|---|
| 1 | $619 | $140 | 10 | $5,152 | $1,053 |
| 2 | $1,179 | $257 | 11 | $5,666 | $1,158 |
| 3 | $1,706 | $368 | 12 | $6,186 | $1,263 |
| 4 | $2,206 | $468 | 13 | $6,699 | $1,369 |
| 5 | $2,666 | $556 | 14 | $7,219 | $1,474 |
| 6 | $3,199 | $666 | 15 | $7,732 | $1,579 |
| 7 | $3,599 | $737 | 16 | $8,252 | $1,684 |
| 8 | $4,112 | $842 | 17 | $8,766 | $1,790 |
| 9 | $4,632 | $948 | 18 | $9,286 | $1,895 |

Add $28 per elderly member. (The same page lists the SNAP maximum for the
48 states and DC for comparison: $250 for one person.)

## Later official changes (one-person household; ADSEF statement p. 6)

| | 2021 | 2022 | 2023 | 2024 |
|---|---|---|---|---|
| Maximum net income | $619 | $619 | $619 | $619 (→ $633 Aug 2024) |
| Maximum benefit | $140 | $165 | $183 | $183 |
| Maximum benefit, Vieques y Culebra | $140 | $198 | $219 | $219 |
| Elderly bonus | $28 | $33 | $37 | $37 |
| Earned-income deduction cap (50%) | $600 | $900 | $1,100 | $1,400 |
| Fixed deduction | $100 | $184 | $198 | $279 |
| Agricultural income deduction | $760 | $760 | $760 | $903 |

August 2024 amendment (Departamento de la Familia, reported by Metro PR
and Sin Comillas on 2024-08-11): fixed deduction $198 → $279; one-person
maximum net income $619 → $633; earned-income cap $1,100 → $1,400; 50%
counting extended to unemployment income; resource limit $15,000 also for
totally disabled members; 30 days to report changes.
- https://www.metro.pr/noticias/2024/08/11/anuncian-aumento-en-los-niveles-de-elegibilidad-del-pan-tras-incremento-en-el-salario-minimo/
- https://sincomillas.com/ajustan-los-niveles-de-elegibilidad-para-beneficiarios-del-pan/

## Open items (needed before PAN can be modelled to the CLAUDE.md standard)

1. **The Tabla de Beneficios itself** — the benefit for each net-income
   band between $0 and the limit, by household size. Neither the reglamento
   nor the SPO prints it. Without it the model can only give the maximum
   benefit and the eligibility cut-off. Request from ADSEF (or from
   Hacienda's data unit, which receives PAN data) together with the
   current FY2026 limits.
2. **FY2025/FY2026 state plans** — not published; FNS posts only the
   approval letter (FY2026 grant $2,978,891,000;
   https://www.fns.usda.gov/nap/pr/state-plan-operations). The 2024
   multi-size limits can be approximated by scaling the October 2021 table
   by 633/619 only as a stopgap, flagged as such.
3. The 2024 amendment to Reglamento 8684 as a numbered reglamento.
4. Third-party 2025–26 tables online (coquilist.com, puertoricoguias.com,
   entrepagosycuentas.com) give a one-person net cap of ~$1,025 and "gross
   limits"; they contradict FNS's statement that NAP has no gross income
   test and ADSEF's $633. Not used.

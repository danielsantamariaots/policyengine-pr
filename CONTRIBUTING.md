# Contributing to policyengine-pr

## Setup

```bash
git clone https://github.com/danielsantamariaots/policyengine-pr
cd policyengine-pr
uv venv --python 3.12 .venv && source .venv/bin/activate
uv pip install -e ".[dev,app]"
make test            # 98 tests
streamlit run app/calculator.py
```

The microdata is not in git. To build it: download the 2023 Puerto Rico
PUMS (`csv_ppr.zip`, `csv_hpr.zip` from
https://www2.census.gov/programs-surveys/acs/data/pums/2023/1-Year/) into
`data/raw/pums_2023/`, unzip, then

```bash
python -c "from policyengine_pr.data import build_prcs, build_calibrated; build_prcs(); build_calibrated()"
```

## How a provision is added (the only workflow)

1. **Get the official text first.** Download the statute, form or
   instruction booklet into `docs/statutes/<agency>/` and record it in that
   folder's `SOURCES.md` with the URL and date. Never write a rule from
   memory; if the document is not there, stop and ask for it.
2. **Parameters.** One YAML per amount under `policyengine_pr/parameters/`,
   mirroring the Código's structure. Every file has `reference:` (section
   and URL, with the page). Anything a reform could change is a parameter,
   not a number in a formula. Dated values; when a value is a stopgap, say
   so in a `gap:` field.
3. **Variables.** One class per file under `policyengine_pr/variables/`,
   `documentation` naming the form line. Use `adds`/`subtracts` when the
   variable is a sum; `formula` otherwise. Household-level programs live
   under `gov/<agency>/<program>/`.
4. **Tests.** A YAML test under `policyengine_pr/tests/` with values
   computed by hand from the official worksheet, and a comment saying
   which. Test names containing a colon must be quoted.
5. **App.** If the provision produces a household-visible amount, add a row
   to `OUTPUTS` in `app/calculator.py` (with the plain-language gloss) and,
   if it is a benefit or tax, a series in `app/cliffwatch.py` (validate the
   colour with the dataviz palette script).
6. **Docs.** Update ROADMAP.md (scope note), docs/TUTORIAL.md and the
   "not included" text in `app/ui.py`.
7. `make test`, `ruff format`, commit with the Código section in the
   message, push. CI runs the tests on every push.

## Conventions

- Spanish labels in the app and docs; English second. Code and commit
  messages in English.
- Amounts exactly as the law states; no rounding or indexing unless the
  law prescribes it.
- Flag anything uncertain in the parameter's `gap:` field and in the app's
  "Qué no incluye" box rather than guessing.

## Scoring a reform

A reform is one YAML file in `reforms/`:

```yaml
name: Ampliar el tramo de 0% a $12,000
name_en: Widen the 0% bracket to $12,000
description: ...
source: Proyecto de la Cámara 1234, 15 de marzo de 2027
start: 2025-01-01
levers:
  gov.hacienda.income.rates[1].threshold: 12000
  gov.hacienda.credits.eitc.max.0: "+20%"     # relative to current law
```

Lever paths are parameter paths (`rates[1]` indexes a bracket). The app
lists every file in `reforms/` under *Reformas de ejemplo* and on the
*Reformas* page; the two-page report is
`python -m policyengine_pr.analysis.report reforms/<file>.yaml docs/informes/<name>.md [eti]`,
then `node docs/hacienda/fuentes_documentos/md2docx.js <md> <docx>`.

## Updating a tax year

When Hacienda publishes the next year's instructions and the Crédito por
Trabajo inflation adjustment (Boletín Informativo, February), add a new
dated value to every parameter that changed, add the booklet to
`docs/statutes/hacienda_<year>/`, bump `YEAR` in `app/calculator.py`,
`app/cliffwatch.py` and `app/ui.py`, and re-run the tests with the new
year's hand computations.

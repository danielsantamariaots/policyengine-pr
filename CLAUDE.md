# policyengine-pr

Open-source tax-benefit microsimulation model of Puerto Rico, built on
policyengine-core (same architecture as policyengine-canada / -us).
Target: public launch March–April 2027, ready to score a PR tax reform
proposal within days of its release. See ROADMAP.md.

## Conventions
- One variable per file under policyengine_pr/variables/, mirroring the
  Código de Rentas Internas de 2011 (Ley 1-2011) structure
  (variables/gov/hacienda/...). Parameters mirror the same tree.
- Every parameter YAML has a `reference:` with the Código section (e.g.
  "Sección 1021.01, Ley 1-2011, as amended by Ley 52-2022") and a URL
  to the official text where available. No parameter without a source.
- Every formula has at least one YAML test under policyengine_pr/tests/,
  with values computed by hand from an official Hacienda worksheet or
  instruction booklet, and a comment saying which.
- Do NOT write tax rules from memory. If the statute text is not in
  docs/statutes/ or provided in the conversation, stop and ask for it.
  Flag anything uncertain rather than guessing.
- Amounts and thresholds exactly as the law states; no rounding or
  indexing unless the law prescribes it.
- Anything a reform could plausibly change must be a parameter, not a
  hard-coded number in a formula (speed of scoring reforms is the product).
- Run `make test` before every commit. Commit small, one provision at a
  time, with the Código section in the commit message.

## Dev
- venv: .venv (Python 3.12). `source .venv/bin/activate && make test`.
- Tests run through `python -m policyengine_core.scripts.policyengine_command test`.

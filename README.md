# policyengine-pr

Open-source tax-benefit microsimulation model of Puerto Rico. Live app: https://policyengine-pr.streamlit.app, built on
[policyengine-core](https://github.com/PolicyEngine/policyengine-core).

Status: scaffold only. Phase 1 covers the individual income tax under the
Código de Rentas Internas de 2011 (Ley 1-2011), PR EITC and PR CTC.

## Setup

```bash
python3.12 -m venv .venv && source .venv/bin/activate
make install
make test
```

Statute texts used as sources live in `docs/statutes/`.

## Prototype calculator

User guide (Spanish and English): [docs/TUTORIAL.md](docs/TUTORIAL.md).

```bash
uv pip install -e ".[app]"
streamlit run app/calculator.py
```

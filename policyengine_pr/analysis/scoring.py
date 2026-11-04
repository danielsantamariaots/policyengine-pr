"""Score a reform on the PRCS microdata: revenue, distribution, winners.

Usage::

    from policyengine_pr.analysis.scoring import score
    from policyengine_pr.reforms.parametric import parametric_reform

    result = score(parametric_reform({"gov.hacienda.income.rates[1].threshold": 12_000}))
    result["totals"]        # DataFrame: baseline, reform, change per aggregate
    result["deciles"]       # DataFrame: by household net-income decile
    result["summary"]       # dict of headline numbers

Caveats (see policyengine_pr/data/prcs.py): the PRCS sample is not yet
calibrated to Hacienda's return totals, incomes are 2023 dollars simulated
under 2025 rules, and PAN is paid at the maximum to every eligible
household. Treat levels as indicative and changes as the useful output.
"""

import numpy as np
import pandas as pd

from policyengine_pr import Simulation
from policyengine_pr.data import PRCS

YEAR = 2025
AGGREGATES = [
    ("pr_income_tax", "Contribución sobre ingresos de PR", "PR income tax"),
    ("pr_eitc", "Crédito por Trabajo", "Crédito por Trabajo"),
    ("federal_actc", "Crédito federal por hijos", "Federal child credit"),
    ("pan", "PAN", "PAN"),
    (
        "household_net_income",
        "Ingreso neto de los hogares",
        "Household net income",
    ),
]


def _household_frame(sim):
    w = sim.calculate("household_weight", YEAR)
    frame = {"weight": w}
    for var, *_ in AGGREGATES:
        frame[var] = sim.calculate(var, YEAR, map_to="household")
    frame["size"] = sim.calculate("pan_household_size", YEAR)
    return pd.DataFrame(frame)


def _weighted_deciles(values, weights, n=10):
    order = np.argsort(values)
    cum = np.cumsum(weights[order]) / weights.sum()
    deciles = np.empty(len(values), dtype=int)
    deciles[order] = np.minimum((cum * n).astype(int) + 1, n)
    return deciles


def score(reform=None, dataset=PRCS, baseline_sim=None):
    base_sim = baseline_sim or Simulation(dataset=dataset)
    base = _household_frame(base_sim)
    ref = (
        _household_frame(Simulation(dataset=dataset, reform=reform))
        if reform
        else base.copy()
    )
    w = base["weight"].to_numpy()

    totals = pd.DataFrame(
        {
            "variable": [v for v, *_ in AGGREGATES],
            "label_es": [es for _, es, _ in AGGREGATES],
            "label_en": [en for _, _, en in AGGREGATES],
            "baseline": [(base[v] * w).sum() for v, *_ in AGGREGATES],
            "reform": [(ref[v] * w).sum() for v, *_ in AGGREGATES],
        }
    )
    totals["change"] = totals["reform"] - totals["baseline"]

    # equivalised ranking: net income per household, deciles weighted by households
    base["decile"] = _weighted_deciles(
        base["household_net_income"].to_numpy(), w
    )
    change = ref["household_net_income"] - base["household_net_income"]
    rows = []
    for d in range(1, 11):
        m = base["decile"] == d
        wd = w[m]
        rows.append(
            {
                "decile": d,
                "households": wd.sum(),
                "mean_net_income": np.average(
                    base.loc[m, "household_net_income"], weights=wd
                ),
                "mean_change": np.average(change[m], weights=wd),
                "share_better_off": np.average(change[m] > 0.5, weights=wd),
                "share_worse_off": np.average(change[m] < -0.5, weights=wd),
                "total_change": (change[m] * wd).sum(),
            }
        )
    deciles = pd.DataFrame(rows)

    tax_row = totals.set_index("variable")
    summary = {
        "revenue_change": -(
            tax_row.loc["pr_income_tax", "change"]
            - tax_row.loc["pr_eitc", "change"]
        ),  # Hacienda's net cost: tax lost plus EITC paid
        "income_tax_change": tax_row.loc["pr_income_tax", "change"],
        "eitc_change": tax_row.loc["pr_eitc", "change"],
        "pan_change": tax_row.loc["pan", "change"],
        "net_income_change": tax_row.loc["household_net_income", "change"],
        "households": w.sum(),
        "share_better_off": np.average(change > 0.5, weights=w),
        "share_worse_off": np.average(change < -0.5, weights=w),
    }
    return {"totals": totals, "deciles": deciles, "summary": summary}

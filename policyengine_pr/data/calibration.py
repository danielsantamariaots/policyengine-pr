"""Calibrate the PRCS household weights to administrative totals.

Minimum-discrimination (entropy) reweighting: find household weights w
closest to the survey weights w0 in the Kullback-Leibler sense such that
sum_h a_kh w_h = t_k for every target k, where a_kh is household h's
contribution to aggregate k (dollars, or 1 for a count). Solved on the
dual with Newton's method; weights stay positive and the ranking of
households is preserved. This is the same family of methods as survey
raking; PolicyEngine-US uses a gradient-descent variant.

Targets live in calibration_targets.yaml; each is a model aggregate
matched to a published figure (see docs/statutes/calibration/SOURCES.md).

Usage::

    from policyengine_pr.data.calibration import calibrate, build_calibrated
    build_calibrated()           # writes data/prcs_2023_calibrated.h5
    report = calibrate(sim)      # DataFrame: target, before, after, published
"""

from pathlib import Path

import h5py
import numpy as np
import pandas as pd
import yaml

from policyengine_core.data import Dataset

from policyengine_pr.data.prcs import OUT, TAX_YEAR, PRCS

TARGETS = Path(__file__).with_name("calibration_targets.yaml")
OUT_CALIBRATED = OUT.with_name("prcs_2023_calibrated.h5")
YEAR = TAX_YEAR


def load_targets(path: Path = TARGETS) -> list[dict]:
    with open(path) as f:
        return yaml.safe_load(f)


def contributions(sim, targets) -> tuple[np.ndarray, np.ndarray]:
    """Matrix A (targets x households) and vector t of target values.

    Each household's contribution to a target is the household-level value
    of the statistic: a sum of dollars, a 1 for every household (count), a 1
    for households where the variable is positive (count_positive), or the
    number of persons (for person counts).
    """
    n = len(sim.calculate("household_weight", YEAR))
    rows, values = [], []
    for tgt in targets:
        var, stat = tgt["variable"], tgt["statistic"]
        if var == "household_weight":
            a = np.ones(n)
        elif var == "person_weight":
            a = sim.calculate("pan_household_size", YEAR).astype(float)
        else:
            x = sim.calculate(var, YEAR, map_to="household")
            a = x if stat == "sum" else (x > 0).astype(float)
        rows.append(np.asarray(a, dtype=float))
        values.append(float(tgt["value"]))
    return np.vstack(rows), np.array(values)


def entropy_reweight(w0, A, t, max_iter=200, tol=1e-9):
    """Minimise sum w log(w/w0) s.t. A w = t. Dual Newton iterations."""
    lam = np.zeros(A.shape[0])
    scale = np.abs(A).max(axis=1)
    scale[scale == 0] = 1
    As, ts = A / scale[:, None], t / scale
    for _ in range(max_iter):
        w = w0 * np.exp(As.T @ lam)
        g = As @ w - ts
        if np.max(np.abs(g) / np.maximum(np.abs(ts), 1)) < tol:
            break
        H = (As * w) @ As.T
        step = np.linalg.solve(H + 1e-12 * np.eye(len(ts)), g)
        # damped step to keep the exponent in range
        alpha = 1.0
        while alpha > 1e-4:
            cand = lam - alpha * step
            wc = w0 * np.exp(As.T @ cand)
            if np.isfinite(wc).all() and wc.max() < 1e12:
                lam = cand
                break
            alpha /= 2
    return w0 * np.exp(As.T @ lam)


def calibrate(sim, targets=None) -> tuple[np.ndarray, pd.DataFrame]:
    """Return calibrated household weights and a before/after report."""
    targets = targets or load_targets()
    w0 = np.asarray(sim.calculate("household_weight", YEAR), dtype=float)
    A, t = contributions(sim, targets)
    w = entropy_reweight(w0, A, t)
    report = pd.DataFrame(
        {
            "target": [x["name"] for x in targets],
            "published": t,
            "before": A @ w0,
            "after": A @ w,
        }
    )
    report["before_ratio"] = report["before"] / report["published"]
    report["after_ratio"] = report["after"] / report["published"]
    return w, report


def build_calibrated(out: Path = OUT_CALIBRATED):
    """Copy the PRCS dataset with calibrated household, tax-unit and person weights."""
    from policyengine_pr import Simulation

    sim = Simulation(dataset=PRCS)
    w, report = calibrate(sim)
    ratio = w / np.asarray(
        sim.calculate("household_weight", YEAR), dtype=float
    )
    with h5py.File(PRCS.file_path, "r") as src:
        data = {k: src[k][()] for k in src}
    hh_of_person = data["person_household_id"]
    hh_of_unit = (
        pd.Series(hh_of_person)
        .groupby(data["person_tax_unit_id"])
        .first()
        .values
    )
    data["household_weight"] = w
    data["person_weight"] = data["person_weight"] * ratio[hh_of_person]
    data["tax_unit_weight"] = data["tax_unit_weight"] * ratio[hh_of_unit]
    PRCSCalibrated().save_dataset(data, out)
    return out, report


class PRCSCalibrated(Dataset):
    name = "prcs_2023_calibrated"
    label = "PRCS 2023 PUMS, Puerto Rico, calibrated to administrative totals"
    data_format = Dataset.ARRAYS
    file_path = OUT_CALIBRATED
    time_period = TAX_YEAR

    def generate(self):
        build_calibrated()

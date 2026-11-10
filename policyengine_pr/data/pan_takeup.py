"""PAN take-up in the PRCS microdata.

The model's eligibility test admits more núcleos than ADSEF pays (888 thousand
against 730 thousand), and the eligible pool is larger and younger than the
participants. Participation is imputed with a logistic probability per
eligible núcleo, p = 1 / (1 + exp(-x'b)), with b solved so that the weighted
participants reproduce ADSEF's monthly averages for September 2024 - August
2025 (docs/statutes/pan/adsef_listados/): casos, participants, participants
aged 60+, with wages and with Social Security. Núcleos with no income always
participate (ADSEF reports more of them than the survey has). Each núcleo
then participates if a uniform draw (seed 20250831) falls below p.
"""

import h5py
import numpy as np

YEAR = 2025
SEED = 20250831
# ADSEF, listados mensuales de emisiones, SERVICIO = PAN, mean Sep 2024 - Aug 2025
TARGETS = {
    "casos": 730_133,
    "participantes": 1_247_785,
    "mayores_60": 427_780,
    "con_salarios": 216_240,
    "con_seguro_social": 449_200,
}


# moments the take-up is solved for; the rest are left to the reweighting
MOMENTS = ("casos", "participantes", "mayores_60")


def _solve(X, w, t, iters=200):
    """b such that sum w * sigmoid(X b) * X = t (convex: Newton + line search)."""
    scale = np.abs(X).max(axis=0)
    Xs, ts = X / scale, t / scale
    b = np.zeros(X.shape[1])

    def obj(b):
        z = np.clip(Xs @ b, -40, 40)
        return (w * np.log1p(np.exp(z))).sum() - ts @ b

    for _ in range(iters):
        p = 1 / (1 + np.exp(-np.clip(Xs @ b, -40, 40)))
        g = Xs.T @ (w * p) - ts
        if np.max(np.abs(g) / np.maximum(np.abs(ts), 1)) < 1e-9:
            break
        H = (Xs * (w * p * (1 - p))[:, None]).T @ Xs
        step = np.linalg.solve(H + 1e-9 * np.trace(H) * np.eye(len(b)), g)
        f0, alpha = obj(b), 1.0
        while alpha > 1e-8 and obj(b - alpha * step) > f0 - 1e-4 * alpha * (
            g @ step
        ):
            alpha /= 2
        b = b - alpha * step
    return 1 / (1 + np.exp(-np.clip(Xs @ b, -40, 40)))


def impute_pan_takeup(dataset, moments=MOMENTS):
    """Write `pan_participates` into the dataset file; returns a summary.
    `moments` are the TARGETS keys the take-up probabilities are solved for."""
    from policyengine_pr import Simulation

    path = dataset.file_path
    with h5py.File(path, "r") as src:
        data = {k: src[k][()] for k in src}
    n = len(data["pan_unit_id"])
    data["pan_participates"] = np.ones(n, dtype=bool)
    dataset().save_dataset(data, path)

    sim = Simulation(dataset=dataset)
    unit = data["person_pan_unit_id"]
    w = np.asarray(sim.calculate("pan_unit_weight", YEAR), dtype=float)
    eligible = np.asarray(sim.calculate("pan_eligible", YEAR), dtype=bool)
    size = np.asarray(sim.calculate("pan_household_size", YEAR), dtype=float)
    elderly = np.asarray(sim.calculate("pan_elderly_count", YEAR), dtype=float)
    wages = np.bincount(
        unit, np.asarray(sim.calculate("employment_income", YEAR)) > 0, n
    )
    ss = np.bincount(
        unit, np.asarray(sim.calculate("social_security", YEAR)) > 0, n
    )
    no_income = np.asarray(sim.calculate("pan_gross_income", YEAR)) <= 0
    X = np.column_stack([np.ones(n), size, elderly, wages, ss])
    t = np.array(list(TARGETS.values()), dtype=float)

    cols = [list(TARGETS).index(k) for k in moments]
    forced = eligible & no_income
    free = eligible & ~no_income
    t_free = (t - X[forced].T @ w[forced])[cols]
    p = np.zeros(n)
    p[forced] = 1.0
    p[free] = _solve(X[free][:, cols], w[free], t_free)
    rng = np.random.default_rng(SEED)
    participates = rng.random(n) < p

    data["pan_participates"] = participates
    dataset().save_dataset(data, path)
    got = X[participates].T @ w[participates]
    return dict(zip(TARGETS, np.round(got))), dict(zip(TARGETS, t))

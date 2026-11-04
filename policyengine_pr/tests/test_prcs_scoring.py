"""The PRCS dataset and the scoring module, when the microdata is present.

The raw PUMS files and the built .h5 are not in the repository (data/ is
ignored); these tests skip when data/prcs_2023.h5 is missing.
"""

import pytest

from policyengine_pr.data import PRCS

pytestmark = pytest.mark.skipif(
    not PRCS.file_path.exists(), reason="data/prcs_2023.h5 not built"
)


def test_baseline_totals_are_plausible():
    from policyengine_pr import Simulation

    sim = Simulation(dataset=PRCS)
    w = sim.calculate("household_weight", 2025)
    # PRCS 2023: 1.28 million occupied households with persons
    assert 1.2e6 < w.sum() < 1.4e6
    wages = (
        sim.calculate("employment_income", 2025, map_to="household") * w
    ).sum()
    assert 25e9 < wages < 45e9  # PUMS weighted wages ~ \$32-35 bn
    status = sim.calculate("pr_filing_status", 2025).decode_to_str()
    assert (status == "JOINT").sum() > 3_000


def test_widening_the_zero_bracket_costs_revenue_and_hurts_nobody():
    from policyengine_pr.analysis.scoring import score
    from policyengine_pr.reforms.parametric import parametric_reform

    r = score(
        parametric_reform({"gov.hacienda.income.rates[1].threshold": 12_000.0})
    )
    assert r["summary"]["income_tax_change"] < 0
    assert r["summary"]["share_worse_off"] == 0
    assert r["summary"]["eitc_change"] == 0
    assert len(r["deciles"]) == 10

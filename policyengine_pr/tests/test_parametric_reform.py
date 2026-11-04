"""Parametric reforms change outcomes exactly as the rate table implies."""

from policyengine_core.parameters import (
    Parameter,
    ParameterNode,
    ParameterScaleBracket,
)

from policyengine_pr import Simulation
from policyengine_pr.reforms.parametric import LEVERS, parametric_reform

SITUATION = {
    "people": {"p": {"age": {2025: 40}, "employment_income": {2025: 30_000}}},
    "tax_units": {"t": {"members": ["p"]}},
    "households": {"h": {"members": ["p"]}},
}


def tax(reform=None):
    sim = Simulation(situation=SITUATION, reform=reform)
    return float(sim.calculate("pr_regular_tax", 2025)[0])


def test_baseline_matches_hand_computation():
    # 26,500 taxable -> 1,120 + 14% x 1,500
    assert abs(tax() - 1_330) < 0.01


def test_raising_the_zero_bracket_lowers_tax():
    # Zero bracket to $12,000: bracket 2 covers 12,000-25,000 (13,000 x 7% = 910),
    # then 14% x 1,500 = 210 -> 1,120
    reform = parametric_reform(
        {"gov.hacienda.income.rates[1].threshold": 12_000}
    )
    assert abs(tax(reform) - 1_120) < 0.01


def test_reform_does_not_leak_into_baseline():
    parametric_reform(
        {"gov.hacienda.income.exemptions.personal.SINGLE": 10_000}
    )
    assert abs(tax() - 1_330) < 0.01


def test_every_lever_path_resolves():
    from policyengine_pr import system

    params = system.parameters
    for path, _, _ in LEVERS:
        node = params
        for name in path.split("."):
            if "[" in name:
                name, index = name.split("[")
                node = node.children[name].brackets[int(index[:-1])]
            else:
                node = node.children[name]
        assert isinstance(
            node, (Parameter, ParameterNode, ParameterScaleBracket)
        ), path

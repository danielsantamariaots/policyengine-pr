"""Reform YAML files load, resolve relative values, and build a Reform."""

from policyengine_pr import Simulation
from policyengine_pr.reforms.files import (
    REFORMS_DIR,
    list_reforms,
    load_reform,
    reform_from_file,
)

SITUATION = {
    "people": {"p": {"age": {2025: 40}, "employment_income": {2025: 30_000}}},
    "tax_units": {"t": {"members": ["p"]}},
    "households": {"h": {"members": ["p"]}},
}


def test_every_example_reform_loads_and_changes_something():
    reforms = list_reforms()
    assert len(reforms) >= 4
    for meta, changes in reforms:
        assert meta["name"] and changes


def test_relative_values_resolve_against_current_law():
    _, changes = load_reform(REFORMS_DIR / "credito_trabajo_mas_20.yaml")
    assert changes["gov.hacienda.credits.eitc.max.0"] == round(1_794 * 1.2, 6)


def test_reform_from_file_changes_the_tax():
    base = float(
        Simulation(situation=SITUATION).calculate("pr_regular_tax", 2025)[0]
    )
    reform = reform_from_file(REFORMS_DIR / "ampliar_tramo_0.yaml")
    new = float(
        Simulation(situation=SITUATION, reform=reform).calculate(
            "pr_regular_tax", 2025
        )[0]
    )
    assert base - new == 210  # 7% x 3,000

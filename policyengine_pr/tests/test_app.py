"""Headless smoke tests for the Streamlit app: every page renders without
an exception in both languages, presets and example reforms apply, and the
Reformas page scores when the microdata is present.

Run by `make test` through policyengine-core's test command (pytest).
"""

from pathlib import Path

import pytest

APP = Path(__file__).resolve().parents[2] / "app" / "calculator.py"
DATA = Path(__file__).resolve().parents[2] / "data" / "prcs_2023_calibrated.h5"


@pytest.fixture
def app():
    from streamlit.testing.v1 import AppTest

    at = AppTest.from_file(str(APP), default_timeout=120)
    return at.run()


def _no_errors(at):
    assert not at.exception, [e.value for e in at.exception]
    assert not at.error, [e.value for e in at.error]


def _radio(at, key):
    return next(r for r in at.sidebar.radio if r.key == key)


def test_home_renders(app):
    _no_errors(app)
    assert app.title[0].value.startswith("Modelo contributivo")


@pytest.mark.parametrize("lang", ["Español", "English"])
def test_calculator_renders_in_both_languages(app, lang):
    at = app
    at.sidebar.radio[0].set_value(lang).run()
    _radio(at, "view").set_value("calc").run()
    _no_errors(at)
    assert len(at.metric) == 4
    assert any("$" in m.value for m in at.metric)


def test_preset_fills_the_sidebar(app):
    at = app
    _radio(at, "view").set_value("calc").run()
    at.sidebar.selectbox(key="preset").set_value("retiree").run()
    _no_errors(at)
    assert at.sidebar.number_input(key="filer_age").value == 65
    assert at.sidebar.number_input(key="filer_pension_income").value == 24_000


def test_example_reform_switches_to_comparison_mode(app):
    at = app
    _radio(at, "view").set_value("calc").run()
    at.sidebar.selectbox(key="example_reform").set_value(
        "ampliar_tramo_0"
    ).run()
    _no_errors(at)
    assert (
        at.sidebar.number_input(
            key="r_gov.hacienda.income.rates[1].threshold"
        ).value
        == 12_000
    )
    assert at.info  # the "reform active" notice


def test_cliffwatch_renders_with_cliffs_table(app):
    at = app
    _radio(at, "view").set_value("cliff").run()
    _no_errors(at)
    assert any("CliffWatch" in t.value for t in at.title)
    assert len(at.metric) >= 8  # shared row + CliffWatch row


@pytest.mark.skipif(
    not DATA.exists(), reason="data/prcs_2023_calibrated.h5 not built"
)
def test_reforms_page_scores(app):
    at = app
    _radio(at, "view").set_value("reform").run()
    _no_errors(at)
    assert any("Reformas" in t.value or "Reforms" in t.value for t in at.title)
    assert at.dataframe  # the scored table

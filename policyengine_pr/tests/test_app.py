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
    assert app.title[0].value.startswith("¿Cuánto paga su hogar")


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
    at.sidebar.toggle(key="show_levers").set_value(True).run()
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


def test_cliffwatch_marriage_penalty_comparison(app):
    at = app
    _radio(at, "view").set_value("cliff").run()
    at.sidebar.selectbox(key="preset").set_value("couple").run()
    at.selectbox(key="compare_with").set_value("unmarried").run()
    _no_errors(at)
    assert any(
        "atrimonio" in m.label or "arriage" in m.label for m in at.metric
    )


def test_voucher_preset_pays_section8(app):
    at = app
    _radio(at, "view").set_value("calc").run()
    at.sidebar.selectbox(key="preset").set_value("voucher").run()
    _no_errors(at)
    assert at.sidebar.checkbox(key="housing_assisted").value is True
    table = next(
        d.value
        for d in at.dataframe
        if d.value.columns[0] in ("Partida", "Item")
    )
    row = table[table.iloc[:, 0].str.contains("Sección 8|Section 8")]
    assert len(row) == 1 and float(row.iloc[0, 1]) > 0


def test_shared_link_restores_household_and_reform():
    from streamlit.testing.v1 import AppTest

    at = AppTest.from_file(str(APP), default_timeout=120)
    at.query_params["view"] = "calc"
    at.query_params["show_levers"] = "1"
    at.query_params["filer_wages"] = "42000"
    at.query_params["joint"] = "1"
    at.query_params["r.gov.hacienda.income.rates[1].threshold"] = "12000"
    at.run()
    _no_errors(at)
    assert at.sidebar.number_input(key="filer_wages").value == 42_000
    assert at.sidebar.toggle(key="joint").value is True
    assert (
        at.sidebar.number_input(
            key="r_gov.hacienda.income.rates[1].threshold"
        ).value
        == 12_000
    )
    assert at.info  # reform notice
    assert at.query_params["filer_wages"] == "42000"

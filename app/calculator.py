"""Household calculator prototype on top of policyengine-pr.

Run with:  streamlit run app/calculator.py
"""

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from policyengine_pr import Simulation, system
from policyengine_pr.reforms.parametric import LEVERS, parametric_reform

YEAR = 2025
BASELINE_COLOR = "#2a78d6"
REFORM_COLOR = "#eb6834"
SERIES = {  # fixed categorical order; validated palette
    "PR income tax": "#2a78d6",
    "Payroll taxes": "#eb6834",
    "Refundable credits": "#1baf7a",
}
OUTPUTS = [
    ("pr_taxable_gross_income", "Adjusted gross income (line 5)"),
    ("pr_deductions", "Deductions, Anejo A (line 6)"),
    ("pr_exemptions", "Personal, veteran and dependent exemptions"),
    ("pr_net_taxable_income", "Net taxable income (line 13)"),
    ("pr_regular_tax", "Tax per table, Sec. 1021.01 (line 14)"),
    ("pr_gradual_adjustment", "Gradual adjustment (line 15)"),
    ("pr_regular_tax_before_credits", "Regular tax after 92%/95% (line 17)"),
    ("pr_abt_excess", "Alternate basic tax excess (line 20)"),
    ("pr_income_tax", "PR income tax (line 26)"),
    ("pr_eitc", "Crédito por Trabajo (line 27C)"),
    ("federal_actc", "Federal additional child tax credit (line 27D)"),
    ("employee_social_security_tax", "Social Security tax withheld"),
    ("employee_medicare_tax", "Medicare tax withheld"),
    ("self_employment_tax", "Self-employment tax (Schedule SE)"),
    ("household_net_income", "Household net income"),
]
RANGE_VARS = [
    "pr_income_tax",
    "employee_social_security_tax",
    "employee_medicare_tax",
    "self_employment_tax",
    "pr_refundable_credits",
    "household_net_income",
]
PERSON_INPUTS = [
    # (variable, label, default, step, help)
    (
        "self_employment_income",
        "Self-employment net profit ($)",
        0,
        1_000,
        "Anejo M, Parte IV, línea 9",
    ),
    (
        "pension_income",
        "Pension from a qualified plan ($)",
        0,
        1_000,
        "Anejo H; $11,000 / $15,000 exempt by age",
    ),
    (
        "social_security",
        "Social Security benefits ($)",
        0,
        1_000,
        "Not taxed in Puerto Rico",
    ),
]
DEDUCTION_INPUTS = [
    (
        "mortgage_interest",
        "Home mortgage interest ($)",
        500,
        "Lesser of paid, 30% of income, $35,000",
    ),
    (
        "medical_expenses",
        "Medical expenses ($)",
        500,
        "Deductible above 6% of AGI",
    ),
    (
        "charitable_contributions",
        "Charitable contributions ($)",
        500,
        "Up to 50% of AGI",
    ),
    (
        "ira_contributions",
        "IRA contributions ($)",
        500,
        "Up to $7,000 per person, limited by earnings",
    ),
    (
        "education_account_contributions",
        "Education accounts ($)",
        100,
        "Up to $1,000 per beneficiary",
    ),
    (
        "student_loan_payments",
        "Student loan payments ($)",
        100,
        "Interest and principal, university level",
    ),
]


def current_value(path):
    """Current-law value of a lever at the start of YEAR."""
    node = system.parameters
    for name in path.split("."):
        if "[" in name:
            name, index = name.split("[")
            node = node.children[name].brackets[int(index[:-1])]
        else:
            node = node.children[name]
    return float(node(f"{YEAR}-01-01"))


def build_situation(hh, filer_wages):
    """hh: dict of household inputs; filer_wages varied separately."""
    filer = {
        "age": {YEAR: hh["filer_age"]},
        "employment_income": {YEAR: filer_wages},
        "is_veteran": {YEAR: hh["filer_veteran"]},
    }
    for var, _, _, _, _ in PERSON_INPUTS:
        filer[var] = {YEAR: hh["filer"][var]}
    for var, _, _, _ in DEDUCTION_INPUTS:
        filer[var] = {YEAR: hh["deductions"][var]}
    people = {"filer": filer}
    if hh["joint"]:
        spouse = {
            "age": {YEAR: hh["spouse_age"]},
            "employment_income": {YEAR: hh["spouse_wages"]},
            "is_veteran": {YEAR: hh["spouse_veteran"]},
        }
        for var, _, _, _, _ in PERSON_INPUTS:
            spouse[var] = {YEAR: hh["spouse"][var]}
        people["spouse"] = spouse
    for i, age in enumerate(hh["child_ages"]):
        people[f"child_{i}"] = {
            "age": {YEAR: age},
            "is_tax_unit_dependent": {YEAR: True},
        }
    members = list(people)
    tax_unit = {
        "members": members,
        "pr_filing_status": {YEAR: "JOINT" if hh["joint"] else "SINGLE"},
        "pr_other_deductions": {YEAR: hh["other_deductions"]},
        "pr_abt_other_income": {YEAR: hh["abt_other_income"]},
    }
    return {
        "people": people,
        "tax_units": {"tax_unit": tax_unit},
        "households": {"household": {"members": members}},
    }


def compute(situation, variables, reform=None):
    sim = Simulation(situation=situation, reform=reform)
    return {v: float(sim.calculate(v, YEAR)[0]) for v in variables}


def person_inputs(prefix):
    with st.expander(f"{prefix} other income"):
        return {
            var: st.number_input(
                label,
                0,
                5_000_000,
                default,
                step=step,
                help=help_,
                key=f"{prefix}_{var}",
            )
            for var, label, default, step, help_ in PERSON_INPUTS
        }


def money(x):
    return f"${x:,.0f}"


st.set_page_config(page_title="PR household calculator", layout="wide")
st.title("Puerto Rico household tax calculator")
st.caption(
    "Prototype on policyengine-pr · tax year 2025 · every rule cited to a "
    "Hacienda or IRS document in docs/statutes/"
)

hh = {}
with st.sidebar:
    st.header("Household")
    hh["joint"] = st.toggle("Married filing jointly", value=False)
    hh["filer_age"] = st.number_input("Filer age", 16, 100, 35)
    filer_wages = st.number_input(
        "Filer wages ($)", 0, 2_000_000, 30_000, step=1_000
    )
    hh["filer_veteran"] = st.checkbox("Filer is a veteran", value=False)
    hh["filer"] = person_inputs("Filer")
    hh["spouse_age"], hh["spouse_wages"] = 35, 0
    hh["spouse_veteran"], hh["spouse"] = False, {}
    if hh["joint"]:
        hh["spouse_age"] = st.number_input("Spouse age", 16, 100, 35)
        hh["spouse_wages"] = st.number_input(
            "Spouse wages ($)", 0, 2_000_000, 0, step=1_000
        )
        hh["spouse_veteran"] = st.checkbox("Spouse is a veteran", value=False)
        hh["spouse"] = person_inputs("Spouse")
    n_children = st.number_input("Dependent children", 0, 8, 2)
    hh["child_ages"] = [
        st.number_input(
            f"Child {i + 1} age", 0, 25, min(4 + 4 * i, 25), key=f"c{i}"
        )
        for i in range(n_children)
    ]
    with st.expander("Deductions (Anejo A)"):
        hh["deductions"] = {
            var: st.number_input(
                label, 0, 1_000_000, 0, step=step, help=help_, key=f"d_{var}"
            )
            for var, label, step, help_ in DEDUCTION_INPUTS
        }
        hh["other_deductions"] = st.number_input(
            "Other deductions ($)",
            0,
            1_000_000,
            0,
            step=500,
            help="Casualty losses and items not computed",
        )
    with st.expander("Advanced"):
        hh["abt_other_income"] = st.number_input(
            "Other income subject to alternate basic tax ($)",
            0,
            5_000_000,
            0,
            step=1_000,
            help="Pass-through and exempt items not modelled; wages are "
            "never subject (2025 instructions, p. 82).",
        )

    st.header("Reform")
    st.caption("Edit any lever; unchanged levers keep current law.")
    changes = {}
    for path, label, kind in LEVERS:
        base_value = current_value(path)
        if kind == "rate":
            new = st.number_input(
                label,
                0.0,
                1.0,
                base_value,
                step=0.01,
                format="%.4f",
                key=f"r_{path}",
            )
        else:
            new = st.number_input(
                label,
                0.0,
                5_000_000.0,
                base_value,
                step=500.0,
                format="%.0f",
                key=f"r_{path}",
            )
        if abs(new - base_value) > 1e-9:
            changes[path] = new
    reform = parametric_reform(changes) if changes else None

situation = build_situation(hh, filer_wages)
extra = ["pr_refundable_credits", "household_market_income", "household_tax"]
variables = [v for v, _ in OUTPUTS] + extra
base = compute(situation, variables)
ref = compute(situation, variables, reform) if reform else None
shown = ref or base
market = base["household_market_income"]

if reform:
    st.info(
        f"Reform active: {len(changes)} lever(s) changed. "
        "Deltas are reform minus current law."
    )


def metric(col, label, key, help_=None, lower_is_better=False):
    delta = money(ref[key] - base[key]) if ref else None
    col.metric(
        label,
        money(shown[key]),
        delta=delta,
        help=help_,
        delta_color="inverse" if lower_is_better else "normal",
    )


c1, c2, c3, c4 = st.columns(4)
metric(c1, "PR income tax", "pr_income_tax", lower_is_better=True)
metric(
    c2,
    "Refundable credits",
    "pr_refundable_credits",
    "Crédito por Trabajo + federal ACTC",
)
metric(c3, "Net income", "household_net_income")
net_rate = (market - shown["household_net_income"]) / market if market else 0.0
c4.metric(
    "Net tax rate",
    f"{net_rate:.1%}",
    help="(market income − net income) / market income; "
    "negative means a net transfer",
)

left, right = st.columns([3, 2])

with left:
    st.subheader("Across the income range")
    st.caption("Same household; filer wages varied from $0 to $150,000.")
    rows = []
    for w in range(0, 150_001, 2_500):
        s = build_situation(hh, w)
        x = compute(s, RANGE_VARS)
        row = {
            "Filer wages": w,
            "PR income tax": x["pr_income_tax"],
            "Payroll taxes": x["employee_social_security_tax"]
            + x["employee_medicare_tax"]
            + x["self_employment_tax"],
            "Refundable credits": x["pr_refundable_credits"],
            "Net income": x["household_net_income"],
        }
        if reform:
            y = compute(s, RANGE_VARS, reform)
            row["Net income (reform)"] = y["household_net_income"]
            row["Change in net income"] = (
                y["household_net_income"] - x["household_net_income"]
            )
        rows.append(row)
    df = pd.DataFrame(rows)

    layout = dict(
        margin=dict(l=10, r=10, t=10, b=10),
        hovermode="x unified",
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        legend=dict(orientation="h", y=1.08, x=0),
        xaxis=dict(
            title="Filer wages", tickprefix="$", tickformat=",", showgrid=False
        ),
        yaxis=dict(
            title=None,
            tickprefix="$",
            tickformat=",",
            gridcolor="rgba(128,128,128,0.18)",
            zeroline=False,
        ),
    )

    if reform:
        fig = go.Figure()
        fig.add_trace(
            go.Scatter(
                x=df["Filer wages"],
                y=df["Change in net income"],
                name="Change in net income",
                mode="lines",
                line=dict(color=REFORM_COLOR, width=2),
                hovertemplate="%{y:$,.0f}<extra>Change in net income</extra>",
            )
        )
        fig.add_hline(y=0, line=dict(color="#9a9a94", width=1))
        fig.add_vline(
            x=filer_wages, line=dict(color="#9a9a94", width=1, dash="dot")
        )
        fig.update_layout(height=300, **layout)
        st.plotly_chart(fig, use_container_width=True)
        st.caption(
            "Positive means the household is better off under the reform."
        )

    fig = go.Figure()
    if reform:
        fig.add_trace(
            go.Scatter(
                x=df["Filer wages"],
                y=df["Net income"],
                name="Net income, current law",
                mode="lines",
                line=dict(color=BASELINE_COLOR, width=2),
                hovertemplate="%{y:$,.0f}<extra>Current law</extra>",
            )
        )
        fig.add_trace(
            go.Scatter(
                x=df["Filer wages"],
                y=df["Net income (reform)"],
                name="Net income, reform",
                mode="lines",
                line=dict(color=REFORM_COLOR, width=2),
                hovertemplate="%{y:$,.0f}<extra>Reform</extra>",
            )
        )
    else:
        for name, color in SERIES.items():
            fig.add_trace(
                go.Scatter(
                    x=df["Filer wages"],
                    y=df[name],
                    name=name,
                    mode="lines",
                    line=dict(color=color, width=2),
                    hovertemplate="%{y:$,.0f}<extra>" + name + "</extra>",
                )
            )
    fig.add_vline(
        x=filer_wages, line=dict(color="#9a9a94", width=1, dash="dot")
    )
    fig.update_layout(height=380, **layout)
    st.plotly_chart(fig, use_container_width=True)

    df["Marginal rate"] = (
        1 - df["Net income"].diff() / df["Filer wages"].diff()
    )
    with st.expander("Table view"):
        st.dataframe(
            df.style.format(
                {c: "${:,.0f}" for c in df.columns if c != "Marginal rate"}
                | {"Marginal rate": "{:.0%}"}
            ),
            use_container_width=True,
            hide_index=True,
            height=320,
        )

with right:
    st.subheader("Line by line")
    if reform:
        table = pd.DataFrame(
            [
                (label, base[v], ref[v], ref[v] - base[v])
                for v, label in OUTPUTS
            ],
            columns=["Item", "Current law", "Reform", "Change"],
        )
        fmt = {
            "Current law": "${:,.0f}",
            "Reform": "${:,.0f}",
            "Change": "{:+,.0f}",
        }
    else:
        table = pd.DataFrame(
            [(label, base[v]) for v, label in OUTPUTS],
            columns=["Item", "Amount"],
        )
        fmt = {"Amount": "${:,.2f}"}
    st.dataframe(
        table.style.format(fmt),
        use_container_width=True,
        hide_index=True,
        height=560,
    )

st.divider()
st.markdown(
    "**Not yet modelled:** interest, dividends and capital gains at "
    "preferential rates; nonrefundable investment credits (Anejo B); "
    "benefits (PAN, Medicaid). Youth exemption (Ley 135-2014) applies "
    "automatically for ages 16–26."
)

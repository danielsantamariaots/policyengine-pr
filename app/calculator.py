"""Household calculator prototype on top of policyengine-pr.

Run with:  streamlit run app/calculator.py
"""

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from policyengine_pr import Simulation

YEAR = 2025
SERIES = {  # fixed categorical order; validated palette
    "PR income tax": "#2a78d6",
    "Payroll taxes": "#eb6834",
    "Refundable credits": "#1baf7a",
}
OUTPUTS = [
    ("pr_taxable_gross_income", "Gross income subject to tax"),
    ("pr_exemptions", "Personal and dependent exemptions"),
    ("pr_net_taxable_income", "Net taxable income"),
    ("pr_regular_tax", "Tax per table (Sec. 1021.01)"),
    ("pr_gradual_adjustment", "Gradual adjustment"),
    ("pr_regular_tax_before_credits", "Regular tax after 92%/95% factor"),
    ("pr_abt_excess", "Alternate basic tax excess"),
    ("pr_income_tax", "PR income tax"),
    ("pr_eitc", "Crédito por Trabajo (PR EITC)"),
    ("federal_actc", "Federal additional child tax credit"),
    ("household_tax", "All taxes incl. Social Security and Medicare"),
    ("household_net_income", "Household net income"),
]


def build_situation(
    filer_age,
    filer_wages,
    joint,
    spouse_age,
    spouse_wages,
    child_ages,
    deductions,
    abt_income,
):
    people = {
        "filer": {
            "age": {YEAR: filer_age},
            "employment_income": {YEAR: filer_wages},
        }
    }
    if joint:
        people["spouse"] = {
            "age": {YEAR: spouse_age},
            "employment_income": {YEAR: spouse_wages},
        }
    for i, age in enumerate(child_ages):
        people[f"child_{i}"] = {
            "age": {YEAR: age},
            "is_tax_unit_dependent": {YEAR: True},
        }
    members = list(people)
    tax_unit = {
        "members": members,
        "pr_filing_status": {YEAR: "JOINT" if joint else "SINGLE"},
        "pr_deductions": {YEAR: deductions},
        "pr_abt_income": {YEAR: abt_income},
    }
    return {
        "people": people,
        "tax_units": {"tax_unit": tax_unit},
        "households": {"household": {"members": members}},
    }


def compute(situation, variables):
    sim = Simulation(situation=situation)
    return {v: float(sim.calculate(v, YEAR)[0]) for v in variables}


st.set_page_config(page_title="PR household calculator", layout="wide")
st.title("Puerto Rico household tax calculator")
st.caption(
    "Prototype on policyengine-pr · tax year 2025 · wage income only · "
    "every rule cited to a Hacienda or IRS document in docs/statutes/"
)

with st.sidebar:
    st.header("Household")
    joint = st.toggle("Married filing jointly", value=False)
    filer_age = st.number_input("Filer age", 16, 100, 35)
    filer_wages = st.number_input(
        "Filer wages ($)", 0, 2_000_000, 30_000, step=1_000
    )
    spouse_age, spouse_wages = 35, 0
    if joint:
        spouse_age = st.number_input("Spouse age", 16, 100, 35)
        spouse_wages = st.number_input(
            "Spouse wages ($)", 0, 2_000_000, 0, step=1_000
        )
    n_children = st.number_input("Dependent children", 0, 8, 2)
    child_ages = [
        st.number_input(
            f"Child {i + 1} age", 0, 25, min(4 + 4 * i, 25), key=f"c{i}"
        )
        for i in range(n_children)
    ]
    with st.expander("Advanced"):
        deductions = st.number_input(
            "Itemized deductions, Anejo A ($)", 0, 500_000, 0, step=500
        )
        abt_income = st.number_input(
            "Income subject to alternate basic tax ($)",
            0,
            5_000_000,
            0,
            step=1_000,
            help="Zero for wage-only filers (2025 instructions, p. 82).",
        )

situation = build_situation(
    filer_age,
    filer_wages,
    joint,
    spouse_age,
    spouse_wages,
    child_ages,
    deductions,
    abt_income,
)
r = compute(situation, [v for v, _ in OUTPUTS] + ["pr_refundable_credits"])
wages = filer_wages + spouse_wages

c1, c2, c3, c4 = st.columns(4)
c1.metric("PR income tax", f"${r['pr_income_tax']:,.0f}")
c2.metric(
    "Refundable credits",
    f"${r['pr_refundable_credits']:,.0f}",
    help="Crédito por Trabajo + federal ACTC",
)
c3.metric("Net income", f"${r['household_net_income']:,.0f}")
net_rate = (wages - r["household_net_income"]) / wages if wages else 0.0
c4.metric(
    "Net tax rate",
    f"{net_rate:.1%}",
    help="(wages − net income) / wages; negative means a net transfer",
)

left, right = st.columns([3, 2])

with left:
    st.subheader("Across the income range")
    st.caption("Same household; filer wages varied from $0 to $150,000.")
    grid = list(range(0, 150_001, 2_500))
    rows = []
    for w in grid:
        s = build_situation(
            filer_age,
            w,
            joint,
            spouse_age,
            spouse_wages,
            child_ages,
            deductions,
            abt_income,
        )
        x = compute(
            s,
            [
                "pr_income_tax",
                "employee_social_security_tax",
                "employee_medicare_tax",
                "pr_refundable_credits",
                "household_net_income",
            ],
        )
        rows.append(
            {
                "Filer wages": w,
                "PR income tax": x["pr_income_tax"],
                "Payroll taxes": x["employee_social_security_tax"]
                + x["employee_medicare_tax"],
                "Refundable credits": x["pr_refundable_credits"],
                "Net income": x["household_net_income"],
            }
        )
    df = pd.DataFrame(rows)

    fig = go.Figure()
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
    fig.update_layout(
        height=380,
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
    table = pd.DataFrame(
        [(label, r[v]) for v, label in OUTPUTS], columns=["Item", "Amount"]
    )
    st.dataframe(
        table.style.format({"Amount": "${:,.2f}"}),
        use_container_width=True,
        hide_index=True,
        height=460,
    )

st.divider()
st.markdown(
    "**Not yet modelled:** self-employment and other non-wage income, "
    "itemized deductions beyond the amount entered, nonrefundable credits, "
    "benefits (PAN, Medicaid). Youth exemption (Ley 135-2014) applies "
    "automatically for ages 16–26."
)

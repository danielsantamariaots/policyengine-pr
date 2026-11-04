"""PRCS PUMS (Puerto Rico Community Survey public-use microdata) as a
policyengine-pr dataset.

Source: Census Bureau, ACS/PRCS 2023 1-year PUMS, Puerto Rico person
(psam_p72.csv) and housing (psam_h72.csv) files,
https://www2.census.gov/programs-surveys/acs/data/pums/2023/1-Year/
(csv_ppr.zip, csv_hpr.zip). Variable codes from the 2023 PUMS data
dictionary.

Mapping (documented simplifications, to be revisited once Hacienda's
tabulations allow calibration):

- Households: occupied housing units only (TYPEHUGQ == 1); group quarters
  are dropped (no tax units can be built for them).
- Tax units: the reference person (RELSHIPP 20) with their spouse (21, 23)
  files jointly; their children (25-27, 30, 36) aged under 21, or under 26
  if enrolled in school (SCH > 1), are their dependents, as are any other
  members under 18. Every other adult files a separate single return with
  no dependents. Unmarried partners (22, 24) file separately.
- Money amounts are PUMS annual amounts times ADJINC (2023 dollars). No
  uprating to the 2025 tax year is applied yet.
- interest_income receives INTP (interest, dividends and net rental
  income together); dividend_income and capital gains are zero.
- is_veteran: served on active duty in the past (MIL == 2).
- is_full_time_student: enrolled in school (SCH > 1) and aged 18 or over.
"""

from pathlib import Path

import numpy as np
import pandas as pd
from policyengine_core.data import Dataset

RAW = Path(__file__).resolve().parents[2] / "data" / "raw" / "pums_2023"
OUT = Path(__file__).resolve().parents[2] / "data" / "prcs_2023.h5"
TAX_YEAR = 2025  # the population is simulated under the 2025 rules

CHILD_CODES = {25, 26, 27, 30, 36}
SPOUSE_CODES = {21, 23}
PERSON_COLS = [
    "SERIALNO",
    "SPORDER",
    "PWGTP",
    "AGEP",
    "RELSHIPP",
    "WAGP",
    "SEMP",
    "RETP",
    "SSP",
    "INTP",
    "SCH",
    "MIL",
    "ADJINC",
]
HOUSEHOLD_COLS = ["SERIALNO", "WGTP", "TYPEHUGQ", "PUMA"]


def build_prcs(raw: Path = RAW, out: Path = OUT) -> Path:
    p = pd.read_csv(raw / "psam_p72.csv", usecols=PERSON_COLS)
    h = pd.read_csv(raw / "psam_h72.csv", usecols=HOUSEHOLD_COLS)
    h = h[
        (h["TYPEHUGQ"] == 1) & h["SERIALNO"].isin(p["SERIALNO"])
    ].reset_index(
        drop=True
    )  # occupied housing units with at least one person (vacant units dropped)
    p = p[p["SERIALNO"].isin(h["SERIALNO"])].reset_index(drop=True)
    adj = p["ADJINC"] / 1_000_000

    p["household_id"] = p["SERIALNO"].map(
        dict(zip(h["SERIALNO"], np.arange(len(h))))
    )
    is_head = p["RELSHIPP"] == 20
    is_spouse = p["RELSHIPP"].isin(SPOUSE_CODES)
    student = p["SCH"].fillna(1) > 1
    child_of_head = p["RELSHIPP"].isin(CHILD_CODES) & (
        (p["AGEP"] < 21) | ((p["AGEP"] < 26) & student)
    )
    minor_other = (p["AGEP"] < 18) & ~is_head & ~is_spouse
    in_head_unit = is_head | is_spouse | child_of_head | minor_other
    # tax unit ids: head's unit = household id; every other adult = own unit
    p["tax_unit_id"] = np.where(
        in_head_unit, p["household_id"], len(h) + np.arange(len(p))
    )
    p["is_dependent"] = (child_of_head | minor_other).astype(bool)
    joint = p.groupby("tax_unit_id")["RELSHIPP"].transform(
        lambda s: s.isin(SPOUSE_CODES).any()
    )

    tu_ids, tu_index = np.unique(p["tax_unit_id"], return_inverse=True)
    tu_household = (
        pd.Series(p["household_id"].values, index=tu_index)
        .groupby(level=0)
        .first()
        .values
    )
    data = {
        # entities
        "person_id": np.arange(len(p)),
        "person_household_id": p["household_id"].values,
        "person_tax_unit_id": tu_index,
        "household_id": np.arange(len(h)),
        "tax_unit_id": np.arange(len(tu_ids)),
        # weights
        "person_weight": p["PWGTP"].values.astype(float),
        "household_weight": h["WGTP"].values.astype(float),
        "tax_unit_weight": h["WGTP"].values[tu_household].astype(float),
        # person inputs
        "age": p["AGEP"].values,
        "employment_income": (p["WAGP"].fillna(0) * adj).values,
        "self_employment_income": (p["SEMP"].fillna(0) * adj).values,
        "pension_income": (p["RETP"].fillna(0) * adj).values,
        "social_security": (p["SSP"].fillna(0) * adj).values,
        "interest_income": (p["INTP"].fillna(0).clip(lower=0) * adj).values,
        "is_tax_unit_dependent": p["is_dependent"].values,
        "is_full_time_student": (student & (p["AGEP"] >= 18)).values,
        "is_veteran": (p["MIL"].fillna(4) == 2).values,
        # tax unit inputs
        # Enum inputs are stored as the index in PRFilingStatus (SINGLE 0, JOINT 1)
        "pr_filing_status": pd.Series(joint.values.astype(int), index=tu_index)
        .groupby(level=0)
        .first()
        .values,
    }
    out.parent.mkdir(parents=True, exist_ok=True)
    PRCS().save_dataset(data, out)
    return out


class PRCS(Dataset):
    name = "prcs_2023"
    label = "PRCS 2023 1-year PUMS, Puerto Rico"
    data_format = Dataset.ARRAYS
    file_path = OUT
    time_period = TAX_YEAR

    def generate(self):
        build_prcs()

"""Reform files: a YAML per reform, the unit EA stores, versions and scores.

    name: Ampliar el tramo de 0% a $12,000
    name_en: Widen the 0% bracket to $12,000
    description: ...
    source: Proyecto de la Cámara 1234, 15 de marzo de 2027
    start: 2025-01-01          # when the new values take effect
    levers:
      gov.hacienda.income.rates[1].threshold: 12000
      gov.hacienda.credits.eitc.max.0: +20%    # relative to current law

Values are numbers, or strings "+20%" / "-10%" relative to the current-law
value at `start`. `load_reform(path)` returns (meta, changes) with changes
resolved to numbers; `reform_from_file(path)` returns the Reform class.

    from policyengine_pr.reforms.files import load_reform, reform_from_file
    meta, changes = load_reform("reforms/ampliar_tramo_0.yaml")
"""

from pathlib import Path

import yaml

from policyengine_pr.reforms.parametric import parametric_reform

REFORMS_DIR = Path(__file__).resolve().parents[2] / "reforms"


def current_value(path: str, instant: str) -> float:
    from policyengine_pr import system

    node = system.parameters
    for name in path.split("."):
        if "[" in name:
            name, index = name.split("[")
            node = node.children[name].brackets[int(index[:-1])]
        else:
            node = node.children[name]
    return float(node(instant))


def resolve(value, path: str, instant: str) -> float:
    if isinstance(value, str) and value.strip().endswith("%"):
        pct = float(value.strip().rstrip("%")) / 100
        return round(current_value(path, instant) * (1 + pct), 6)
    return float(value)


def load_reform(path):
    """(meta, changes) for a reform file; changes are {lever path: value}."""
    path = Path(path)
    doc = yaml.safe_load(path.read_text())
    start = str(doc.get("start", "2025-01-01"))
    levers = doc.get("levers") or {}
    changes = {k: resolve(v, k, start) for k, v in levers.items()}
    meta = {k: v for k, v in doc.items() if k != "levers"}
    meta.setdefault("name_en", meta.get("name"))
    meta["start"] = start
    meta["file"] = str(path)
    return meta, changes


def reform_from_file(path):
    meta, changes = load_reform(path)
    return parametric_reform(changes, start=meta["start"])


def list_reforms(directory=REFORMS_DIR):
    """All reform files in a directory, sorted by file name."""
    return [load_reform(p) for p in sorted(Path(directory).glob("*.yaml"))]

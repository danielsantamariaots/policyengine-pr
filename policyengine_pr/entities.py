"""
Entities for the Puerto Rico model.

Taxes are assessed on the tax unit (contribuyente individual or casados que
rinden planilla conjunta); benefits will mostly be assessed on the household.
"""

from policyengine_core.entities import build_entity

Household = build_entity(
    key="household",
    plural="households",
    label="Household",
    doc="A group of people sharing a living space.",
    roles=[
        {
            "key": "member",
            "plural": "members",
            "label": "Member",
            "doc": "A member of the household.",
        },
    ],
)

TaxUnit = build_entity(
    key="tax_unit",
    plural="tax_units",
    label="Tax unit",
    doc="The people included on a single Puerto Rico individual income tax return (planilla).",
    roles=[
        {
            "key": "member",
            "plural": "members",
            "label": "Member",
            "doc": "A member of the tax unit (filer, spouse or dependent).",
        },
    ],
)

PANUnit = build_entity(
    key="pan_unit",
    plural="pan_units",
    label="PAN núcleo de servicio",
    doc="The people who buy and prepare food together (Reglamento 8684, Art. 5): parents with their children of any age and anyone who moves in with them; a member aged 60+ who is not the head or spouse, a disabled adult or an independent student may be a separate núcleo.",
    roles=[
        {
            "key": "member",
            "plural": "members",
            "label": "Member",
            "doc": "A member of the núcleo de servicio.",
        },
    ],
)

Person = build_entity(
    key="person",
    plural="people",
    label="Person",
    doc="A single person.",
    is_person=True,
)

entities = [Household, TaxUnit, PANUnit, Person]

from policyengine_pr.model_api import *


class HUDArea(Enum):
    SAN_JUAN = "San Juan-Guaynabo, PR HUD Metro FMR Area"
    CAGUAS = "Caguas, PR HUD Metro FMR Area"
    FAJARDO = "Fajardo, PR HUD Metro FMR Area"
    BARRANQUITAS = "Barranquitas-Aibonito, PR HUD Metro FMR Area"
    AGUADILLA = "Aguadilla-Isabela, PR MSA"
    LARES_UTUADO = "Lares-Utuado, PR Exception Area (income limits; Aguadilla-Isabela FMRs)"
    ARECIBO = "Arecibo, PR MSA"
    GUAYAMA = "Guayama, PR MSA"
    MAYAGUEZ = "Mayagüez, PR MSA"
    LAS_MARIAS = "Las Marías Municipio, PR Exception Area (income limits; Mayagüez FMRs)"
    SAN_GERMAN = "San Germán, PR MSA"
    PONCE = "Ponce, PR MSA"
    ADJUNTAS = (
        "Adjuntas Municipio, PR Exception Area (income limits; Ponce FMRs)"
    )
    YAUCO = "Yauco, PR MSA"
    NONMETRO = "Puerto Rico HUD Nonmetro Area"


class hud_area(Variable):
    value_type = Enum
    possible_values = HUDArea
    default_value = HUDArea.SAN_JUAN
    entity = Household
    label = "HUD FMR / income-limit area"
    documentation = "Input: the HUD area of the household's municipio (policyengine_pr/data/hud_areas.py maps all 78 municipios). Sets the Section 8 income limits and payment standard. In the PRCS it is assigned from the PUMA."
    definition_period = YEAR

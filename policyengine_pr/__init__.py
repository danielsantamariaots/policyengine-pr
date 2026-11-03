from policyengine_core.simulations import Simulation as CoreSimulation
from policyengine_core.taxbenefitsystems import TaxBenefitSystem

from policyengine_pr.entities import entities

from .constants import COUNTRY_DIR


class CountryTaxBenefitSystem(TaxBenefitSystem):
    entities = entities
    variables_dir = COUNTRY_DIR / "variables"
    parameters_dir = COUNTRY_DIR / "parameters"
    auto_carry_over_input_variables = True
    basic_inputs = [
        "age",
        "employment_income",
    ]

    def __init__(self):
        super().__init__(entities)


system = CountryTaxBenefitSystem()


class Simulation(CoreSimulation):
    default_tax_benefit_system = CountryTaxBenefitSystem
    default_tax_benefit_system_instance = system
    default_role = "member"
    default_calculation_period = 2024
    default_input_period = 2024


# Microsimulation is added once a PRCS-based dataset exists (phase 2).

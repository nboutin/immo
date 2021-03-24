
from openfisca_france import FranceTaxBenefitSystem
from openfisca_core.simulation_builder import SimulationBuilder


entities = {
    'individus': {'Nicolas': {'revenu_assimile_salaire': {'2020': 34000}},
                  'Audrey': {'revenu_assimile_salaire': {'2020': 25000}},
                  'Lya': {}},
    'foyers_fiscaux': {'roles': {'declarants': ['Nicolas', 'Audrey'],
                                 'personnes_a_charge': ['Lya']}},
    'menages': {'roles': {'personne_de_reference': 'Nicolas',
                          'conjoint': 'Audrey',
                          'enfants': 'Lya'}},
    'familles': {'roles': {'parents': ['Nicolas', 'Audrey'],
                           'enfants': ['Lya']}},
}


def main():
    tax_benefit_system = FranceTaxBenefitSystem()

    simulation_builder = SimulationBuilder()
    simulation = simulation_builder.build_from_entities(tax_benefit_system, entities)

    irpp = simulation.calculate('irpp', '2020')
    print("irpp", irpp)


if __name__ == '__main__':
    main()


from openfisca_france import FranceTaxBenefitSystem
from openfisca_core.simulation_builder import SimulationBuilder

# https://fr.openfisca.org/legislation/#search-input
# https://github.com/openfisca/openfisca-france/issues/1385

# impot_du: 3339.46
# don :200
# syndicat 143
# 3113
entities = {
    'individus': {'Nicolas': {'revenu_assimile_salaire': {'2019': 31407}},
                  'Audrey': {'revenu_assimile_salaire': {'2019': 23055},
                             'f7ac': {'2019': 143}},
                  'Lya': {}},
    'foyers_fiscaux': {'foyer1': {'declarants': ['Nicolas', 'Audrey'],
                                  'personnes_a_charge': ['Lya'],
                                  'f7uf': {'2019': 200},
                                  },
                       },
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
    # simulation.trace = True

    annee = '2019'

    print("revenu_assimile_salaire_apres_abattements", simulation.calculate(
        'revenu_assimile_salaire_apres_abattements', annee))
    print("revenu_categoriel_tspr", simulation.calculate('revenu_categoriel_tspr', annee))
    print("revenu_categoriel_foncier", simulation.calculate('revenu_categoriel_foncier', annee))
    print("rbg", simulation.calculate('rbg', annee))
    print("rng", simulation.calculate('rng', annee))
    print("rni", simulation.calculate('rni', annee))
    print("rfr", simulation.calculate('rfr', annee))
    print("ir_brut", simulation.calculate('ir_brut', annee))
    print("maries_ou_pacses", simulation.calculate('maries_ou_pacses', annee))
    print("nb_adult", simulation.calculate('nb_adult', annee))
    print("nbptr", simulation.calculate('nbptr', annee))
    print("ir_plaf_qf", simulation.calculate('ir_plaf_qf', annee))
    print("decote", simulation.calculate('decote', annee))
    print("ip_net", simulation.calculate('ip_net', annee))
    print("iai", simulation.calculate('iai', annee))
    print("f7ac", simulation.calculate('f7ac', annee))
    print("cotsyn", simulation.calculate('cotsyn', annee))
    print("credit_cotisations_syndicales", simulation.calculate('credit_cotisations_syndicales', annee))
    print("credits_impot", simulation.calculate('credits_impot', annee))
    print("irpp", simulation.calculate('irpp', annee))

    # simulation.tracer.print_computation_log()


if __name__ == '__main__':
    main()

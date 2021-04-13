#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
@date: 2021-04
@author: nboutin
'''

entities = {
    'lot': {'lot1': {'lot_type': {'2021-01': 'Commerce'},
                     'surface': {'2021-01': 64.85},
                     'loyer_nu': {'2021': 550 * 12},
                     'pno': {'2021': 100},
                     },
            'lot2': {'lot_type': {'2021-01': 'T3'},
                     'surface': {'2021-01': 62},
                     'loyer_nu': {'2021': 476 * 12},
                     'pno': {'2021': 100},
                     },
            'lot3': {'lot_type': {'2021-01': 'T3'},
                     'surface': {'2021-01': 62},
                     'loyer_nu': {'2021': 476 * 12},
                     'pno': {'2021': 100},
                     },
            'commun': {'lot_type': {'2021-01': 'Commun'}
                       },
            'not_used': {'loyer_nu': {'2021-01': 100}},
            },
    'bien_immo': {'bi1': {'lot': ['lot1', 'lot2', 'lot3', 'commun'],
                          'prix_achat': {'2021-01': 115000},
                          'taux_notaire': {'2021-01': 0.08},
                          'taux_agence': {'2021-01': 0.07},
                          'apport': {'2021-01': 0},
                          }},
    'credit': {'c1': {'duree': {'2021-01': 20 * 12},
                      'taux_interet': {'2021-01': 0.0115},
                      'taux_assurance': {'2021-01': 0.0035},
                      'frais_dossier': {'2021-01': 300},
                      'frais_garantie': {'2021-01': 0},
                      }},
    # 'analyse': {'ana1': {'bien_immo': 'bi1',
    # 'credit': 'c1',
    # 'groupe_fiscal': {}},
    # }
}

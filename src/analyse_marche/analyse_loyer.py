#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__NAME = 'Analyse loyer'
__VERSION = '0.1.0-dev'
__DATA_FILENAME = "data/location 20201205.csv"

import sys
from tabulate import tabulate
from analyse_tools import (load_csv, calcul_moyenne_median)


def main(argv):

    print('{} {}'.format(__NAME, __VERSION))

    data_csv = load_csv(__DATA_FILENAME)

    request = (
        {'ville': None, 'type': None, 'exploitation': 'Non-meublé', 'data': {}},
        {'ville': 'Châtellerault', 'type': 'T1', 'exploitation': 'Non-meublé', 'data': {}},
        {'ville': 'Châtellerault', 'type': 'T2', 'exploitation': 'Non-meublé', 'data': {}},
        {'ville': 'Châtellerault', 'type': 'T3', 'exploitation': 'Non-meublé', 'data': {}},
        {'ville': 'Châtellerault', 'type': 'T4', 'exploitation': 'Non-meublé', 'data': {}},
    )

    for r in request:
        filters = {'Ville': r['ville'], 'Type': r['type'], 'Exploitation': r['exploitation']}
        n, moy, med = calcul_moyenne_median(data_csv, critere='Loyer', filters=filters)
        r['data']['count'] = n
        r['data']['loyer_moyen'] = moy
        r['data']['loyer_median'] = med

        n, moy, med = calcul_moyenne_median(data_csv, critere='Surface', filters=filters)
        r['data']['surface_moyen'] = moy
        r['data']['surface_median'] = med

        r['data']['prix_surface_moyen'] = r['data']['loyer_moyen'] / r['data']['surface_moyen']
        r['data']['prix_surface_median'] = r['data']['loyer_median'] / r['data']['surface_median']

    output = [
        ['Ville', 'Type', 'Count', 'Loyer\nmoyen', 'Loyer\nmédian', 'Surface\nmoyenne', 'Surface\nmédianne',
         'Prix\nmoyen\ne/m²', 'Prix\nmedian\ne/m²'],
    ]

    input = list()
    for r in request:
        data = r['data']
        input = (r['ville'],
                 r['type'], data['count'],
                 '{:.2f}'.format(data['loyer_moyen']),
                 '{:.2f}'.format(data['loyer_median']),
                 '{:.2f}'.format(data['surface_moyen']),
                 '{:.2f}'.format(data['surface_median']),
                 '{:.2f}'.format(data['prix_surface_moyen']),
                 '{:.2f}'.format(data['prix_surface_median']),
                 )

        output.append(input)

    print(tabulate(output, headers="firstrow"))


if __name__ == '__main__':
    main(sys.argv[1:])

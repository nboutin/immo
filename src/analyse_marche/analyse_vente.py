#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__NAME = 'Analyse vente'
__VERSION = '0.1.0-dev'
__DATA_FILENAME = "data/vente.csv"

import sys
from tabulate import tabulate
from analyse_tools import (load_csv, calcul_moyenne_median)


def main(argv):

    print('{} {}'.format(__NAME, __VERSION))

    data_csv = load_csv(__DATA_FILENAME)

    print(data_csv[0])

    request = (
        {'ville': 'CHATELLERAULT', 'type': None, 'data': {}},
        {'ville': 'CHATELLERAULT', 'type': '1', 'data': {}},
        {'ville': 'CHATELLERAULT', 'type': '2', 'data': {}},
        {'ville': 'CHATELLERAULT', 'type': '3', 'data': {}},
        {'ville': 'CHATELLERAULT', 'type': '4', 'data': {}},
    )

    for r in request:
        filters = {'commune': r['ville'], 'nb_pieces': r['type']}
        n, moy, med = calcul_moyenne_median(data_csv, critere='surface_utile', filters=filters)
        r['data']['count'] = n
        r['data']['surface_moyen'] = moy
        r['data']['surface_median'] = med

        n, moy, med = calcul_moyenne_median(data_csv, critere='prix', filters=filters)
        r['data']['prix_moyen'] = moy
        r['data']['prix_median'] = med

        r['data']['prix_surface_moyen'] = r['data']['prix_moyen'] / r['data']['surface_moyen']
        r['data']['prix_surface_median'] = r['data']['prix_median'] / r['data']['surface_median']

    output = [
        ['Ville', 'Type', 'Count',
         'Surface\nmoyen', 'Surface\nmedian',
         'Prix\nmoyen', 'Prix\nmedian',
         'Prix\nmoyen\ne/m²', 'Prix\nmedian\ne/m²'],
    ]

    input = list()
    for r in request:
        data = r['data']
        input = (r['ville'],
                 r['type'], data['count'],
                 '{:.2f}'.format(data['surface_moyen']),
                 '{:.2f}'.format(data['surface_median']),
                 '{:.2f}'.format(data['prix_moyen']),
                 '{:.2f}'.format(data['prix_median']),
                 '{:.2f}'.format(data['prix_surface_moyen']),
                 '{:.2f}'.format(data['prix_surface_median']),
                 )

        output.append(input)

    print(tabulate(output, headers="firstrow"))


if __name__ == '__main__':
    main(sys.argv[1:])

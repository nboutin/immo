#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__NAME = 'Analyse marché'
__VERSION = '0.1.0-dev'
__DATA_FILENAME = "data/invest_immo-suivi_de_marche.csv"

import csv
import sys
import statistics
from tabulate import tabulate


def main(argv):

    print('{} {}'.format(__NAME, __VERSION))

    data_csv = load_csv(__DATA_FILENAME)

    request = (
        {'ville': None, 'type': None, 'data':{}},
        {'ville':'Châtellerault', 'type':'T1', 'data':{}},
        {'ville':'Châtellerault', 'type':'T2', 'data':{}},
        {'ville':'Châtellerault', 'type':'T3', 'data':{}},
        {'ville':'Châtellerault', 'type':'T4', 'data':{}},
        )

    for r in request:
        filters = {'Ville':r['ville'], 'Type':r['type']}
        n, moy, med = calcul_moyenne_median(data_csv, critere='Loyer', filters=filters)
        r['data']['count'] = n
        r['data']['loyer_moyen'] = moy
        r['data']['loyer_median'] = med

        n, moy, med = calcul_moyenne_median(data_csv, critere='Surface', filters=filters)
        r['data']['surface_moyen'] = moy
        r['data']['surface_median'] = med

        r['data']['prix_surface'] = r['data']['loyer_moyen'] / r['data']['surface_moyen']

    output = [
        ['Ville', 'Type', 'Count', 'Loyer\nmoyen', 'Loyer\nmédian', 'Surface\nmoyenne', 'Surface\nmédianne', 'Prix\ne/m²'],
    ]

    input = list()
    for r in request:
        data = r['data']
        input = (r['ville'], r['type'], data['count'], '{:.2f}'.format(data['loyer_moyen']), '{:.2f}'.format(data['loyer_median']),
                    '{:.2f}'.format(data['surface_moyen']), '{:.2f}'.format(data['surface_median']), '{:.2f}'.format(data['prix_surface']))

        output.append(input)

    print(tabulate(output, headers="firstrow"))


def load_csv(pathname):
    '''
    Convert CSV file into 
    @input: CSV file pathname
    @return: List of Ordered Dictionary
    '''
    result = list()

    # Load CSV file
    with open(pathname, newline='') as file:
        reader = csv.DictReader(file, delimiter=',')

        # Clean loaded data
        for row in reader:
            row.pop(None, None)  # Remove entry with key None from row dictionary
            row.pop('', None)  # Remove entry with empty key

            # Remove row with all fields equal to None or are empty
            if not all(v == None or v == '' for k, v in row.items()):
                result.append(row)

    return result


def calcul_moyenne_median(data_csv, critere, filters):

    selection = list()

    for row in data_csv:

        select = True
        for k, v in filters.items():

            if (select and row[k] == v) or v == None:
                select = True
            else:
                select = False

        if select:
            selection.append(int(row[critere]))

    return len(selection), statistics.mean(selection), statistics.median_grouped(selection)


if __name__ == '__main__':
    main(sys.argv[1:])

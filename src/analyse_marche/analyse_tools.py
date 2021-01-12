#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import csv
import statistics


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

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import calcul

__DATA_FILENAME = "data.json"


def main():
    
    with open(__DATA_FILENAME, 'r') as file:
        data = json.load(file)
    
    bien_immo = dict()    
    
    prepare_data(data, bien_immo)
    
    bien_immo['r_brut'] = calcul_rendement_brut(data, bien_immo)
    
    print_repport(data, bien_immo)


def prepare_data(data, bien_immo):
    
    bien_immo['loyers_mensuel_total'] = sum(data['loyers_mensuel'])
    bien_immo['loyers_annuel_total'] = bien_immo['loyers_mensuel_total'] * 12 


def calcul_rendement_brut(data, bien_immo):
    
    return calcul.rendement_brut(bien_immo['loyers_annuel_total'], data['prix_achat'])


def compute_rendement_net(data, bien_immo):
    
    return 0


def print_repport(data, bien_immo):
    
    print('Input:', data)
    print('Output:', bien_immo)


if __name__ == '__main__':
  main()

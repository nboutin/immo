#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import calcul

__DATA_FILENAME = "data.json"


def main():
    
    with open(__DATA_FILENAME, 'r') as file:
        bien_immo = json.load(file)
    
    prepare_inputs(bien_immo)
    
    calcul_rendement_brut(bien_immo)
    
    print_repport(bien_immo)


def prepare_inputs(bien_immo):
    
    bien_immo['loyers_mensuel_total'] = 0
    for lot in bien_immo['lots']:
        bien_immo['loyers_mensuel_total'] += lot['loyer_mensuel']
    
    bien_immo['loyers_annuel_total'] = bien_immo['loyers_mensuel_total'] * 12 


def calcul_rendement_brut(bien_immo):
    
    bien_immo['r_brut'] = calcul.rendement_brut(bien_immo['loyers_annuel_total'], bien_immo['prix_achat'])


def compute_rendement_net(bien_immo):
    
    return 0


def print_repport(bien_immo):
    
    print(bien_immo)


if __name__ == '__main__':
  main()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json

__DATA_FILENAME = "data.json"


def main():
    
    with open(__DATA_FILENAME, 'r') as file:
        data = json.load(file)
    
    bien_immo = dict()    
    
    prepare_data(data, bien_immo)
    
    bien_immo['r_brut'] = compute_rendement_brut(data, bien_immo)
    
    print_repport(data, bien_immo)


def prepare_data(data, bien_immo):
    
    bien_immo['loyers_sum'] = sum(data['loyers'])


def compute_rendement_brut(data, bien_immo):
    
    return bien_immo['loyers_sum'] / (data['prix_achat'])


def print_repport(data, bien_immo):
    
    print('Input:', data)
    print('Output:', bien_immo)


if __name__ == '__main__':
  main()

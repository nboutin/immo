#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Charge recuperable/locative
    https://www.service-public.fr/particuliers/vosdroits/F947
    Les charges locatives (ou charges récupérables) sont des dépenses payées initialement par le propriétaire. 
    Le propriétaire se fait rembourser par le locataire.
    - entretien de l'immeuble et des equipements
    - consommations communes
    - consommations personnelles
    - taxe enlevement ordures menageres
    - autres
Charge deductible:
    - frais administration et gestion
    - prime d'assurance (pno, impayé)
    - depenses reparation, entretien, amelioration
    - charges recuperable non recuperees au depart du locataire
    - indeminité d'eviction, frais de relogement
    - taxe fonciere, taxe annexes
    - regimes particuliers, deduction spécifiques
Charge non-deductible:
    - capital d'emprunt (amortissement)
    - autres
Interet d'emprunt (inclu assurance et frais)
Syndic de copropriete:
    - provision pour charges
    - Arrete des comptes
        - saisie rapide du decompte annuel
        - charges recuperable/locative
        - charges deductibles
        - remboursement recu du syndic
        - versement complementaire au syndic
    - avance, provisions et cotisation travaux (non deductible)
    - gros travaux deductibles
'''

class Charge:
    
    def __init__(self):
        pass
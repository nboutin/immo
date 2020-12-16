#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from charge import Charge


class Impot_Regime_Reel:
    '''
    https://www.corrigetonimpot.fr/impot-location-vide-appartement-proprietaire-calcul/
    
    charges deductibles:
        - interet d'emprunt
        - assurance emprunteur
        - assurance PNO
        - taxe fonciere
        - frais bancaire, frais de dossier, fond mutuelle de garantie
        - frais postaux a destination du locataire
        - travaux
    '''

    def __init__(self, database, bien_immo, tmi):

        self._database = database        
        self._bi = bien_immo
        self._tmi = tmi
        
    @property
    def base_impossable(self):
        base = self._bi.loyer_nu_annuel

        base -= self._bi.get_charge(
            [Charge.deductible_e.copropriete,
             Charge.deductible_e.taxe_fonciere,
             Charge.deductible_e.prime_assurance,
             Charge.gestion_e.agence_immo, ])

        # todo: interet
        # todo: assurance emprunteur
        return base
        
    @property
    def revenu_foncier_impossable(self):
        return self.base_impossable * self._tmi
    
    @property
    def prelevement_sociaux_montant(self):
        return self.base_impossable * self._database.prelevement_sociaux_taux
    
    @property
    def impot_total(self):
        return self.revenu_foncier_impossable + self.prelevement_sociaux_montant
        

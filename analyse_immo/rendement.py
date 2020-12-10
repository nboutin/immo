#!/usr/bin/env python3
# -*- coding: utf-8 -*-


class Rendement:
    
    def __init__(self, bien_immo):
        
        self._bien_immo = bien_immo
        
    @property
    def rendement_brut(self):
        return self._bien_immo.loyer_annuel_total / self._bien_immo.investissement_initial

    @property
    def rendement_methode_larcher(self):
        '''
        La méthode larcher de calcul du rendement permet une approximation rapide 
        du rendement net.
        Les charges sont évaluées à 25% soit 3 mois de loyer
        '''
        return (self._bien_immo.loyer_mensuel_total * 9) / self._bien_immo.investissement_initial

    @property
    def rendement_net(self):
        return (self._bien_immo.loyer_annuel_total - self._bien_immo.charges_annuel_total) / \
            self._bien_immo.investissement_initial

    def cashflow_mensuel(self, credit):
        return self.cashflow_annuel(credit) / 12

    def cashflow_annuel(self, credit):
        return self._bien_immo.loyer_annuel_total - credit.get_mensualite_avec_assurance() * 12 \
            -self._bien_immo.charges_annuel_total

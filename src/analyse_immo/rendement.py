#!/usr/bin/env python3
# -*- coding: utf-8 -*-


class Rendement:

    def __init__(self, bien_immo, credit=None):

        self._bi = bien_immo
        self._credit = credit

    @property
    def rendement_brut(self):
        try:
            return self._bi.loyer_nu_brut_annuel / self.investissement_initial
        except ZeroDivisionError:
            return 0

    @property
    def rendement_methode_larcher(self):
        '''
        La méthode larcher de calcul du rendement permet une approximation rapide
        du rendement net.
        Les charges sont évaluées à 25% soit 3 mois de loyer
        '''
        try:
            return (self._bi.loyer_nu_brut_mensuel * 9) / self.investissement_initial
        except ZeroDivisionError:
            return 0

    @property
    def rendement_net(self):
        try:
            return (self._bi.loyer_nu_net_annuel - self._bi.charges -
                    self._bi.provisions) / self.investissement_initial
        except ZeroDivisionError:
            return 0

    @property
    def investissement_initial(self):
        result = self._bi.prix_net_vendeur + self._bi.notaire_montant + self._bi.agence_montant + \
            self._bi.budget_travaux - self._bi.apport
        return result

    @property
    def cashflow_net_mensuel(self):
        return self.cashflow_net_annuel / 12

    @property
    def cashflow_net_annuel(self):
        return self._bi.loyer_nu_net_annuel - self._credit.get_mensualite_avec_assurance() * 12 - self._bi.charges - \
            self._bi.provisions

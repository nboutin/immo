#!/usr/bin/env python3
# -*- coding: utf-8 -*-


class Rendement:

    def __init__(self, bien_immo, credit=None):

        self._bi = bien_immo
        self._credit = credit

    @property
    def rendement_brut(self):
        return self._bi.loyer_nu_annuel / self.investissement_initial

    @property
    def rendement_methode_larcher(self):
        '''
        La méthode larcher de calcul du rendement permet une approximation rapide
        du rendement net.
        Les charges sont évaluées à 25% soit 3 mois de loyer
        '''
        return (self._bi.loyer_nu_mensuel * 9) / self.investissement_initial

    @property
    def rendement_net(self):
        return (self._bi.loyer_nu_annuel - self._bi.charge_gestion - self._bi.charge_fonciere) \
            / self.investissement_initial

    @property
    def investissement_initial(self):
        result = self._bi.prix_net_vendeur + self._bi.notaire_montant + self._bi.agence_montant + \
            self._bi.budget_travaux - self._bi.apport

#         if self._credit:
#             result += self._credit.frais_dossier + self._credit.frais_garantie

        return result

    @property
    def cashflow_mensuel(self):
        return self.cashflow_annuel / 12

    @property
    def cashflow_annuel(self):
        return self._bi.loyer_nu_annuel - self._credit.get_mensualite_avec_assurance() * 12 \
            - self._bi.charge_gestion - self._bi.charge_fonciere

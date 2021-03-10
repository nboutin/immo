#!/usr/bin/env python3
# -*- coding: utf-8 -*-


class Rendement:

    def __init__(self, bien_immo, credit, irpp):
        self._bi = bien_immo
        self._credit = credit
        self._irpp = irpp

    @property
    def rendement_brut(self):
        try:
            return self._bi.loyer_nu_brut_annuel(1) / self.investissement_initial
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
            return (self._bi.loyer_nu_brut_mensuel(1) * 9) / self.investissement_initial
        except ZeroDivisionError:
            return 0

    def rendement_net(self, i_year):
        '''
        :param i_year: int start at 1
        '''
        try:
            return (self._bi.loyer_nu_net_annuel(i_year) - self._bi.charges(i_year) -
                    self._bi.provisions(i_year)) / self.investissement_initial
        except ZeroDivisionError:
            return 0

    @property
    def investissement_initial(self):
        result = self._bi.prix_net_vendeur + self._bi.notaire_montant + self._bi.agence_montant + \
            self._bi.travaux_montant - self._bi.apport
        return result

    def cashflow_net_mensuel(self, i_year):
        '''
        moyenne du cashflow annuel rapporté sur un mois
        :param i_year : int, start at 1
        '''
        return self.cashflow_net_annuel(i_year) / 12

    def cashflow_net_annuel(self, i_year):
        '''
        :param i_year : int, start at 1
        '''
        e_month = i_year * 12
        b_month = e_month - 12 + 1
        return self._bi.loyer_nu_net_annuel(i_year) - self._credit.get_mensualite_avec_assurance(
            b_month, e_month) - self._bi.charges(i_year) - self._bi.provisions(i_year)

    def cashflow_net_net_annuel(self, i_year):
        '''
        cashflow net après impot
        '''
        e_month = i_year * 12
        b_month = e_month - 12 + 1
        return self._bi.loyer_nu_net_annuel(i_year) - self._credit.get_mensualite_avec_assurance(
            b_month, e_month) - self._bi.charges(i_year) - self._bi.provisions(i_year) - self._irpp[i_year - 1].impots_revenu_foncier

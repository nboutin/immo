#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from analyse_immo import credit


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
            self._bi.travaux_montant + self._credit.frais_dossier + self._credit.frais_garantie - self._bi.apport
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

    def cashflow_net_net_annuel(self, annee: str):
        '''
        cashflow net après impot
        '''
        annee_int = int(annee)
        e_month = annee_int * 12
        b_month = annee_int - 12 + 1
        return self._bi.loyer_nu_net_annuel(annee_int) - self._credit.get_mensualite_avec_assurance(
            b_month, e_month) - self._bi.charges(annee_int) - self._bi.provisions(annee_int) - self._irpp.impot_revenu_foncier(annee)

    def ratio_locatif_bancaire(self, i_year):
        '''
        :brief Ratio locatif bancaire positif si mensualité de credit < 70% des loyers mensuels HC
        :return tuple (boolean, ratio)
        '''
        e_month = i_year * 12
        b_month = e_month - 12 + 1
        credit_mensualite = self._credit.get_mensualite_avec_assurance(b_month, e_month)
        loyer_mensuel_hc = self._bi.loyer_nu_net_annuel(i_year)

        ratio_status = True if loyer_mensuel_hc * .7 >= credit_mensualite else False
        ratio_value = credit_mensualite / loyer_mensuel_hc

        return (ratio_status, ratio_value)

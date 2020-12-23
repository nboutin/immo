#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from enum import unique, Enum, auto
from ligne import Ligne
from analyse_immo.impots.annexe_2044 import Annexe_2044

L1AJ_salaire = Ligne('1AJ', 'Salaires - Déclarant 1')
L1BJ_salaire = Ligne('1BJ', 'Salaires - Déclarant 2')
L7UF_dons = Ligne('7UF', 'Dons aux oeuvres')
L7AE_syndicat = Ligne('7AE', 'Cotisations syndicales - Déclarant 2')

# 4BE Micro foncier - recettes brutes
# 4BA Revenu foncier impossable


class IRPP:
    '''
    L’impôt sur le revenu des personnes physiques (IRPP)
    IR = IRPP + CSG(secu) + CRDS (dettes)
    https://www.tacotax.fr/guides/impot-sur-le-revenu

    Revenu
        Salaire & deduction
        revenu foncier
        Total = Revenu fiscale de reference

        salaires = auto()
        investissement = auto()  # Action, assurance vie, PEA, PER, ...
        revenu_foncier = auto()
        plus_value_immobiliere = auto()
        bic = auto() # benefice commerciaux et industrielle
        ba = auto() # benefice commerciaux agricoles
        retraite = auto()
        indemnite = auto()
        primes = auto()
    '''

    def __init__(self, database, annee, part_fiscale, n_enfant):
        '''
        :param salaires: list des salaires du foyer
        '''
        self._database = database
        self._annee = annee
        self._part_fiscale = part_fiscale
        self._n_enfant = n_enfant

        self._lignes = list()
        self._annexes = list()

    def add_ligne(self, type_, value):
        self._lignes.append((type_, value))

    def add_annexe(self, annexe):
        self._annexes.append(annexe)

    @property
    def salaires(self):
        return self.__get_ligne(('1AJ', '1BJ'))

    @property
    def revenu_fiscale_reference(self):
        '''
        :todo Ajouter revenu foncier
        '''
        rfr = self.salaires * (1 - self._database.salaire_abattement)
        for annexe in self._annexes:
            if isinstance(annexe, Annexe_2044):
                rfr += annexe.revenu_foncier_taxable
        return rfr

    @property
    def total_reduction_impot(self):
        return self.__get_ligne(('7UF'))

    @property
    def total_credit_impot(self):
        return self.__get_ligne(('7AE'))

    @property
    def impots_brut(self):
        '''
        impot sur le revenu sousmis au bareme
        '''
        quotient_familial = self.revenu_fiscale_reference / self._part_fiscale
        impot_brut = self._impots_brut(self._database.TMI(str(self._annee)), quotient_familial)
        impot_brut *= self._part_fiscale
        return impot_brut

    @property
    def impots_net(self):
        net = self.impots_brut
        net -= self._database.reduction_dons * self.total_reduction_impot
        net -= self._database.reduction_syndicat * self.total_credit_impot
        return net

    def __get_ligne(self, numero):
        return sum(ligne[1] for ligne in self._lignes if ligne[0].numero in numero)

    def _impots_brut(self, tmi, quotient_familial):

        impots_brut = 0
        tranche_p = 0

        for tranche, taux in tmi:

            impots_brut += max(min(tranche - tranche_p, quotient_familial - tranche_p) * taux, 0)
            tranche_p = tranche

        return impots_brut

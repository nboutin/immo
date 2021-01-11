#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# from enum import unique, Enum, auto
from analyse_immo.impots.ligne import Ligne
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

    Source:
    https://www.service-public.fr/particuliers/vosdroits/F34328
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

    def __init__(self, database, annee_revenu, part_fiscale, n_enfant):
        '''
        :param annee_revenu(int): annee_revenu + 1 = annee_imposition
        '''
        self._database = database
        self._annee_revenu = annee_revenu
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
    def revenu_net_impossable(self):
        '''
        sommes des salaires retrancher de 10% moins les charges déductibles et abattements
        '''
        return self.salaires * (1 - self._database.salaire_abattement)

    @property
    def revenu_fiscale_reference(self):
        rfr = self.revenu_net_impossable
        rfr += self.revenu_foncier
        return rfr

    @property
    def revenu_foncier(self):
        return sum(
            annexe.revenu_foncier_taxable for annexe in self._annexes if isinstance(
                annexe, Annexe_2044))

    @property
    def total_reduction_impot(self):
        return self.__get_ligne(('7UF'))

    @property
    def total_credit_impot(self):
        return self.__get_ligne(('7AE'))

    @property
    def quotient_familial(self):
        return self.revenu_fiscale_reference / self._part_fiscale

    @property
    def impots_brut(self):
        '''
        impot sur le revenu sousmis au bareme
        '''
        impot_brut = self.__impots_brut_part_fiscale()

        # Controler dépassement d'abattement enfant
        impot_brut_sans_enfant = self.__impots_brut_sans_enfant()

        reduction_enfants = impot_brut_sans_enfant - impot_brut
        plafond_quotient_familial = self._database.plafond_quotient_familial(
            self._annee_revenu + 1) * self._n_enfant

        if reduction_enfants > plafond_quotient_familial:
            impot_brut += reduction_enfants - plafond_quotient_familial

        return impot_brut

    @property
    def impots_net(self):
        net = self.impots_brut
        net -= self._database.reduction_dons * self.total_reduction_impot
        net -= self._database.reduction_syndicat * self.total_credit_impot
        return net

    # Private

    def __get_ligne(self, numero):
        return sum(ligne[1] for ligne in self._lignes if ligne[0].numero in numero)

    def __impots_brut_sans_enfant(self):
        import copy
        part = self._part_fiscale - self._n_enfant / 2
        irpp_sans_enfant = copy.deepcopy(self)
        irpp_sans_enfant._part_fiscale = part
        irpp_sans_enfant._n_enfant = 0
        return irpp_sans_enfant.__impots_brut_part_fiscale()
#         irpp_sans_enfant = IRPP(self._database, self._annee_revenu, part, 0)
#         irpp_sans_enfant.add_ligne(L1AJ_salaire, salaires)
#         return irpp_sans_enfant.__impots_brut_part_fiscale()

    def __impots_brut_part_fiscale(self):
        bareme = self._database.irpp_bareme(str(self._annee_revenu + 1))
        impot_brut = self._impots_brut(bareme, self.quotient_familial)
        impot_brut *= self._part_fiscale
        return impot_brut

    def _impots_brut(self, bareme, quotient_familial):

        impots_brut = 0
        tranche_p = 0

        for tranche, taux in bareme:
            tranche_restant = min(tranche - tranche_p, quotient_familial - tranche_p)
            tranche_restant = max(tranche_restant, 0)
            impots_brut += tranche_restant * taux
            tranche_p = tranche + 1

        return impots_brut

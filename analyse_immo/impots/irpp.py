#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from enum import unique, Enum, auto


class IRPP:
    '''
    L’impôt sur le revenu des personnes physiques (IRPP)
    IR = IRPP + CSG(secu) + CRDS (dettes)
    https://www.tacotax.fr/guides/impot-sur-le-revenu

    Revenu
        Salaire & deduction
        revenu foncier

        Total = Revenu fiscale de reference

    '''

    @unique
    class revenu_e(Enum):
        salaires = auto()
        investissement = auto()  # Action, assurance vie, PEA, PER, ...
        revenu_foncier = auto()
        plus_value_immobiliere = auto()
#         bic = auto() # benefice commerciaux et industrielle
#         ba = auto() # benefice commerciaux agricoles
#         retraite = auto()
#         indemnite = auto()
#         primes = auto()

    @unique
    class reduction_e(Enum):
        dons = auto()
        cotisations_syndicales = auto()

    def __init__(self, database, annee, part_fiscale, n_enfant):
        '''
        :param salaires: list des salaires du foyer
        '''
        self._database = database
        self._annee = annee
        self._part_fiscale = part_fiscale
        self._n_enfant = n_enfant
        self._revenus = list()
        self._reductions = list()

    def add_revenu(self, type_, value):
        self._revenus.append((type_, value))

    def get_revenu(self, type_):
        value = 0
        for revenu in self._revenus:
            if type_ == revenu[0]:
                value += revenu[1]
        return value

    def add_reduction(self, type_, value):
        self._reductions.append((type_, value))

    def get_reduction(self, type_):
        value = 0
        for reduction in self._reductions:
            if type_ == reduction[0]:
                value += reduction[1]
        return value

    @property
    def revenu_fiscale_reference(self):
        rfr = self.get_revenu(IRPP.revenu_e.salaires) * \
            (1 - self._database.salaire_abattement)
        rfr += self.get_revenu(IRPP.revenu_e.revenu_foncier)

        return rfr

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
        net -= self._database.reduction_dons * self.get_reduction(IRPP.reduction_e.dons)
        net -= self._database.reduction_syndicat * \
            self.get_reduction(IRPP.reduction_e.cotisations_syndicales)
        return net

    def _impots_brut(self, tmi, quotient_familial):

        impots_brut = 0
        tranche_p = 0

        for tranche, taux in tmi:

            impots_brut += max(min(tranche - tranche_p, quotient_familial - tranche_p) * taux, 0)
            tranche_p = tranche

        return impots_brut

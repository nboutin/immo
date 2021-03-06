#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from analyse_immo.charge import Charge


class Lot:

    def __init__(self, type_, surface, loyer_nu_mensuel):
        self._type = type_
        self._surface = surface
        self._loyer_nu_mensuel = loyer_nu_mensuel
        self.charge = Charge(self, None)

    @property
    def type(self):
        return self._type

    @property
    def surface(self):
        return self._surface

    @property
    def loyer_nu_brut_mensuel(self):
        return self._loyer_nu_mensuel

    @property
    def loyer_nu_brut_annuel(self):
        return self.loyer_nu_brut_mensuel * 12

    @property
    def loyer_nu_net_mensuel(self):
        return self.loyer_nu_net_annuel / 12

    @property
    def loyer_nu_net_annuel(self):
        '''
        Provision sur loyer nu brut de:
            - vacance locative
        '''
        vacance_locative = self.charge.get_montant_annuel(Charge.charge_e.vacance_locative)
        return self.loyer_nu_brut_annuel - vacance_locative

    @property
    def charge(self):
        return self._charge

    @charge.setter
    def charge(self, value):
        self._charge = value

#     @property
#     def vacance_locative_taux_annuel(self):
#         return self._vacance_locative_taux_annuel
#
#     @property
#     def vacance_locative_montant_annuel(self):
#         return self.loyer_nu_brut_annuel * self._vacance_locative_taux_annuel

#     @property
#     def pno_montant_annuel(self):
#         return self._PNO
#
#     @property
#     def gestion_agence_montant_annuel(self):
#         return self.loyer_nu_brut_annuel * self._gestion_agence_taux
#
#     @property
#     def copropriete_mensuel(self):
#         return self._copropriete_mensuel
#
#     @property
#     def copropriete_annuel(self):
#         return self.copropriete_mensuel * 12

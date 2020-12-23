#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from charge import Charge


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
    def loyer_nu_mensuel(self):
        return self._loyer_nu_mensuel

    @property
    def loyer_nu_annuel(self):
        return self.loyer_nu_mensuel * 12

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
#         return self.loyer_nu_annuel * self._vacance_locative_taux_annuel

#     @property
#     def pno_montant_annuel(self):
#         return self._PNO
#
#     @property
#     def gestion_agence_montant_annuel(self):
#         return self.loyer_nu_annuel * self._gestion_agence_taux
#
#     @property
#     def copropriete_mensuel(self):
#         return self._copropriete_mensuel
#
#     @property
#     def copropriete_annuel(self):
#         return self.copropriete_mensuel * 12

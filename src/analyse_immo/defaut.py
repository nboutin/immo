#!/usr/bin/env python3
# -*- coding: utf-8 -*-


class Defaut:

    def __init__(self, provision_travaux_taux,
                 vacance_locative_taux_T1,
                 vacance_locative_taux_T2,
                 gestion_agence_taux):

        self._provision_travaux_taux = provision_travaux_taux
        self._vacance_locative_taux = {}
        self._vacance_locative_taux['T1'] = vacance_locative_taux_T1
        self._vacance_locative_taux['T2'] = vacance_locative_taux_T2
        self._gestion_agence_taux = gestion_agence_taux

    @property
    def provision_travaux_taux(self):
        return self._provision_travaux_taux

    def vacance_locative_taux(self, type_):
        try:
            return self._vacance_locative_taux[type_]
        except KeyError:
            return 0

    @property
    def gestion_agence_taux(self):
        return self._gestion_agence_taux

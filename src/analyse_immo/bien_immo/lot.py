#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from .charge import Charge


class Lot:
    '''
    IRL
    2020 T4: 130.52 +0.19%
    2019 T4: 130.26 +0.95%
    2018 T4: 129.03 +1.74%
    2017 T4: 126.82 +1.05%
    2016 T4: 125.50
    '''

    def __init__(self, type_, surface, loyer_nu_mensuel, irl_taux=None):
        '''
        @param type_: type du lot T1,T2,T3,T4
        @param surface: surface en m² du lot
        @param loye_nu_mensuel: loyer du lot hors charges par mois
        @param irl_taux: taux d'évolution annuel de l'indice de reference des loyers
        '''
        self._type = type_
        self._surface = surface
        self._loyer_nu_mensuel = loyer_nu_mensuel
        self._irl_taux = irl_taux
        self._charge = Charge(self, None)

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
        '''
        @see: loyer_nu_net_annuel
        '''
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

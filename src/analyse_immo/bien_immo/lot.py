#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from .charge import Charge
from analyse_immo.tools import finance


class Lot:
    '''
    IRL
    https://www.anil.org/outils/indices-et-plafonds/tableau-de-lirl/
    2020 T4: 130.52 +0.19%
    2019 T4: 130.26 +0.95%
    2018 T4: 129.03 +1.74%
    2017 T4: 126.82 +1.05%
    2016 T4: 125.50
    '''

    def __init__(self, type_, surface, loyer_nu_mensuel, irl_taux_annuel=0):
        '''
        @param type_: type du lot T1,T2,T3,T4
        @param surface: surface en m² du lot
        @param loye_nu_mensuel: loyer du lot hors charges par mois
        @param irl_taux: taux d'évolution annuel de l'indice de reference des loyers
        '''
        self._type = type_
        self._surface = surface
        self._loyer_nu_brut_mensuel = loyer_nu_mensuel
        self._irl_taux_annuel = irl_taux_annuel
        self._charge = Charge(self, None)

    @property
    def type(self):
        return self._type

    @property
    def surface(self):
        return self._surface

    @property
    def irl_taux_annuel(self):
        return self._irl_taux_annuel

    def loyer_nu_brut_mensuel(self, i_month=1):
        '''
        @param i_month: month index start at 1
        '''
        i_month -= 1
        i_year = int(i_month / 12) + 1
        return self.loyer_nu_brut_annuel(i_year) / 12

    def loyer_nu_brut_annuel(self, i_year=1):
        '''
        @param: i_year: year index start at 1
        '''
        i_year -= 1
        return finance.capital_compose(self._loyer_nu_brut_mensuel * 12, self._irl_taux_annuel, i_year)

    def loyer_nu_net_mensuel(self, i_month=1):
        '''
        @see: loyer_nu_net_annuel
        '''
        i_month -= 1
        i_year = int(i_month / 12) + 1
        return self.loyer_nu_net_annuel(i_year) / 12

    def loyer_nu_net_annuel(self, i_year=1):
        '''
        Provision sur loyer nu brut de:
            - vacance locative
        '''
        vac_loc_taux = self.charge.get_taux(Charge.charge_e.vacance_locative)
        return self.loyer_nu_brut_annuel(i_year) * (1 - vac_loc_taux)

    @property
    def charge(self):
        return self._charge

    @charge.setter
    def charge(self, value):
        self._charge = value

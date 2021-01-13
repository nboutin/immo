#!/usr/bin/env python3
# -*- coding: utf-8 -*-


'4EB Micro Foncier'


class Micro_Foncier:
    '''
    https://www.corrigetonimpot.fr/impot-location-vide-appartement-proprietaire-calcul/
    '''

    def __init__(self):
        pass

    @property
    def revenu_foncier_taxable(self):
        return 0

#     def __init__(self, database, revenu_foncier, tmi):
#         self._database = database
#         self._revenu_foncier = revenu_foncier
#         self._tmi = tmi
#
#         if revenu_foncier > self._database.micro_foncier_revenu_foncier_plafond:
#             raise Exception("Revenu Foncier supérieur au plafond")
#
#     @property
#     def base_impossable(self):
#         return self._revenu_foncier * (1 - self._database.micro_foncier_taux)
#
#     @property
#     def revenu_foncier_impossable(self):
#         return self.base_impossable * self._tmi
#
#     @property
#     def prelevement_sociaux_montant(self):
#         return self.base_impossable * self._database.prelevement_sociaux_taux
#
#     @property
#     def impot_total(self):
#         return self.revenu_foncier_impossable + self.prelevement_sociaux_montant

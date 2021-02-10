#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from .ligne import Ligne

L4EB_recettes_brutes = Ligne('4EB', 'Micro foncier - recettes brutes')


class Micro_Foncier:
    '''
    https://www3.impots.gouv.fr/simulateur/calcul_impot/2020/aides/fonciers.htm
    https://www.corrigetonimpot.fr/impot-location-vide-appartement-proprietaire-calcul/
    '''

    def __init__(self, database):
        self._database = database
        self._lignes = list()

    def add_ligne(self, type_, valeur):
        if type_ == L4EB_recettes_brutes and valeur > self._database.micro_foncier_revenu_foncier_plafond:
            raise Exception("Revenu Foncier supérieur au plafond {}".format(
                self._database.micro_foncier_revenu_foncier_plafond))

        self._lignes.append({'type': type_, 'valeur': valeur})

    def get_ligne(self, lignes):
        if not isinstance(lignes, list):
            lignes = [lignes]
        return sum(ligne['valeur'] for ligne in self._lignes if ligne['type'] in lignes)

    @property
    def recettes_brutes(self):
        return self.get_ligne(L4EB_recettes_brutes)

    @property
    def revenu_foncier_taxable(self):
        return self.recettes_brutes * (1 - self._database.micro_foncier_taux)

    @property
    def prelevement_sociaux(self):
        return self.revenu_foncier_taxable * self._database.prelevement_sociaux_taux

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from enum import Enum, unique, auto
from charge import Charge


class Ligne:
    def __init__(self, numero, nom):
        self._numero = numero
        self._nom = nom

    @property
    def numero(self):
        return self._numero


L211_loyer_brut = Ligne(211, "loyer brut")
L221_frais_administration = Ligne(221, "frais d'administration")
L222_autre_frais_gestion = Ligne(222, "autre frais de gestion")
L223_prime_assurance = Ligne(223, "Prime d'assurance")
L224_travaux = Ligne(224, "Travaux reparation, entretien, amelioration")
L227_taxe_fonciere = Ligne(227, "Taxe fonciere")
L229_copropriete_provision = Ligne(229, "copropriete: provision pour charge")
L230_copropriete_regularisation = Ligne(230, "copropriete: regularisation des provision pour charges")
L250_interet_emprunt = Ligne(250, "interet d'emprunt")
L250_assurance_emprunteur = Ligne(250, "assurance emprunteur")
L250_frais_dossier = Ligne(250, "Frais de dossier")
L250_frais_garantie = Ligne(250, "Frais de garantie")


class Annexe_2044:
    '''
    https://www.corrigetonimpot.fr/impot-location-vide-appartement-proprietaire-calcul/

    210 Recettes (Titre)
    211 Loyer brut (année concernée, arriéré et percu d'avance)
    212 Dépense à payer par le proprietaire que le locataire à payé
    213 Subvention et indemnité impayé
    215 Total des recettes (211 à 214)
    220 Frais et charges (Titre)
    221 Frais d'administration (gardien, agence location, comptable, syndicat (UNPI), Procedure (avocat, huissier, expert))
    222 Autre frais de gestion (appel, courrier au locataire, 20€/lot)
    223 Prime d'assurance (PNO)
    224 Travaux reparation, entretien, amelioration
        https://www.corrigetonimpot.fr/revenu-foncier-travaux-deductibles-calcul-impot-revenu-louer/
    225 Charge recuperable non recupere au depart du locataire
    226 Indeminite eviction pour amelioration du logement
    227 Taxe fonciere (ne pas inclure les taxe d'ordure menagere)
    228 Deduction specifique (Besson, Borlo, Cosse)
    229 coproriete: provision pour charge annee n
    230 copropriete: regularisation des provisions pour charge annee n-1
    240 Total frais et charges: 221 à 229 - 230
    250 Interet d'emprunt, assurance emprunteur, frais dossier, frais garantie, ...
    261 Revenu foncier taxable: 215-240-250
    '''

    def __init__(self):
        self._lignes = list()

    def add_ligne(self, ligne, valeur):
        self._lignes.append((ligne, valeur))

    @property
    def total_recettes(self):
        '''Ligne 215'''
        return self.__get_ligne(211, 214)

    @property
    def total_frais_et_charges(self):
        '''Ligne 240'''
        return self.__get_ligne(221, 229) - self.__get_ligne(230)

    @property
    def total_charges_emprunt(self):
        '''Ligne 250'''
        return self.__get_ligne(250)

    @property
    def revenu_foncier_taxable(self):
        '''Ligne 260'''
        return self.total_recettes - self.total_frais_et_charges - self.total_charges_emprunt

    def __get_ligne(self, start, stop=None):
        if not stop:
            stop = start + 1
        else:
            stop += 1

        value = 0
        for ligne in self._lignes:
            if ligne[0].numero in range(start, stop):
                value += ligne[1]
        return value


#     def __init__(self, database, bien_immo, credit, tmi):
#         self._database = database
#         self._bi = bien_immo
#         self._credit = credit
#         self._tmi = tmi
#
#     @property
#     def base_impossable(self):
#         base = self._bi.loyer_nu_annuel
#
#         base -= self._bi.get_charge(
#             [Charge.deductible_e.copropriete,
#              Charge.deductible_e.taxe_fonciere,
#              Charge.deductible_e.prime_assurance,
#              Charge.gestion_e.agence_immo])
#
#         base -= self._credit.get_interet(1, 12)
#         base -= self._credit.get_mensualite_assurance(1, 12)
#         return base
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

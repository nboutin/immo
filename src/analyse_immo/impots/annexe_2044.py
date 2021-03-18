#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from .ligne import Ligne_Model
from .ligne_definition import *


class Annexe_2044:
    '''
    http://impotsurlerevenu.org/revenus-fonciers/781-la-declaration-de-revenus-fonciers-2044-notice-explicative.php
    https://www.corrigetonimpot.fr/impot-location-vide-appartement-proprietaire-calcul/
    Déficit foncier:
    https://www.journaldunet.fr/patrimoine/guide-des-finances-personnelles/1201987-deficit-foncier-2021-imputation-report-et-calcul/
    https://votreargent.lexpress.fr/conseils-placements/le-mecanisme-du-deficit-foncier-calcul-imputation-et-report_2122509.html
    '''

    def __init__(self, database):
        self._database = database
        self._ligne_model = Ligne_Model()
        self._deficit_reportable = None

    def add_ligne(self, ligne, value):
        self._ligne_model.add(ligne, value)
        self.compute()

    def sum_ligne(self, lignes):
        return self._ligne_model.sum(lignes)

    def compute(self):
        # Ligne 215 = 211 à 214
        self._ligne_model.update(L215_total_des_recettes,
                                 self.sum_ligne(
                                     [L211_loyer_brut,
                                      L212_depense_charge_locataire,
                                      L213_recettes_brutes_diverse,
                                      L214_valeur_locative]))
        # Case E = somme des ligne 215
        self._ligne_model.update(
            CaseE_total_recettes, self.sum_ligne(L215_total_des_recettes))

        # Ligne 240 = 221 à 229 bis - 230
        self._ligne_model.update(L224_total_travaux, self.sum_ligne([L224_travaux_provision, L224_travaux_renovation]))

        self._ligne_model.update(L240_total_frais_et_charges,
                                 self.sum_ligne(
                                     [L221_frais_administration,
                                      L222_autre_frais_gestion,
                                      L223_prime_assurance,
                                      L224_total_travaux,
                                      L225_charges_recuperable,
                                      L226_indemnites_eviction,
                                      L227_taxe_fonciere,
                                      L228_deductions_specifiques,
                                      L229_copropriete_provision,
                                      L229bis_deduction_travaux]) - self.sum_ligne(L230_regularisation_des_provisions))

        # Case F = somme des lignes 240
        self._ligne_model.update(CaseF_total_frais_charges, self.sum_ligne(L240_total_frais_et_charges))

        # Case G = somme des lignes 250, total des interets
        self._ligne_model.update(L250_total_emprunt,
                                 self.sum_ligne(
                                     [L250_assurance_emprunteur,
                                      L250_frais_dossier,
                                      L250_frais_garantie,
                                      L250_interet_emprunt]))
        self._ligne_model.update(CaseG, self.sum_ligne(L250_total_emprunt))

        # Ligne 260 Revenus foncier taxables
        self._ligne_model.update(L261_revenus_foncier_taxable,
                                 self.sum_ligne(L215_total_des_recettes)
                                 - self.sum_ligne(L240_total_frais_et_charges)
                                 - self.sum_ligne(L250_total_emprunt))
        # Ligne 263 = 261 + 262
        self._ligne_model.update(L263_benefice_deficit_foncier,
                                 self.sum_ligne([L261_revenus_foncier_taxable,
                                                 L262_reintegration_supplement_deduction]))
        # Case H : somme ligne 262
        self._ligne_model.update(CaseH, self.sum_ligne(
            L262_reintegration_supplement_deduction))

        # Case I: somme ligne 263
        self._ligne_model.update(
            CaseI, self.sum_ligne(L263_benefice_deficit_foncier))

        # L420 = case D + case I
        self._ligne_model.update(L420_resultat_foncier, self.sum_ligne(CaseI))

        self._ligne_model.update(L4BA_benefice_foncier, 0)
        self._ligne_model.update(L4BB_deficit_foncier_imputable_revenu_foncier, 0)
        self._ligne_model.update(L4BC_deficit_foncier_imputable_revenu_global, 0)

        L420 = self.sum_ligne(L420_resultat_foncier)
        if L420 > 0:
            self._ligne_model.update(L4BA_benefice_foncier, L420)
        else:
            # L431 = A + E + H
            self._ligne_model.update(L431_total_revenus_bruts,
                                     self.sum_ligne([CaseE_total_recettes, CaseH]))
            # L432 = C + G
            self._ligne_model.update(L432_total_interets_emprunts, self.sum_ligne([CaseG]))
            # L433 = B + F
            self._ligne_model.update(L433_total_autres_frais_et_charges, self.sum_ligne([CaseF_total_frais_charges]))

            self._ligne_model.update(L435_report_433, 0)
            self._ligne_model.update(L436_report_433, 0)
            self._ligne_model.update(L437_report_difference, 0)
            self._ligne_model.update(L438_total, 0)
            self._ligne_model.update(L440_report_420, 0)
            self._ligne_model.update(L441_report_420, 0)

            if self.sum_ligne(L432_total_interets_emprunts) > self.sum_ligne(L431_total_revenus_bruts):
                L433 = self.sum_ligne(L433_total_autres_frais_et_charges)
                self._ligne_model.update(L435_report_433, min(10700, L433))
                self._ligne_model.update(L436_report_433, max(0, L433 - 10700))
                self._ligne_model.update(L437_report_difference, self.sum_ligne(L432_total_interets_emprunts)
                                         - self.sum_ligne(L431_total_revenus_bruts))
                self._ligne_model.update(L438_total, self.sum_ligne([L436_report_433, L437_report_difference]))

                self._ligne_model.update(L4BC_deficit_foncier_imputable_revenu_global, self.sum_ligne(L435_report_433))
                self._ligne_model.update(L4BB_deficit_foncier_imputable_revenu_foncier, self.sum_ligne(L438_total))
            else:
                L420 = self.sum_ligne(L420_resultat_foncier)
                self._ligne_model.update(L440_report_420, min(10700, L420))
                self._ligne_model.update(L441_report_420, max(0, L420 - 10700))
                self._ligne_model.update(L4BC_deficit_foncier_imputable_revenu_global, self.sum_ligne(L440_report_420))
                self._ligne_model.update(L4BB_deficit_foncier_imputable_revenu_foncier, self.sum_ligne(L441_report_420))

    @property
    def total_charges_taux(self):
        return 1 - (self.sum_ligne(L420_resultat_foncier) / self.sum_ligne(CaseE_total_recettes))

    # @property
    # def prelevement_sociaux(self):
        # '''
        # @todo should not be here but in IRPP
        # '''
        # resultat_foncier = self.sum_ligne(L420_resultat_foncier)
        # if resultat_foncier > 0:
        # return resultat_foncier * self._database.prelevement_sociaux_taux
        # else:
        # return 0

    # @property
    # def L215_total_des_recettes(self):
        # return self.sum_ligne(L215_total_des_recettes)
        #
    # @property
    # def total_frais_et_charges(self):
        # pass
        #
    # @property
    # def total_charges_emprunt(self):
        # '''Ligne 250'''
        # return self.sum_ligne([L250_interet_emprunt, L250_assurance_emprunteur,
        # L250_frais_dossier, L250_frais_garantie])

    # @property
    # def resultat_foncier(self):
        # '''
        # Ligne 420: case D + case I
        # Si bénéfice, à reporter 4BA 2042
        # '''
        # return self.total_recettes - self.total_frais_et_charges - self.total_charges_emprunt

    # @property
    # def deficit_imputable_revenu_global(self):
        # '''
        # Si déficit foncier
        # Ligne 440: report ligne 420, limite 10700 ou 15300, a reporter 4BC 2042
        # '''
        # if self.resultat_foncier >= 0:
        # return 0
        #
        # plafond = self._database.deficit_foncier_plafond_annuel
        # return max(plafond, self.resultat_foncier)

    # @property
    # def deficit_imputable_revenu_foncier(self):
        # '''
        # Si déficit foncier
        # Ligne 441: report ligne 420, dépassant 10700 ou 15300, a reporter 4BB 2024
        # '''
        # if self.resultat_foncier >= 0:
        # return 0
        #
        # plafond = self._database.deficit_foncier_plafond_annuel
        # return self.resultat_foncier - plafond

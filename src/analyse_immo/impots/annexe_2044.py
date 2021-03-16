#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from .ligne import Ligne, Ligne_Model

# 210 Recettes
L211_loyer_brut = Ligne('211', "loyer brut")
L212_depense_charge_locataire = Ligne(
    '212', 'Depenses mise par convention a la charge des locataires')
L213_recettes_brutes_diverse = Ligne(
    '213', 'Recettes brutes diverses, subvention ANAH, indemnites assurance')
L214_valeur_locative = Ligne(
    '214', 'Valeur locative reelle des proprietes dont vous vous reservez la jouissance')
L215_total_des_recettes = Ligne('215', 'Total des recettes 211 à 214')

# 220 Frais et charges
L221_frais_administration = Ligne('221', "frais d'administration")
L222_autre_frais_gestion = Ligne('222', "autre frais de gestion")
L223_prime_assurance = Ligne('223', "Prime d'assurance")
L224_travaux = Ligne('224', "Travaux reparation, entretien, amelioration")
L225_charges_recuperable = Ligne(
    '225', 'Charges recuperables non recuperees au depart du locataire')
L226_indemnites_eviction = Ligne(
    '226', 'Indemnites d eviction, frais de relogement')
L227_taxe_fonciere = Ligne('227', "Taxe fonciere")

# Regimes particuliers
L228_deductions_specifiques = Ligne(
    '228', 'Deduction specifique de la ligne 215')

# Immeuble en copropriete
L229_copropriete_provision = Ligne('229', "copropriete: provision pour charge")
L229bis_deduction_travaux = Ligne(
    '229b', 'Deduction de 50% du montant des travaux deductibles')
L230_regularisation_des_provisions = Ligne(
    '230', "copropriete: regularisation des provision pour charges")
L240_total_frais_et_charges = Ligne('240', 'Total des frais et charges')

L250_interet_emprunt = Ligne('250', "interet d'emprunt")
# L250_assurance_emprunteur = Ligne('250b', "assurance emprunteur")
# L250_frais_dossier = Ligne('250c', "Frais de dossier")
# L250_frais_garantie = Ligne('250d', "Frais de garantie")

# 260 Revenu foncier taxable
L261_revenus_foncier_taxable = Ligne('261', 'Revenus foncier taxable')
L262_reintegration_supplement_deduction = Ligne('262', 'Reintegration du supplement de deduction')
L263_benefice_deficit_foncier = Ligne('263', 'Benefice ou deficit foncier')

L420_resultat_foncier = Ligne('420', 'Resultat benifice ou deficit')
L431_total_revenus_bruts = Ligne('431', 'Total des revenus bruts A+E+H')
L432_total_interets_emprunts = Ligne('432', 'Total des interets d emprunts')
L433_total_autres_frais_et_charges = Ligne(
    '433', 'Total des autres frais et charges')

L435_report_433 = Ligne('435', '')
L436_report_433 = Ligne('436', '')
L437_report_difference = Ligne('437', '')
L438_total = Ligne('438', '')
L440_report_420 = Ligne('440', '')
L441_report_420 = Ligne('441', '')

L451_deficit_foncier_anterieur = Ligne(
    '451', 'Deficit foncier anterieur non encore imputés')

LA_revenus_bruts = Ligne('A', 'Revenus bruts')  # Add L111
LB_frais_et_charges = Ligne(
    'B', 'Frais et charges sauf interets d emprunt')  # Add L112
LC_interets_emprunt = Ligne('C', 'Interets d emprunts')  # Add L113
LD_benefice_deficit = Ligne('D', 'Benefice ou deficit')  # Add L114
CaseE = Ligne('E', '')
CaseF = Ligne('F', '')
CaseG = Ligne('G', '')
CaseH = Ligne('H', '')
CaseI = Ligne('I', '')


class Annexe_2044:
    '''
    http://impotsurlerevenu.org/revenus-fonciers/781-la-declaration-de-revenus-fonciers-2044-notice-explicative.php
    https://www.corrigetonimpot.fr/impot-location-vide-appartement-proprietaire-calcul/
    Déficit foncier:
    https://www.journaldunet.fr/patrimoine/guide-des-finances-personnelles/1201987-deficit-foncier-2021-imputation-report-et-calcul/
    https://votreargent.lexpress.fr/conseils-placements/le-mecanisme-du-deficit-foncier-calcul-imputation-et-report_2122509.html

    Total case = somme des lignes
    Case A, Lignes 111 Revenus bruts
    Case B, Lignes 112 Frais et charges(sauf interet emprunt)
    Case C, Lignes 113 Interet d'emprunt
    Case D, Lignes 114 Benefice ou deficit

    210 Recettes (Titre)
    211 Loyer brut (année concernée, arriéré et percu d'avance)
    212 Dépense à payer par le proprietaire que le locataire à payé
    213 Subvention et indemnité impayé
    214 Valeur locative réelle des propriétés dont vous vous réservez la jouissance
    215 Total des recettes (total 211 à 214)

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

    261 Revenu foncier taxable: +215-240-250
    262 Reintegration du supplément de deduction
    263 Benefice ou deficit: 261+262
    Case I : Bénéfice ou déficit foncier global

    420 Resultat
    430-441 uniquement en cas de deficit
    431 Total des revenus bruts
    432 Total des interet d'emprunt
    433 Total autres frais et charges

    434 Si la ligne 432 est supérieure à la ligne 431
    435 Report de la ligne 433 dans la limite de 10 700 €
    436 Report de la ligne 433 : montant dépassant 10 700 €
    437 Report de la différence : ligne 432 – ligne 431
    438 Total : ligne 436 + ligne 437

    439 Si la ligne 432 est inférieure ou égale à la ligne 431
    440 Report de la ligne 420 dans la limite de 10 700 €
    441 Report de la ligne 420 : montant dépassant 10 700 €
    '''

    def __init__(self, database):
        self._database = database
        self._ligne_model = Ligne_Model()
        self._deficit_reportable = None

    def add_ligne(self, ligne, value, double=False):
        self._ligne_model.add(ligne, value, double)
        self.update()

    def sum_ligne(self, lignes):
        return self._ligne_model.sum(lignes)

    def update(self):
        # Ligne 215 = 211 à 214
        self._ligne_model.update(L215_total_des_recettes,
                                 self.sum_ligne(
                                     [L211_loyer_brut,
                                      L212_depense_charge_locataire,
                                      L213_recettes_brutes_diverse,
                                      L214_valeur_locative]))
        # Case E = somme des ligne 215
        self._ligne_model.update(
            CaseE, self.sum_ligne(L215_total_des_recettes))

        # Ligne 240 = 221 à 229 bis - 230
        self._ligne_model.update(self.sum_ligne(
            [L221_frais_administration,
             L222_autre_frais_gestion,
             L223_prime_assurance,
             L224_travaux,
             L225_charges_recuperable,
             L226_indemnites_eviction,
             L227_taxe_fonciere,
             L228_deductions_specifiques,
             L229_copropriete_provision,
             L229bis_deduction_travaux]) - self.sum_ligne(L230_regularisation_des_provisions))

        # Case F = somme des lignes 240
        self._ligne_model.update(
            CaseF, self.sum_ligne(L240_total_frais_et_charges))

        # Case G = somme des lignes 250, total des interets
        self._ligne_model.update(CaseG, self.sum_ligne(L250_interet_emprunt))

        # Ligne 260 Revenus foncier taxables
        self._ligne_model.update(L261_revenus_foncier_taxable,
                                 self.sum_ligne(L215_total_des_recettes)
                                 - self.sum_ligne(L240_total_frais_et_charges)
                                 - self.sum_ligne(L250_interet_emprunt))
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

        if self.sum_ligne(L420_resultat_foncier) <= 0:
            # L431 = A + E + H
            self.update(L431_total_revenus_bruts,
                        self.sum_ligne([CaseE, CaseH]))
            # L432 = C + G
            self.update(L432_total_interets_emprunts, self.sum_ligne([CaseG]))
            # L433 = B + F
            self.update(L433_total_autres_frais_et_charges, self.sum_ligne([CaseF]))

            self.update(L435_report_433, 0)
            self.update(L436_report_433, 0)
            self.update(L437_report_difference, 0)
            self.update(L438_total, 0)
            self.update(L440_report_420, 0)
            self.update(L441_report_420, 0)
            
            if self.sum_ligne(L432_total_interets_emprunts) > self.sum_ligne(L431_total_revenus_bruts):
                L433 = self.sum_ligne(L433_total_autres_frais_et_charges)
                self.update(L435_report_433, min(10700, L433))
                self.update(L436_report_433, max(0, L433 - 10700))
                self.update(L437_report_difference, self.sum_ligne(L432_total_interets_emprunts)
                            - self.sum_ligne(L431_total_revenus_bruts))
                self.update(L438_total, self.sum_ligne([L436_report_433, L437_report_difference]))
            else:
                L420 = self.sum_ligne(L420_resultat_foncier)
                self.update(L440_report_420, min(10700, L420))
                self.update(L441_report_420, max(0, L420 - 10700))

    @property
    def total_charges_taux(self):
        return 1 - (self.resultat_foncier / self.total_recettes)

    @property
    def prelevement_sociaux(self):
        if self.resultat_foncier > 0:
            return self.resultat_foncier * self._database.prelevement_sociaux_taux
        else:
            return 0

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

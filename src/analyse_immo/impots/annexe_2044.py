#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from .ligne import Ligne


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
        self._lignes = list()
        self._deficit_reportable = None

    def add_ligne(self, type_, valeur):
        self._lignes.append({'type': type_, 'valeur': valeur})

    def get_ligne(self, lignes):
        if not isinstance(lignes, list):
            lignes = [lignes]
        return sum(ligne['valeur'] for ligne in self._lignes if ligne['type'] in lignes)

    @property
    def total_recettes(self):
        '''Ligne 215 = 211 à 214'''
        return self.get_ligne(L211_loyer_brut)

    @property
    def total_frais_et_charges(self):
        '''Ligne 240'''
        return self.get_ligne([L221_frais_administration,
                               L222_autre_frais_gestion,
                               L223_prime_assurance,
                               L224_travaux,
                               L227_taxe_fonciere,
                               L229_copropriete_provision]) - self.get_ligne(L230_copropriete_regularisation)

    @property
    def total_charges_emprunt(self):
        '''Ligne 250'''
        return self.get_ligne([L250_interet_emprunt, L250_assurance_emprunteur,
                               L250_frais_dossier, L250_frais_garantie])

    @property
    def total_charges_taux(self):
        return 1 - (self.revenu_foncier_taxable / self.total_recettes)

    @property
    def resultat_foncier(self):
        '''
        Ligne 420: case D + case I
        Si bénéfice, à reporter 4BA 2042
        '''
        return self.total_recettes - self.total_frais_et_charges - self.total_charges_emprunt

    @property
    def deficit_imputable_revenu_global(self):
        '''
        Si déficit foncier
        Ligne 440: report ligne 420, limite 10700 ou 15300, a reporter 4BC 2042
        '''
        if self.resultat_foncier >= 0:
            return 0

        plafond = self._database.deficit_foncier_plafond_annuel
        return max(plafond, self.resultat_foncier)

    @property
    def deficit_imputable_revenu_foncier(self):
        '''
        Si déficit foncier
        Ligne 441: report ligne 420, dépassant 10700 ou 15300, a reporter 4BB 2024
        '''
        if self.resultat_foncier >= 0:
            return 0
        
        plafond = self._database.deficit_foncier_plafond_annuel
        return self.resultat_foncier - plafond
        

    @property
    def prelevement_sociaux(self):
        return self.revenu_foncier_taxable * self._database.prelevement_sociaux_taux


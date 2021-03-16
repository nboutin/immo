#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
@date: 2021-03-16
@author: nboutin
'''

from .ligne import Ligne

# IRPP Declaration 2042

L1AJ_salaire = Ligne('1AJ', 'Salaires - Declarant 1')
L1BJ_salaire = Ligne('1BJ', 'Salaires - Declarant 2')
L7UF_dons = Ligne('7UF', 'Dons aux oeuvres')
L7AE_syndicat = Ligne('7AE', 'Cotisations syndicales - Declarant 2')

L4BA_benefice_foncier = Ligne('4BA', 'Resultat foncier positif')
L4BB_deficit_foncier_imputable_revenu_foncier = Ligne('4BB', 'Deficit foncier imputable sur revenu foncier')
L4BC_deficit_foncier_imputable_revenu_global = Ligne('4BC', 'Deficit foncier imputable sur revenu globale')
L4BD_deficit_foncier_anterieur = Ligne('4BD', 'Deficit foncier ant�rieur')
L4_revenus_ou_deficits_nets_fonciers = Ligne('4', 'Revenus ou Deficits nets fonciers')

# 4BE Micro foncier - recettes brutes

# Annexe 2044

# 210 Recettes
L211_loyer_brut = Ligne('211', "loyer brut")
L212_depense_charge_locataire = Ligne('212', 'Depenses mise par convention a la charge des locataires')
L213_recettes_brutes_diverse = Ligne('213', 'Recettes brutes diverses, subvention ANAH, indemnites assurance')
L214_valeur_locative = Ligne('214', 'Valeur locative reelle des proprietes dont vous vous reservez la jouissance')
L215_total_des_recettes = Ligne('215', 'Total des recettes 211 � 214')

# 220 Frais et charges
L221_frais_administration = Ligne('221', "frais d'administration")
L222_autre_frais_gestion = Ligne('222', "autre frais de gestion")
L223_prime_assurance = Ligne('223', "Prime d'assurance")
L224_travaux = Ligne('224', "Travaux reparation, entretien, amelioration")
L225_charges_recuperable = Ligne('225', 'Charges recuperables non recuperees au depart du locataire')
L226_indemnites_eviction = Ligne('226', 'Indemnites d eviction, frais de relogement')
L227_taxe_fonciere = Ligne('227', "Taxe fonciere")

# Regimes particuliers
L228_deductions_specifiques = Ligne('228', 'Deduction specifique de la ligne 215')

# Immeuble en copropriete
L229_copropriete_provision = Ligne('229', "copropriete: provision pour charge")
L229bis_deduction_travaux = Ligne('229b', 'Deduction de 50% du montant des travaux deductibles')
L230_regularisation_des_provisions = Ligne('230', "copropriete: regularisation des provision pour charges")
L240_total_frais_et_charges = Ligne('240', 'Total des frais et charges')

L250_interet_emprunt = Ligne('250', "interet d'emprunt")
L250_assurance_emprunteur = Ligne('250', "assurance emprunteur")
L250_frais_dossier = Ligne('250', "Frais de dossier")
L250_frais_garantie = Ligne('250', "Frais de garantie")

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
    '451', 'Deficit foncier anterieur non encore imput�s')

LA_revenus_bruts = Ligne('A', 'Revenus bruts')  # Add L111
LB_frais_et_charges = Ligne('B', 'Frais et charges sauf interets d emprunt')  # Add L112
LC_interets_emprunt = Ligne('C', 'Interets d emprunts')  # Add L113
LD_benefice_deficit = Ligne('D', 'Benefice ou deficit')  # Add L114
CaseE = Ligne('E', '')
CaseF = Ligne('F', '')
CaseG = Ligne('G', '')
CaseH = Ligne('H', '')
CaseI = Ligne('I', '')

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from charge import Charge


class Impot_Regime_Reel:
    '''
    https://www.corrigetonimpot.fr/impot-location-vide-appartement-proprietaire-calcul/

    charges deductibles:
        - interet d'emprunt
        - assurance emprunteur
        - assurance PNO
        - taxe fonciere
        - frais bancaire, frais de dossier, fond mutuelle de garantie
        - frais postaux a destination du locataire
        - travaux

    210 Recettes (Titre)
    211 Loyer brut (année concernée, arriéré et percu d'avance)
    212 Dépense à payer par le proprietaire que le locataire à payé
    213 Subvention et indemnité impayé
    220 Frais et charges (Titre)
    221 Frais d'administration (gardien, agence location, comptable, syndicat (UNPI), Procedure (avocat, huissier, expert))
    222 Autre frais de festion (appel, courrier au locataire, 20€/lot)
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

    def __init__(self, database, bien_immo, credit, tmi):
        self._database = database
        self._bi = bien_immo
        self._credit = credit
        self._tmi = tmi

    @property
    def base_impossable(self):
        base = self._bi.loyer_nu_annuel

        base -= self._bi.get_charge(
            [Charge.deductible_e.copropriete,
             Charge.deductible_e.taxe_fonciere,
             Charge.deductible_e.prime_assurance,
             Charge.gestion_e.agence_immo])

        base -= self._credit.get_interet(1, 12)
        base -= self._credit.get_mensualite_assurance(1, 12)
        return base

    @property
    def revenu_foncier_impossable(self):
        return self.base_impossable * self._tmi

    @property
    def prelevement_sociaux_montant(self):
        return self.base_impossable * self._database.prelevement_sociaux_taux

    @property
    def impot_total(self):
        return self.revenu_foncier_impossable + self.prelevement_sociaux_montant

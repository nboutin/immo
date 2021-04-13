#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
@date: 2021-04
@author: nboutin
'''
# path must be absolute
from immo_analyse.core.variable import Variable
from immo_analyse.core.periods import ETERNITY, MONTH, YEAR
from immo_analyse.model.entities import Lot, BienImmo

# --- Lot


class lot_type(Variable):
    value_type = str
    entity = Lot
    period = MONTH
    label = 'Catégorisation du lot suivant son nombre de pièce à vivre'
    value_accepted = ['T1', 'T2', 'T3', 'Commercial', 'Commun']


class surface(Variable):
    value_type = float
    entity = Lot
    # entity = [Lot, BienImmo]
    period = MONTH
    label = 'surface habitable suivant la loi carrez'


class surface_annexe(Variable):
    value_type = float
    entity = Lot
    # entity = [Lot, BienImmo]
    period = MONTH
    label = 'surface annexe (cave, garage, ...)'


class loyer_nu(Variable):
    value_type = int
    entity = Lot
    period = MONTH
    year_to_month = True
    label = 'Loyer hors charges'


class travaux(Variable):
    value_type = float
    entity = Lot
    period = MONTH
    label = "Montant total des travaux"


class subvention(Variable):
    value_type = float
    entity = Lot
    period = MONTH
    label = "Subvention sum"

    def formula(population, period, parameter):
        anah = population('anah_subvention', period)
        habiter_mieux = population('prime_habiter_mieux', period)
        return anah + habiter_mieux


class anah_subvention(Variable):
    value_type = float
    entity = Lot
    period = MONTH
    label = ""


class anah_subvention_taux(Variable):
    value_type = float
    entity = Lot
    period = MONTH
    label = ""


class anah_subvention_plafond(Variable):
    value_type = float
    entity = Lot
    period = MONTH
    label = ""


class anah_subvention_base(Variable):
    value_type = float
    entity = Lot
    period = MONTH
    label = ""


class prime_habiter_mieux(Variable):
    value_type = float
    entity = Lot
    period = MONTH
    label = ""


class deficit_foncier_eligible(Variable):
    value_type = float
    entity = Lot
    period = MONTH
    label = ""


class charge_provision(Variable):
    value_type = int
    entity = Lot
    period = YEAR
    label = ''


class copropriete(Variable):
    value_type = int
    entity = Lot
    period = YEAR
    label = ''


class taxe_fonciere(Variable):
    value_type = int
    entity = Lot
    period = YEAR
    label = ''


class gestion_agence_taux(Variable):
    value_type = float
    entity = Lot
    period = YEAR
    label = ''


class pno(Variable):
    value_type = int
    entity = Lot
    period = YEAR
    label = 'Assurance proprietaire non-occupant'


class travaux_provision_taux(Variable):
    value_type = float
    entity = Lot
    period = YEAR
    label = ''


class vacance_locative_taux(Variable):
    value_type = float
    entity = Lot
    period = YEAR
    label = ''


# --- Bien Immo


class prix_achat(Variable):
    value_type = float
    entity = BienImmo
    period = MONTH
    label = "prix d'achat du bien immobilier sans frais annexe (notaire, agence, apport, subvention, ...)"


class taux_notaire(Variable):
    value_type = float
    entity = BienImmo
    period = MONTH
    label = "Taux des frais de notaire pour l'acquisition"


class frais_notaire(Variable):
    value_type = float
    entity = BienImmo
    period = MONTH
    label = "Frais de notaire pour l'acquisition"

    def formula(population, period, parameter):
        taux_notaire = population('taux_notaire', period)
        prix_achat = population('prix_achat', period)
        return prix_achat * taux_notaire


class taux_agence(Variable):
    value_type = float
    entity = BienImmo
    period = MONTH
    label = "Frais d'agence pour l'acquisition"


class frais_agence(Variable):
    value_type = float
    entity = BienImmo
    period = MONTH
    label = "Frais d'agence pour l'acquisition"

    def formula(population, period, parameter):
        taux_notaire = population('taux_agence', period)
        prix_achat = population('prix_achat', period)
        return prix_achat * taux_notaire


class apport(Variable):
    value_type = float
    entity = BienImmo
    period = MONTH
    label = "Apport personnel pour l'acquisition"


class financement(Variable):
    value_type = float
    entity = BienImmo
    period = MONTH
    label = "Somme des cout liés à l'acquisition du bien immobilier moins l'apport"

    def formula(population, period, parameter):
        prix_achat = population('prix_achat', period)
        frais_notaire = population('frais_notaire', period)
        frais_agence = population('frais_agence', period)
        travaux = population('travaux', period, entity_key=financement.entity.key)
        apport = population('apport', period)

        return prix_achat + frais_notaire + frais_agence + travaux - apport

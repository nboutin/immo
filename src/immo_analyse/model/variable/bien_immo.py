#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
@date: 2021-04
@author: nboutin
'''
# path must be absolute
from immo_analyse.core.variable import Variable
from immo_analyse.core.periods import ETERNITY
from immo_analyse.model.entities import Lot, BienImmo


class lot_type(Variable):
    value_type = str
    entity = Lot
    period = ETERNITY
    label = 'Catégorisation du lot suivant son nombre de pièce à vivre'
    value_accepted = ['T1', 'T2', 'T3', 'Commercial', 'Commun']


class surface_carrez(Variable):
    value_type = float
    entity = [Lot, BienImmo]
    period = ETERNITY
    label = 'surface habitable suivant la loi carrez'


class prix_achat(Variable):
    value_type = float
    entity = BienImmo
    period = ETERNITY
    label = "prix d'achat du bien immobilier sans frais annexe (notaire, agence, apport, subvention, ...)"


class frais_notaire(Variable):
    value_type = float
    entity = BienImmo
    period = ETERNITY
    label = "Frais de notaire pour l'acquisition"


class financement(Variable):
    value_type = float
    entity = BienImmo
    period = ETERNITY
    label = "Somme des cout liés à l'acquisition du bien immobilier"

    def formula(population, period, parameter):
        prix_achat = population('prix_achat', period)
        notaire = population('frais_notaire', period)
        return prix_achat + notaire

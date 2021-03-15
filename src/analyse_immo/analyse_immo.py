#!/usr/bin/env python3
# -*- coding: utf-8 -*-


class Analyse_Immo:

    def __init__(self,
                 defaut,
                 bien_immo,
                 annee_achat,
                 credit,
                 projection_duree,
                 irpp_2044_projection,
                 irpp_micro_foncier_projection,
                 rendement):
        self.defaut = defaut
        self.bien_immo = bien_immo
        self.annee_achat = annee_achat
        self.credit = credit
        self.projection_duree = projection_duree
        self.irpp_2044_projection = irpp_2044_projection
        self.irpp_micro_foncier_projection = irpp_micro_foncier_projection
        self.rendement = rendement

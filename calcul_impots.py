#!/usr/bin/env python3
# -*- coding: utf-8 -*-


def impots_brut(tmi, quotient_familial):

    impots_brut = 0
    tranche_p = 0

    for tranche, taux in tmi:

        impots_brut += max(min(tranche - tranche_p, quotient_familial - tranche_p) * taux, 0)
        tranche_p = tranche

    return impots_brut

#!/usr/bin/env python3
# -*- coding: utf-8 -*-


class Ligne:
    def __init__(self, numero, nom):
        self._numero = numero
        self._nom = nom

    @property
    def numero(self):
        return self._numero

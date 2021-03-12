#!/usr/bin/env python3
# -*- coding: utf-8 -*-


class Ligne:
    def __init__(self, numero, nom, value=0):
        self._numero = numero
        self._nom = nom
        self._value = value

    @property
    def numero(self):
        return self._numero

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, v):
        self._value = v

    def __hash__(self):
        return hash((self.numero))

    def __eq__(self, other):
        return self.numero == other.numero

    def __ne__(self, other):
        return not self.__eq__(other)

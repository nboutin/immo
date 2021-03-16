#!/usr/bin/env python3
# -*- coding: utf-8 -*-


class Ligne:
    def __init__(self, code, name, value=0):
        '''
        :param code (str)
        :param name (str)
        :param value (int)
        '''
        self._code = code
        self._name = name
        self._value = value

    @property
    def code(self):
        return self._code

    @property
    def name(self):
        return self._name

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, v):
        self._value = v

    def __hash__(self):
        return hash((self.code))

    def __eq__(self, other):
        return self.code == other.code

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return '{}, {}, {}'.format(self.code, self.name, self.value)


class Ligne_Model():

    def __init__(self):
        self._lignes = list()

    def add(self, ligne, value):
        import copy
        if ligne in self._lignes:
            raise Exception('Ligne already present {}'.format(ligne.code))
        ligne_copy = copy.deepcopy(ligne)
        ligne_copy.value = value
        self._lignes.append(ligne_copy)

    def remove(self, ligne):
        if ligne in self._lignes:
            self._lignes.remove(ligne)

    def update(self, ligne, value):
        '''
        @todo manage case multiple ligne were added
        '''
        self.remove(ligne)
        self.add(ligne, value)

    def sum(self, lignes):
        '''
        :param lignes (list of Ligne)
        '''
        if not isinstance(lignes, (list, tuple)):
            lignes = (lignes,)
        return sum(ligne.value for ligne in self._lignes if ligne in lignes)

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


class Ligne_Model():

    def __init__(self):
        self._lignes = list()

    # def __iter__(self):
        # return self._lignes.__iter__()
        #
    # def __next__(self):
        # return self._lignes.__next__()

    def add(self, ligne, value):
        if ligne in self._lignes:
            raise Exception('Ligne already present {}'.format(ligne.code))
        ligne.value = value
        self._lignes.append(ligne)

    def remove(self, ligne):
        if ligne in self._lignes:
            self._lignes.remove(ligne)

    def update(self, ligne, value):
        if ligne in self._lignes:
            self.remove(ligne)
        else:
            self.add(ligne, value)

    def sum(self, lignes):
        '''
        :param lignes (list of Ligne)
        '''
        if not isinstance(lignes, (list, tuple)):
            lignes = (lignes,)
        intersection = set(self._lignes).intersection(lignes)
        return sum(ligne.value for ligne in intersection)

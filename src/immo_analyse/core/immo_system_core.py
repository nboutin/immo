#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
@date: 2021-03
@author: nboutin
'''
import os
import glob
import imp
import logging
import inspect
import typing

from .variable import Variable
from .entity import Entity
from .population import Population

log = logging.getLogger(__name__)


class ImmoSystemCore:

    def __init__(self, entities):
        '''
        :param entities : list of entity supported
        '''
        self.variables = {}
        self.entities = entities

    def add_variables_from_directory(self, dir_path):
        """
        Recursively explores a directory, and adds all OpenFisca variables found there to the tax and benefit system.
        """
        py_files = glob.glob(os.path.join(dir_path, "*.py"))
        for py_file in py_files:
            self.add_variables_from_file(py_file)
        subdirectories = glob.glob(os.path.join(dir_path, "*/"))
        for subdirectory in subdirectories:
            self.add_variables_from_directory(subdirectory)

    def add_variables_from_file(self, file_path):
        """
        Adds all OpenFisca variables contained in a given file to the tax and benefit system.
        """
        try:
            file_name = os.path.splitext(os.path.basename(file_path))[0]

            #  As Python remembers loaded modules by name, in order to prevent collisions, we need to make sure that:
            #  - Files with the same name, but located in different directories, have a different module names. Hence the file path hash in the module name.
            #  - The same file, loaded by different tax and benefit systems, has distinct module names. Hence the `id(self)` in the module name.
            module_name = '{}_{}_{}'.format(id(self), hash(os.path.abspath(file_path)), file_name)

            module_directory = os.path.dirname(file_path)
            try:
                module = imp.load_module(module_name, *imp.find_module(file_name, [module_directory]))
            except NameError as e:
                logging.error(
                    str(e) +
                    ": if this code used to work, this error might be due to a major change in OpenFisca-Core. Checkout the changelog to learn more: <https://github.com/openfisca/openfisca-core/blob/master/CHANGELOG.md>")
                raise
            potential_variables = [getattr(module, item) for item in dir(module) if not item.startswith('__')]
            for pot_variable in potential_variables:
                # We only want to get the module classes defined in this module (not imported)
                if inspect.isclass(pot_variable) and issubclass(
                        pot_variable, Variable) and pot_variable.__module__ == module_name:
                    self.load_variable(pot_variable)
        except Exception:
            log.error('Unable to load OpenFisca variables from file "{}"'.format(file_path))
            raise

    def load_variable(self, variable_class, update=False):
        name = variable_class.__name__

        # Check if a Variable with the same name is already registered.
        baseline_variable = self.get_variable(name)
        if baseline_variable and not update:
            # raise VariableNameConflict(
            raise Exception(
                'Variable "{}" is already defined. Use `update_variable` to replace it.'.format(name))

        variable = variable_class()
        self.variables[variable.name] = variable

        return variable

    def get_variable(self, variable_name, check_existence=False):
        """
        :param variable_name: Name of the requested variable.
        :param check_existence: If True, raise an error if the requested variable does not exist.
        """
        variables = self.variables
        found = variables.get(variable_name)
        if not found and check_existence:
            # raise VariableNotFound(variable_name, self)
            raise Exception(variable_name, self)
        return found

    def build_population(self):
        '''
        :return {entity.key : Population(entity)}
        '''
        entities: typing.Dict[Entity.key, Population] = {}
        for entity in self.entities:
            entities[entity.key] = Population(entity)
        return entities

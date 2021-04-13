#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
@date: 2021-04
@author: nboutin
'''
import logging
from tabulate import tabulate
from ..core.periods import Period


class ReportGenerator:

    def __init__(self, period: Period, duration, simulation):
        self.period = period
        self.duration = duration
        self.simu = simulation

    def generate_all(self):

        self.report_overview()
        self.report_acquisition()
        self.report_fiscalite()
        self.report_go_nogo()

    def report_overview(self):

        data_name = ['Date',
                     'Financement',
                     'Loyer annuel',
                     'Charges/Provision',
                     'Charges credit',
                     'Amortissement',
                     'Credit duree/taux']

        data = [
            self.period,
            self.simu.compute('financement', self.period),
            self.simu.compute('loyer_nu', self.period, entity_key='bien_immo'),
            0,
            0,
            0,
            0,
        ]

        self._print("Overview", data_name, data)

    def report_acquisition(self):

        data_name = ['Prix net vendeur',
                     'Notaire',
                     'Agence',
                     'Travaux',
                     'Subvention',
                     'Apport',
                     'Financement',
                     'Prix €/m² (louable/final)',
                     ]

        data = [
            self.simu.compute('prix_achat', self.period),
            self.simu.compute('frais_notaire', self.period),
            self.simu.compute('frais_agence', self.period),
            self.simu.compute('travaux', self.period, entity_key='bien_immo'),
            self.simu.compute('subvention', self.period, entity_key='bien_immo'),
            self.simu.compute('apport', self.period),
            self.simu.compute('financement', self.period),
            0
        ]
        self._print("Acquisition", data_name, data)

    def report_fiscalite(self):
        '''
        Compare resultat financier suivant le regime fiscale
        '''

        data_name = ['Regime fiscal',
                     'Resultat foncier',
                     'Import foncier',
                     'Differentiel net-net']

        data = ['', 0, 0, 0]

        self._print("Fiscalite", data_name, data)

    def report_go_nogo(self):
        '''
        Indicateur simple pour discriminer les projets
        '''
        data_name = [
            'R Brut (%)',
            'Ratio locatif bancaire',
            'Différentiel net', ]

        data = [self.simu.compute('rdt_brut', self.period) * 100,
                0,
                0]

        self._print("GO NoGO", data_name, data)

    def _set_title(self, title: str):

        logging.info(title)
        logging.info('#' * 10)

    def _print(self, title: str, data_name, data):

        report = []

        # Format data to string
        data_str = ['{:.0f}'.format(v) if isinstance(v, float) else v for v in data]
        report.append(data_str)

        report.append(data_name)
        report = list(zip(*report[::-1]))

        self._set_title(title)
        logging.info(tabulate(report))

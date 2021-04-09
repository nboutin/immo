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

        self.overview_report()

    def overview_report(self):

        data_name = ['Date',
                     'Financement',
                     'Loyer annuel']

        data = [
            self.period,
            self.simu.compute('financement', self.period),
            self.simu.compute('loyer_nu', self.period)
        ]

        self._print("Overview", data_name, data)

    def _set_title(self, title: str):

        logging.info(title)
        logging.info('#' * 10)

    def _print(self, title: str, data_name, data):

        report = []
        report.append(data)
        report.append(data_name)
        report = list(zip(*report[::-1]))

        self._set_title(title)
        logging.info(tabulate(report))

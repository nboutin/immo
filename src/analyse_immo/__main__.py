#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys

from analyse_immo import analyse_immo

if __name__ == '__main__':
    import locale
    locale.setlocale(locale.LC_ALL, '')
    analyse_immo.main(sys.argv[1:])

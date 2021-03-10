#!/bin/sh

coverage erase
coverage run -a --source=analyse_immo.bien_immo.travaux --branch -m unittest -v test.bien_immo.test_travaux
coverage run -a --source=analyse_immo.bien_immo.commun --branch -m unittest -v test.bien_immo.test_commun
coverage run -a --source=analyse_immo.bien_immo.lot --branch -m unittest -v test.bien_immo.test_lot
coverage run -a --source=analyse_immo.bien_immo.charge --branch -m unittest -v test.bien_immo.test_charge
coverage run -a --source=analyse_immo.bien_immo.bien_immo --branch -m unittest -v test.bien_immo.test_bien_immo
coverage run -a --source=analyse_immo.rendement --branch -m unittest -v test.test_rendement
coverage run -a --source=analyse_immo.credit --branch -m unittest -v test.credit.test_credit test.credit.test_credit_fixecrd test.credit.test_credit_lacentraledefinancement
coverage run -a --source=analyse_immo.database --branch -m unittest -v test.test_database
coverage run -a --source=analyse_immo.defaut --branch -m unittest -v test.test_defaut
coverage run -a --source=analyse_immo.impots.irpp,analyse_immo.impots.ligne --branch -m unittest -v test.impots.test_irpp
coverage run -a --source=analyse_immo.impots.annexe_2044 --branch -m unittest -v test.impots.test_annexe_2044
coverage run -a --source=analyse_immo.impots.micro_foncier --branch -m unittest -v test.impots.test_micro_foncier
coverage run -a --source=analyse_immo.tools.finance --branch -m unittest -v test.tools.test_finance

coverage report --skip-empty -m
coverage html -d ./test/coverage/html --skip-empty
coverage annotate -d ./test/coverage/annotate

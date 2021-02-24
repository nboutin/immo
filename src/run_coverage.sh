#!/bin/sh

coverage erase
coverage run -a --source=analyse_immo.bien_immo.lot --branch -m unittest -v test.bien_immo.test_lot
coverage run -a --source=analyse_immo.bien_immo.charge --branch -m unittest -v test.bien_immo.test_charge
coverage run -a --source=analyse_immo.bien_immo.bien_immo --branch -m unittest -v test.bien_immo.test_bien_immo
coverage run -a --source=analyse_immo.rendement --branch -m unittest -v test.test_rendement
coverage run -a --source=analyse_immo.credit --branch -m unittest -v test.test_credit

coverage report --skip-empty -m
coverage html -d ./test/coverage/html --skip-empty
coverage annotate -d ./test/coverage/annotate

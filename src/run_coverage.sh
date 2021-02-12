#!/bin/sh

#coverage run --source=analyse_immo --branch -m unittest -v test

#coverage run --source=analyse_immo.bien_immo.lot --branch -m unittest -v test.bien_immo.test_lot
#coverage run --source=analyse_immo.bien_immo.charge --branch -m unittest -v test.bien_immo.test_charge
coverage run --source=analyse_immo.bien_immo.bien_immo --branch -m unittest -v test.bien_immo.test_bien_immo

coverage report --skip-empty -m
coverage html -d ./test/coverage/html --skip-empty
coverage annotate -d ./test/coverage/annotate

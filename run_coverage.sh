#!/bin/sh

coverage run --source=analyse_immo --branch -m unittest -v
coverage report --skip-empty -m
coverage html -d ./test/coverage/html --skip-empty
coverage annotate -d ./test/coverage/annotate

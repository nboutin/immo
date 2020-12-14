#!/bin/sh

python analyse_immo.py && python -m unittest -v && python analyse_immo.py

#!/bin/sh

python3 analyse_immo.py && python3 -m unittest -v && python3 analyse_immo.py

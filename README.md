# How-To Use

Complete data.json file.

Run script:

    $ python rendement.py

# Test
Run Unittest

    $ cd analyse_immo
    $ python -m unittest -v
    $ python -m unittest test.test_rendement

# Todo

- [ ] Calcul de la rentabilité nette de prelevement sociaux (https://www.devenir-rentier.fr/t1918-2)
- [ ] Calculer rendement net-net (net d'impot)
- [ ] Evaluer restauration de la tresorerie avec le différré d'amortissement
- [ ] Capacité d'investissement 70% loyer >= credit
- [ ] Cout copropriete au m²
- [ ] Indicateur global Go/NoGo
- [ ] Prendre en compte les impots dans le calcul du cashflow
- [x] Prix au m²
- [x] Ajouter parametre d'entree apport personnel

# Dependencies

- tabulate 0.8.7
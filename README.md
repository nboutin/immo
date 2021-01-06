# How-To Use

Complete data/input.json file.

Run script:

    $ python analyse_immo.py
    
Report is generated in output folder

# Test
Run Unittest

    $ cd analyse_immo
    $ python -m unittest -v
    $ python -m unittest test.test_rendement

# Todo

- [ ] Exprimer le cashflow par ann�e
- [ ] Calcul de la rentabilit� nette de prelevement sociaux (https://www.devenir-rentier.fr/t1918-2)
- [ ] Calculer rendement net-net (net d'impot)
- [ ] Evaluer restauration de la tresorerie avec le diff�rr� d'amortissement
- [ ] Capacit� d'investissement 70% loyer >= credit
- [ ] Cout copropriete au m�
- [ ] Indicateur global Go/NoGo
- [ ] Prendre en compte les impots dans le calcul du cashflow
- [x] Prix au m�
- [x] Ajouter parametre d'entree apport personnel

# Dependencies

- tabulate 0.8.7
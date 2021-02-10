# How-To Use

Complete data/input.json file.

Run script:

    cd src
    python -m analyse_immo
    python -m analyse_immo -i analyse_immo/data/input.json
    
Report is generated in analyse_immo/output folder

# Test
Run Unittest

    python -m unittest -v
    python -m unittest test.test_rendement
    
# Code coverage

    pip install --user coverage 
    
## Unittest

    coverage run --source=analyse_immo --branch -m unittest -v
    coverage report -m
    coverage html -d ./test/coverage/html
    coverage annotate -d ./test/coverage/annotate
    
    coverage erase

# Todo

- [ ] Prendre en compte travaux dans les Impots
- [ ] Calculer le cashflow net-net
- [ ] Exprimer le cashflow par année
- [ ] Prise en compte indexation des loyers (options)

- [ ] Calcul de la rentabilitï¿½ nette de prelevement sociaux (https://www.devenir-rentier.fr/t1918-2)
- [ ] Calculer rendement net-net (net d'impot)
- [ ] Evaluer restauration de la tresorerie avec le diffï¿½rï¿½ d'amortissement
- [ ] Capacitï¿½ d'investissement 70% loyer >= credit
- [ ] Cout copropriete au m/ï¿½
- [ ] Indicateur global Go/NoGo
- [ ] Prendre en compte les impots dans le calcul du cashflow

# Dependencies

- tabulate 0.8.7

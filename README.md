# How-To Use

> Complete data/input.json file.

Run script:

    cd src
    python -m analyse_immo
    python -m analyse_immo -i analyse_immo/data/input.json
    
Report is generated in analyse_immo/output folder

# Test
Run Unittest

    cd src 
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

# Dependencies

- tabulate 0.8.7

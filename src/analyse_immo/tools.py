'''
@author:
'''
import math


def interets_compose(capital, taux, duree_annee):
    '''
    @return: capital cumul = capital * (1 + taux)^(duree_annee)
    '''
    return capital * math.pow((1 + taux), duree_annee)

'''
@date: 2021-03-10
@author: nboutin
'''


class Travaux:

    def __init__(self, montant, subvention=[], is_deficit_foncier=False):
        '''
        :param montant list of int
        :param subvention list of int
        :param is_deficit_foncier boolean
        '''
        self._montant = montant
        self._subvention = subvention
        self._is_deficit_foncier = is_deficit_foncier

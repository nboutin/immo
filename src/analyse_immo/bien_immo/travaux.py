'''
@date: 2021-03-10
@author: nboutin
'''


class Travaux:

    def __init__(self, montant=[], subvention=[], deficit_foncier=[]):
        '''
        :param montant list of int
        :param subvention list of int
        :param deficit_foncier list of int
        '''
        self._montant = montant
        self._subvention = subvention
        self._deficit_foncier = deficit_foncier

        if (self.montant_total - self.subvention_total) < self.deficit_foncier_total:
            raise Exception("Montant de deficit foncier trop grand {} < {}".format(
                self.montant_total - self.subvention_total, self.deficit_foncier_total))

    @property
    def montant_total(self):
        return sum(self._montant)

    @property
    def subvention_total(self):
        return sum(self._subvention)

    @property
    def deficit_foncier_total(self):
        return sum(self._deficit_foncier)

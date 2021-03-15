#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from .ligne import Ligne, Ligne_Model
from .annexe_2044 import L451_deficit_foncier_anterieur

L1AJ_salaire = Ligne('1AJ', 'Salaires - Déclarant 1')
L1BJ_salaire = Ligne('1BJ', 'Salaires - Déclarant 2')
L7UF_dons = Ligne('7UF', 'Dons aux oeuvres')
L7AE_syndicat = Ligne('7AE', 'Cotisations syndicales - Déclarant 2')

L4BA_benefice_foncier = Ligne('4BA', 'Resultat foncier positif')
L4BB_deficit_foncier_imputable_revenu_foncier = Ligne('4BB', 'Deficit foncier imputable sur revenu foncier')
L4BC_deficit_foncier_imputable_revenu_global = Ligne('4BC', 'Deficit foncier imputable sur revenu globale')
L4BD_deficit_foncier_anterieur = Ligne('4BD', 'Deficit foncier antérieur')
L4_revenus_ou_deficits_nets_fonciers = Ligne('4', 'Revenus ou Deficits nets fonciers')

# 4BE Micro foncier - recettes brutes


class IRPP:
    '''
    L’impôt sur le revenu des personnes physiques (IRPP)
    IR = IRPP + CSG(secu) + CRDS (dettes)

    Source:
    https://www.service-public.fr/particuliers/vosdroits/F34328
    https://www.tacotax.fr/guides/impot-sur-le-revenu

    Revenu
        Salaire & deduction
        revenu foncier
        Total = Revenu fiscale de reference

        salaires = auto()
        investissement = auto()  # Action, assurance vie, PEA, PER, ...
        revenu_foncier = auto()
        plus_value_immobiliere = auto()
        bic = auto() # benefice commerciaux et industrielle
        ba = auto() # benefice commerciaux agricoles
        retraite = auto()
        indemnite = auto()
        primes = auto()
    '''

    def __init__(self, database, annee_revenu, part_fiscale, n_enfant):
        '''
        :param annee_revenu(int): annee_revenu + 1 = annee_imposition
        '''
        self._database = database
        self._annee_revenu = annee_revenu
        self._part_fiscale = part_fiscale
        self._n_enfant = n_enfant

        self._ligne_model = Ligne_Model()
        self._annexe_2044 = None
        self._micro_foncier = None

    def add_ligne(self, ligne, value):
        self._ligne_model.add(ligne, value)

    def sum_ligne(self, lignes):
        return self._ligne_model.sum(lignes)

    def _compute_ligne_4(self):

        # Report depuis Annexe 2044
        L420 = self._annexe_2044.resultat_foncier
        if L420 > 0:
            self.add_ligne(L4BA_benefice_foncier, L420)
        else:
            L440 = self._annexe_2044.deficit_imputable_revenu_global
            L441 = self._annexe_2044.deficit_imputable_revenu_foncier
            self.add_ligne(L4BB_deficit_foncier_imputable_revenu_foncier, L441)
            self.add_ligne(L4BC_deficit_foncier_imputable_revenu_global, L440)

        self.add_ligne(L4BD_deficit_foncier_anterieur,
                       self._annexe_2044.sum_ligne(L451_deficit_foncier_anterieur))

        # Calcul ligne 4
        L4BA = self.sum_ligne(L4BA_benefice_foncier)
        L4BB = self.sum_ligne(L4BB_deficit_foncier_imputable_revenu_foncier)
        L4BC = self.sum_ligne(L4BC_deficit_foncier_imputable_revenu_global)
        L4BD = self.sum_ligne(L4BD_deficit_foncier_anterieur)

        # Bénifice foncier
        if L4BA > 0:
            # Sans deficit antérieur
            if L4BD == 0:
                self.add_ligne(L4_revenus_ou_deficits_nets_fonciers, L4BA)
            else:
                reste_net = L4BA + L4BD
                if reste_net > 0:
                    self.add_ligne(L4_revenus_ou_deficits_nets_fonciers, reste_net)
                else:
                    self.add_ligne(L4_revenus_ou_deficits_nets_fonciers, 0)
        # Deficit imputable sur revenu global
        elif L4BC < 0:
            self.add_ligne(L4_revenus_ou_deficits_nets_fonciers, L4BC)
        # Deficit imputable sur revenu foncier
        elif L4BB < 0:
            self.add_ligne(L4_revenus_ou_deficits_nets_fonciers, 0)
        else:
            raise Exception('Ligne 4 not updated')

    @property
    def annexe_2044(self):
        return self._annexe_2044

    @annexe_2044.setter
    def annexe_2044(self, annexe_2044):
        self._annexe_2044 = annexe_2044
        if self._annexe_2044:
            self._compute_ligne_4()

    @property
    def micro_foncier(self):
        return self._micro_foncier

    @micro_foncier.setter
    def micro_foncier(self, micro_foncier):
        self._micro_foncier = micro_foncier

    @property
    def salaires(self):
        return self.sum_ligne((L1AJ_salaire, L1BJ_salaire))

    @property
    def revenu_net_impossable(self):
        '''
        sommes des salaires retrancher de 10% moins les charges déductibles et abattements
        '''
        return self.salaires * (1 - self._database.salaire_abattement)

    @property
    def revenu_fiscale_reference(self):
        '''
        ligne 5: Revenu ou deficit brut global
        '''
        rfr = self.revenu_net_impossable
        rfr += self.sum_ligne(L4_revenus_ou_deficits_nets_fonciers)
        return rfr

    @property
    def revenu_foncier(self):
        return self.sum_ligne(L4_revenus_ou_deficits_nets_fonciers)

    # @property
    # def revenu_foncier(self):
        # if self._annexe_2044 and self._micro_foncier:
        # raise Exception()
        #
        # if self._annexe_2044:
        # # Bénéfice foncier
        # if self._annexe_2044.resultat_foncier >= 0:
        # return self._annexe_2044.resultat_foncier
        # # Revenu global
        # elif self._annexe_2044.deficit_imputable_revenu_global < 0:
        # return self._annexe_2044.deficit_imputable_revenu_global
        # # Revenu foncier
        # elif self._annexe_2044.deficit_imputable_revenu_foncier:
        # result = self._annexe_2044.deficit_imputable_revenu_foncier
        # result += self.sum_ligne((L4BD_deficit_foncier_anterieur))
        # return result
        #
        # elif self._micro_foncier:
        # return self._micro_foncier.revenu_foncier_taxable
        # else:
        # return 0

    @property
    def total_reduction_impot(self):
        return self.sum_ligne((L7UF_dons))

    @property
    def total_credit_impot(self):
        return self.sum_ligne((L7AE_syndicat))

    @property
    def quotient_familial(self):
        return self.revenu_fiscale_reference / self._part_fiscale

    @property
    def impots_brut(self):
        '''
        impot sur le revenu sousmis au bareme
        '''
        impot_brut = self.__impots_brut_part_fiscale()

        # Controler dépassement d'abattement enfant
        impot_brut_sans_enfant = self.__impots_brut_sans_enfant()

        reduction_enfants = impot_brut_sans_enfant - impot_brut
        plafond_quotient_familial = self._database.plafond_quotient_familial(
            self._annee_revenu + 1) * self._n_enfant

        if reduction_enfants > plafond_quotient_familial:
            impot_brut += reduction_enfants - plafond_quotient_familial

        return impot_brut

    @property
    def impots_net(self):
        net = self.impots_brut
        net += self.prelevement_sociaux_foncier
        net -= self._database.reduction_dons * self.total_reduction_impot
        net -= self._database.reduction_syndicat * self.total_credit_impot
        return net

    @property
    def impots_salaires_net(self):
        '''
        :return impot net en considérant uniquement les salaires
        '''
        import copy
        irpp = copy.deepcopy(self)
        irpp.annexe_2044 = None
        irpp._ligne_model.remove(L4_revenus_ou_deficits_nets_fonciers)
        return irpp.impots_net

    @property
    def impots_revenu_foncier(self):
        ''' revenu foncier taxable et prelevement sociaux foncier'''
        return self.impots_net - self.impots_salaires_net

    @property
    def prelevement_sociaux_foncier(self):
        if self.annexe_2044:
            return self.annexe_2044.prelevement_sociaux
        elif self.micro_foncier:
            return self.micro_foncier.prelevement_sociaux
        else:
            return 0

    # Private

    def __impots_brut_sans_enfant(self):
        import copy
        part = self._part_fiscale - self._n_enfant / 2
        irpp_sans_enfant = copy.deepcopy(self)
        irpp_sans_enfant._part_fiscale = part
        irpp_sans_enfant._n_enfant = 0
        return irpp_sans_enfant.__impots_brut_part_fiscale()

    def __impots_brut_part_fiscale(self):
        bareme = self._database.irpp_bareme(str(self._annee_revenu + 1))
        impot_brut = self._impots_brut(bareme, self.quotient_familial)
        impot_brut *= self._part_fiscale
        return impot_brut

    def _impots_brut(self, bareme, quotient_familial):

        impots_brut = 0
        tranche_p = 0

        for tranche, taux in bareme:
            tranche_restant = min(tranche - tranche_p, quotient_familial - tranche_p)
            tranche_restant = max(tranche_restant, 0)
            impots_brut += tranche_restant * taux
            tranche_p = tranche + 1

        return impots_brut

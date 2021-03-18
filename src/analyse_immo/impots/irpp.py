#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from .ligne import Ligne_Model
from .ligne_definition import *


class IRPP:
    '''
    L’impôt sur le revenu des personnes physiques (IRPP)
    IR = IRPP + CSG(secu) + CRDS (dettes)

    Source:
    https://www.service-public.fr/particuliers/vosdroits/F34328
    https://www.tacotax.fr/guides/impot-sur-le-revenu
    '''

    def __init__(self, database, annee_revenu):
        '''
        :param annee_revenu(int): annee_revenu + 1 = annee_imposition
        '''
        self._database = database
        self._annee_revenu = annee_revenu

        self._ligne_model = Ligne_Model()
        self._annexe_2044 = None
        self._micro_foncier = None

    def add_ligne(self, ligne, value):
        self._ligne_model.add(ligne, value)
        self.compute()

    def sum_ligne(self, lignes):
        return self._ligne_model.sum(lignes)

    def compute(self):
        # Ligne 1
        L1a = self.sum_ligne([L1AJ_salaire, L1BJ_salaire])
        L1b = L1a * 0.1
        L1c = L1a - L1b
        self._ligne_model.update(L1_1_traitements_salaires_pensions, L1c)

        # Ligne 5: Total 1 a 4
        self._ligne_model.update(L1_5_revenu_brut_global,
                                 self.sum_ligne([L1_1_traitements_salaires_pensions,
                                                 L4_revenus_ou_deficits_nets_fonciers]))

        # Ligne 7: 5-6
        self._ligne_model.update(L3_7_revenu_net_global, self.sum_ligne(L1_5_revenu_brut_global))

        # Ligne R: 7-8
        self._ligne_model.update(LR_revenu_net_impossable, self.sum_ligne(L3_7_revenu_net_global))

        # Ligne Q
        self._ligne_model.update(LQ_quotient_familial,
                                 self.sum_ligne(LR_revenu_net_impossable) / self.sum_ligne(LN_nombre_de_part))
        # Ligne I: Impot
        quotient_familial = self.sum_ligne(LQ_quotient_familial)
        n_part_fiscale = self.sum_ligne(LN_nombre_de_part)
        LI = self._ligne_model.update(LI_impot, self.__impots_brut_part_fiscale(quotient_familial, n_part_fiscale))

        # Ligne 6A
        n_personne_a_charge = self.sum_ligne(L4_personne_a_charge)
        L6A = self._ligne_model.update(L6A_plafonnement_quotient_familial,
                                       self.__impots_brut_part_fiscale(
                                           quotient_familial,
                                           n_part_fiscale - n_personne_a_charge / 2))
        # Ligne 6B
        L6B = self._ligne_model.update(
            L6B_plafonnement_quotient_familial,
            self._database.plafond_quotient_familial(
                self._annee_revenu + 1) * n_personne_a_charge)

        # Ligne 6C
        L6C = self._ligne_model.update(L6C_plafonnement_quotient_familial, L6A - L6B)

        # Check plafonnement
        if L6C <= LI:  # Sans plafonnement
            LI1 = self._ligne_model.update(LI1_impot, LI)
            # if n_part_fiscale == 1 and LI1 < 1611:
            # raise Exception("todo: Appliquer decote, voir L7 diminution de l'impot {}".format(LI1))
            # elif n_part_fiscale == 2 and LI1 < 2653:
            # raise Exception("todo: Appliquer decote, voir L7 diminution de l'impot {}".format(LI1))
        else:
            LI1 = self._ligne_model.update(LI1_impot, L6C)

        # Ligne 7E Impot avant reductions d'impots
        L7E = self._ligne_model.update(L7E_impot_avant_reduction_impot, LI1)

        # Ligne 8 Reductions d'impots
        dons = self.sum_ligne(L7UF_dons) * self._database.reduction_dons
        L8g = self._ligne_model.update(L8g_dons_et_cotisations_aux_partis_politiques, dons)

        L8F = self._ligne_model.update(L8F_total_reductions_impots, L8g)

        # Ligne 8G = 7E - 8F
        L8G = self._ligne_model.update(L8G_impot_apres_reductions_impots, L7E - L8F)

        # Ligne 9PS Prelevement sociaux
        L9PS = self._ligne_model.update(L9PS_prelevement_sociaux,
                                        self.sum_ligne(L4_revenus_ou_deficits_nets_fonciers)
                                        * self._database.prelevement_sociaux_taux)

        # Ligne 9H Impot apres corrections
        L9H = self._ligne_model.update(L9H_impot_apres_corrections, L8G + L9PS)

        # Ligne 9I Imputations
        cotisations = self.sum_ligne(L7AE_syndicat) * self._database.reduction_syndicat
        L9u = self._ligne_model.update(L9u_cotisations_syndicales, cotisations)
        L9I = self._ligne_model.update(L9I_total_imputations, L9u)

        # Ligne 9 Impot du: H - I
        self._ligne_model.update(L9_impot_du, L9H - L9I)

    def _compute_ligne_4(self):

        # Report from Annexe 2044
        self.add_ligne(L4BA_benefice_foncier, self.annexe_2044.sum_ligne(L4BA_benefice_foncier))
        self.add_ligne(L4BB_deficit_foncier_imputable_revenu_foncier,
                       self.annexe_2044.sum_ligne(L4BB_deficit_foncier_imputable_revenu_foncier))
        self.add_ligne(L4BC_deficit_foncier_imputable_revenu_global,
                       self.annexe_2044.sum_ligne(L4BC_deficit_foncier_imputable_revenu_global))
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

        self.compute()

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
    def impot_sans_revenu_foncier(self):
        '''
        :return impot net en considérant uniquement les salaires
        '''
        import copy
        irpp = copy.deepcopy(self)
        irpp.annexe_2044 = None
        irpp._ligne_model.remove(L4_revenus_ou_deficits_nets_fonciers)
        irpp.compute()
        return irpp.sum_ligne(L9_impot_du)

    @property
    def impots_revenu_foncier(self):
        ''' revenu foncier taxable et prelevement sociaux foncier'''
        # return self.impots_net - self.impots_salaires_net
        return self.sum_ligne(L9_impot_du) - self.impot_sans_revenu_foncier

    def __impots_brut_part_fiscale(self, quotient_familial, n_part_fiscale):
        bareme = self._database.irpp_bareme(str(self._annee_revenu + 1))
        impot_brut = self._impots_brut(bareme, quotient_familial)
        impot_brut *= n_part_fiscale
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

    # @property
    # def salaires(self):
        # return self.sum_ligne((L1AJ_salaire, L1BJ_salaire))

    # @property
    # def revenu_net_impossable(self):
        # '''
        # sommes des salaires retrancher de 10% moins les charges déductibles et abattements
        # '''
        # return self.salaires * (1 - self._database.salaire_abattement)

    # @property
    # def revenu_fiscale_reference(self):
        # '''
        # ligne 5: Revenu ou deficit brut global
        # '''
        # rfr = self.revenu_net_impossable
        # rfr += self.sum_ligne(L4_revenus_ou_deficits_nets_fonciers)
        # return rfr

    # @property
    # def revenu_foncier(self):
        # return self.sum_ligne(L4_revenus_ou_deficits_nets_fonciers)

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

    # @property
    # def total_reduction_impot(self):
        # return self.sum_ligne((L7UF_dons))
        #
    # @property
    # def total_credit_impot(self):
        # return self.sum_ligne((L7AE_syndicat))

    # @property
    # def quotient_familial(self):
        # # return self.revenu_fiscale_reference / self._part_fiscale
        # return self.sum_ligne(LR_revenu_net_impossable) / self.sum_ligne(LN_nombre_de_part)

    # @property
    # def impots_brut(self):
        # '''
        # impot sur le revenu sousmis au bareme
        # '''
        # n_part_fiscale = self.sum_ligne(LN_nombre_de_part)
        # n_personne_a_charge = self.sum_ligne(L4_personne_a_charge)
        #
        # impot_brut = self.__impots_brut_part_fiscale(n_part_fiscale)
        #
        # # Controler dépassement d'abattement enfant
        # # impot_brut_sans_enfant = self.__impots_brut_sans_enfant()
        # impot_brut_sans_enfant = self.self.__impots_brut_part_fiscale(n_part_fiscale - n_personne_a_charge / 2)
        #
        # reduction_enfants = impot_brut_sans_enfant - impot_brut
        # plafond_quotient_familial = self._database.plafond_quotient_familial(
        # self._annee_revenu + 1) * self._n_enfant
        #
        # if reduction_enfants > plafond_quotient_familial:
        # impot_brut += reduction_enfants - plafond_quotient_familial
        #
        # return impot_brut

    # @property
    # def impots_net(self):
        # net = self.impots_brut
        # net += self.prelevement_sociaux_foncier
        # net -= self._database.reduction_dons * self.total_reduction_impot
        # net -= self._database.reduction_syndicat * self.total_credit_impot
        # return net

    # @property
    # def prelevement_sociaux_foncier(self):
        # if self.annexe_2044:
        # return self.annexe_2044.prelevement_sociaux
        # elif self.micro_foncier:
        # return self.micro_foncier.prelevement_sociaux
        # else:
        # return 0

    # Private

    # def __impots_brut_sans_enfant(self):
        # import copy
        # part = self._part_fiscale - self._n_enfant / 2
        # irpp_sans_enfant = copy.deepcopy(self)
        # irpp_sans_enfant._part_fiscale = part
        # irpp_sans_enfant._n_enfant = 0
        # return irpp_sans_enfant.__impots_brut_part_fiscale()

    # def __impots_brut_part_fiscale(self):
        # bareme = self._database.irpp_bareme(str(self._annee_revenu + 1))
        # impot_brut = self._impots_brut(bareme, self.quotient_familial)
        # impot_brut *= self._part_fiscale
        # return impot_brut

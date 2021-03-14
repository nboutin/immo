#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from analyse_immo.defaut import Defaut
from analyse_immo.bien_immo.bien_immo import Bien_Immo
from analyse_immo.bien_immo.charge import Charge
from analyse_immo.bien_immo.lot import Lot
from analyse_immo.bien_immo.commun import Commun
from analyse_immo.bien_immo.travaux import Travaux
from analyse_immo.credit import Credit
from analyse_immo.impots.irpp import IRPP, L1AJ_salaire, L1BJ_salaire, L7UF_dons, L7AE_syndicat, L4BB_deficit_foncier_imputable_revenu_foncier
from analyse_immo.impots.annexe_2044 import Annexe_2044, L211_loyer_brut, L221_frais_administration, L222_autre_frais_gestion, \
    L223_prime_assurance, L224_travaux, L227_taxe_fonciere, L229_copropriete_provision, L250_interet_emprunt, L250_assurance_emprunteur,\
    L250_frais_dossier, L250_frais_garantie, L451_deficit_foncier_anterieur
from analyse_immo.impots.micro_foncier import Micro_Foncier, L4EB_recettes_brutes
from analyse_immo.tools.finance import capital_compose


class Factory:

    @staticmethod
    def make_travaux(travaux_data):
        return Travaux(montant=travaux_data['montant'],
                       subvention=travaux_data['subvention'],
                       deficit_foncier=travaux_data['deficit_foncier'])

    @staticmethod
    def make_commun(commun_data):
        travaux = Factory.make_travaux(commun_data['travaux'])
        return Commun(travaux=travaux)
    
    @staticmethod
    def make_charges(charges_data, defaut, lot_type):
        charge = Charge(defaut, lot_type)
        charge.add(Charge.charge_e.charge_locative, charges_data['provision_charge_mensuel'])
        
        charge.add(Charge.charge_e.copropriete, charges_data['copropriete'])
        charge.add(Charge.charge_e.taxe_fonciere, charges_data['taxe_fonciere'])
        charge.add(Charge.charge_e.prime_assurance, charges_data['PNO'])
        charge.add(Charge.charge_e.agence_immo, charges_data['agence_immo'])
        
        charge.add(Charge.charge_e.provision_travaux, charges_data['travaux_provision_taux'])
        charge.add(Charge.charge_e.vacance_locative, charges_data['vacance_locative_taux'])
        return charge

    @staticmethod
    def make_bien_immo(achat_data, commun_data, lots_data, defaut):

        commun = Factory.make_commun(commun_data)

        bien_immo = Bien_Immo(achat_data['prix_net_vendeur'],
                              achat_data['frais_agence'],
                              achat_data['frais_notaire'],
                              achat_data['apport'],
                              commun=commun)

        for lot_data in lots_data:

            irl = lot_data['irl_taux_annuel']
            if irl == 1:
                irl = defaut.irl_taux_annuel
                print('use defaut {}'.format(irl))

            etat = Lot.etat_e.louable if lot_data['etat'] == 'louable' else ''
            etat = Lot.etat_e.amenageable if lot_data['etat'] == 'amenageable' else etat

            travaux = Factory.make_travaux(lot_data['travaux'])

            lot = Lot(lot_data['type'],
                      lot_data['surface'],
                      lot_data['loyer_nu_mensuel'],
                      irl,
                      etat=etat,
                      travaux=travaux)

            lot.charge = Factory.make_charges(lot_data['charges'])

            bien_immo.add_lot(lot)

        return bien_immo

    @staticmethod
    def make_credit(credit_data, bien_immo):

        if credit_data['mode'] == 'fixe_ci':
            mode = Credit.mode_e.fixe_CI
        elif credit_data['mode'] == 'fixe_crd':
            mode = Credit.mode_e.fixe_CRD
        elif credit_data['mode'] == 'degressive_crd':
            mode = Credit.mode_e.degressive_CRD
        else:
            raise Exception('Bad Credit mode')

        credit = Credit(bien_immo.financement_total,
                        credit_data['duree_annee'] * 12,
                        credit_data['taux_interet'],
                        Credit.taux_e.periodique,
                        credit_data['taux_assurance'],
                        mode,
                        credit_data['frais_dossier'],
                        credit_data['frais_garantie'])
        return credit

    @staticmethod
    def make_defaut(defaut_data):

        defaut = Defaut(defaut_data['irl_taux_annuel'],
                        defaut_data['provision_travaux_taux'],
                        defaut_data['vacance_locative_taux_T1'],
                        defaut_data['vacance_locative_taux_T2'],
                        defaut_data['gestion_agence_taux'],)

        return defaut

    @staticmethod
    def make_irpp_projection(duration, annee_achat, database, impot_data, salaire_taux, bien_immo, credit):

        irpp_2044_projection = list()

        for i_annee in range(duration):
            annee_revenu = annee_achat + i_annee
            irpp = Factory.make_irpp(database, impot_data, annee_revenu, i_annee, salaire_taux)

            deficit_foncier_anterieur = 0
            if i_annee > 0:
                deficit_foncier_anterieur = irpp_2044_projection[i_annee - \
                    1].sum_ligne(L4BB_deficit_foncier_imputable_revenu_foncier)

            irpp.annexe_2044 = Factory.make_annexe_2044(
                database, bien_immo, credit, i_annee + 1, deficit_foncier_anterieur)
            irpp_2044_projection.append(irpp)
        return irpp_2044_projection

    @staticmethod
    def make_irpp(database, impot_data, annee_revenu, i_annee, salaire_taux):
        '''
        :param annee_revenu: int, current year
        :param i_annee: int, index annee
        '''
        try:
            impot = impot_data[str(annee_revenu)]
        except KeyError:
            impot = impot_data['2020']

        irpp = IRPP(database, annee_revenu, part_fiscale=impot['parts_fiscales'], n_enfant=impot['enfants'])
        irpp.add_ligne(L1AJ_salaire, capital_compose(impot['salaires'][0], salaire_taux, i_annee))
        irpp.add_ligne(L1BJ_salaire, capital_compose(impot['salaires'][1], salaire_taux, i_annee))
        irpp.add_ligne(L7UF_dons, impot['dons'])
        irpp.add_ligne(L7AE_syndicat, impot['syndicat'])
        return irpp

    @staticmethod
    def make_annexe_2044(database, bien_immo, credit, i_annee, deficit_foncier_anterieur):
        '''
        :param i_annee: start at 1, annee n depuis l'achat du bien
        :todo put 20€ pour frais de gestion dans la database
        '''
        an = Annexe_2044(database)

        # bien_immo loyer_nu_net = import loyer_nu_brut
        an.add_ligne(L211_loyer_brut, bien_immo.loyer_nu_net_annuel(i_annee))
        an.add_ligne(L221_frais_administration, bien_immo.get_charge(Charge.charge_e.agence_immo, i_annee))
        an.add_ligne(L222_autre_frais_gestion, 20 * bien_immo.lot_count)
        an.add_ligne(L223_prime_assurance, bien_immo.get_charge(Charge.charge_e.prime_assurance, i_annee))
        an.add_ligne(L224_travaux, bien_immo.get_charge(Charge.charge_e.provision_travaux, i_annee))
        an.add_ligne(L227_taxe_fonciere, bien_immo.get_charge(Charge.charge_e.taxe_fonciere, i_annee))
        an.add_ligne(L229_copropriete_provision, bien_immo.get_charge(Charge.charge_e.copropriete, i_annee))

        if i_annee == 1:
            an.add_ligne(L224_travaux, bien_immo.travaux_montant, double=True)

        month_stop = i_annee * 12
        month_start = month_stop - 11
        an.add_ligne(L250_interet_emprunt, credit.get_interet(month_start, month_stop))
        an.add_ligne(L250_assurance_emprunteur, credit.get_mensualite_assurance(month_start, month_stop))

        if i_annee == 1:
            an.add_ligne(L250_frais_dossier, credit.frais_dossier)
            an.add_ligne(L250_frais_garantie, credit.frais_garantie)

        an.add_ligne(L451_deficit_foncier_anterieur, deficit_foncier_anterieur)

        return an

    @staticmethod
    def make_micro_foncier(database, bien_immo, i_annee):
        try:
            mf = Micro_Foncier(database)

            # bien_immo loyer_nu_net = import loyer_nu_brut
            mf.add_ligne(L4EB_recettes_brutes, bien_immo.loyer_nu_net_annuel(i_annee))
            return mf
        except Exception:
            return None

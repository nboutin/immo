#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from bien_immo import Bien_Immo
from defaut import Defaut
from charge import Charge
from lot import Lot
from credit import Credit
from defaut import Defaut


class Factory:
    
    @staticmethod
    def make_bien_immo(achat_data, lots_data, defaut=Defaut(0, 0, 0, 0)):
        
        bien_immo = Bien_Immo(achat_data['prix_net_vendeur'],
                              achat_data['frais_agence'],
                              achat_data['frais_notaire'],
                              achat_data['budget_travaux'],
                              achat_data['apport'])
        
        for lot_data in lots_data:
            
            lot = Lot(lot_data['type'],
                      lot_data['surface'],
                      lot_data['loyer_nu_mensuel'])
    
            charge = Charge(lot, defaut)
    
            charge_data = lot_data['charge']
            charge.add(charge.gestion_e.charge_locative, charge_data['provision_charge_mensuel'])
            charge.add(charge.deductible_e.copropriete, charge_data['copropriete'])
            charge.add(charge.deductible_e.taxe_fonciere, charge_data['taxe_fonciere'])
            charge.add(charge.deductible_e.prime_assurance, charge_data['PNO'])
            
            gestion_data = lot_data['gestion']
            charge.add(Charge.gestion_e.provision_travaux, gestion_data['travaux_provision_taux'])
            charge.add(Charge.gestion_e.vacance_locative, gestion_data['vacance_locative_taux'])
            charge.add(Charge.gestion_e.agence_immo, gestion_data['agence_immo'])
            lot.charge = charge
            
            bien_immo.add_lot(lot)
        
        return bien_immo

    @staticmethod
    def make_credit(credit_data, montant_emprunte):
        
        credit = Credit(montant_emprunte,
                        credit_data['duree_annee'] * 12,
                        credit_data['taux_interet'],
                        credit_data['taux_assurance'],
                        credit_data['mode'],
                        credit_data['frais_dossier'],
                        credit_data['frais_garantie'])
        return credit

    @staticmethod
    def make_defaut(defaut_data):
        
        defaut = Defaut(defaut_data['provision_travaux_taux'],
                        defaut_data['vacance_locative_taux_T1'],
                        defaut_data['vacance_locative_taux_T2'],
                        defaut_data['gestion_agence_taux'],)
        
        return defaut


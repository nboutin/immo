#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from bien_immo import Bien_Immo
from defaut import Defaut
from charge import Charge
from lot import Lot


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

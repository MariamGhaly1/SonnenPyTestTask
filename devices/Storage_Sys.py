from devices.Inverter import Inverter
from devices.BMS import BMS


class Storage_System:
    def __init__(self, inverter: Inverter, bms: BMS, num_modules: int = 1 ):
        self.inverter = inverter
        self.bms = bms
        self.num_modules = num_modules
        self.power_command = 0.0 
        self.grid_power = 0.0             # grid power is calculated not measured
    

    def on_power_command_calc_grid_power(self, pv_power, consumption_power, power_command):

        surplus = pv_power - consumption_power
    
        if surplus > 0:

            self.grid_power = - (surplus + power_command)
            
        elif surplus < 0:
            deficit = - surplus


            self.grid_power = deficit - power_command 
            
        else:
            self.grid_power = - power_command






    def on_measurement_change(self, pv_power, consumption_power) :

        max_charge_discharge = min(float(self.inverter.max_power), float(self.bms.max_power)*self.num_modules)
 
        surplus = pv_power - consumption_power
 
        if surplus > 0:
            charge_power = min(surplus, max_charge_discharge)

            self.inverter.active_power = - charge_power
            self.bms.active_power = self.inverter.active_power / self.num_modules
            self.grid_power = - (surplus - charge_power)
            
        elif surplus < 0:
            deficit = - surplus
            discharge_power = min(deficit, max_charge_discharge)

            self.inverter.active_power = discharge_power
            self.bms.active_power = self.inverter.active_power / self.num_modules

            self.grid_power = deficit - discharge_power
            
        else:
            self.inverter.active_power= 0.0
            self.bms.active_power = 0.0
            self.grid_power = 0.0



        
        
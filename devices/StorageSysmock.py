from devices.Invertermock import Inverter
from devices.BMSmock import BMS


class StorageSystem:
    def __init__(self, inverter: Inverter, bms: BMS, num_modules: int = 1 ):
        self.inverter = inverter
        self.bms = bms
        self.num_modules = num_modules
        self.grid_power = 0.0             # grid power is calculated not measured

    # @property
    # def max_storage_power_command(self):
    #     return min(
    #         self.inverter.max_power, self.bms.max_power
    #     )  # Watts  (+ = discharge, - = charge)

    # def get(self, param: str):
    #     if param == "max_storage_power_command":
    #         return self.storage_power_command
    #     raise KeyError(param)

    # def set(self, param: str, value) -> bool:
    #     if param == "storage_power_command":
    #         self.storage_power_command = float(value)
    #         return True
    #     return False



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



        
        
from devices.Invertermock import Inverter
from devices.BMSmock import BMS

class StorageSystem():
    def __init__(self, inverter: Inverter, bms: BMS):
        self.inverter = inverter
        self.bms = bms
        self.storage_power_command = 0.0                       # Watts  (+ = discharge, - = charge)
    


    def get(self, param: str):
        if param == "storage_power_command":
            return self.storage_power_command
        raise KeyError(param)
 
    def set(self, param: str, value) -> bool:
        if param == "storage_power_command":
            self.storage_power_command = float(value)
            return True
        return False
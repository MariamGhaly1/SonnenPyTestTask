from devices.Meter import PV_Meter 
from devices.Meter import Consumption_Meter
from devices.Storage_Sys import Storage_System


"""
Mock implementation of the sonnenBatterie DUT.

    Design assumptions:
    - Each battery module supports up to 2000W charge/discharge power.
    - System configs cap module count: Basic <= 2, Standard <= 3, Pro <= 5.
    - Sign conventions: inverter.active_power (+discharge/-charge),
    grid.power (+import/-export).
    - On surplus/deficit bigger than the battery can absorb/supply, the grid
    takes up the remainder.
"""


class DUT ():
    """
    DUT: Device Under Test 
    
    """


    def __init__(self, pv_meter: PV_Meter, consumption: Consumption_Meter, storage_system: Storage_System ):
 
        self.pv_meter = pv_meter
        self.consumption_meter = consumption
        self.storage = storage_system

        self.storage.on_measurement_change(self.pv_meter.power, self.consumption_meter.power)
        self._grid_power = self.storage.grid_power

    @property
    def system_setup(self)-> str:
        match self.storage.num_modules:
            case 1 | 2:
                return "basic"
            case 3:
                return "standard"
            case 4 |5 :
                return "pro"
            case _:
                return None
        


    #----------------------------------------------------------------
    #-------------- setter, getter and reset-------------------------

    def get(self, key: str) -> str:
        component, _, param = key.partition(".")
        if component == "system":
            if param == "setup":
                return self.system_setup
            else:
                print(f"system component doesn't have this paramter {param}")
                return ""
            
        elif component == "grid" and param == "power":
            return str(self.storage.grid_power)
        
        else:
            target = self._component(component)
            if target is None:
                print(f"{component}this component name is not found")
                return ""
            else: 
                try:
                    return str(target.get(param))
                except (KeyError, IndexError, ValueError):
                    print(f"{param} doesn't exist inside the component {component}")
                    return ""


    def set(self, key: str, value) -> bool:
        component, _, param = key.partition(".")
        if component == "storage" and param == "power_command":
            self.storage.power_command = float(value)
            self.storage.on_power_command_calc_grid_power(
                self.pv_meter.power,
                self.consumption_meter.power,
                self.storage.power_command,
            )
            return True
        else:
            target = self._component(component)
        if target is None:
            return False
        else:
            try:
                ok = target.set(param, value)
            except (KeyError, IndexError, ValueError):
                print(f"{param} doesn't exist inside the component {component}")
                return False
            
            if ok and component in ("pv", "consumption"):
                self.storage.on_measurement_change(self.pv_meter.power, self.consumption_meter.power)
                return True    
              

    def reset(self) -> None:
        """Restore the DUT to its initial state. Called after each test."""
        self.pv_meter.power = 0.0
        self.pv_meter.voltage = 0.0
        self.pv_meter.frequency = 0.0
        self.consumption_meter.power = 0.0 
        self.consumption_meter.voltage = 0.0
        self.consumption_meter.frequency = 0.0

        self.storage.inverter.active_power = 0.0
        self.storage.inverter.battery_voltage = 0.0
        self.storage.inverter.grid_frequency = 0.0
        self.storage.inverter.grid_voltage = 0.0

        self.storage.bms.active_power = 0.0
        self.storage.bms.voltage = 0.0

        self.storage.power_command = 0.0
        self.storage.grid_power = 0.0
        self.storage.on_measurement_change(self.pv_meter.power, self.consumption_meter.power)

        

    #----------------------------------------------------------
    #------------------------internals-------------------------

    def _component(self, name: str):
        return {
            "pv": self.pv_meter,
            "consumption": self.consumption_meter,
            "inverter": self.storage.inverter,
            "bms": self.storage.bms,
        }.get(name)




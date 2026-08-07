from devices.PVmock import PV
from devices.Consumptionmock import Consumption
from devices.StorageSysmock import StorageSystem


"""
Mock implementation of the sonnenBatterie DUT.

    Design assumptions:
    - Each battery module supports up to 2000W charge/discharge power.
    - System configs cap module count: Basic <= 2, Standard <= 3, Pro <= 5.
    - Sign conventions: inverter.power_flow (+discharge/-charge),
    grid.power (+import/-export).
    - On surplus/deficit bigger than the battery can absorb/supply, the grid
    takes up the remainder.
"""

# assumptions for the mock DUT

MODULE_POWER_W = 2000
    
CONFIG_MAX_MODULES = {
    "basic": 2,
    "standard": 3,
    "pro": 5,
}

DEFAULT_MODULES = 1


class DUT ():
    """
    DUT: Device Under Test 
    
    """


    def __init__(self, pv: PV, consumption: Consumption, storage_system: StorageSystem ):
 
        self.pv = pv
        self.consumption = consumption
        self.storage = storage_system

        self.storage.on_measurement_change(self.pv.power, self.consumption.power)
        self._grid_power = self.storage.grid_power

    @property
    def system_setup(self)-> str:
        print(f"this is the setup name")
        pass


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
                self.storage.on_measurement_change(self.pv.power, self.consumption.power)
                return True    
              

    def reset(self) -> None:
        """Restore the DUT to its initial state. Called after each test."""
        self.pv.power = 0.0
        self.consumption.power = 0.0 
        self.storage.on_measurement_change(self.pv.power, self.consumption.power)

        

    #----------------------------------------------------------
    #------------------------internals-------------------------

    def _component(self, name: str):
        return {
            "pv": self.pv,
            "consumption": self.consumption,
            "inverter": self.storage.inverter,
            "bms": self.storage.bms,
            "storage": self.storage,
        }.get(name)




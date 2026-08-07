from devices.PVmock import PV
from devices.Consumptionmock import Consumption
from devices.StorageSysmock import StorageSystem
from devices.Invertermock import Inverter
from devices.BMSmock import BMS

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


    def __init__(self ):
        self._config = "basic"
        self._modules = DEFAULT_MODULES
 
        self.pv = PV()
        self.consumption = Consumption()
        self.inverter = Inverter(modules=self._modules, module_power_w=MODULE_POWER_W)
        self.bms = BMS(num_modules=self._modules, module_power_w=MODULE_POWER_W)
        self.storage = StorageSystem(self.inverter, self.bms)
 
        self._grid_power = 0.0
        self._recompute_flows()
    
    #----------------------------------------------------------------
    #-------------- setter, getter and reset-------------------------

    def get(self, key: str) -> str:
        component, _, param = key.partition(".")
 
        if component == "system":
            if param == "config":
                return self._config
            elif param == "modules":
                return str(self._modules)
            else:
                print(f"system component doesn't have this paramter {param}")
                return ""
 
        elif component == "grid" and param == "power":
            return str(self._grid_power)
        
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
 
        if component == "system":
            return self._set_system(param, value)
 
        elif component == "grid":
            return False  # grid values are derived, not writable
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
                    self._recompute_flows()
                    return True      

    def reset(self) -> None:
        """Restore the DUT to its initial state. Called after each test."""
        self.__init__()

    #----------------------------------------------------------
    #------------------------internals-------------------------

    def _component(self, name: str):
        return {
            "pv": self.pv,
            "consumption": self.consumption,
            "inverter": self.inverter,
            "bms": self.bms,
            "storage": self.storage,
        }.get(name)
 
    def _set_system(self, param: str, value) -> bool:
        if param == "config":
            value = str(value).lower()
            if value not in CONFIG_MAX_MODULES:
                return False
            self._config = value
            self._modules =  CONFIG_MAX_MODULES[value]
            self._apply_module_count()
            return True
        else:
            return False
    
    def _apply_module_count(self) -> None:
        self.inverter.modules = self._modules
        self.bms.num_modules = self._modules
        self._recompute_flows()
 
    def _recompute_flows(self) -> None:
        pv = float(self.pv.power)
        consumption = float(self.consumption.power)
        max_charge_discharge = min(float(self.inverter.max_power), float(self.bms.max_power))
 
        surplus = pv - consumption
 
        if surplus > 0:
            charge_power = min(surplus, max_charge_discharge)
            self.inverter.power_flow = -charge_power
            self._grid_power = -(surplus - charge_power)
        elif surplus < 0:
            deficit = -surplus
            discharge_power = min(deficit, max_charge_discharge)
            self.inverter.power_flow = discharge_power
            self._grid_power = deficit - discharge_power
        else:
            self.inverter.power_flow = 0.0
            self._grid_power = 0.0





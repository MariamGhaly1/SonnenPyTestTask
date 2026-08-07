class Inverter:
    """
    Inverter readings/controls. 
    max charge/discharge power are derived from module count (the module count
    itself is managed by the DUT based on system config).
    """

    def __init__(self, modules: int = 1, module_power_w: float = 2000):
        self.modules = modules
        self.module_power_w = module_power_w
        self.battery_voltage = 48.0                             # Volts
        self.battery_current = 0.0                              # Amps
        self.power_flow = 0.0                                    # Watts  # -ve > charge batterie
        self.grid_frequency = 50.0                               # Hertz
        self.grid_voltage = 220.0                                # Volts

    @property
    def max_power(self) -> float:
        return self.modules * self.module_power_w

    def get(self, param: str):
        if not hasattr(self, param):
            print(f"get: {param} not found")
            raise KeyError(param)
        return getattr(self, param)
 
    def set(self, param: str, value) -> bool:
        if not hasattr(self, param):
            print(f"set: {param} not found")
            return False
        if param == "max_power":
            print(f"para: {param} is not editable")
            return False
        setattr(self, param, value)
        return True

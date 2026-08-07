class BMS:
    """ Battery Management System (BMS) readings.
    assumption: All batteries have the same specs"""


    def __init__(self, num_modules: int = 1, module_power_w: float = 2000 ):
         
        self.temp =  25.0                             # Celsius
        self.voltage = 48.0                           # Volts
        self.current = 0.0                            # Amps
        self.soc = 60.0                               # percentage
        self.num_modules = num_modules
        self.module_power_w = module_power_w


    @property
    def max_power(self) -> float:
        return self.module_power_w * self.num_modules

    def get(self, param: str):
        if not hasattr(self, param):
            print(f"get: {param} not found")
            raise KeyError(param)
        return getattr(self, param)
 
    def set(self, param: str, value) -> bool:
        if param == "max_power" or param == "num_modules":
            print(f"para: {param} is not editable")
            return False
        elif not hasattr(self, param):
            print(f"set: {param} not found")
            raise KeyError(param)
        
        
        setattr(self, param, value)
        return True

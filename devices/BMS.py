class BMS:
    """ Battery Management System (BMS) readings.
    assumption: All batteries have the same specs"""


    def __init__(self,  max_power: float = 2000 ):
         
        self.temp =  0.0                             # Celsius
        self.voltage = 0.0                           # Volts
        self.soc = 0.0                               # percentage
        self.max_power = max_power
        self.active_power = 0.0

    @property
    def active_current(self)-> float:
        try: 
            return float(self.active_power / self.voltage)             # Amps
        except(ZeroDivisionError):
            print("batterie voltage is 0!!")

    def get(self, param: str):
        if not hasattr(self, param):
            print(f"get: {param} not found")
            raise KeyError(param)
        return getattr(self, param)
 
    def set(self, param: str, value) -> bool:
        if param == "active_power" or param == "active_current":
            print(f"para: {param} is not editable")
            return False
        elif not hasattr(self, param):
            print(f"set: {param} not found")
            raise KeyError(param)
        else:
            setattr(self, param, value)
            return True

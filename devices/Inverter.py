class Inverter:
    """
    Inverter readings/controls. 
    """

    def __init__(self, max_power: float = 9000.0):
    
        self.max_power = max_power
        self.active_power = 0.0                                 # Watts  # -ve > charge batterie
        self.battery_voltage = 0.0                             # Volts
        self.grid_frequency = 0.0                               # Hertz
        self.grid_voltage = 0.0                                # Volts

    @property
    def battery_current(self)-> float:
        try: 
            return float(self.active_power / self.battery_voltage)             # Amps  // assuming no power loss
        except:
            print("batterie voltage is 0!!")


    def get(self, param: str):
        if not hasattr(self, param):
            print(f"get: {param} not found")
            raise KeyError(param)
        return getattr(self, param)
 
    def set(self, param: str, value) -> bool:
        if not hasattr(self, param):
            print(f"set: {param} not found")
            return False
        elif param == "active_power" or param =="battery_current":
            print(f"para: {param} is not editable")
            return False
        else: 
            setattr(self, param, value)
            return True

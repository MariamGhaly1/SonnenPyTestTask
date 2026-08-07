class PV :
    """PV panel readings."""

    def __init__(self):
        self.power =  0.0                          # Watts 
        self.voltage = 220.0                       # Volts
        self.current = 0.0                         # Amps
        self.frequency = 50.0                       # Hertz
    

    def get(self, param: str):
        if not hasattr(self, param):
            raise KeyError(param)
        return getattr(self, param)
 
    def set(self, param: str, value) -> bool:
        if not hasattr(self, param):
            raise KeyError(param)
        setattr(self, param, value)
        return True
    

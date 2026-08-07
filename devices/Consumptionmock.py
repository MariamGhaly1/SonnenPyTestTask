class Consumption:
    """Household consumption meter readings."""

    def __init__(self):
        self.power = 0.0                        # Watts
        self.voltage = 220.0                    # Volts
        self.frequency = 50.0                   # Hertz

    @property
    def current(self) -> float:
        try: 
            return float(self.power / self.voltage)             # Amps
        except:
            print("consumption voltage is 0!!")

    def get(self, param: str):
        if not hasattr(self, param):
            raise KeyError(param)
        return getattr(self, param)
 
    def set(self, param: str, value) -> bool:
        if not hasattr(self, param):
            raise KeyError(param)
        setattr(self, param, value)
        return True


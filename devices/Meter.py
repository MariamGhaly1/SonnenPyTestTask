class Meter:
    """"General class for meters"""

    def __init__(self):
        self.power = 0.0                        # Watts
        self.voltage = 0.0                    # Volts
        self.frequency = 0.0                   # Hertz

    @property
    def current(self) -> float:
            try: 
                return float(self.power / self.voltage)             # Amps
            except(ZeroDivisionError):
                print("calculating current while voltage is 0!!")

    def get(self, param: str):
        if not hasattr(self, param):
            raise KeyError(param)
        return getattr(self, param)
 
    def set(self, param: str, value) -> bool:
        if not hasattr(self, param):
            raise KeyError(param)
        setattr(self, param, value)
        return True


class Consumption_Meter(Meter):
    """Household consumption meter readings."""

    def __init__(self):
       super().__init__()



class PV_Meter(Meter):
    """PV panel readings."""

    def __init__(self):
           super().__init__()

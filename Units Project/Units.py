class Dimension:
    def __init__(self, magnitude:int | float, units:str):
        self.magnitude = magnitude

        self.fund_units = {
            "Length":0,
            "Mass":0,
            "Temperature":0,
            "Time":0,
            "Charge":0,
            "Lum":0,
            "Mole":0,
        }

    def _unit_parser(self, unit_str:str):
        pass

    def _unit_decoder(self, unit_str:str,pow:int):
        pass

    def convert_units(self, target:str, ndigits:int):
        pass

    def __str__(self):
        pass

    # might only need one of str or repr
    def __repr__(self):
        pass

    def __int__(self):
        return int(self.magnitude)
    
    def __float__(self):
        return float(self.magnitude)
    
    def __round__(self, ndigits:int):
        self.magnitude = round(self.magnitude, ndigits)
        return self

    # numerical Hellscape below

    def __eq__(self, other):
        pass

    def __ne__(self, other):
        pass

    def __lt__(self, other):
        pass

    def __le__(self, other):
        pass

    def __gt__(self, other):
        pass

    def __ge__(self, other):
        pass

    def __add__(self, other):
        pass

    def __radd__(self, other):
        return self.__add__(other)
    
    def __iadd__(self, other):
        pass
    
    def __sub__(self, other):
        pass

    def __rsub__(self, other):
        pass

    def __isub__(self, other):
        pass
    
    def __mul__(self, other):
        pass

    def __rmul__(self, other):
        pass

    def __imul__(self, other):
        pass

    def __truediv__(self, other):
        pass

    def __rtruediv__(self, other):
        pass

    def __itruediv__(self, other):
        pass
    
    def __mod__(self, other):
        pass

    def __rmod__(self, other):
        pass

    def __imod__(self, other):
        pass

    def __floordiv__(self, other):
        pass

    def __rfloordiv__(self, other):
        pass

    def __ifloordiv__(self, other):
        pass

    def __pow__(self, other):
        pass

    def __rpow__(self, other):
        pass

    def __ipow__(self, other):
        pass

    def __matmul__(self, other):
        pass

    def __imatmul__(self, other):
        pass

    def __divmod__(self, other):
        pass

    def __rdivmod__(self, other):
        pass

    def __abs__(self, other):
        pass

    def __round__(self, other):
        pass
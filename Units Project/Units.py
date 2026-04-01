class Dimension:
    compound_units = {
        "N":["kg","m","-s","-s"],
        "lbf":["slug","ft","-s","-s"],
        "J":["N","m"],
        "Pa":["N","-m","-m"],
        "atm":["101325*Pa"]
        } 
    length_units = {
        "m":1,
        "mm":1e-3,
        "cm":1e-2,
        "km":1e3,
        "ft":0.3048,
        "in":2.54/100,
    }
    mass_units = {
        "kg":1,
        "g":1e-3,
        "slug":14.59390,
        "lbm":14.59390/32.174
    }   
    temp_units = {
        "K":1,
        "R":5/9,
    }
    time_units = {
        "s":1,
        "ms":1e-3,
        "min":60,
        "hr":3600,
        "hrs":3600,
    }

    def __init__(self, magnitude:int | float, units:str):
        self.magnitude = magnitude

        # set all initial powers to 0
        self.fund_units = {
            "Length":0,
            "Mass":0,
            "Temperature":0,
            "Time":0,
            "Charge":0,
            "Lum":0,
            "Mole":0,
        }

        # check if units are just C or F, these cause problems otherwise
        if (units == "F"):
            self.fund_units["Temperature"] += 1
            self.magnitude = (self.magnitude - 32)*5/9 + 273.15
            return
        
        if (units == "C"):
            self.fund_units["Temperature"] += 1
            self.magnitude += 273.15
            return

        self._unit_parser(units)

    def _unit_parser(self, unit_str:str):
        # loop until there are no more * or / separators
        end = False; skip = False
        while(not end):
            if unit_str[0] == '*':
                pow = 1
                unit_str = unit_str[1:]
            elif unit_str[0] == '/':
                pow = -1
                unit_str = unit_str[1:]
            else:
                pow = 1

            # loop through every char in string
            for i in range(len(unit_str)):
                # check if at the end of the string
                if i == len(unit_str) - 1:
                    i+=1
                    end = True
                    break

                # check if in the middle of "**"
                elif skip == True:
                    skip = False

                elif unit_str[i] == '*':
                    # need to check if this is actually "**"
                    if unit_str[i+1] == '*':
                        skip = True
                    else:
                        break

                elif unit_str[i] == '/':
                    break

            # separate into current and everything after (not including sep)
            crnt_str = unit_str[:i]
            unit_str = unit_str[i:]
            #print(f"DEBUG: crnt str = {crnt_str}, unit str = {unit_str}")

            # separate current string into label and power
            # truncate string if it has an exponent
            for i in range(len(crnt_str)):
                # if it makes it all the way to the end, then it has no exponent
                if crnt_str[i] == '*' and crnt_str[i+1] == '*':
                    try:
                        pow = pow*int(crnt_str[i+2:])
                    # throw an error if it isn't an integer
                    except ValueError:
                        raise TypeError(f"Could not convert exponent in {crnt_str} to int.")
                    
                    crnt_str = crnt_str[:i]
                    break

                elif crnt_str[i] == '^':
                    try:
                        pow = pow*int(crnt_str[i+1:])
                    # throw an error if it isn't an integer
                    except ValueError:
                        raise TypeError(f"Could not convert exponent in \"{crnt_str}\" to int.")

                    crnt_str = crnt_str[:i]
                    break
            
            if pow == 0:
                raise ValueError(f"Exponent of \"{crnt_str}\" should not be 0.")

            #print(f"DEBUG: crnt str = {crnt_str}, pow = {pow}")

            # run the decoder for each str index
            self._unit_decoder(crnt_str, pow)

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

dim1 = Dimension(32,"kg**2*m^4/s**3")
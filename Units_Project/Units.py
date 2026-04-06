class Dimension:
    compound_units = {
        "N":"kg*m/s**2",
        "lbf":"slug*ft/s**2",
        "J":"N*m",
        "Pa":"N/m**2",
        "atm":{"scale":101325,"units":"Pa"}
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
    charge_units = {

    }
    luminosity_units = {

    }
    molar_units = {
        "mol":1
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
            "Luminosity":0,
            "Mole":0,
        }

        # remove all of the empty spaces in str
        units = units.replace(" ","")
        units = units.replace("\t","")

        # check if the units string is empty
        if (units == ""):
            return

        # check if units are just C or F, these cause problems otherwise
        # convert to Kelvin
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
        """function to separate the input string into individual units and their exponent"""
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

    def _unit_decoder(self, unit_str:str, pow:int):
        """function to contribute a unit to self magnitude and funamental unit powers"""

        # some of the compound units use this to show that they have negative exp
        # (I didn't want to send them through the parser again)
        if unit_str[0] == '-':
            pow *= -1
            unit_str = unit_str[1:]

        # first, check if it's in the compound unit list
        # if it is, recurse it through the parser and decoder
        if unit_str in self.compound_units.keys():
            comp = self.compound_units[unit_str]

            # some of these have an additional scale attached
            if isinstance(comp, dict):
                self.magnitude *= comp["scale"]
                self._unit_parser(comp["units"])

            else:
                self._unit_parser(comp)

        # check to see if the string exists in any of the other dicts
        elif unit_str in self.length_units.keys():
            self.magnitude *= self.length_units[unit_str]
            self.fund_units["Length"] += pow

        elif unit_str in self.mass_units.keys():
            self.magnitude *= self.mass_units[unit_str]
            self.fund_units["Mass"] += pow

        elif unit_str in self.temp_units.keys():
            self.magnitude *= self.temp_units[unit_str]
            self.fund_units["Temperature"] += pow

        elif unit_str in self.time_units.keys():
            self.magnitude *= self.time_units[unit_str]
            self.fund_units["Time"] += pow

        elif unit_str in self.charge_units.keys():
            self.magnitude *= self.charge_units[unit_str]
            self.fund_units["Charge"] += pow

        elif unit_str in self.luminosity_units.keys():
            self.magnitude *= self.luminosity_units[unit_str]
            self.fund_units["Luminosity"] += pow

        elif unit_str in self.molar_units.keys():
            self.magnitude *= self.molar_units[unit_str]
            self.fund_units["Mole"] += pow

        # string not recognized anywhere, either not implemented or typo
        else:
            raise NotImplementedError(f"Unit \"{unit_str}\" not implemented.")
            
    def convert_units(self, target_str:str, ndigits:int=4):
        """function to convert to a specific unit string and print
            if conversion fails, raises a mismatch error"""
        target = Dimension(1, target_str)

        # check if the fund unit dicts have the same parameters
        if self.fund_units == target.fund_units:
            conv_magnitude = self.magnitude/target.magnitude
            conv_magnitude = round(conv_magnitude,ndigits)
            print(f"{conv_magnitude} {target_str}")

        else:
            raise ValueError(f"Unit conversion to \"{target_str}\" failed.")

    def compare_units(self, other:int | float | Dimension) -> bool:
        units_equal = True

        if type(other) is not Dimension:
            for key in self.fund_units.keys():
                if self.fund_units[key] != 0:
                    units_equal = False

        else: # if other is also Dimension
            if self.fund_units != other.fund_units:
                units_equal = False

        return units_equal
            
    def __repr__(self):
        si_units = ["m","kg","K","s","c","candela","mol"]

        frmt_str = ""
        i = 0
        for key in self.fund_units.keys():
            pow = self.fund_units[key]

            if pow == 1:
                frmt_str += f"{si_units[i]} "

            elif pow != 0:
                frmt_str += f"{si_units[i]}^{pow} "
            
            i+=1

        return (f"{self.magnitude} {frmt_str}")

    def __int__(self):
        return int(self.magnitude)
    
    def __float__(self):
        return float(self.magnitude)
    
    def __round__(self, ndigits:int=None):
        if ndigits is None:
            self.magnitude = int(self.magnitude)
            return self

        self.magnitude = round(self.magnitude, 4)
        return self

    def __abs__(self, other):
        if self.magnitude < 0:
            self.magnitude *= -1

        return self
    
    # numerical Hellscape below

    def __eq__(self, other):
        equal = True

        if type(other) is str:
            other_dim = Dimension(1,other)
            if not self.compare_units(other_dim):
                equal = False

        elif type(other) is Dimension:
            if not self.compare_units(other):
                equal = False

            if self.magnitude == other.magnitude:
                equal = False

        # must be float or int
        elif self.magnitude != other:
            equal = False

        return equal

    def __ne__(self, other):
        return not self.__eq__(other)

    def __lt__(self, other:int | float | Dimension):
        if type(other) not in [int,float,Dimension]:
            raise TypeError(f"Type \"{type(other)}\" not allowed for inequalities.")
    
        if type(other) == Dimension:
            less_than = self.magnitude < other.magnitude

        else:
            less_than = self.magnitude < other

        return less_than

    def __le__(self, other):
        if type(other) not in [int,float,Dimension]:
            raise TypeError(f"Type \"{type(other)}\" not allowed for inequalities.")
        
        if type(other) == Dimension:
            less_than_eq = self.magnitude <= other.magnitude

        else:
            less_than_eq = self.magnitude <= other

        return less_than_eq

    def __gt__(self, other):
        if type(other) not in [int,float,Dimension]:
            raise TypeError(f"Type \"{type(other)}\" not allowed for inequalities.")
        
        if type(other) == Dimension:
            greater_than = self.magnitude > other.magnitude

        else:
            greater_than = self.magnitude > other

        return greater_than

    def __ge__(self, other):
        if type(other) not in [int,float,Dimension]:
            raise TypeError(f"Type \"{type(other)}\" not allowed for inequalities.")
        
        if type(other) == Dimension:
            greater_than_eq = self.magnitude >= other.magnitude

        else:
            greater_than_eq = self.magnitude >= other

        return greater_than_eq

    def __add__(self, other):
        if self.compare_units(other) == False:
            raise TypeError("Units do not match.")
        
        elif type(other) == Dimension:
            self.magnitude += other.magnitude
        
        else:
            self.magnitude += other
            
        return self

    def __radd__(self, other):
        return self.__add__(other)
    
    def __sub__(self, other):
        if self.compare_units(other) == False:
            raise TypeError("Units do not match.")
        
        elif type(other) == Dimension:
            self.magnitude -= other.magnitude
        
        else:
            self.magnitude -= other
            
        return self

    def __rsub__(self, other):
        return self.__sub__(other)
    
    def __mul__(self, other):
        if type(other) not in [int,float,Dimension]:
            raise TypeError(f"Type \"{type(other)}\" not allowed for multiplication.")
        
        if type(other) == Dimension:
            for key in self.fund_units.keys():
                self.fund_units[key] += other.fund_units[key]

            self.magnitude *= other.magnitude

        else:
            self.magnitude *= other

        return self

    def __rmul__(self, other):
        return self.__mul__(other)

    def __truediv__(self, other):
        if type(other) not in [int,float,Dimension]:
            raise TypeError(f"Type \"{type(other)}\" not allowed for division.")
        
        if type(other) == Dimension:
            for key in self.fund_units.keys():
                self.fund_units[key] -= other.fund_units[key]

            self.magnitude /= other.magnitude

        else:
            self.magnitude /= other

        return self

    def __rtruediv__(self, other):
        if type(other) not in [int,float,Dimension]:
            raise TypeError(f"Type \"{type(other)}\" not allowed for division.")
        
        if type(other) == Dimension:
            for key in self.fund_units.keys():
                self.fund_units[key] -= other.fund_units[key]

            self.magnitude = other.magnitude / self.magnitude

        else:
            self.magnitude = other / self.magnitude
            for key in self.fund_units.keys():
                self.fund_units[key] *= -1

        return self
    
    def __mod__(self, other):
        if type(other) not in [int,float,Dimension]:
            raise TypeError(f"Type \"{type(other)}\" not allowed for modulo.")
        
        elif type(other) == Dimension:
            return self.magnitude % other.magnitude
        
        else:
            return self.magnitude % other

    def __rmod__(self, other):
        if type(other) not in [int,float,Dimension]:
            raise TypeError(f"Type \"{type(other)}\" not allowed for modulo.")
        
        elif type(other) == Dimension:
            return other.magnitude % self.magnitude
        
        else:
            return other % self.magnitude

    def __floordiv__(self, other):
        if type(other) not in [int,float,Dimension]:
            raise TypeError(f"Type \"{type(other)}\" not allowed for division.")
        
        if type(other) == Dimension:
            for key in self.fund_units.keys():
                self.fund_units[key] -= other.fund_units[key]

            self.magnitude //= other.magnitude

        else:
            self.magnitude //= other

        return self

    def __rfloordiv__(self, other):
        if type(other) not in [int,float,Dimension]:
            raise TypeError(f"Type \"{type(other)}\" not allowed for division.")
        
        if type(other) == Dimension:
            for key in self.fund_units.keys():
                self.fund_units[key] -= other.fund_units[key]

            self.magnitude = other.magnitude / self.magnitude

        else:
            self.magnitude = other / self.magnitude
            for key in self.fund_units.keys():
                self.fund_units[key] *= -1

        return self

    def __pow__(self, other):
        # cannot be Dimension
        if type(other) not in [int,float]:
            raise TypeError(f"Type \"{type(other)}\" not allowed for exponent.")
        
        else:
            self.magnitude **= other
            for key in self.fund_units.keys():
                self.fund_units[key] *= other

            return self

    def __rpow__(self, other):
        # only happens if the dimension is the exponent
        raise TypeError(f"Type \"{type(self)}\" not allowed for exponent.")
"""
    def __matmul__(self, other):
        pass

    def __imatmul__(self, other):
        pass

    def __divmod__(self, other):
        pass

    def __rdivmod__(self, other):
        pass"""
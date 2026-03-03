from __future__ import annotations
import sys

""" Dimension object is made up of float | int object and Units object
    Units object is a list of Unit objects"""

class Dimension():
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
    fund_units = [length_units,mass_units,temp_units,time_units]

    def __init__(self, unit_str:str):
        print(f"DEBUG: input str = {unit_str}")
        if "-" in unit_str:
            self.pos_exp = 0
            unit_str = unit_str.replace("-","")
        else:
            self.pos_exp = 1

        for char_i in range(len(unit_str)):
            if unit_str[char_i] == "*":
                self.exp = int(unit_str[char_i+2+self.pos_exp:])
                unit_str = unit_str[:char_i]
                break
            elif unit_str[char_i] == "^":
                self.exp = int(unit_str[char_i+1+self.pos_exp:])
                unit_str = unit_str[:char_i]
                break
            else:
                self.exp = 1

        self.dim_str = unit_str
        print(f"DEBUG: output str = {unit_str}**{self.pos_exp}{self.exp}")

class Units():
    def __init__(self, units:str):
        # check if str or list
        if type(units) == str:
            str_list = []

            # index at * or /
            sep = []
            neg_exp = []
            i = 0
            while i < len(units) - 1:
                if units[i] == "*":
                    # check if "*" is actually part of an exponent
                    if units[i+1] == "*":
                        i+=1
                    else:
                        sep.append(i)
                elif units[i] == "/":
                    sep.append(i)
                    # mark index with negative exponent
                    neg_exp.append(len(sep))
                i+=1

            # starting indicies need to begin at the beginning :)
            start = [0] + [s+1 for s in sep]

            for i in range(len(sep)):
                str_list.append(units[start[i]:sep[i]])
            # final unit should be from final sep index to the end of str
            str_list.append(units[start[-1]:])

            """# expand exponents into individual indicies
            frmt_list = []
            for exp_i in range(len(str_list)):
                crnt_str = str_list[exp_i]

                exp = 1 # set default value
                for char_i in range(len(crnt_str)):
                    crnt_char = crnt_str[char_i]
                    if crnt_char == "^":
                        new_str = crnt_str[0:char_i]
                        exp = crnt_str[char_i+1:]
                        break
                    elif crnt_char == "*":
                        new_str = crnt_str[0:char_i]
                        exp = crnt_str[char_i+2:] # account for extra "*"
                        break

                if "-" in exp:
                    exp = exp[1:]
                    # concatenate "-" in front
                    new_str = "-" + new_str

                exp = int(exp)
                for iter in range(exp):
                    frmt_list.append(new_str)"""

        else:
            print("Warning: unit must be string")
            sys.exit

        # check if secretly dimensionless
        if str_list == [""]:
            str_list = []

        self.scale = 1
        unit_i = 0
        while unit_i < len(str_list):
            crnt_unit = Dimension(str_list[unit_i])
            if crnt_unit.dim_str in Dimension.compound_units:
                insrt_list = Dimension.compound_units[crnt_unit.dim_str]
                if crnt_unit.pos_exp == 0:
                    for unit_j in range(len(insrt_list)):
                        if "-" in insrt_list[unit_j]: # check if already negative
                            insrt_list[unit_j] = insrt_list[unit_j].replace("-","")
                        else:
                            insrt_list[unit_j] = "-"+insrt_list[unit_j]
                
            else:
                unit_i+=1
            print(f"DEBUG: crnt_list = {str_list}")
            
"""
            if crnt_unit in Compound_Dimension.units:
                new_unit_list = Compound_Dimension.units[crnt_unit]
                for new_unit_i in range(len(new_unit_list)):
                    new_unit = new_unit_list[new_unit_i]
                    if "*" in new_unit:
                        for char_i in range(len(new_unit)):
                            if new_unit[char_i] == "*":
                                if "-" in new_unit: # "-" always in front if at all
                                    self.scale = self.scale*new_unit[1:char_i]
                                else:
                                    self.scale = self.scale*new_unit[0:char_i]
                        new_unit_list[new_unit_i] = new_unit[char_i+1:]

                frmt_list = frmt_list[0:i] + new_unit_list + frmt_list[i+1:]

                unit_i = 0 # reset back to beginning (could have a save state to go back to instead)

            else:
                unit_i = unit_i + 1
"""
        

class Compound_Dimension():
    units = {
        "N":["kg","m","-s","-s"],
        "lbf":["slug","ft","-s","-s"],
        "J":["N","m"],
        "Pa":["N","-m","-m"],
        "atm":["101325*Pa"]
        }

    def __init__(self, unit_str:str):
        pass

class Fundamental_Dimension():
    units = {}

    def __init__(self, unit_str:str):
        if unit_str in self.units:
            self.scale = self.units[unit_str]
        else:
            print("Error: Dimension \""+unit_str+"\" not implemented")
            sys.exit()

class Length(Fundamental_Dimension):
    units = {
        "m":1,
        "mm":1e-3,
        "cm":1e-2,
        "km":1e3,
        "ft":0.3048,
        "in":2.54/100,
    }

class Mass(Fundamental_Dimension):
    units = {
        "kg":1,
        "g":1e-3,
        "slug":14.59390,
        "lbm":14.59390/32.174
    }

class Temp(Fundamental_Dimension):
    units = {
        "K":1,
        "R":5/9,
    }

class Time(Fundamental_Dimension):
    units = {
        "s":1,
        "ms":1e-3,
        "min":60,
        "hr":3600,
        "hrs":3600,
    }

"""
class Unit():
    fundamental_dimensions = ("L","M","T","Theta","Q","C","N")
    metric_fund_units = ("m","g","s","K","A","cd","mol")
    metric_secd_units = ("N","J")
    metric_prefixes = ("G","M","k","c","m","μ")
    imp_fund_units = ("ft","slug","s","R")
    imp_secd_units = ("lbm","lbf","kip","psi","ksi")

    def __init__(self, unit:str):
        if unit in Length.units:
            
        
    @staticmethod
    def expand_units(secondary_unit:str) -> str:
        pass
"""

"""class Metric_Unit():
    # Just a singular unit - no *, /, **, or ^

    fundamental_units = ("m","g","s","A","K","mol","cd")
    secondary_units = ("N","J")
    prefixes = ("G","M","k","c","m","μ")

    def __init__(self, unit:str):
        self.prefix = ""
        self.mult = 1
        self.primary = ""
        self.fund = False #bool whether unit is fundamental idk if I need this

        # Metric prefixes are always one letter:
        if unit[0] in self.prefixes:
            self.prefix = unit[0]
            self.mult = Metric_Unit.prefix_multipler(self.prefix)
            unit = unit[1:-1] #remove first letter from string finder

        if unit in self.fundamental_units:
            self.primary = unit
            self.fund = True
        elif unit in self.secondary_units:
            self.primary = unit
            self.fund = False
        else:
            self.prefix = None
            self.mult = None
            self.fund = None

    @staticmethod
    def expand_units(secondary_unit:str) -> str:
        if secondary_unit not in Metric_Unit.secondary_units:
            print(f"Warning: Unit \"{secondary_unit}\" not supported")
            sys.exit()

        if secondary_unit == "N":
            return "kg*m*s**-2"
        elif secondary_unit == "J":
            return "kg*m**2*s**-2"
        else:
            print(f"Warning: the dumbass who made this needs to add \"{secondary_unit}\" to the function!")
            sys.exit()

    @staticmethod
    def prefix_multipler(prefix:str) -> str:
        ("G","M","k","c","m","μ")
        if prefix == "G":
            return 1e9
        elif prefix == "M":
            return 1e6
        elif prefix == "k":
            return 1e3
        elif prefix == "c":
            return 1e-2
        elif prefix == "m":
            return 1e-3
        elif prefix == "μ":
            return 1e-6"""

class Operator():
    def __init__(self, value:float | int, units:str):
        self.value = value
        self.unit_obj = self.define_unit(units)

    def define_unit(self, units:str) -> Units:
        # temporary while I only have Metric Units - otherwise would have to detect
        return Units(units)

    def __repr__(self) -> str:
        return f"{self.value} {self.unit_obj.disp}"

    def __add__(self, other:float | int | Operator) -> Operator:
        if type(other) != Operator:
            if self.unit_obj.fund == "":
                new_value = self.value + other
                return Operator(new_value, "")
            else:
                print("Warning: cannot add dimension with dimensionless")
        
        elif self.unit_obj.fund == other.unit_obj.fund:
            new_value = self.value + other.value
            return Operator(new_value, self.unit_obj.fund)
        
        else:
            print("Warning: dimensions do not match")
        
        return NotImplemented
        
    def __radd__(self, other:float | int) -> Operator:
        # The only way this should get called is if the left operand isn't Operator
        if type(other) != float and type(other) != int:
            print("Hey buddy, you were wrong about reverse addition!")
            return
        
        return self.__add__(other)

"""
for stringy in Length.units:
    print(stringy+" = "+str(Length.units[stringy]))
"""
a = Units("Pa^-4/s^3")
from Units import Dimension

dim1 = Dimension(9,"atm")
print(dim1.magnitude)
print(dim1.fund_units)
dim1.convert_units("atm",0)
from Units import Dimension

dim1 = Dimension(19,"kg*m/s")
#print(dim1.magnitude)
#print(dim1.fund_units)
#print(round(dim1,1))
#dim1.convert_units("slug*ft/hr",10)
dim2 = Dimension(3,"kg^3*m/s")

dim1  = dim2**0.3
print(dim1)
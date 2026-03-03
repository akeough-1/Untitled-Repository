from Shock_Flow import Shock
from Isentropic_Flow import calculate_ideal_gas as ig
from Isentropic_Flow import mach2vel
from Isentropic_Flow import vel2mach
from Isentropic_Flow import Isentropic_Flow as IF
from Isentropic_Flow import Metric_Constants as MC, Imperial_Constants as IC
import numpy as np

"""
U1 = 1215
T1 = 300
M1 = vel2mach(MC.R,U1,T1)
shock2 = Shock(M1=M1)
M2 = shock2.vals["M2"]
T_ratio = shock2.vals["T_ratio"]
T2 = T_ratio*T1
U2 = mach2vel(MC.R,M2,T2)
print(U2)
"""
"""
# Given infs and point, find vel at point
p_inf = 0.61*101000
rho_inf = 0.819
V_inf = 340
p1 = 0.3*101000

#target: V1
T_inf = ig("metric",pressure=p_inf,density=rho_inf)
T1 = T_inf*(p1/p_inf)**(2/7)

T0 = T_inf + V_inf**2/2/MC.Cp
V1 = (2*MC.Cp*(T0 - T1))**0.5
print(V1)

# Bernoulli: 1/2*rho_inf*V_inf^2 + p_inf = 1/2*rho1*V1^2 + p1, rho_inf = rho1
V1_B = (V_inf**2 + (p_inf - p1)*2/rho_inf)**0.5
print(V1_B)

percentage_error = (V1 - V1_B)/V1*100
print(percentage_error)
"""
"""
# Given resivoir temp and test section velocity, find mach
T0 = 519
V1 = 1355

T1 = T0 - V1**2/2/IC.Cp
M1 = vel2mach(IC.R,V1,T1)
print(M1)
"""
"""
M_inf = 1.93
P0 = 0.751*101000
PA = 0.5*101000
TA = 300

A_list = IF.calculate_values("P",P0/PA)
MA = A_list[0]
print("Mach_A = "+str(MA))

T_ratio = A_list[3]
T0 = T_ratio*TA
print("stag_temp = "+str(T0))

inf_list = IF.calculate_values("M",M_inf)
T_inf_ratio = inf_list[3]
T_inf = T0/T_inf_ratio
print("T inf = ",str(T_inf))
"""
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import fsolve

with open("nozzle.dat","r") as file:
    profile = np.loadtxt(file,delimiter=" ",)

# convert radius values to area
for i in range(len(profile)):
    rad = profile[i,1]
    profile[i,1] = 2*np.pi*rad**2


A_star = min(profile[:,1])

A_e = profile[-1,1]

def residual(M,A_ratio):
    return 1/M*(2/(1+1.4)*(1 + (1.4 - 1)/2*M**2))**((1.4+1)/(2*(1.4-1))) - A_ratio

M_c1 = fsolve(residual, x0=0.1, args=(A_e/A_star))[0]
print(f"M_c1 = {M_c1}")

P1_ratio = (1 + (1.4-1)/2*M_c1**2)**-(1.4/(1.4-1))
print(f"P1_ratio = {P1_ratio}")


M_c3 = fsolve(residual, x0=10, args=(A_e/A_star))[0]
print(f"M_c3 = {M_c3}")

P3_ratio = (1 + (1.4-1)/2*M_c3**2)**-(1.4/(1.4-1))
print(f"P3_ratio = {P3_ratio}")


M_c2 = ((1 + (1.4-1)/2*M_c3**2)/(1.4*M_c3**2 - (1.4 - 1)/2))**0.5
P2_ratio = (1 + (1.4-1)/2*M_c2**2)**-(1.4/(1.4-1))

P2_1_ratio = ((1 + (1.4-1)/2*M_c2**2)/(1 + (1.4-1)/2*M_c1**2))**-(1.4/(1.4-1))
P2_ratio = P2_ratio*P2_1_ratio

print(f"Mc_2 = {M_c2}")
print(f"P2_ratio = {P2_ratio}")

Pb = 101 #kPa
Pt = 1000 #kPa
Rt = 10 #mm
Tt = 300 #K
atm_ratio = Pb/Pt
print(f"atm_ratio = {atm_ratio}")

if atm_ratio > P1_ratio:
    Me = (2/(1.4-1) * atm_ratio**(1.4/(1.4-1)) - 1)**0.5

elif atm_ratio > P2_ratio:
    Me = -1/(1.4-1) + (1/(1.4-1)**2 + 2/(1.4-1) * (2/(1.4+1)**((1.4+1)/(1.4-1))) / (A_e/A_star*atm_ratio)**2)**0.5

elif atm_ratio > P3_ratio:
    Me = M_c3

else:
    Me = M_c3

print(f"exit mach = {Me}")

Gamma = (1.4 * (2/(1.4+1))**((1.4+1)/(1.4-1)))**0.5
m_dot = Gamma*(Pt/1000)/(Rt/1000*Tt)

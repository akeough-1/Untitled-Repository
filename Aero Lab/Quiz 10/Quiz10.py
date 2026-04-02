import re
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import fsolve

with open("nozzle.dat","r") as file:
    profile = np.loadtxt(file,delimiter=" ",)

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


def residual(M,A_ratio):
    return 1/M*(2/(1+1.4)*(1 + (1.4 - 1)/2*M**2))**((1.4+1)/(2*(1.4-1))) - A_ratio

M_c3 = fsolve(residual, x0=4, args=(A_e/A_star))[0]
print(f"M_c3 = {M_c3}")

P3_ratio = (1 + (1.4-1)/2*M_c3**2)**-(1.4/(1.4-1))
print(f"P3_ratio = {P3_ratio}")


M_c2 = ((1 + (1.4-1)/2*M_c3**2)/(1.4*M_c3**2 - (1.4 - 1)/2))**0.5
P2_ratio = (1 + (1.4-1)/2*M_c2**2)**-(1.4/(1.4-1))

P2_1_ratio = ((1 + (1.4-1)/2*M_c2**2)/(1 + (1.4-1)/2*M_c1**2))**(1.4/(1.4-1))
P2_ratio = P2_ratio*P2_1_ratio

print(f"Mc_2 = {M_c2}")
print(f"P2_ratio = {P2_ratio}")

Pb = 101 #kPa
Pt = 1000 #kPa
atm_ratio = Pb/Pt

print(f"atm_ratio = {atm_ratio}")
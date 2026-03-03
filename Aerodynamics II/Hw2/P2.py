p_inf = 0.61 #atm
rho_inf = 0.819 #kg/m^3
V_inf = 300 #m/s

p = 0.52 #atm

R = 287
Cp = 7/2*R
gamma = 1.4

T_inf = p_inf*101e3/rho_inf/R

a_inf = (gamma*R*T_inf)**.5

M_inf = V_inf/a_inf

pO = p_inf*(1 + M_inf**2/5)**(7/2)

M1 = (5*((pO/p)**(2/7) - 1))**.5

TO = T_inf*(pO/p_inf)**(2/7)
T = TO*(pO/p)**(-2/7)

a = (gamma*R*T)**.5
U = M1*a
print(U)
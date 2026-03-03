from Isentropic_Flow import Isentropic_Flow as IF

M_inf = 0.82
M = 0.74
P_inf = 1455.6 #lb/ft^2
T_inf = 483.04 #R

# find P and T at point
# Probably use p2/p1 equation?

inf_vals_list = IF.calculate_values("M",M_inf)

P_inf_ratio = inf_vals_list[2]
T_inf_ratio = inf_vals_list[3]

vals_list = IF.calculate_values("M",M)

P_ratio = vals_list[2]
T_ratio = vals_list[3]

P2 = P_inf*P_inf_ratio/P_ratio
T2 = T_inf*T_inf_ratio/T_ratio

print(f"P2 = {P2}, T2 = {T2}")

#1426
#480
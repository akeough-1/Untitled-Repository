from Isentropic_Flow import Isentropic_Flow as IF

P = 1*101000 #Pa
T = 230 #K
M = 2.5

vals_list = IF.calculate_values("M",M)

P_ratio = vals_list[2]
T_ratio = vals_list[3]

P_0 = P_ratio*P
T_0 = T_ratio*T

print(f"P0 = {P_0/101000}, T0 = {T_0}")
from Isentropic_Flow import Isentropic_Flow as IF

T = 300 #K
P = 1.2*101000 #Pa
U = 285 #m/s

R = 287
Cp = 7/2*R
gamma = 1.4

# find P_0, T_0, rho*, T*, and M* at this point!

# M* = U/a* -> M*^2 = (gamma+1)*M^2/(2+(gamma-1)*M^2)
# T_0/T = 1 + (gamma -1)/2*M^2 (isentropic flow)
# P_0/P = (1 + (gamma - 1)/2*M^2)^(gamma/(gamma-1)

# T*/T_0 = 2/(gamma + 1) = 0.833
# rho*/rho_0 = (2/(gamma + 1))^(1/(gamma - 1)) = 0.634
# P*/P_0 = (2/(gamma+1))^(gamma/(gamma-1)) = 0.528

# use Pv = nRT to get P? P = rho*R*T
# get M from basic vel eqn: U^2/(2*Cp*T) = (gamma -1)/2*M^2
# -> M = sqrt(U^2/(2*Cp*T) * 2/(gamma - 1))

M = ((U**2/(2*Cp*T) * 2/(gamma - 1)))**0.5
rho = P/R/T

M_star = ((gamma+1)*M**2/(2 + (gamma-1)*M**2))**0.5

T_ratio = 1 + (gamma - 1)/2 * M**2

ratio_list = IF.calculate_values("T",T_ratio)

T_0 = T_ratio*T
P_0 = ratio_list[2]*P

T_star = 0.833*T_0
P_star = 0.528*P_0

print(f"T0 = {T_0}, T* = {T_star}, P0 = {P_0/101000}, P* = {P_star/101000}, M* = {M_star}")
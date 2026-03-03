from Flow_Library import Shock
from Flow_Library import calculate_ideal_gas as ig
from Flow_Library import Isentropic_Flow as IF
from Flow_Library import Metric_Constants as MC, Imperial_Constants as IC

M1 = float(input("Enter M1: "))
T1 = float(input("Enter T1 (K): "))
P1 = float(input("Enter P1 (atm): "))
P1 = MC.atm2Pa(P1)
rho1 = ig("metric",pressure=P1,temp=T1)

isen = IF(M=M1,P1=P1,T1=T1)
P0_1 = isen.P0
T0_1 = isen.T0

print(f"\nUpstream Side, M1 = {round(M1,4)}")
print(f"T1 = {round(T1,4)}, T_0 = {round(T0_1,4)}")
print(f"P1 = {round(MC.Pa2atm(P1),4)}, P0_1 = {round(MC.Pa2atm(P0_1),4)}")
print(f"rho1 = {round(rho1,4)}")

s = Shock("metric",M1=M1,P1=P1,P0_1=P0_1,T1=T1,T0_1=T0_1,rho1=rho1)
P0_ratio = s.P0_2/P0_1

print(f"\nDownstream Side, M2 = {round(s.M2,4)}")
print(f"T2 = {round(s.T2,4)}, T_0 = {round(s.T0_2,4)}")
print(f"P2 = {round(MC.Pa2atm(s.P2),4)}, P0_2 = {round(MC.Pa2atm(s.P0_2),4)}")
print(f"rho2 = {round(s.rho2,4)}")
print(f"P0_2/P0_1 = {round(P0_ratio,4)}")
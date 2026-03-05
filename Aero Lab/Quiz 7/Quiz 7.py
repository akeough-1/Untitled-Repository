import re
import matplotlib.pyplot as plt
import numpy as np

with open("Aero Lab/zone1.txt","r") as file:
    lines = file.readlines()

    z1_Cd = 0
    prev_y = -1
    for line in lines:
        line = re.sub(r"\s+"," ", line.strip())
        vals = [float(x) for x in line.split(" ")]
        index, y, u, v, uu, vv, uv = vals
        uv *= -1

        dy = y - prev_y
        prev_y = y
        
        z1_Cd += u*(1 - u)*dy/24

    z1_Cd *= 2
    print(z1_Cd)

with open("Aero Lab/zone2.txt","r") as file:
    lines = file.readlines()

    z2_Cd = 0
    prev_y = -2.8
    prev_u = 0.979
    uu_ary = []
    u_ary = []
    du_dy = []
    for line in lines:
        line = re.sub(r"\s+"," ", line.strip())
        vals = [float(x) for x in line.split(" ")]
        index, y, u, v, uu, vv, uv = vals
        uv *= -1

        du = u - prev_u
        dy = y - prev_y
        prev_y = y
        
        z2_Cd += u*(1 - u)*dy/24

        uu_ary.append(uu)
        u_ary.append(u)
        du_dy.append(du/dy)

    z2_Cd *= 2
    print(z2_Cd)
    y_c = np.linspace(-1.6/24,1.6/24,len(uu_ary))
    plt.figure()
    plt.plot(uu_ary,y_c)
    plt.xlabel("U'^2")
    plt.ylabel("y/c")
    plt.show()

    plt.figure()
    plt.plot(u_ary,y_c)
    plt.xlabel("u/U_inf")
    plt.ylabel("y/c")
    plt.show()

    plt.figure()
    plt.plot(du_dy,y_c)
    plt.xlabel("du/dy")
    plt.ylabel("y/c")
    plt.show()
    

with open("Aero Lab/zone3.txt","r") as file:
    lines = file.readlines()

    z3_Cd = 0
    prev_y = -1.6
    for line in lines:
        line = re.sub(r"\s+"," ", line.strip())
        vals = [float(x) for x in line.split(" ")]
        index, y, u, v, uu, vv, uv = vals
        uv *= -1

        dy = y - prev_y
        prev_y = y
        
        z3_Cd += u*(1 - u)*dy/24

    z3_Cd *= 2
    print(z3_Cd)
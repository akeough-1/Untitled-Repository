import numpy as np
import matplotlib.pyplot as plt
import sys

# Values for figure font size
axis_font_size = 15
tick_mark_size = 10
title_font_size = 20

# having directory issues, but this way as long as the files are in the same folder it will work
rel_path = sys.path[0]

with open(rel_path+"/foil_locations.csv", encoding="utf-8-sig") as f:
    Foil_locations = np.loadtxt(f, delimiter=",")
chord = 101 # mm

angles_deg = (-4,0,4,6,8,10,12,14,16) #degrees
ports_size = np.array(range(0,16))
ports = np.concat([(ports_size + 2),(ports_size + 36),(ports_size[:-3] + 70)])

A_port = 43
E_port = 44
Foil_ports = list(range(0,43)) + [0]

def get_mean_data(angle_deg:int,test_letter:str="a") -> dict:
    filename = rel_path + "/aoa" + str(angle_deg) + ".csv"
    if test_letter == "b":
        filename = filename[:-4] + "b" + filename[-4:]

    data = np.loadtxt(filename, delimiter=",")
    p_data = data[:,ports]

    mean_p = np.zeros([len(ports)])
    for col in range(len(ports)):
        mean_p[col] = np.mean(p_data[:,col])

    A_pressure = mean_p[A_port]
    E_pressure = mean_p[E_port]
    Foil_pressure = mean_p[Foil_ports]
    pressures = {
        "A":A_pressure,
        "E":E_pressure,
        "F":Foil_pressure,
    }
    return pressures

cl = np.zeros([len(angles_deg)])
cd = np.zeros([len(angles_deg)])
cm = np.zeros([len(angles_deg)])
cp = []
Re = []
for j in range(len(angles_deg)):
    test_a = get_mean_data(angles_deg[j])
    test_b = get_mean_data(angles_deg[j],"b")

    A_pressure = float(np.mean([test_a["A"],test_b["A"]]))
    E_pressure = float(np.mean([test_a["E"],test_b["E"]]))
  
    # this line lmao
    Foil_pressure = np.array([float(np.mean([test_a["F"][i],test_b["F"][i]])) for i in range(len(test_a["F"]))])
    K = 1.1 # Wind tunnel calibration constant

    Foil_Cp = (Foil_pressure - E_pressure)/K/(A_pressure - E_pressure)

    cN = 0
    cA = 0
    cM = 0
    for i in range(len(Foil_locations) - 1): # account for first point repeated at end of array
        dx_i = Foil_locations[i+1,0] - Foil_locations[i,0]
        dy_i = Foil_locations[i+1,1] - Foil_locations[i,1]

        x_ihalf = (Foil_locations[i+1,0] + Foil_locations[i,0])/2
        y_ihalf = (Foil_locations[i+1,1] + Foil_locations[i,1])/2

        Cp_ihalf = (Foil_Cp[i+1] + Foil_Cp[i])/2

        cN += Cp_ihalf*dx_i
        cA -= Cp_ihalf*dy_i
        cM -= (Cp_ihalf*dx_i*x_ihalf + Cp_ihalf*dy_i*y_ihalf)

    angle_rad = np.deg2rad(angles_deg[j])
    cl[j] = cN*np.cos(angle_rad) - cA*np.sin(angle_rad)
    cd[j] = cN*np.sin(angle_rad) + cA*np.cos(angle_rad)
    cm[j] = cM

    cp.append(Foil_Cp)

    rho = 100000/287/(18.7+273.15)
    q = 1.1*(A_pressure - E_pressure)
    V = (2*q/rho)**0.5
    mu = 1.81e-5
    Re.append(rho*V*(chord/1000)/mu)

# First Plot: airfoil shape and Tap positions
plt.figure()
pnts_mm = Foil_locations*chord
plt.plot(pnts_mm[:,0],pnts_mm[:,1], zorder=0, label="_nolegend_")
plt.scatter(pnts_mm[:,0],pnts_mm[:,1], color="red", s=15, zorder=1, label="Pressure Taps")
plt.xlim(-1,chord+1)
plt.ylim(-chord/2 - 0.5,chord/2 + 0.5)
plt.xlabel("x (mm)", fontsize=axis_font_size)
plt.ylabel("y (mm)", fontsize=axis_font_size)
plt.legend()
plt.title("GA(W)-1 Airfoil Pressure Taps", fontsize=title_font_size)
plt.tick_params(axis='both', labelsize=tick_mark_size)
plt.show()

num_taps = len(Foil_locations) -1
Foil_angles = np.zeros([num_taps])
Foil_magnitudes = np.zeros([num_taps])
for i in range(num_taps):
    x = float(Foil_locations[i,0]) - 0.5
    y = float(Foil_locations[i,1])

    if x == 0:
        if y == 0:
            Foil_angles[i] = 270
        else:
            Foil_angles[i] = 90

    else:
        a_rad = np.atan(y/x)
        if x < 0:
            a_rad += np.pi

        while a_rad < 0:
            a_rad += 2*np.pi
        while a_rad > 2*np.pi:
            a_rad -= 2*np.pi

        Foil_angles[i] = np.rad2deg(a_rad)
    Foil_magnitudes[i] = (x**2 + y**2)**0.5

# Second Plot: angular Tap positions
plt.figure()
x = np.zeros(num_taps)
y = np.zeros(num_taps)
for pnt_i in range(num_taps):
    x[pnt_i] = Foil_magnitudes[pnt_i]*np.cos(np.deg2rad(Foil_angles[pnt_i])) + 0.5
    y[pnt_i] = Foil_magnitudes[pnt_i]*np.sin(np.deg2rad(Foil_angles[pnt_i]))
plt.scatter(x,y)
plt.scatter(x[0],y[0],color="green",s=40)
plt.scatter(x[20],y[20],color="yellow",s=40)
plt.scatter(x[-1],y[-1],color="red")
plt.ylim(-0.5,0.5)
plt.grid(True)
plt.show()


def plot_coef(coef,name:str):
    plt.figure()
    plt.plot(angles_deg, coef)
    plt.tick_params(axis='both', labelsize=tick_mark_size)
    plt.xlabel("Angle of Attack (deg)", fontsize=axis_font_size)
    plt.ylabel(name, fontsize=axis_font_size)
    plt.title(name + " vs AoA", fontsize=title_font_size)
    plt.grid(True)
    plt.show()

# Plots 3-6: Coeficients
plot_coef(cl,"Cl")
plot_coef(cd,"Cd")
plot_coef(cm,"Cm")


Foil_angles[:20] = Foil_angles[:20] - 360

def plot_Cp(index:int):
    Cp = cp[index][:-1]
    plt.figure()
    plt.plot(Foil_angles, Cp)
    plt.tick_params(axis='both', labelsize=tick_mark_size)
    plt.xlabel("Airfoil Location (deg)", fontsize=axis_font_size)
    plt.ylabel("Cp", fontsize=axis_font_size)
    plt.title(f"Cp at {angles_deg[index]} deg AoA", fontsize=title_font_size)
    plt.grid(True)
    plt.show()

# Plots 7-15: Pressure Coeficients
for plot in range(9):
    plot_Cp(plot)

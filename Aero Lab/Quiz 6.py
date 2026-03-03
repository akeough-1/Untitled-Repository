import numpy as np

with open("Aero Lab 5/foil_locations.csv", encoding="utf-8-sig") as f:
    Foil_locations = np.loadtxt(f, delimiter=",")
print(len(Foil_locations))
p_data = np.loadtxt("Quiz6_data.csv",delimiter=",",skiprows=1)

#x_c = p_data[:,0]
#y_c = p_data[:,1]
#cp = p_data[:,2]
x_c = Foil_locations[:,0]
y_c = Foil_locations[:,1]
cp = np.array([-0.25845495,0.64484586,0.8003378,0.67264751,0.54567309,0.44563177,0.37097662,0.29423077,0.18022396,0.01097608,-0.09192433,-0.1671543,-0.24310792,-0.28618594,-0.25612457,-0.21367767,-0.15411545,-0.12097543,-0.12634809,-0.14181248,-0.75825369,-0.80719957,-0.804247,-0.8437265,-0.8506985,-0.85112805,-0.85126056,-0.84755963,-0.84260781,-0.8383198,-0.83478051,-0.83266851,-0.83048703,-0.83032604,-0.82970218,-0.82904016,-0.82265768,-0.82043458,-0.81460976,-0.81120397,-0.8138848,-0.89517876,-1.17379445,-0.25845495])

#alpha = np.deg2rad(-2)
alpha = np.deg2rad(16)

cN = 0
cA = 0
cm = 0
for i in range(len(Foil_locations) - 1):
    dx_i = x_c[i+1] - x_c[i]
    dy_i = y_c[i+1] - y_c[i]

    x_half = (x_c[i] + x_c[i+1])/2
    y_half = (y_c[i] + y_c[i+1])/2

    cp_half = (cp[i] + cp[i+1])/2

    cN += cp_half*dx_i
    cA -= cp_half*(dy_i)

    cm -= (cp_half*dx_i*x_half + cp_half*dy_i*y_half)

cl = cN*np.cos(alpha) - cA*np.sin(alpha)
cd = cN*np.sin(alpha) + cA*np.cos(alpha)

#print(f"cA = {cA}, cN = {cN}")

print(f"cl = {cl}, cd = {cd}, cm_LE = {cm}")
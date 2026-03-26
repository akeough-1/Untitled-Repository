import re
from scipy.optimize import curve_fit
from numpy import mean

U = 12.07
x = 1.625
nu = 1.5233e-5
Re = U*x/nu

theoretical = {
    "delta":0.37*x/Re**(1/5),
    "delta_star":0.048*x/Re**(1/5),
    "theta":0.037*x/Re**(1/5),
    "CD":0.074/Re**(1/5),
    "tau_w":0.058/Re**(1/5)/2*1.225*U**2
}
print(theoretical["tau_w"])

delta_slope = [0]
delta_star = [0]
theta = [0]
tau_w = [0]

with open("Aero Lab/Quiz 9/U12.07","r") as file:
    lines = file.readlines()
    
    prev_y = 0
    prev_u = 0

    for line in lines:
        line = re.sub(r"\s+"," ", line.strip())
        vals = [float(x) for x in line.split(" ")]
        y, u = vals

        du = u - prev_u
        dy = y - prev_y

        if u >= 0.99*U:
            delta = y

        prev_u = u
        prev_y = y

        delta_star.append((1 - u/U)*dy)
        theta.append(u/U*(1 - u/U)*dy)
        tau_w.append(1.8255e-5*du/dy)

    delta_star = sum(delta_star)
    theta = sum(theta)
    tau_w = sum(tau_w)
    print(f"delta_star = {delta_star}")
    print(f"theta = {theta}")
    print(f"tau_w = {tau_w}")
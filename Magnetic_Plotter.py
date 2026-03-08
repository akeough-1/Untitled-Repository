import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("C:/Users/ack84/Downloads/HeliosCSV.csv", usecols=["time","magnetometer_x","magnetometer_y","magnetometer_z","acceleration_z"])

t = df["time"]
x = df["magnetometer_x"]
y = df["magnetometer_y"]
z = df["magnetometer_z"]
accel = df["acceleration_z"]

plt.figure()
plt.plot(t,accel,label="vert accel")
plt.xlabel("Time (s)")
plt.ylabel("Acceleration (m/s^2)")
plt.title("Helios Vertical Acceleration")
plt.legend()
plt.grid()
plt.show()

plt.figure()
plt.plot(t,x,label="x")
plt.plot(t,y,label="y")
plt.plot(t,z,label="z")
plt.xlabel("Time (ms)")
plt.ylabel("Intensity (µT)")
plt.title("Helios Magnetometer Measurements")
plt.legend()
plt.grid()
plt.show()

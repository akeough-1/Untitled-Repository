import numpy as np
from pyulog import ULog
import matplotlib.pyplot as plt

file_path = "3-1_Flight_Data.ulg"
ulg = ULog(file_path)

try:
    vehicle_status = ulg.get_dataset('vehicle_status')
except (KeyError, IndexError, ValueError) as error:
    print(type(error), "(vehicle_status):", error)

data_list = ulg.data_list

#for d in data_list:
#    print(d.name)

# to find title of parameter, use dataset.data.keys() and that is the string to index

# check units
time_ary = vehicle_status.data['takeoff_time']
timestamp = vehicle_status.data['timestamp']

for t in time_ary:
    if t != 0:
        takeoff_time = t 
        break

for i in range(len(timestamp)-1,0,-1):
    if time_ary[i] != 0:
        landing_time = timestamp[i] 
        break

print(f"takeoff: {takeoff_time} landing: {landing_time}")
#print(timestamp)

#x = range(len(accel_x))

#assume sample rate of 30hz :)

"""plt.figure()
plt.plot(x, accel_x)
plt.xlabel("x")
plt.ylabel("x acceleration")
plt.title("acceleration")
plt.grid(True)
plt.show()
"""

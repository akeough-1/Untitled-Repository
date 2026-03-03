import numpy as np
import matplotlib.pyplot as plt

def simple(arr:np.array):
    result = np.zeros(len(arr))
    for i in range(len(arr)):
        if arr[i,0] != 1 and arr[i,1] >= 11:
            result[i] = 1
    return result

def complex(arr:np.array):
    result = np.zeros(len(arr))
    for i in range(len(arr)):
        if arr[i,0] != 1:
            check = arr[i:i+10,1]
            for j in range(len(check)):
                if check[j] >= 11:
                    result[i] = 1
    return result

axis_font_size = 15
tick_mark_size = 10
title_font_size = 20

volt = np.loadtxt("voltage.csv", delimiter=",", skiprows=1)

result = complex(volt)

x = np.linspace(0,254,len(result))

csv_ary = np.vstack([x,result]).T
print(csv_ary[:,0:3])
np.savetxt("R2U2-with_time_interval.csv",csv_ary,delimiter=',')

"""
plt.figure()
plt.plot(x, result)
plt.tick_params(axis='both', labelsize=tick_mark_size)
plt.xlabel("Time Armed", fontsize=axis_font_size)
plt.ylabel("Output", fontsize=axis_font_size)
plt.title("R2U2 Output - with time interval", fontsize=title_font_size)
plt.grid(True)
plt.show()
"""
import numpy as np
import pandas as pd
from pyulog import ulog2csv
from pyulog import ULog

dataset = "battery_status"
parameter = "voltage_v"

file_path = "3-1_Flight_Data.ulg"
ulg = ULog(file_path)
dataset_ulog = ulg.get_dataset(dataset)
parameter_ary = dataset_ulog.data[parameter]

file_name = parameter + ".csv"
header = parameter.title()[0]
np.savetxt(file_name,parameter_ary,delimiter=',',header=header)
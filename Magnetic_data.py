from pywmm import WMMv2
from pywmm.date_utils import decimal_year
from datetime import datetime
import time

# Current location (Argonia, KS)
lat = 37.1678
lon = -97.7398
alt = 0.5  # sea level in km

current_date = datetime.now().strftime("%Y-%m-%d") + " 13:000"
current_date = current_date.partition(" ")[0]
print(f"expected date format: {current_date}")
year = decimal_year(current_date)

# Initialize the model
wmm = WMMv2()

t_start = time.time()
# Calculate all field components at once (most efficient)
north_intens = wmm.get_north_intensity(lat,lon,year,alt)
east_intens = wmm.get_east_intensity(lat,lon,year,alt)
vert_intens = wmm.get_vertical_intensity(lat,lon,year,alt)
t_end = time.time()

mag_ary = [north_intens,east_intens,vert_intens]
for i in range(len(mag_ary)):
    mag_ary[i] = mag_ary[i]/1000

t_elapsed = (t_end - t_start)*1000 #ms
# Now all properties are available
print(f"North Component: {mag_ary[0]:.1f} µT")
print(f"East Component: {mag_ary[1]:.1f} µT")
print(f"Vertical Component: {mag_ary[2]:.1f} µT (positive downward)")
print(f"get time = {t_elapsed:.3f}ms")
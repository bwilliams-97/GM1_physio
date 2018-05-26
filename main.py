# Main device operation

import arduino_bt as bt 
import clock_sync as sync
import smoother
import time
import dataplotter as dp
import numpy as np

t0 = time.time()
elapsed = 0.0;

xarray_up = []
xarray_lo = []
yarray_up = []
yarray_lo = []
flexarray_up = []
flexarray_lo = []

# Define bluetooth connections
bd_addr_1 = "30:14:11:19:00:48"
bd_addr_2 = "20:14:11:14:11:13"

sock_up, data_up = bt.connect(bd_addr_1)
sock_lo, data_lo = bt.connect(bd_addr_2)

t0 = time.time()
while (elapsed < 10):
	x_rot_up, y_rot_up, flex_up, success, data_up = bt.get_knee_data(sock_up, data_up)
	#print(data_up)
	if success is True:
		print("upper", x_rot_up, y_rot_up, flex_up, elapsed, sep=" ")
		xarray_up.append(x_rot_up)
		yarray_up.append(y_rot_up)
		flexarray_up.append(flex_up)
	
	x_rot_lo, y_rot_lo, flex_lo, success, data_lo = bt.get_knee_data(sock_lo, data_lo)
	#print(data_lo)
	if success is True:
		print("lower", x_rot_lo, y_rot_lo, flex_lo, elapsed, sep=" ")
		xarray_lo.append(x_rot_lo)
		yarray_lo.append(y_rot_lo)
		flexarray_lo.append(flex_lo)
	
	elapsed = time.time() - t0

xarray_up = smoother.smooth(np.array(xarray_up).astype(np.float))
bt.close(sock_up)
bt.close(sock_lo)
dp.data_plot(xarray_up, yarray_up, flexarray_up)

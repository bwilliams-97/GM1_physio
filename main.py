# Main device operation

import arduino_bt as bt 
import clock_sync as sync
import smoother
import time
import dataplotter as dp

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

sock_up = bt.connect(bd_addr_1)
sock_lo = bt.connect(bd_addr_2)


while (elapsed < 10):
	(x_rot_up, y_rot_up, flex_up) = bt.get_knee_data(sock_up)
	print(x_rot_up, y_rot_up, flex_up, elapsed, sep=" ")
	xarray_up.append(x_rot_up)
	yarray_up.append(y_rot_up)
	flexarray_up.append(flex_up)
	
	(x_rot_lo, y_rot_lo, flex_lo) = bt.get_knee_data(sock_lo)
	print(x_rot_lo, y_rot_lo, flex_lo, elapsed, sep=" ")
	xarray_up.append(x_rot_lo)
	yarray_up.append(y_rot_lo)
	flexarray_up.append(flex_lo)
	
	elapsed = time.time() - t0

	"""
	if len(xarray) > 20:
		x_to_smooth = xarray[-20:]
		y_to_smooth = yarray[-20:]
		flex_to_smooth = flex[-20:]
	else:
		continue
	
	x_smoothed = smoother.smooth(x_to_smooth, x_to_smooth.size, 'Hamming')
	y_smoothed = smoother.smooth(y_to_smooth, y_to_smooth.size, 'Hamming')
	flex_smoothed = smoother.smooth(flex_to_smooth, flex_to_smooth.size, 'Hamming')
"""
bt.close(sock_up)
bt.close(sock_lo)
dp.data_plot(xarray, yarray, flexarray)

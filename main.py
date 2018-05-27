#!/usr/bin/python3

# Main device operation

import arduino_bt as bt 
import clock_sync as sync
import smoother
import time
import dataplotter as dp
import numpy as np
import sys
import Xenplate_Functions as xf

def max_difference(array):
	min_elem = array[0]
	max_elem = array[0]
	max_diff = -1
	
	for elem in array[1:]:
		min_elem = min(elem, min_elem)
		if elem > max_elem:
			max_diff = max(max_diff, elem-min_elem)
			max_elem = elem
	
	return max_diff

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

# Set boolean success criteria
ula_success = False
ulm_success = False
lla_success = False
llm_success = False

im1l, im1r, im2l, im2r, im3l, im3r, im4l, im4r = dp.gui_plot() # Open GUI

t0 = time.time() # Start timer
while (elapsed < 50):
	# Read data in
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
	
	# Make decision about leg above ground
	if yarray_up[-1] > -5.0:
		ula_success = True
	else:
		ula_success = False
	
	# Make decision about leg straight
	if xarray_lo[-1]-xarray_up[-1] < 10.0:
		lla_success = True
	else:
		lla_success = False
		
	# Make decision about muscle contraction - test for step change (upper)
	if (max_difference(flexarray_up[-5:]) > 0.05):
		ulm_success = not ulm_success
	else:
		ulm_successs = ulm_success
		
	# Make decision about muscle contraction - test for step change (lower)
	if (max_difference(flexarray_lo[-5:]) > 0.05):
		llm_success = not ulm_success
	else:
		llm_successs = ulm_success
		
	dp.toggle_images(ula_success,lla_success,ulm_success,llm_success, im1l, im1r, im2l, im2r, im3l, im3r, im4l, im4r)


# xarray_up = smoother.smooth(np.array(xarray_up).astype(np.float))
bt.close(sock_up)
bt.close(sock_lo)
dp.data_plot(xarray_up, yarray_up, flexarray_up)
#dp.data_plot(xarray_lo, yarray_lo, flexarray_lo)


#======================================================================
plate_id = xf.get_newest_plate_id("5") #enter record_id as string, e.g. "5"
print(plate_id)

template_id, plate_version = xf.get_plate_template_id_and_version("5", plate_id) #enter record_id and plate_id's as strings, e.g. "5", "1121"
print(template_id)
print(plate_version)

xf.create_plate("5", template_id, plate_version)

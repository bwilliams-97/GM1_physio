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
import re
from operator import add
import math
import requests
from datetime import datetime


user = "GroupThree"
key = "wRjUm82tln5ZYPpd1tQ3rV0c"
certif = "N3s7i2uYJ0pgAiRxEHv2FNYw"

path = r"/home/pi/GM1_sensors/GM1_physio/Xenplate_permissions/L2S2-2018-CUEDGroup3-20180509"

cert_path = path + ".crt"
key_path = path + ".key.decrypted"

s = "01/12/2011"
t_stamp = time.mktime(datetime.strptime(s, "%d/%m/%Y").timetuple()) + 5364662400 #add seconds from 00:00:00 01/01/1800 to epoch (1970)
t_now = datetime.now().timestamp() + 5364662400

# Function that finds the max difference in an array
# Not currently used (would be useful for detecting step changes over fixed interval)
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
	
# Function that finds the number of lines in a string by detecting new line characters
def find_no_lines(string):
	indices = [match.start() for match in re.finditer(re.escape('\n'), string)]
	return len(indices)

elapsed = 0.0;

# Initialise data arrays
xarray_up = []; xarray_lo = []
yarray_up = []; yarray_lo = []
zarray_up = []; zarray_lo = []
flexarray_up = []; flexarray_lo = []
time_up = []; time_lo = []

# Initialise Xenplate variables
upper_angle_success = False; max_upper_angle_time = 0.0; t0_upper_angle = 0.0; upper_angle_instances = 0;
straight_angle_success = False; max_straight_angle_time = 0.0; t0_straight_angle = 0.0; straight_angle_instances = 0
upper_muscle_success = False; max_upper_muscle_time = 0.0; t0_upper_muscle = 0.0; upper_muscle_instances = 0
lower_muscle_success = False; max_lower_muscle_time = 0.0; t0_lower_muscle = 0.0; lower_muscle_instances = 0

# Define bluetooth connections
bd_addr_1 = "30:14:11:19:00:48"
bd_addr_2 = "20:14:11:14:11:13"

# Connect to bluetooth
sock_up, data_up = bt.connect(bd_addr_1)
sock_lo, data_lo = bt.connect(bd_addr_2)

# Initialise boolean success criteria
ula_success = False
ulm_success = False
lla_success = False
llm_success = False

ulm_timer = 0 # Used for step change

im1l, im1r, im2l, im2r, im3l, im3r, im4l, im4r = dp.gui_plot() # Open GUI

t0 = time.time() # Start timer
while (elapsed < 30):
	# Read data in - upper leg
	x_rot_up, y_rot_up, z_rot_up, flex_up, success, data_up = bt.get_knee_data(sock_up, data_up)
	if success is True: # If data read in, print out and append to data array
		print("upper", x_rot_up, y_rot_up, z_rot_up, flex_up, elapsed, sep=" ")
		xarray_up.append(x_rot_up)
		yarray_up.append(y_rot_up)
		zarray_up.append(z_rot_up)
		flexarray_up.append(flex_up)
		time_up.append(elapsed)
	# Read data in - lower leg
	x_rot_lo, y_rot_lo, z_rot_lo, flex_lo, success, data_lo = bt.get_knee_data(sock_lo, data_lo)
	if success is True: # If data read in, print out and append to data array
		print("lower", x_rot_lo, x_rot_lo, z_rot_lo, flex_lo, elapsed, sep=" ")
		xarray_lo.append(x_rot_lo)
		yarray_lo.append(y_rot_lo)
		zarray_lo.append(z_rot_lo)
		flexarray_lo.append(flex_lo)
		time_lo.append(elapsed)
	
	elapsed = time.time() - t0 # Update timer
	
	# Bin the entries in the buffer if it gets too long
	data_lines = find_no_lines(data_up)
	if data_lines > 3:
		data_up = ""
		data_lo=""
		
    
	# Make decision about leg above ground
	if yarray_up[-1] > -5:
		ula_success = True # Data variable (continuously updates)
		upper_angle_success = True # Xenplate variable (only need one instance)
		if t0_upper_angle < 0.01:
			t0_upper_angle = time.time() # Reference time for measuring max time leg is above ground
			upper_angle_instances += 1
	else:
		ula_success = False
		upper_angle_time = 0.0
		if t0_upper_angle > 0.01:
			if ((time.time()-t0_upper_angle)>max_upper_angle_time):
				max_upper_angle_time = time.time()-t0_upper_angle
			t0_upper_angle = 0.0
	
	# Make decision about leg straight - compares upper leg angle change with lower leg
	if (np.absolute((yarray_lo[0]-yarray_lo[-1])-(yarray_up[-1]-yarray_up[0])) < 10.0):
		lla_success = True
		straight_angle_success = True # Xenplate variable (only need one instance)
		if t0_straight_angle < 0.01:
			t0_straight_angle = time.time() # Reference time for measuring max time leg is above ground
			straight_angle_instances += 1
	else:
		lla_success = False
		if t0_straight_angle > 0.01:
			if ((time.time()-t0_straight_angle)>max_straight_angle_time):
				max_straight_angle_time = time.time()-t0_straight_angle
			t0_straight_angle = 0.0 # Reset timer
		
	# Make decision about muscle contraction - test for step change (upper)
	if (flexarray_up[-1]-flexarray_up[0]>0.05):
		ulm_success = True
		upper_muscle_success = True # Xenplate variable (only need one instance)
		if t0_upper_muscle < 0.01:
			t0_upper_muscle = time.time() # Reference time for measuring max time leg is above ground
			upper_muscle_instances += 1
	else:
		ulm_success = False
		if t0_upper_muscle > 0.01:
			if ((time.time()-t0_upper_muscle)>max_upper_muscle_time):
				max_upper_muscle_time = time.time()-t0_upper_muscle
			t0_upper_muscle = 0.0 # Reset timer
		
	# Make decision about muscle contraction - test for step change (lower)
	if (flexarray_lo[-1]-flexarray_lo[0]<-0.06):
		llm_success = True
		lower_muscle_success = True # Xenplate variable (only need one instance)
		if t0_lower_muscle < 0.01:
			t0_lower_muscle = time.time() # Reference time for measuring max time leg is above ground
			lower_muscle_instances += 1
	else:
		llm_success = False 
		if t0_lower_muscle > 0.01:
			if ((time.time()-t0_lower_muscle)>max_lower_muscle_time):
				max_lower_muscle_time = time.time()-t0_lower_muscle
			t0_lower_muscle = 0.0 # Reset timer
		
	# Toggle tick/cross images depending on status
	dp.toggle_images(ula_success,lla_success,ulm_success,llm_success, im1l, im1r, im2l, im2r, im3l, im3r, im4l, im4r)


# xarray_up = smoother.smooth(np.array(xarray_up).astype(np.float)) # Function that smooths data
bt.close(sock_up) # Close bluetooth connections
bt.close(sock_lo)


# Plot all data
dp.data_plot(xarray_up, yarray_up, zarray_up, flexarray_up, time_up)
#======================================================================
##all of the top level xenplate functions working (still need to add figures and raw data)
##but should be pretty simple to use, all that is needed is to edit the green numbers and move
#need to connect first because of a bug in the code
session = requests.Session()
file_connect = session.get('https://cued2018.xenplate.com/api/file/connect',
                               headers={'Authorization': 'X-API-KEY: ' + key},
                               cert=(cert_path, key_path)
                              )
print(file_connect.text)

#add stupid '\\' to end of string to get backslash
path = r"fig.jpg"

#print(path + '\\' + file)

with open(path, 'rb') as picture: #have to convert to rb to stream the picture in
    file_create = session.post('https://cued2018.xenplate.com/api/file/create', 
                                data = picture, 
                                headers={'Authorization': 'X-API-KEY: ' + key},
                                cert=(cert_path, key_path)
                               )
    print(file_create.text)

    
#print(upload_files(path, file))

#this is bad code, if more time, use regular expressions
def get_file_id(text):
    #pick out and store the plate_data_id from when we create the plate
    i = 0
    while text[i] != "":
        if i < len(text) - 17: #stops it going to the end to prevent errors
            if text[i:i+10] == '"file_id":':
                idnum = text[i+11:i+51]
        
        else: break

        i = i+1
    
    return idnum

file_id = get_file_id(file_create.text)
lr = xf.LegRaiseSessions(1)

c = [							#these are the green circles
    xf.Calf(lower_muscle_success, math.floor(max_lower_muscle_time*10)/10, lower_muscle_instances), # Yes or no, time, number of attempts
    xf.Thigh(upper_muscle_success, math.floor(max_upper_muscle_time*10)/10, upper_muscle_instances), 
    xf.Straight(straight_angle_success, math.floor(max_straight_angle_time*10)/10, straight_angle_instances),
    xf.Angle(upper_angle_success, math.floor(max_upper_angle_time*10)/10, upper_angle_instances)
]
p = xf.Plate("13", "3a5c9958-dc82-4c74-be84-ded2514fd9d8", "17", c, lr, xf.data_plot(file_id, 'File upload.jpg'))
print(p.to_json_dict())

# Currently leg raise session is set to 1 - this should be altered with a log file

xf.create_plate(p)
#======================================================================
#dp.data_plot(xarray_lo, yarray_lo, zarray_lo, flexarray_lo, time_lo)




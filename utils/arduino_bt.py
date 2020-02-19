# Takes in string of accelerometer values from bluetooth
# Outputs chip orientation

import time
import bluetooth
import math
 
def dist(a,b): # Function to give hypotenuse length
    return math.sqrt((a*a)+(b*b))
 
def get_y_rotation(x,y,z): # Converts x,y,z into y tilt angle
    radians = math.atan2(x,dist(y,z))
    return -math.degrees(radians)
 
def get_x_rotation(x,y,z): # Converts x,y,z into x tilt angle
    radians = math.atan2(y,dist(x,z))
    return math.degrees(radians)	
   
def get_z_rotation(x,y,z):
	radians = math.atan2(z, dist(y, x))
	return math.degrees(radians)
    
def connect(bd_addr): # Set up bluetooth connection
	port = 1
	print("Running")
	print("In-knee-ciating "+bd_addr)
	sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
	sock.connect((bd_addr,port))
	print("Connected")
	data=""
	return sock, data

def close(sock): # Close bluetooth connection
	sock.close()
	
def get_knee_data(sock, data):
	# Uses bluetooth connection to obtain acc and flex data as string, separates into variables
	try:
		x_rotation = 0
		y_rotation = 0
		z_rotation = 0
		flex = 0
		success = False # Variable to be updated depending on if data is successfully read
		data += str(sock.recv(1024), 'utf-8')
		data_end = data.find('\n') # Look for an end line character
		if data_end != -1:
			rec=data[:data_end]
			comma_position = [pos for pos, char in enumerate(rec) if char==',']
			if len(comma_position) == 3: 
				# Separate string into separate variables (look for comma)
				string_x = rec[0:comma_position[0]-1]
				string_y = rec[comma_position[0]+1:comma_position[1]-1]
				string_z = rec[comma_position[1]+1:comma_position[2]-1]		
				string_flex = rec[comma_position[2]+1:]		
				try:
					acc_x = float(string_x)/ 16384.0 # Scale factor
					acc_y = float(string_y)/ 16384.0
					acc_z = float(string_z)/ 16384.0
					flex = float(string_flex)
				
					x_rotation = get_x_rotation(acc_x, acc_y, acc_z)
					y_rotation = get_y_rotation(acc_x, acc_y, acc_z)
					z_rotation = get_z_rotation(acc_x, acc_y, acc_z)
					success = True
				except:
					print('No data this time')
			data = data[data_end+1:]
		else:
			x_rotation = 0
			y_rotation = 0
			z_rotation = 0
			flex = 0
	except:
		x_rotation = 0
		y_rotation = 0
		z_rotation = 0
		flex = 0
	return x_rotation, y_rotation, z_rotation, flex, success, data
	

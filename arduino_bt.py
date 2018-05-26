# Takes in string of accelerometer values from bluetooth
# Outputs chip orientation

import time
import bluetooth
import math
 
def dist(a,b):
    return math.sqrt((a*a)+(b*b))
 
def get_y_rotation(x,y,z):
    radians = math.atan2(x, dist(y,z))
    return -math.degrees(radians)
 
def get_x_rotation(x,y,z):
    radians = math.atan2(y, dist(x,z))
    return math.degrees(radians)	
    
def connect(bd_addr):
	port = 1
	print("Running")
	print("In-knee-ciating")
	sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
	sock.connect((bd_addr,port))
	print("Connected")
	data=""
	return sock

def close(sock):
	sock.close()
	
def get_knee_data(sock):
	# Uses bluetooth connection to obtain acc and flex data as string, separates  	
	try:
		data += str(sock.recv(1024), 'utf-8')
		data_end = data.find('\n')
		if data_end != -1:
			rec=data[:data_end]
			comma_position = [pos for pos, char in enumerate(rec) if char==',']
			if len(comma_position) == 3:
				string_x = rec[0:comma_position[0]-1]
				string_y = rec[comma_position[0]+1:comma_position[1]-1]
				string_z = rec[comma_position[1]+1:comma_position[2]-1]		
				string_flex = rec[comma_position[2]+1:]		
				try:
					acc_x = float(string_x)/ 16384.0
					acc_y = float(string_y)/ 16384.0
					acc_z = float(string_z)/ 16384.0
					flex = float(string_flex)
				
					x_rotation = get_x_rotation(acc_x, acc_y, acc_z)
					y_rotation = get_y_rotation(acc_x, acc_y, acc_z)
					print(str(x_rotation), str(y_rotation), string_flex, sep=" ")
				except:
					print('No data this time')
			data = data[data_end+1:]
	except KeyboardInterrupt:
		print('Keyboard interrupted')
		x_rotation = 0
		y_rotation = 0
		flex = 0
	return (x_rotation, y_rotation, flex)
	

import requests
from datetime import datetime
import time
import json

#codes for convenience
user = "GroupThree"
key = "wRjUm82tln5ZYPpd1tQ3rV0c"
certif = "N3s7i2uYJ0pgAiRxEHv2FNYw"

path = r"/home/pi/GM1_sensors/GM1_physio/Xenplate_permissions/L2S2-2018-CUEDGroup3-20180509"

cert_path = path + ".crt"
key_path = path + ".key.decrypted"

print(datetime.fromtimestamp(1346236702))
s = "01/12/2011"
t_stamp = time.mktime(datetime.strptime(s, "%d/%m/%Y").timetuple()) + 5364662400 #add seconds from 00:00:00 01/01/1800 to epoch (1970)
t_now = datetime.now().timestamp() + 5364662400
print(t_stamp)
print(t_now)   

record_search = requests.post('https://cued2018.xenplate.com/api/record/search',
                        json={"filters": [{
                                        "operator": 2,          #comparison operator. 1 = "=", 2 = "<", 4 = ">". (There is no 3, and 0 is invalid)
                                        "property": "IdNumber", #Inconsistency in code means "records" uses IdNumber, but the others use id_number
                                        "value": 7000000000     #can have a number or a string here
                                        }]
                            },
                        headers={'Authorization': 'X-API-KEY: ' + key},
                        cert=(cert_path, key_path)                          #dont need the certificate password as we have unlocked it
                     )
#attrs = vars(record_search)
#print('\n'.join("%s: %s" % item for item in attrs.items())) 
#print(record_search.text)

#=======================================================================
#=======================================================================
class Plate(object):
    """Class representing a plate record to send"""
    def __init__(self, rec_id, temp_id, version, control_values, leg_raise_sessions, data_plot): #, raw_data
        self.record_id = rec_id
        self.temp_id = temp_id
        self.version = version
        self.control_values = control_values
        self.leg_raise_sessions = leg_raise_sessions
        self.data_plot = data_plot
#        self.raw_data = raw_data

    def to_json_dict(self):
        # append each input to plate_data_create to the control_json string ( .to_json_dict() ) note-this is a dictionary
        control_json = [self.leg_raise_sessions.to_json_dict()]
        for c in self.control_values:
            control_json += c.to_json_list()

        control_json += [self.data_plot.to_json_dict()]
#        control_json += [self.raw_data.to_json_dict()]

        return {
            "data":{
                "record_id": self.record_id,
                "plate_template_id": self.temp_id,
                "plate_template_version": self.version,
                "control_values": control_json
            }
        }


class LegRaiseSessions(object):
    """docstring for LegRaiseSessions"""
    def __init__(self, c):
        self.count = c

    def to_json_dict(self):
        return {
            "id": 4,
            "value": self.count
        }

class Calf(object):
    """control value class"""
    def __init__(self, c, t, a):
        self.complete = c
        self.time = t
        self.attempts = a

    def to_json_list(self):
        return [
            {"id": 9, "value": str(self.complete)},
            {"id": 10,"value": self.time},
            {"id": 22,"value": self.attempts}
        ]
    
class Thigh(object):
    """control value class"""
    def __init__(self, c, t, a):
        self.complete = c
        self.time = t
        self.attempts = a

    def to_json_list(self):
        return [
            {"id": 13, "value": str(self.complete)},
            {"id": 16,"value": self.time},
            {"id": 23,"value": self.attempts}
        ]
    
class Straight(object):
    """control value class"""
    def __init__(self, c, t, a):
        self.complete = c
        self.time = t
        self.attempts = a

    def to_json_list(self):
        return [
            {"id": 14, "value": str(self.complete)},
            {"id": 17,"value": self.time},
            {"id": 24,"value": self.attempts}
        ]

class Angle(object):
    """control value class"""
    def __init__(self, c, t, a):
        self.complete = c
        self.time = t
        self.attempts = a

    def to_json_list(self):
        return [
            {"id": 15, "value": str(self.complete)},
            {"id": 18,"value": self.time},
            {"id": 25,"value": self.attempts}
        ]

class data_plot(object):
    """control value class"""
    def __init__(self, k, n):
        self.key = k
        self.name = n

    def to_json_dict(self):
        return {"attachments":[{"description":"", "key":str(self.key), 
                                "original_file_name":str(self.name), "saved_date_time":int(t_now)}], 
            "id": 29, "value": ""}
    
#class raw_data(object):
#    """control value class"""
#    def __init__(self, k, n):
#        self.key = k
#        self.name = n
#
#    def to_json_dict(self):
#        return {"attachments":[{"description":"", "key":str(self.key), 
#                                "original_file_name":str(self.name), "saved_date_time":t_now}], 
#            "id": 32, "value": ""}




def create_plate(controls):
    plate_data_create = requests.post('https://cued2018.xenplate.com/api/data/create',
                            json=controls.to_json_dict(),
                        headers={'Authorization': 'X-API-KEY: ' + key},
                        cert=(cert_path, key_path)
                     )


#=======================================================================
#=======================================================================
def get_newest_plate_id(recordID = "5"):
	
	plate_data_read_newest = requests.get('https://cued2018.xenplate.com/api/data/list/newest?record_id='+recordID,
		headers={'Authorization': 'X-API-KEY: ' + key},
		cert=(cert_path, key_path)
		)
	
	i = 0
	while plate_data_read_newest.text[i] != "":
		if i < len(plate_data_read_newest.text) - 17:
            
			if plate_data_read_newest.text[i:i+5] == '"id":':
				plt_id =plate_data_read_newest.text[i+5:i+9]
		else: break
		i = i+1
    
	return plt_id #returns a string

#=======================================================================
#=======================================================================
def get_plate_template_id_and_version(recordID = "5", pltID = "1078"):
    #pick out and store the plate_data_id from when we create the plate
	plate_data_read = requests.get('https://cued2018.xenplate.com/api/data/read/id?record_id='+recordID+'&plate_data_id='+pltID, #1078 for knee
		headers={'Authorization': 'X-API-KEY: ' + key},         #1015 for blood sugar
		cert=(cert_path, key_path)
		)

	i = 0
	while plate_data_read.text[i] != "":
		if i < len(plate_data_read.text) - 5: #stops it going to the end to prevent errors
			if plate_data_read.text[i:i+20] == '"plate_template_id":':
				temp_id = plate_data_read.text[i+21:i+57]
                
			if plate_data_read.text[i:i+25] == '"plate_template_version":':
				version_num = plate_data_read.text[i+25:i+27]
		else: break
		i = i+1
    
	return temp_id, version_num


import requests
from datetime import datetime
import time
import json
import sys

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
def create_plate(rec_id = "5", temp_id = "3a5c9958-dc82-4c74-be84-ded2514fd9d8", vers = "15"):
	plate_data_create = requests.post('https://cued2018.xenplate.com/api/data/create',
		json={"data": {
			"record_id": rec_id,
			"plate_template_id": temp_id, #what is a plate template id?
			"plate_template_version": vers,          #keep this as the latest iteration of leg raise template
			#"prior_data_id": "",                  #optional
			#"track_id": "",
			"control_values":                       
						[
							{"id": "4", "value": 10}, #leg raise sessions
                        #first green bubble
							{"id": 9, "value": "True"},  #completed?
							{"id": 10, "value": 17.3}, #best time
							{"id": 22, "value": 12},   #attempts
						#second green bubble
							{"id": 13, "value": "True"},  #completed?
							{"id": 16, "value": 17.3}, #best time
							{"id": 23, "value": 12},   #attempts
						#third green bubble
							{"id": 14, "value": "True"},  #completed?
							{"id": 17, "value": 17.3}, #best time
							{"id": 24, "value": 12},   #attempts
						#fourth green bubble
							{"id": 15, "value": "True"},  #completed?
							{"id": 18, "value": 17.3}, #best time
							{"id": 25, "value": 12},   #attempts
                                            
						#comparison to last session's tasks
							{"id": 28, "value": "10%"},
						#figure and raw data attachment?
						]
					}
				},
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


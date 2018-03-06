# Milling Machine 
# This script create a JSON payload for NGSI using a CSV external data
# Author: Fernando Mendez Requena - fernando.mendez@atos.net
# 

import json
import csv

device_id = 'Sensor_0'
entity_name = 'Milling Machine'
entity_type = 'FirstMachineDevice'


#This section is focused to build a device

SV = 'Transfer_data_MPT_18_Impeller_0001_ref_APS_nok.csv'
path = '/home/osboxes/Desktop/Proyectos/FI-NEXT/FIWARE-Milling-CMM/'

def readFromCSV():

	my_file = os.path.join(path, CSV)

	with open(my_file) as csvfile:
		reader = csv.DictReader(csvfile)
		attributeName = reader.fieldnames
		typeAttributeName = reader.next()
		tamAttributes= len(attributeName)
		ty = "type"
		val = "value"
		device = "devices"
		attributes= "attributes"

		content = {}
		content.update( 
			{ device: {"device_id":device_id}, 
			{"protocol": "GENERIC_PROTO"}, 
			{"entity_name": entity_name},
			{"entity_type": entity_type}, 
			{"transport": "HTTP" }})

		for row in reader:
			for i in range(0,tamAttributes):
				aux_attributeName = attributeName[i]
				aux_typeAttributeName = typeAttributeName[aux_attributeName]
				value = row[attributeName[i]]
				
				content.update({ aux_attributeName: { ty: aux_typeAttributeName, val:value}})
        	output = json.dumps(content, indent=4)		

		return output



def writeDeviceProvisioning():
	data = readFromCSV()
	with open("provisionDevice1.json", "w") as f:
		f.write(data)

if __name__ == "__main__":

	print "It builds a device prosivioning all attributes" 	
	writeDeviceProvisioning()

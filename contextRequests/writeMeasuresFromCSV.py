# Milling Machine 
# This script create a JSON payload for NGSI using a CSV external data
# Author: Fernando Mendez Requena - fernando.mendez@atos.net
# 

import csv
import sys
import json
import os

CSV = 'Transfer_data_MPT_18_Impeller_0001_ref_APS_nok.csv'
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
		content = {}

		for row in reader:
			for i in range(0,tamAttributes):
				aux_attributeName = attributeName[i]
				aux_typeAttributeName = typeAttributeName[aux_attributeName]
				value = row[attributeName[i]]
		
				content.update({ aux_attributeName: { ty: aux_typeAttributeName, val:value}})

        	output = json.dumps(content, indent=4)		

		return output


# It builds a multiple measures JSON file from a CSV" 

def writeMeasures():
	data = readFromCSV()
	with open("multipleMeasures.json", "w") as f:
		f.write(data)

if __name__ == "__main__":

	print "It builds a multiple measures JSON file from a CSV" 	
	writeMeasures()
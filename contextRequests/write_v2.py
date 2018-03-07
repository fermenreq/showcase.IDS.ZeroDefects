# Milling Machine Traductor
# This script create a JSON payload for NGSI using a CSV external data
# Author: Fernando Mendez Requena - fernando.mendez@atos.net
# 

import csv
import sys
import json
import os

#The name of the colum that excel show
nameColum = 'DA'

#Principal CSV that index using "nameColum" to the CSV file that has got all measures
principalIndexCSV='APS_V2_data.csv'

#Secondary CSV: It has got all sensor measures
CSV = 'Transfer_data_MPT_18_Impeller_0001_ref_APS_nok.csv'

#Addres path
path = '/home/osboxes/Desktop/Proyectos/FI-NEXT/FIWARE-Milling-CMM/'


#Translate the name of the colum to a number  
def colToNum():
    expn = 0
    colToNum = 0
    for char in reversed(nameColum):
        colToNum += (ord(char) - ord('A') + 1) * (26 ** expn)
        expn += 1
    return colToNum


def getTypeDataMeasure():

	my_file = os.path.join(path, principalIndexCSV)

	with open(my_file) as csvfile:
		reader = csv.DictReader(csvfile)
		line = reader.next()
		typeData = line['Type']

	return typeData

#It builds a multiple measures JSON file from a CSV" 

def buildMultipleMeasures():

	my_file = os.path.join(path, CSV)
	
	positionAtts = colToNum() - 1
	typeData = getTypeDataMeasure()
	ty = "type"
	val = "value"
	content = {}
	castingValue = ""

	with open(my_file) as csvfile:
		reader = csv.DictReader(csvfile)
		attributeName = reader.fieldnames
		nameField = attributeName[positionAtts]
		
		for row in reader:
			value = row[attributeName[positionAtts]]

			def casting():
				if typeData == "Integer":
					castingValue= int(value)
				
				return castingValue

			castingValue = casting()

			date = row[attributeName[0]]
			time = row[attributeName[1]]

			content.update({ "Date": { ty: "DateTime", val:date+time}})
			content.update({ nameField: {ty: typeData, val: castingValue}})
			
			output = json.dumps(content, indent=4)

		return output


def writeMultipleMeasuresJsonFormat():
	data = buildMultipleMeasures()
	with open("multipleMeasures.json", "w") as f:
		f.write(data)
		
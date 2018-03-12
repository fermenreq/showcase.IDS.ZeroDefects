# Copyright (C) 2018 ATOS

# This file is part of [FIWARE MILLING CMM].

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.##
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# Author: Fernando Mendez Requena - fernando.mendez@atos.net


import csv
import sys
import json
import os
import io
import sys
import ConfigParser
import requests
import string

from urllib2 import Request, urlopen

#Secondary CSV: It has got all sensor measures
#CSV = 'Transfer_data_MPT_18_Impeller_0001_ref_APS_nok.csv'
#Addres path
path = '../FIWARE-Milling-CMM/'
CONFIG_FILE = path + 'config/config.json'
CONFIG_INI = path + 'config/config.ini'

ENTITY_NAME = 'MillingMachine'
#DEVICE_ID = 'Sensor_0'
ENTITY_TYPE = 'FirstMachineDevice'

NUM_ARG=len(sys.argv)

SCRIPT_NAME=sys.argv[0]
DEVICE_ID=sys.argv[1]
FILE_NAME_CSV=sys.argv[2]


if NUM_ARG !=3:
	print 'Usage: '+SCRIPT_NAME+' [DEVICE ID] + [CSV NAME]'

CSV = FILE_NAME_CSV


with open(CONFIG_INI,'r+') as f:
	sample_config = f.read()

config = ConfigParser.RawConfigParser(allow_no_value=True)
config.readfp(io.BytesIO(sample_config))

CONTEXTBROKER_HOST = config.get('ORION','host')
CONTEXTBROKER_PORT = config.get('ORION','port')
#FIWARE_SERVICE = config.get('ORION','fiware_service')
#FIWARE_SERVICEPATH = config.get('ORION','fiware_servicepath')

f.close()

headers = {
  'Content-Type': 'application/json'
}
URL = "http://"+CONTEXTBROKER_HOST+":"+CONTEXTBROKER_PORT+'/v2/entities/?options=keyValues'


def readConfigFile():
	config = []
	data = json.load(open(CONFIG_FILE))
		
	for i in data["config"]:
		#dic.update({ i["colunm_name"].encode("ascii","replace"): i["type"].encode("ascii","replace")})
		config.append(i);

	return config


def attributeNameType():
	
	data = json.load(open(CONFIG_FILE))
	
	lista = []

	for i in data["config"]:
		lista.append({"name": i["attribute_name"].encode("ascii","replace"), "type": i["type"].encode("ascii","replace")})
		
	return lista


def colToNum():
    d = readConfigFile()
    lista = []
    for i in d.keys():
	    number = translateColToNum(i)
	    lista.append(number)

    return lista

#def translateColToNum(col):
#	expn = 0
#	colToNum = 0
#	nameColum=col
#	for char in reversed(nameColum):
#		colToNum += (ord(char) - ord('A') + 1) * (26 ** expn)
#		expn += 1
#	return colToNum


#def translateColToNum(col):
#    num = 0
#    for c in col:
#        if c in string.ascii_letters:
#            num = num * 26 + (ord(c.upper()) - ord('A')) + 1
#    return num

def casting(value, typeData):
	if typeData == "Integer":
		castingValue= int(value)
	if typeData == "Float":
		castingValue = float(value)
	if typeData == "Long":
		castingValue = long(value)
		
	return castingValue

def sendMeasures():
	my_file = os.path.join(path, CSV)
	configTranslate = readConfigFile()
	ty = "type"
	val = "value"
	content = {}
	i = 0
	with open(my_file) as csvfile:
		reader = csv.DictReader(csvfile, delimiter=';', quoting=csv.QUOTE_NONE)
		attributeName = reader.fieldnames
		for row in reader:
			date = row[attributeName[0]]
			time = row[attributeName[1]]
					
				#content = { "Date" :  {ty : "DateTime", val:date+time } ,
				#		  nameField: {ty: types, val: cast}}
				
			#content["timeStamp"] = {ty : "DateTime", val:date } #conver also time
			content["currentPart"] = CSV
			for j in configTranslate:
				value = row[j.get("colunm_name")]
				types = j.get("type")
                        	cast = casting(value, types)

				i=i+1
				content[j.get("attribute_name")] = { ty: types, val: cast} 
			output = json.dumps(content, indent=4)
			
			print output

			#requests.post(URL,data=output, headers=HEADERS)
			i=0
			print "======================="
						
def createEntity():
	content = {}
	content["type"] = ENTITY_TYPE 
	content["id"]= ENTITY_NAME				
	content["currentPart"] = CSV.split('/')[1].split('.')[0]
		
	my_file = os.path.join(path, CSV)
	configTranslate = readConfigFile()
	ty = "type"
	val = "value"
	

	with open(my_file) as csvfile:
		reader = csv.DictReader(csvfile, delimiter=';', quoting=csv.QUOTE_NONE)
		attributeName = reader.fieldnames
		
		for j in configTranslate:
			
			attributeName = j.get("attribute_name")
			content[attributeName] = { ty: "default", val: "0"}
		
		output = json.dumps(content, indent=4)
	
	return output
			

if __name__ == "__main__":
	payload = createEntity()
	print payload
	r = requests.post(URL, data = payload, headers=headers)
	print str(r.status_code)
	print str(r.text)

	#sendMeasures()

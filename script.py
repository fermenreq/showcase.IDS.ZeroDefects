#!/usr/bin/python

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
import os

from urllib2 import Request, urlopen
import urlparse
from datetime import datetime


#Addres path
CONFIG_FILE =  './config/config.json'


ENTITY_NAME = 'MillingMachine005'
ENTITY_TYPE = 'Machine'
ENTITY_CATEGORY = 'millingMachine'

NUM_ARG=len(sys.argv)

SCRIPT_NAME=sys.argv[0]
FILE_NAME_CSV= sys.argv[1]

if NUM_ARG !=2:
	print 'Usage: ' + SCRIPT_NAME + '[CSV NAME]'
 
CSV = FILE_NAME_CSV



headers = {
  'Content-Type': 'application/json'
}

if (('ORION_URL' in os.environ) and (os.environ['ORION_URL'] is not None)):
	URL = os.environ['ORION_URL']
else:
	URL = "http://localhost:1026"



def readConfigFile():
	config = []
	data = json.load(open(CONFIG_FILE))
		
	for i in data["config"]:
		#dic.update({ i["colunm_name"].encode("ascii","replace"): i["type"].encode("ascii","replace")})
		config.append({"colunm_name": i["colunm_name"].encode("ascii","replace"),
			"type": i["type"].encode("ascii","replace"),
			"attribute_name": i["attribute_name"].encode("ascii","replace")});
	return config


def attributeNameType():
	
	data = json.load(open(CONFIG_FILE))
	
	lista = []

	for i in data["config"]:
		lista.append({"name": i["attribute_name"].encode("ascii","replace"), "type": i["type"].encode("ascii","replace")})
		
	return lista


def casting(value, typeData):
	if typeData == "Integer":
		castingValue= int(value)
	if typeData == "Float":
		castingValue = float(value)
	if typeData == "Long":
		castingValue = long(value)
		
	return castingValue

def sendMeasures():
	my_file = os.path.join('./', CSV)
	configTranslate = readConfigFile()

	parts = urlparse.urlparse(URL)
	parts = parts._replace(path="v2/entities/"+ENTITY_NAME+"/attrs/?options=keyValues")
	final = parts.geturl()

	ty = "Type"
	val = "Value"
	content = {}
	i = 0
	with open(my_file) as csvfile:
		reader = csv.DictReader(csvfile, delimiter=';', quoting=csv.QUOTE_NONE)
		attributeName = reader.fieldnames
		for row in reader:
			date = row[attributeName[0]]
			time = row[attributeName[1]]

			d = datetime.strptime(date,'%d-%b-%Y')
			newDate = d.strftime('%Y-%m-%d')
			

			hour= int(time.split(':')[0])
			minute=int(time.split(':')[1])
			seconds=float(time.split(':')[2])

			
			string_date = str(newDate+time)
			aux = str(datetime.strptime(string_date, "%Y-%m-%d%H:%M:%S.%f"))

			#import pyt
			#timezone= pytz.timezone('Europe/Madrid')

			#prueba = datetime(2018,5,15,11,58,25,02, tzinfo=pytz.utc)

			new_date=str(aux.split(" ")[0])

			new_year = str(new_date.split("-")[0])
			new_month = str(new_date.split("-")[1])
			new_day = str(new_date.split("-")[2])
			aux_new_date=new_year+"-"+new_month+"-"+new_day+"T"
			
	
			new_time=str(aux.split(" ")[1])

			new_hours = str(new_time.split(":")[0])
			new_minutes=str(new_time.split(":")[1])
			new_seconds=str(new_time.split(":")[2])		
			aux_new_time= new_hours+":"+new_minutes+":"+new_seconds+"Z"

			timestamp = str(aux_new_date+aux_new_time)

			
			# import dateutil.parser

			# aux =  dateutil.parser.parser(aux)

			# print datetime.

			content["TimeInstant"] = {ty: "ISO8601", val: timestamp}
			content["currentPart"] = {ty: "text", val: CSV}

			for j in configTranslate:

				value = row[j.get("colunm_name")]
				types = j.get("type")
                        	cast = casting(value, types)

				if value !="":
					content[j.get("attribute_name")]  = { ty: types, val: cast} 
			
			output = json.dumps(content )
			r = requests.post(final,data=output, headers=headers)
				
		        print str(r.status_code)
			print str(r.text)
			i=0
			


						
def createEntity():
	content = { 'type': ENTITY_TYPE, 'id': ENTITY_NAME} #, 'category': ENTITY_CATEGORY}
	
	#content["type"] = ENTITY_TYPE 
	#content["id"]= ENTITY_NAME				
	#content["category"] = "ENTITY_CATEGORY"	

	my_file = os.path.join('./', CSV)
	configTranslate = readConfigFile()
	ty = "type"
	val = "value"
	with open(my_file) as csvfile:
		reader = csv.DictReader(csvfile, delimiter=';', quoting=csv.QUOTE_NONE)
		attributeName = reader.fieldnames

		for j in configTranslate:
			value = 0
			types = j.get("type")
                       	cast = casting(value, types)

			attributeName = j.get("attribute_name")
			content[attributeName] = { ty: types, val: value}
		
		output = json.dumps(content,  encoding='ascii', ensure_ascii=True, indent=4)
	
	return output
			

if __name__ == "__main__":

	payloadEntity = createEntity()
	
	parts = urlparse.urlparse(URL)
	parts = parts._replace(path="/v2/entities/?options=keyValues")
	new_url = parts.geturl()

	r = requests.post(new_url, data = payloadEntity, headers=headers)
	if ((r.status_code == 201) or (r.status_code == 422)):
	 	print "Initial entity created"
		
		sendMeasures()
	else:
		print "unexpected errror"
		print r.text


	



	

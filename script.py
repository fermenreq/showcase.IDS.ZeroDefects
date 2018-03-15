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
import time


CONFIG_FILE =  './config/config.json'
ENTITY_NAME = 'MillingMachine005'
ENTITY_TYPE = 'Machine'
ENTITY_CATEGORY = 'millingMachine'


SCRIPT_NAME = sys.argv[0]
FILE_NAME_CSV = sys.argv[1]

NUM_ARG=len(sys.argv)

if NUM_ARG < 2:
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

def totalRowsCSV():
	my_file = os.path.join('./', CSV)
	
	with open(my_file) as csvfile:
		reader = csv.DictReader(csvfile, delimiter=';', quoting=csv.QUOTE_NONE)
		attributeName = reader.fieldnames		
		rows = list(reader)
		totalrows= len(rows)
	return totalrows

def sendMeasuresSimulator():
	my_file = os.path.join('./', CSV)
	configTranslate = readConfigFile()

	parts = urlparse.urlparse(URL)
	parts = parts._replace(path="v2/entities/"+ENTITY_NAME+"/attrs/?options=keyValues")
	final = parts.geturl()

	ty = "type"
	val = "value"
	content = {}
	i = 0
	seconds_viejos= 0.00
	delay = 0.00
	seconds1 = float(0.00)

	with open(my_file) as csvfile:
		reader = csv.DictReader(csvfile, delimiter=';', quoting=csv.QUOTE_NONE)
		attributeName = reader.fieldnames		
		total = totalRowsCSV()
			
		for row in reader:
			i = i +1
			date = row[attributeName[0]]
			times = row[attributeName[1]]

			d = datetime.strptime(date,'%d-%b-%Y')
			newDate = d.strftime('%Y-%m-%d')
			hour= int(times.split(':')[0])
			minute=int(times.split(':')[1])
			seconds=float(times.split(':')[2])

			string_date = str(newDate+times)
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
			
			t = seconds - seconds_viejos

			seconds_viejos = float(seconds)
			minutes_viejos = float(minute)

			# if seconds_viejos <= 0:
			# 	seconds_viejos * -1

			if t <= 0:
				t = (minute * 60) + seconds - (minutes_viejos * 60) + seconds_viejos						
			
			#print "minutes + seconds parte negativa: ", t
			#print "delay", t
		
			print "Sending measure number: ", i
			print "Time delay used: "+str(t)+" seconds"

			time.sleep(t)

			r = requests.post(final,data=output, headers=headers)
				
		        print "Response: " + str(r.status_code)
			#print str(r.text)
			print "--------------------------------------"
			print 

			if i == total:
				print "Finished the manufacture of the piece: ", CSV

def sendMeasures():
	my_file = os.path.join('./', CSV)
	configTranslate = readConfigFile()

	parts = urlparse.urlparse(URL)
	parts = parts._replace(path="v2/entities/"+ENTITY_NAME+"/attrs/?options=keyValues")
	final = parts.geturl()

	ty = "type"
	val = "value"
	content = {}
	i = 0
	seconds_viejos= 0.00
	delay = 0.00
	seconds1 = float(0.00)

	with open(my_file) as csvfile:
		reader = csv.DictReader(csvfile, delimiter=';', quoting=csv.QUOTE_NONE)
		attributeName = reader.fieldnames		
		total = totalRowsCSV()
			
		for row in reader:
			i = i +1
			date = row[attributeName[0]]
			times = row[attributeName[1]]

			d = datetime.strptime(date,'%d-%b-%Y')
			newDate = d.strftime('%Y-%m-%d')
			hour= int(times.split(':')[0])
			minute=int(times.split(':')[1])
			seconds=float(times.split(':')[2])

			string_date = str(newDate+times)
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
			
			output = json.dumps(content)
			print "Sending measure number: ", i
			r = requests.post(final,data=output, headers=headers)
				
		        print "Response: " + str(r.status_code)
			#print str(r.text)
			print "--------------------------------------"
			print 
			
						
def createEntity():
	content = { 'type': ENTITY_TYPE, 'id': ENTITY_NAME }
	
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

	 	if NUM_ARG == 3 and sys.argv[2] == "enable-time-simulator":
	 		print "Initial entity created"
	 		print
	 		sendMeasuresSimulator()

		if NUM_ARG == 2:
			print "Initial entity created"
	 		print
			sendMeasures()
		
		else:
			print 'You can use the following commands: '
			print
			print '1. Using script without simulator time: ' + SCRIPT_NAME + ' [CSV NAME]'
			print
			print '2. Using script with a simulator time: ' + SCRIPT_NAME + ' [CSV NAME] ' + 'enable-time-simulator'

	else:
		print "unexpected errror"
		print r.text


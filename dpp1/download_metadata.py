#!/usr/bin/env python

import os
from Bio import Entrez
from Bio import GenBank

Entrez.email = 'andrea.silverj@gmail.com'

idname=os.environ["nameSEQ"]

handle = Entrez.efetch(db="nucleotide", id=idname, rettype="gb", retmode="text")

def format_date(date):
	replaced_date=date.replace("Jan", "01").replace("Feb", "02").replace("Mar", "03").replace("Apr", "04").replace("May", "05").replace("Jun", "06").replace("Jul", "07").replace("Aug", "08").replace("Sep", "09").replace("Oct", "10").replace("Nov", "11").replace("Dec", "12")
	return replaced_date

try:
	for record in GenBank.parse(handle):

		feature=record.features[0]

		check_date_location=[]
		date=[]
		location=[]

		for qualifier in feature.qualifiers:

			if qualifier.key=="/country=":
				if qualifier.value!=None:
					check_date_location+=["location_present"]
					location+=[qualifier.value.strip('"')]

			if qualifier.key=="/collection_date=":
				if qualifier.value!=None:
					check_date_location+=["date_present"]
					date+=[qualifier.value.strip('"')]

		if len(check_date_location)==2:

			mydate=str(date[0]).split("-")
			mydatelen=len(mydate)

			mynewdate1=[]
			mynewdate2=[]
			mynewdate3=[]

			if mydatelen==1:
				mynewdate1+=[mydate[0]]

			elif mydatelen==2:
				mynewdate2+=[mydate[1]]
				mynewdate2+=[format_date(mydate[0])]

			elif mydatelen==3:
				mynewdate3+=[mydate[2]]
				mynewdate3+=[format_date(mydate[1])]
				mynewdate3+=[format_date(mydate[0])]
			else:
				pass

			date_lists=[mynewdate1,mynewdate2,mynewdate3]
			formatted_date=[x for x in date_lists if x][0]

			if len(formatted_date)==1:

				print(str(record.version)+"\t"+str(location[0].split(":")[0])+"\t"+str(formatted_date[0]))

			elif len(formatted_date)==2:
				print(str(record.version)+"\t"+str(location[0].split(":")[0])+"\t"+str(formatted_date[0])+"-"+str(formatted_date[1]))

			elif len(formatted_date)==3:
				print(str(record.version)+"\t"+str(location[0].split(":")[0])+"\t"+str(formatted_date[0])+"-"+str(formatted_date[1])+"-"+str(formatted_date[2]))

	handle.close()

except Exception:
        print(str(idname)+"\tFAILED")

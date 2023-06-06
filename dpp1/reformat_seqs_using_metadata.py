#!/usr/bin/env python
import sys
import csv
import re
from Bio import SeqIO

args=sys.argv

fasta_file=args[1]
NCBI_Virus_metadata=args[2]

NCBI_Virus_metadata_list=[]
with open(NCBI_Virus_metadata, 'r') as f:
	read_header= csv.reader(f, delimiter='\t')
	list_header = next(read_header) # Store header in a list
	tab_metadata = csv.reader(f,delimiter='\t') # Read text file as tsv
	for row in tab_metadata:
		NCBI_Virus_metadata_list.append(row) # Add the data from the text file to the list

#####################
##### Functions #####
def check_fields(field_name,header):
	if field in header:
		return header.index(field)

def turn_to_beast_date(date):
# Format the dates for BEAST and BEAST2	
	if date != "":
		if re.findall(r'(\d+-\d+-\d+)',date):
			return [date.replace("-", "/").replace("/XX/","/08/").replace("/XX","/31")]
		elif re.findall(r'(\d+-\d+)',date): # Place the date in the half of the month if it is uncertain 
			return [str(date.replace("-", "/"))+"/15"]	
		elif re.findall(r'(\d+)',date): # Place the date in the half of the year if it is uncertain
			return [str(date)+"/08/31"]
	else:
		return ["NO_DATE"]

def select_only_country(location):
# Select only the country from the location field	
	if location != "":
		return [list(str([location.replace(" ","_").replace(":","_").replace(",","_")]).split("__"))[0].replace("[","").replace("]","").replace("'","")]
	else:
		return ["NO_LOCATION"]

##############################################################################################
##### Create a 'Id':'formatted_information' dictionary starting from NCBI virus metadata #####
fields_of_interest={'Accession':None,'Country':None,'Host':None,'Collection_Date':None}
for field in fields_of_interest.keys():
	fields_of_interest[field]=check_fields(field,list_header)

record_ids=[]
record_location=[]
record_date=[]

for record in NCBI_Virus_metadata_list:
	record_ids+=[record[fields_of_interest.get('Accession')]]
	record_location+=[record[fields_of_interest.get('Country')]]
	record_date+=[record[fields_of_interest.get('Collection_Date')]]

record_location_formatted=[]
for location in record_location:
	record_location_formatted+=select_only_country(location)

record_date_beast=[]
for date in record_date:
	record_date_beast+=turn_to_beast_date(str(date))


information_meta=[m+"|"+str(n) for m,n in zip(record_location_formatted,record_date_beast)]
metadata_dict=dict(zip(record_ids,information_meta))

################################################################################################################
##### Create a single line FASTA file with formatted ids incorporating part of the NCBI virus metadata #####
for rec in SeqIO.parse(fasta_file, "fasta"):
	for key,value in metadata_dict.items():
		if rec.id == key:
			print(">"+rec.id+"|"+value+"\n"+str(rec.seq))



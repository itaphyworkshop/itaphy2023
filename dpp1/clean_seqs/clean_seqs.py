#!/usr/bin/env python

__author__ = 'Andrea Silverj'
__version__='0.9_beta'
__date__='27 March 2022'


import argparse,sys,os
import re
from Bio import SeqIO

arguments=sys.argv
help_keys=['-h', '--help']


#############
#####CLI#####
if len(arguments) > 1:
	if any(hlp in arguments for hlp in help_keys):
		print("###############################################################################\n##############################--|clean_seqs.py|--##############################\n")
	else:
		pass

parser=argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter, description="Hello dear User, and welcome to 'clean_seqs.py'!\nThis program filters sequences according to the selected parameters.\nEnjoy!\n\n###############################################################################")

parser.add_argument("-f", help="File in FASTA format", metavar='fasta_file', required=False)
parser.add_argument("-gapN", action='store_true', help="Convert N characters in gaps", required=False)
parser.add_argument("-maxl", help="Filter sequences >= a specified threshold length", metavar='max_length', required=False)
parser.add_argument("-minl", help="Filter sequences <= a specified threshold length", metavar='min_length', required=False)
parser.add_argument("-gp", help="Filter sequences >= a specified percentage of gaps", metavar="0-100", required=False)
parser.add_argument("-np", help="Filter sequences >= a specified percentage of N characters", metavar="0-100", required=False)
parser.add_argument("-std_characters", action='store_true', help="Replace all unusual characters with N", required=False)
parser.add_argument("-v", action='store_true', help="Print the version of the program", required=False)
parser.add_argument("-credits", action='store_true', help="Print credits of the program", required=False)

args=parser.parse_args()
arg_parsed=vars(args)

fasta_file=arg_parsed.get("f")
maxlength_threshold=arg_parsed.get("maxl")
minlength_threshold=arg_parsed.get("minl")
percGaps=arg_parsed.get("gp")
percNchar=arg_parsed.get("np")

gapN_option=arg_parsed.get("gapN")
std_characters_option=arg_parsed.get("std_characters")
ref_option=arg_parsed.get("v")
credits_option=arg_parsed.get("credits")

if fasta_file==None and maxlength_threshold==None and minlength_threshold==None and gapN_option == False and percGaps==None and percNchar==None and std_characters_option == False and ref_option==False and credits_option==False:
	print("Hello User! Type 'clean_seqs.py -h' or 'clean_seqs.py --help' to see how to use this program.")
else:
	pass	

if credits_option is True and ref_option==False and fasta_file == None and maxlength_threshold == None and minlength_threshold == None and gapN_option == False and percGaps==None and percNchar==None and std_characters_option == False:
	print("Author: Andrea Silverj, MSc in Evolutionary Biology\nPosition: PhD student\nInstitution: University of Trento, Italy\nDepartment: FEM-C3A, Rota-Stabelli Lab | CIBIO CM, Segata Lab\nContacts: andrea.silverj@unitn.it")
else:
	pass	

if ref_option is True and credits_option==False and fasta_file == None and maxlength_threshold == None and minlength_threshold == None and gapN_option == False and percGaps==None and percNchar==None and std_characters_option == False:
	print("Version: 0.9 Beta\nYear: 2021")
else:
	pass	


#####################
##### Functions #####
def retain_only_ACTGUN_characters(sequence):
	sequence_str=str(sequence)
	sequence_str_upper=sequence_str.upper()
	standard_characters="ACTGUN"
	if "T" and "U" in sequence_str_upper:
		return "mixedTU"
	else:
		for c in sequence_str_upper:
			if c not in standard_characters:
				sequence_str_upper=sequence_str_upper.replace(c, "N")
			else:
				pass
		return sequence_str_upper


def calculate_percent_gaps(sequence):
	seqlength=len(sequence)
	GapsCounts=sequence.upper().count("-")
	GapsPercentage=round((GapsCounts/seqlength)*100, 3)
	return GapsPercentage


def calculate_percent_n(sequence):
	seqlength=len(sequence)
	Ncounts=sequence.upper().count("N")
	Npercentage=round((Ncounts/seqlength)*100, 3)
	return Npercentage


def gap_ns(sequence):
	gapped_seq=str(sequence).upper().replace("N","-")
	return gapped_seq


def length_filter(sequence):
	if sequence != None:		
		if maxlength_threshold != None and minlength_threshold == None and len(sequence) <= int(maxlength_threshold):
			return "max"
		elif maxlength_threshold == None and minlength_threshold != None and len(sequence) >= int(minlength_threshold):
			return "min"
		elif maxlength_threshold != None and minlength_threshold != None and len(sequence) <= int(maxlength_threshold) and len(sequence) >= int(minlength_threshold):
			return "maxmin"
	else:
		pass


##################################
##### Filtering combinations #####
if credits_option==False and ref_option==False:
	
	if fasta_file == None:
		if maxlength_threshold != None or minlength_threshold != None or gapN_option != False or percGaps!=None or percNchar!=None or std_characters_option != False:
			print("Please, select a fasta file.\nFor further information: 'python clean_seqs.py --help'")
	
	else:
		if gapN_option == True or std_characters_option == True:
			if maxlength_threshold != None or minlength_threshold != None or percGaps!=None or percNchar!=None or gapN_option == std_characters_option:
				print("The options '-gapN' and '-std_characters' can\'t be combined together or with other options.")
	
			else:
				if gapN_option == True:
					for rec in SeqIO.parse(fasta_file, "fasta"):
							print(">"+str(rec.id)+"\n"+gap_ns(rec.seq))

				elif std_characters_option == True:
					for rec in SeqIO.parse(fasta_file, "fasta"):
						if str(retain_only_ACTGUN_characters(rec.seq)) == "mixedTU":
							exit("The sequence named "+"'"+str(rec.id)+"'"+" has a mix of T and U characters. Please, check your sequences and re-run the program.")
						else:
							print(">"+str(rec.id)+"\n"+str(retain_only_ACTGUN_characters(rec.seq)))
		else:
			if maxlength_threshold == None and minlength_threshold == None and gapN_option == False and percGaps==None and percNchar==None and credits_option==False and ref_option==False and std_characters_option == False:
				print("Please, select at least one filtering option.\nFor further information: 'python clean_seqs.py --help'")

			elif maxlength_threshold != None or minlength_threshold != None and percGaps==None and percNchar == None and gapN_option == False and std_characters_option == False:
				for rec in SeqIO.parse(fasta_file, "fasta"):
					if length_filter(rec.seq) == "max":
						print(">"+rec.id+"\n"+str(rec.seq))
					elif length_filter(rec.seq) == "min":
						print(">"+rec.id+"\n"+str(rec.seq))
					elif length_filter(rec.seq) == "maxmin":
						print(">"+rec.id+"\n"+str(rec.seq))

			elif maxlength_threshold == None and minlength_threshold == None and percGaps!=None and percNchar == None and gapN_option == False and std_characters_option == False:
				for rec in SeqIO.parse(fasta_file, "fasta"):
					if calculate_percent_gaps(rec.seq) <= float(percGaps):
						print(">"+rec.id+"\n"+str(rec.seq))

			elif maxlength_threshold == None and minlength_threshold == None and percGaps==None and percNchar != None and gapN_option == False and std_characters_option == False:
				for rec in SeqIO.parse(fasta_file, "fasta"):
					if calculate_percent_n(rec.seq) <= float(percNchar):
						print(">"+rec.id+"\n"+str(rec.seq))

			elif maxlength_threshold != None or minlength_threshold != None and percGaps!=None and percNchar == None and gapN_option == False and std_characters_option == False:
				for rec in SeqIO.parse(fasta_file, "fasta"):
					if calculate_percent_gaps(rec.seq) <= float(percGaps):
						if length_filter(rec.seq) == "max": 
							print(">"+rec.id+"\n"+str(rec.seq))
						elif length_filter(rec.seq) == "min":
							print(">"+rec.id+"\n"+str(rec.seq))
						elif length_filter(rec.seq) == "maxmin":
							print(">"+rec.id+"\n"+str(rec.seq))					

			elif maxlength_threshold != None or minlength_threshold != None and percGaps==None and percNchar != None and gapN_option == False and std_characters_option == False:
				for rec in SeqIO.parse(fasta_file, "fasta"):
					if calculate_percent_n(rec.seq) <= float(percNchar):
						if length_filter(rec.seq) == "max":
							print(">"+rec.id+"\n"+str(rec.seq))
						elif length_filter(rec.seq) == "min":
							print(">"+rec.id+"\n"+str(rec.seq))
						elif length_filter(rec.seq) == "maxmin":
							print(">"+rec.id+"\n"+str(rec.seq))											

			elif maxlength_threshold != None or minlength_threshold != None and percGaps!=None and percNchar != None and gapN_option == False and std_characters_option == False:
				for rec in SeqIO.parse(fasta_file, "fasta"):
					if calculate_percent_gaps(rec.seq) <= float(percGaps) and calculate_percent_n(rec.seq) <= float(percNchar):
						if length_filter(rec.seq) == "min":
							print(">"+rec.id+"\n"+str(rec.seq))
						elif length_filter(rec.seq) == "max":
							print(">"+rec.id+"\n"+str(rec.seq))
						elif length_filter(rec.seq) == "maxmin":
							print(">"+rec.id+"\n"+str(rec.seq))

			elif maxlength_threshold == None and minlength_threshold == None and percGaps!=None and percNchar != None and gapN_option == False and std_characters_option == False:
				for rec in SeqIO.parse(fasta_file, "fasta"):
					if calculate_percent_gaps(rec.seq) <= float(percGaps) and calculate_percent_n(rec.seq) <= float(percNchar):
						print(">"+rec.id+"\n"+str(rec.seq))			
else:
	if len(arguments) > 2 :
		print("Type 'python clean_seqs.py -credits' or 'python clean_seqs.py -v' if you want to print the credits or the version of the program, respectively.")

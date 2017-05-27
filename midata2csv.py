#!/usr/bin/env python
# (C) 2017 Joel Schneider. All rights reserved
# See LICENSE for licensing information

import csv, sys, datetime

#MIDATA format (, separator):
#Transaction Date,Transaction Type,Merchant/Description,Debit/Credit,Balance
#1		  2		   3			4	     5
#Homebank CSV format (; separator):
#date;	  payment;	info;	payee;	amount;	category;	tags
#DD-MM-YY
#1*	  2*		3#	3#	4	2/3/4#		2/3/4#
#* = format needs changed
## = can extract from

# GLOBAL VARIABLES:
inrows = []
outrows = []

# FUNCTIONS:
def usage():
	print "Usage:\t", sys.argv[0], "[-b] <input.csv> <output.csv>"
	print "\t-b\tUse initial balance as transfer"
	print "\tinput.csv\tMiData formatted file"
	print "\toutput.csv\tHomebank CSV formatted file"

def open_file(infile, outfile):
	#try:
	midata_file = infile
	csv_file = outfile
	#except:
	#	usage()
	#	sys.exit(3)
	try:
		with open(midata_file, 'rb') as input_file:
			dialect = csv.Sniffer().sniff(input_file.read(1024))
			input_file.seek(0)
			reader = csv.reader(input_file, dialect)
			for row in reader:
				inrows.append(row)
	except:
		print "Can't open \'", midata_file, "\'!"
		usage()
		sys.exit(4)

# SANITY CHECK:
if len(sys.argv) < 3:
	usage()
	sys.exit(1)

if (sys.argv[1] == "-b"):
	get_initial_balance = True
	if len(sys.argv) < 4:
		usage()
		sys.exit(1)
	open_file(sys.argv[2], sys.argv[3])
	csv_file =  sys.argv[3]
else:
	get_initial_balance = False
	open_file(sys.argv[1], sys.argv[2])
	csv_file =  sys.argv[2]

def get_transaction_code(incode):
	if incode == "CREDITCARD":	# ? == 1 == credit card TODO
		transaction_type = 1
	elif incode == "CHQ":		# CHQ == 2 == cheque
		transaction_type = 2
	elif incode == "CPT":		# CPT == 3 == cash
		transaction_type = 3
	elif incode == "TFR?":		# ? == 4 == transfer
		transaction_type = 4	# semi-broken on import :(
	elif incode == "TFR":		# TFR == 5 == internal transfer
		transaction_type = 4	# semi-broken on import :(
	#elif incode == "TFR":		# TFR broken on import so import as 0
	#	transaction_type = 0	# FIXME manually 
	elif incode == "BGC":		# BGC == 8 == electronic payment
		transaction_type = 8
	elif incode == "DD":		# DD == 11 == direct debit
		transaction_type = 11
	elif incode == "DEB":		# DEB == 6 == debit card
		transaction_type = 6
	else:
		transaction_type = 0
	return transaction_type
	
def get_category_and_tags(transaction_title):
	category = "undefined"
	tags = ""
	if transaction_title[:4] == "LNK ":
		category = "cash machine"
	if transaction_title == "":
		if amount == "+5.00":	# Guess
			category = "cashback"
			#print row[3]
			#sys.exit(2)
		elif amount == "+3.00":	# Guess
			#print row[3]
			category = "cashback"
		else:	# Guess
			category = "unknown"
	if transaction_title[:4] == "WWW.":
		category = "online purchase"
		tags = tags + "online "
	if transaction_title[:6] == "CALMAC":
		category = "travel"
		tags = tags + "CalMac "
	if transaction_title[:3] == "SKY":
		category = "communication"
		tags = tags + "Sky "
	if transaction_title[:8] == "TALKTALK":
		category = "communication"
		tags = tags + "Talktalk "
	if transaction_title[:10] == "WWW.CALMAC":
		category = "travel"
		tags = tags + "CalMac "
	if transaction_title[:5] == "COSTA":
		category = "food"
		tags = tags + "Costa "
	if transaction_title[:17] == "WELCOME BREAK KFC":
		category = "food"
		tags = tags + "KFC "
	if transaction_title[:18] == "MDN WEL/CB/WAITROS":
		category = "food"
		tags = tags + "Waitrose "
	if transaction_title[:9] == "MCDONALDS":
		category = "food"
		tags = tags + "McDonalds "
	if transaction_title[:17] == "BRITISH SCHOOL OF":
		category = "car"
		tags = tags + "BSM "
	if transaction_title[:17] == "ARNOLD CLARK AUTO":
		category = "car"
		tags = tags + "Arnold Clark "
	if transaction_title[:13] == "AA MEMBERSHIP":
		category = "car"
		tags = tags + "AA membership "
	if transaction_title[:11] == "POST OFFICE":
		category = "postage"
		tags = tags + "Post Office "
	if transaction_title[:8] == "HOMEBASE":
		category = "home"
		tags = tags + "Homebase "
	if transaction_title[:8] == "WH SMITH":
		category = "shopping"
		tags = tags + "WH Smith "
	if transaction_title[:9] == "POUNDLAND":
		category = "shopping"
		tags = tags + "Poundland "
	if transaction_title[:8] == "LAKELAND":
		category = "kitchen"
		tags = tags + "Lakeland "
	if transaction_title[:8] == "PC WORLD":
		category = "IT"
		tags = tags + "PC World "
	if transaction_title[:8] == "T K MAXX":
		category = "clothes"
		tags = tags + "TK Maxx "
	if transaction_title[:15] == "THE CLARKS SHOP":
		category = "clothes"
		tags = tags + "Clarks "
	if transaction_title[:13] == "MARKS&SPENCER":
		category = "clothes"
		tags = tags + "M&S "
	if transaction_title[:4] == "ASDA":
		category = "supermarket"
		tags = tags + "Asda "
	elif transaction_title[:4] == "LIDL":
		category = "supermarket"
		tags = tags + "Lidl "
	elif transaction_title[:4] == "ALDI":
		category = "supermarket"
		tags = tags + "Aldi "
	elif transaction_title[:5] == "TESCO":
		category = "supermarket"
		tags = tags + "Tesco "
	elif transaction_title[:10] == "SAINSBURYS":
		category = "supermarket"
		tags = tags + "Sainsburys "
	elif transaction_title[:11] == "W M MORRISO":
		category = "supermarket"
		tags = tags + "Morrisons "
	elif transaction_title[:11] == "WM MORRISON":
		category = "supermarket"
		tags = tags + "Morrisons "
	elif transaction_title[:5] == "CO-OP":
		category = "supermarket"
		tags = tags + "Co-Op "
	elif transaction_title[:5] == "SHELL":
		category = "petrol station"
		tags = tags + "Shell "
	elif transaction_title[:4] == "ESSO":
		category = "petrol station"
		tags = tags + "Esso "
	elif transaction_title[:9] == "KEELE SOU":
		category = "petrol station"
		tags = tags + "Keele station "
	elif transaction_title[:6] == "Q PARK":
		category = "parking"
		tags = tags + "Qpark "
	elif transaction_title[:8] == "SCOTRAIL":
		category = "travel"
		tags = tags + "scotrail "
	elif transaction_title[:16] == "NATIONAL EXPRESS":
		category = "travel"
		tags = tags + "National Express "
	elif transaction_title[:14] == "VIRGINTRAINSEC":
		category = "travel"
		tags = tags + "Virgin Trains East Coast "
	elif transaction_title[:16] == "VIRGIN TRAINS EC":
		category = "travel"
		tags = tags + "Virgin Trains East Coast "
	elif transaction_title[:18] == "LUL TICKET MACHINE":
		category = "travel"
		tags = tags + "LU ticket "
	elif transaction_title[:10] == "TRAVELODGE":
		category = "accommodation"
		tags = tags + "Travelodge "
	elif transaction_title[:5] == "*****":
		category = "masked"
		tags = tags + "Hidden transaction "
	# TODO - you can uncomment this to highlight transactions for specific amounts:
	#if amount == "x":
	#	category = "x"
	#elif amount == "y":
	#	category = "y"
	return category, tags

# GET CONVERTING:
outrows.append(["date", "payment", "info", "payee", "amount", "category", "tags"])

for row in inrows:
	try:
		new_date = datetime.datetime.strptime(row[0], "%d/%m/%Y")
		date_string = new_date.strftime("%d-%m-%y")
		last_row = row
	except:	#invalid date, skip row
		continue
	transaction_type = get_transaction_code(row[1])
	payee = row[2]
	info = row[2]
	amount = row[3]
	category, tags = get_category_and_tags(row[2])
	outrow = [date_string, transaction_type, payee, info, row[2], amount, category, tags]
	outrows.append(outrow)

#print last_row
#sys.exit()
#print last_row[4]	#Balance
if get_initial_balance == True:
	pre_balance = float(last_row[4]) - float(last_row[3])
	pre_balance = str(round(pre_balance, +2))
	#print float(last_row[4]), float(last_row[3]), pre_balance
	#sys.exit()
	amount = pre_balance
	outrows.append(["01-01-70", "4", "Starting balance", "Imported starting balance", "Bal", amount, "balance", "starting_balance"])

#print inrows[1]
#print outrows[0]
#sys.exit()

try:
	with open(csv_file, 'wb') as output_file:
		writer = csv.writer(output_file, delimiter = ';')
		for row in outrows:
			writer.writerow(row)
except:
	print "Can't write ", csv_file, "\'!"
	usage()
	sys.exit(6)
print "Done."

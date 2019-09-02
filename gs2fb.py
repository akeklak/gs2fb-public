from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

import pyrebase

# google sheet scope(read only), id, range
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

RANGE_NAME = 'Sheet1'

def connectToGS():

	#do a bunch of google stuff
	creds = None
	# The file token.pickle stores the user's access and refresh tokens, and is
	# created automatically when the authorization flow completes for the first
	# time.
	if os.path.exists('token.pickle'):

		with open('token.pickle', 'rb') as token:

			creds = pickle.load(token)
	# If there are no (valid) credentials available, let the user log in.
	if not creds or not creds.valid:

		if creds and creds.expired and creds.refresh_token:

			creds.refresh(Request())

		else:

			flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)

			creds = flow.run_local_server(port=0)
		# Save the credentials for the next run
		with open('token.pickle', 'wb') as token:

			pickle.dump(creds, token)

	return creds

def readFromSheet(sheetname, rangename, creds):

	#do a bunch of google stuff
	service = build('sheets', 'v4', credentials=creds)
	sheet = service.spreadsheets()
	result = sheet.values().get(spreadsheetId=sheetname,range=rangename).execute()
	values = result.get('values', [])

	return values

def parseGSData(GSdata):

	#the entry titles are in the first row.  The rest is data
	titles = GSdata[0]
	entries = GSdata[1:]

	return titles, entries

def connectToDB(config):

	#connect to firebase with pyrebase api
	firebase = pyrebase.initialize_app(config)
	#create db instance
	db = firebase.database()

	return db

def writeToDB(dbref, titles, entries, tablename):

	# for each row of entries
	for entry in entries:

		# create a key out of whatever column is labeled "id"
		key = entry[titles.index("id")]

		# for each label: value pair, 
		for title, item in zip(titles, entry):
		
			# the ID should be saved as an integer
			if title == "id":

				item = int(item)

			# make anything with commas into a list
			elif item.find(",") != -1:

				item = item.split(", ")

			#upload to firebase: account table -> id -> title: item
			dbref.child(tablename).child(key).child(title).set(item)
			#print(title, ":", item)

def updateTable(tablename, tableID, config):

	#create a GS connection
	credentials = connectToGS()
	#take data from GS
	data = readFromSheet(tableID, RANGE_NAME, credentials)
	#format data
	titles, entries = parseGSData(data)
	#create a db ref	
	ref = connectToDB(config)
	#upload the data 
	writeToDB(ref, titles, entries, tablename)


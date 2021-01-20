#https://docs.google.com/spreadsheets/d/1BJYoGAokrFlxkyH5Ludz8QFLVDMVTu1mZxLKTr9DgJ8/edit#gid=2049409995
#----------------------------------------------------------------------------------------------
#from __future__ import print_function
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import pprint
import datetime
import dateutil.parser
import pdb
import requests, json
import boto3
import time
from slackclient import SlackClient

CLIENT_SECRET = 'credentials.json'
SCOPE = 'https://www.googleapis.com/auth/spreadsheets.readonly'
#STORAGE = Storage('credentials.storage')


# If modifying these scopes, delete the file token.json.
SCOPES = 'https://www.googleapis.com/auth/spreadsheets'

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = "1Fur2J6_7PYzZxwcoUgMjP7h2KVJUu1NaUuSBNN9kouw"
ROTA_SPREADSHEET_ID = "1Fur2J6_7PYzZxwcoUgMjP7h2KVJUu1NaUuSBNN9kouw"
SAMPlE_GRID_ID=0
RANGE_NAME = '!A1:N50'

# Start the OAuth flow to retrieve credentials
def buildserivce():
    store = file.Storage('credentials.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('sheets', 'v4', http=creds.authorize(Http()))
    allrows = service.spreadsheets().values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,range=RANGE_NAME).execute()

    allrows1 = service.spreadsheets().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,fields = "sheets").execute()

    return service, allrows

    services, rows = buildserivce()

    print (services, rows)
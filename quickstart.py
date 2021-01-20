from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import datetime
from slackclient import SlackClient
import requests, json

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

# The ID and range of a sample spreadsheet.
SPREADSHEET_ID = '1_yqizmCADeUBiAmWLeTpdsNPy0snk2uGV1JC1BT-TyM'
RANGE_NAME = '!A1:F64'

def main():
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    fullNames={'taha':'UHW1X0W05', 'sidra':'U3PG0NPFZ', 'areeba':'U3JFNUZ4K'
    ,'kamran':'UEHR2TP0V','quhafa':'U1NFSHL74', 'omer': 'UFMQ019FC', 'saqib': 'UQPJ85UHG'}
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
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('sheets', 'v4', credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SPREADSHEET_ID,
                                range=RANGE_NAME).execute()
    singlerotarecord=None
    nowobject=datetime.datetime.now()
    now = nowobject.strftime("%d-%b-%y") #26-Nov-18
    now1 = str(int(nowobject.strftime("%d")))+nowobject.strftime("-%b-%y") #catering 1-jan and 01-jan
    #print result
    for eachline in result['values']:
        if len(eachline)>=4: # there are empty lines as well.
            if eachline[4] == now or eachline[4] == now1 :
                singlerotarecord = eachline #got the record for today
                #print(eachline[3], singlerotarecord[1:4])
                break
    #pdb.set_trace()
    #find 3 people on duty,
    names=""
    if singlerotarecord[3]:
        #print (singlerotarecord[3])
        #for eachname in singlerotarecord[4]:
        if singlerotarecord[1].lower() in fullNames:
            value = fullNames[singlerotarecord[1].lower()]
            print (value)
            #names.append(fullNames[lowercasename])
            #print (names)
            #new = names.replace("'","")
            #print (new)
        else:
            names.append(singlerotarecord)
    else:
        print ("Single rota record is None ")
    return value

def sendslacknotification(message):
    slack_token = 'xoxb-19067173008-643547807508-0fZtIuqjiwHc3Mr6OvsXn6D6'
    user_id = 'NightShift Bot'
    url = 'https://slack.com/api/chat.postMessage'
    # channel = "GLX0HSBSA" #channel_name is daily_ops_report
    #channel = "C01B7HL9PDJ"  # channel_name is tmp_nightshit_bot
    channel = "CDTNNFFPB" # channel_name is dddd
    # title = '@here :bangbang: Check this out'
    headers = {'content-type': 'application/json'}
    data = [
        ('token', slack_token),
        ('username', user_id),
        # ('as_user', 'false'),
        ('link_names', 1),
        # ('text', title),
        ('attachments', json.dumps([
            {
                "fallback": "Required plain-text summary of the attachment.",
                # "color": "blue",
                # "title": title,
                "text": message,
            }
        ])
         ),
        ('channel', channel)
        # ('icon_emoji', ':pencil2:')
    ]
    response = requests.post(url, data, headers)
    print(response.text)

if __name__ == '__main__':
    handler = main()
    mesg = "<@" + handler +"> you are in night shift today"
    sendslacknotification(mesg)

    
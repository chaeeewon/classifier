from __future__ import print_function
import pickle
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

import sys
import os
import shutil
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from PIL import Image
import imghdr
#If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

# The ID and range of a sample spreadsheet.
#SAMPLE_SPREADSHEET_ID = '1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms'
#SAMPLE_RANGE_NAME = 'Class Data!A2:E'

SPREADSHEET_ID = '1BxlhiJCKj-LllOOIQ3ML0Vsl9umivXPttpBEQ-b__cI'
RANGE_NAME = 'data!A1:L1000'
#RANGE_NAME = 'data!A1:L10'

def SearchDirectory(ret,directory,filename):
    for t in os.listdir(directory):
        if os.path.isdir(os.path.join(directory,t)):
            SearchDirectory(ret,os.path.join(directory,t),filename)
        else:
            if filename in t :
                ret.append(os.path.join(directory,t))
    return

    
def rename(filename,values):
    values = values[1:]    
    pokename = filename.split('/')[-1]
    pokefoldername = filename.split('/')[-2].replace('/','').lower()
    print(pokefoldername)
    pokename = pokename.split('.')[0]
    pokename = pokename.split('-')[0]
    pokename = pokename.lower()

    
    for row in values:
        flag=False
        number = int(row[0])
        kor_name = row[1]
        eng_name = row[3].lower()
        
        if pokefoldername in kor_name or pokefoldername in eng_name:                
            flag=True
        '''
        else:
            try:
                pokename = int(pokename)
                if pokename == number:
                    flag=True
                    print(pokename, number,kor_name,eng_name,pokename==number)
            except:
                if pokename in kor_name or pokename in eng_name:
                    flag=True           
                    print(pokename, number,kor_name,eng_name,pokename in eng_name)
        '''    
        if flag:
            re_pokename = row[0].zfill(3) + '_' + row[1]
            re_pokename.replace(' ','')
            return re_pokename#, pokename
   

def main(argv):

    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
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
    values = result.get('values', [])

    '''
    if not values:
        print('No data found.')
    else:
        print('Name, Major:')
        for row in values:
            # Print columns A and E, which correspond to indices 0 and 4.
            print('%s, %s' % (row[0], row[1]))
    ''' 

    path = argv[1].replace('/','')
    imglist = []
    SearchDirectory(imglist,path,'.png')
    SearchDirectory(imglist,path,'.jpg')
    SearchDirectory(imglist,path,'.gif')

    savepath = path+'_rename/'
    cnt = 2439
    unusable = []
    for img in imglist:
        imgformat = img[-4:]
        re_pokename = rename(img,values)
        if not os.path.exists(savepath):
            os.mkdir(savepath) 
        if re_pokename:
            re_pokename = re_pokename+'_'+ str(cnt).zfill(5)+imgformat
            shutil.copy(img,os.path.join(savepath,re_pokename)) 
            cnt+=1
        else:
            unusable.append(img)
    print('usable data:', cnt)
    print('unusable data num :', len(unusable))
    print("\n".join(unusable))


    


if __name__ == '__main__':
    if(len(sys.argv) < 1):
        print("Usage: python sourceFolder recFolder recCh")
    elif(len(sys.argv) >= 1):
        main(sys.argv)


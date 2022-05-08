from distutils.log import error
import os

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.errors import HttpError
from apiclient import errors


SCOPES = ['https://www.googleapis.com/auth/drive.readonly']
tokenJson = os.path.join('test', 'token.json')
clientJson = os.path.join('test', 'client_secret_drive.json')
creds = None

#print(os.getcwd())

def ConnectGoogleDrive():
  
  if os.path.exists(tokenJson):
    global creds 
    creds = Credentials.from_authorized_user_file(tokenJson, SCOPES)
  else:
    print('[LOG] Client Json does not exists.')
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(clientJson, SCOPES)
      creds = flow.run_local_server(port=0)
    with open(tokenJson, 'w') as token:
      token.write(creds.to_json())

  try:
    service = build('drive', 'v3', credentials=creds)
    print('conncet')

  except:
    print('[FAIL]conncet')

  return service

def retrieve_all_files(service):

  Found = []
  pToken = None
  
  while True:
    results = service.files().list(
      pageSize=10, fields='nextPageToken, files(id, name)',
      pageToken=pToken).execute()
    items = results.get('files', [])

    if not items:
      print('No files found.')
      break
    
    print('FILES: ')
    for item in items :
      print(u'{0}, ({1})' .format(item['name'], item['id']))

    pToekn = results.get('nextPageToken')    
    if not pToken:
      break

  return results



def DisconnectService(service):
  #service.close()
  print('close')
  return


def main():
  print('[main] Start')

  service = ConnectGoogleDrive()
  retrieve_all_files(service)
  
  DisconnectService(service)

  print('[main] End')
  return



print('name:', __name__)
if __name__ == '__main__':
    main()
elif __name__ == 'test':
    print('Imported!!!')
else:
    raise Exception('Invalid Name!!!')

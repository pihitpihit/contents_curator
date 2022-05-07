import os

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials


SCOPES = ['https://www.googleapis.com/auth/drive.readonly']
tokenJson = os.path.join('test', 'token.json')
clientJson = os.path.join('test', 'client_secret_drive.json')
creds = None

#print(os.getcwd())

def ConnectService():
  
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

  service = build('drive', 'v3', creds)
  print('conncet')
  return service


def DisconnectService(service):
  #service.close()
  print('close')
  return


def main():
  service = ConnectService()
  print('[main]')
  DisconnectService(service)

  return



print('name:', __name__)
if __name__ == '__main__':
    main()
elif __name__ == 'test':
    print('Imported!!!')
else:
    raise Exception('Invalid Name!!!')

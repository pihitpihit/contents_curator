from fileinput import filename
import mimetypes
import os
import io

from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from apiclient import errors
from requests import request


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
    print('[SUCESS] conncet')

  except:
    print('[FAIL]conncet')

  return service

def RetrieveAllFilesFolders(service):

  print('[Retrieve] Start')
  contentsList = []
  pToken = None
  
  while True:
    results = service.files().list(
      pageSize=500, 
      fields='nextPageToken, files(id, name)',
      pageToken=pToken).execute()
    items = results.get('files', [])

    contentsList.extend(items)
    #for item in items:
    #  contentsList.append(item)
    
    pToken = results.get('nextPageToken')
    if not pToken:
      break

  print('[Retrieve] End')

  return contentsList

def PrintContentsList(contents):
  
  if contents is not None :
    print('[FILES] %d' %(int(len(contents))))
    for content in contents :
      print(u'{0}, ({1})' .format(content['name'], content['id']))

  return

#Not Impliment Yet
def IsExistFile(service, fileName):
  """
    fileName과 동일한 파일 네임이 존재하는지 검사.
  """
  #print(fileName)
  contentsList = list()
  pToken = None
  
  while True:
    results = service.files().list(
      #q="name='StudyJordy.png'",
      q = "fullText contains 'Jordy' and mimeType != 'application/vnd.google-apps.folder'",
      pageSize=500, 
      fields='nextPageToken, files(id, name)',
      pageToken=pToken).execute()
    items = results.get('files', [])
    
    contentsList.extend(items)
    #for item in items:
    #  contentsList.append(item)
    
    pToken = results.get('nextPageToken')
    if not pToken:
      break
  
  print( 'List Size : %d' % len(contentsList) )
  print( contentsList )
  return contentsList

def DownloadByFileId(service, fId):
  """
    File ID를 이용하여 파일 다운로드
  """

  print( '[Downlaod] Start')
  request = service.files().get_media(fileId=fId)
  #fh = io.BytesIO()
  fh = io.FileIO('test.png', mode='wb')
  downLoader = MediaIoBaseDownload(fh, request, chunksize=1024*1024)
  done = False

  while done is False:
    status, done = downLoader.next_chunk()
    #print (status.progress())
    print( "Download %d%%" %int(status.progress()* 100) ) 
    
  print( '[Downlaod] End')

  return


def DisconnectService(service):
  #service.close()
  print('close')
  return


def main():
  print('[main] Start')
  contentsList = None
  
  #파일 및 폴더 검색
  service = ConnectGoogleDrive()
  contentsList = RetrieveAllFilesFolders(service)
  PrintContentsList(contentsList)
  
  #다운로드 By FileID
  #StudyJordyFileID = '1wyNFNt1CaWfOQMBD0XkqS_8kfcltvqlR'
  #DownloadByFileId(service, StudyJordyFileID)

  #타겟 파일 검색
  #contentsList = RetrieveAllFilesFolders(service)
  #targetList = IsExistFile(service, 'StudyJordy.png')
  # if not targetList:
  #   for target in targetList:
  #     print( target['name'] )

  #PrintContentsList(contentsList)

  # if bExist is True:
  #   print( 'Jordy is In!!!!!!!')
  # else:
  #   print( 'Jordy is Not')

  # PrintContentsList(contentsList)

  # if contentsList is None:
  #   print( 'Contents List Is None' )  
  # else:
  #   print( 'Contents List is Exist' )  

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

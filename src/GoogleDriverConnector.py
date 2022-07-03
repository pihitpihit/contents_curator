import os
import io

from ast import Not
from asyncio.windows_events import NULL
from binhex import getfileinfo
from ctypes import BigEndianStructure
from distutils.filelist import FileList
from fileinput import filename
from ftplib import ftpcp

from sqlite3 import Timestamp
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseDownload
from requests import request

JSON_FOLDER = 'test'
SCOPES = ['https://www.googleapis.com/auth/drive.readonly']
CRED_TOKEN_JSON = os.path.join(JSON_FOLDER, 'token.json')
CLIENT_JSON     = os.path.join(JSON_FOLDER, 'client_secret_drive.json')

class FInfo :
    #(name, path, hash, timestamp, isFile,)
    name        : str
    path        : str
    hash        : str 
    createdTime : str      
    timestamp   : str       
    isFile      : bool      #파일 일경우 Ture

    #[WARNNING] isFile은 bool
    def __init__(self, name, path, hash, createdTime, timestamp, isFile):
        self.name = name
        self.path = path
        self.hash = hash
        self.createdTime = createdTime
        self.timestamp = timestamp
        self.isFile = isFile
        return

    def print(self) :
        print('Name : ' + self.name )
        print('hash : ' + self.hash )
        print('path : ' + self.path )
        print('createdTime : ' + self.createdTime)
        print('timeStamp : ' + self.timestamp)
        if (self.isFile == True) :
            isFile = 'True'
        else :
            isFile = 'False'

        print('isFile: ' + isFile + '\n')

        return

class GoogleDriver :
    
    #TODO : CLIENT_JSON 파일을 지정할 수 있도록...
    def __init__(self):
        self.GetCred()
        self.service = self.BuildService()
        return
    
    def GetCred(self):
        creds = None
        if os.path.exists(CRED_TOKEN_JSON):
            print('[LOG] Create CRED')
            creds = Credentials.from_authorized_user_file(CRED_TOKEN_JSON, SCOPES)
        else:
            print('[LOG] Client Json does not exists.')
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(CLIENT_JSON, SCOPES)
                creds = flow.run_local_server(port=0)
        
            if(creds is not None) :
                with open(CRED_TOKEN_JSON, 'w') as token:
                    print('[LOG] WRITE CRETE JSON')
                    token.write(creds.to_json())

            else :
                print('[LOG] CRED is None')
            
        self.creds = creds
        return creds

    def BuildService(self):
        try:
          service = build('drive', 'v3', credentials=self.creds)
          print('[SUCESS] conncet')

        except:
          print('[FAIL]conncet')
        self.service = service
        return service

    #입력한 이름이 
    #[return]
    # 파일일 경우   : 'file'
    # 폴더일 경우   : 'folder'
    # 둘다 아닐 경우: 'None'
    # 둘다 일 경우  : 'both'
    def GetType(self, fname):
        result = None

        bExistDir = self.ExistDir(fname)
        if bExistDir == True:
            result = 'folder'

        bExistFile = self.ExistFile(fname)
        if bExistFile == True:
            if result is None:
                result = 'file'
            else :
                result = 'both'

        return result

    # True/False 디렉토리 존재 여부
    def ExistDir(self, DirName):
        bResult = True
        q = "fullText contains '" + DirName + "'" 
        q = q + "AND mimeType = 'application/vnd.google-apps.folder'"
        response = self.SendQuery(input=q)
        print(response)
        #{'files': []} -> 없을때,
        
        list1 = response.get('files')
        if not list1:
            bResult = False

        return bResult
    
    # 입력한 이름이 파일이 존재 하는 경우 Return : True
    def ExistFile(self, input):
        bResult = True
        q = "fullText contains '" + input + "'" 
        q = q + "AND mimeType != 'application/vnd.google-apps.folder'"
        response = self.SendQuery(input=q)
        print(response)
        #{'files': []} -> 없을때,
        
        list1 = response.get('files')
        if not list1:
            bResult = False

        return bResult
    
    # 파일정보 획득
    # return
    # 지정 경로 없음 : None
    # 지정된 경로가 폴더 : None
    # 지정된 경로가 파일일 경우 (name, path, hash, timestamp, isFile)
    #  isFile은 항상 true
    def GetFileInfo(self, input) :
        print("GetFileInfo : " + input + '\n')
        #path와 timeStamp는 정상 정보가 아니다.
        result = None
            
        query = "name='" + input + "'"
        query = query + " AND mimeType != 'application/vnd.google-apps.folder'"
        result = self.SendQuery(input=query)
        
        fileList = self.MakeFInfoList(result)

        return fileList

    # 파일 이름에 문자열 input 이 포함된 파일을 찾는다.
    # 반환 : list(str)
    def GetFileListContain(self, input) :
        query = "fullText contains \'" + input + "\'"
        query = query + ' AND ' + 'mimeType != \'application/vnd.google-apps.folder\''
        #query = query + "AND mimeType='image/jpeg'"
        #print(query)
        result = self.SendQuery(input=query)
        fileList = self.MakeFInfoList(result)

        return fileList

    #특정 날짜 이후 추가 된 파일 2012-06-04T12:00:00
    def GetFileUpdateAfter(self, date):
        query = 'createdTime > \'' + date + '\''
        query = query + ' and ' + 'mimeType != \'application/vnd.google-apps.folder\''
        result = self.SendQuery(input=query)
        fileList = self.MakeFInfoList(result)
    
        return fileList

    # 옵션
    #  -noFolder : True or False
    #  -recursive: True or False
    # 반환
    #  지정된 경로가 없음 : None
    #  지정된 경로가 파일 : None
    #  지정된 경로가 폴더 : List of FileInfo =(name, path, hash, timestamp, isFile)
    #   -noFolder 옵션 True : isFile == True 인 항목 제외 
    #   -recursive 옵션 False : 지정된 폴더 하위 1 depth 검색
    #   -recursive 옵션 True  : 지정된 폴더 하위 모든 폴더 파악
    def GetFolderInfo(self, FolderName) :
        #특정 폴더의 해쉬를 갖고 있으면 검색이 가능하다.
        #ex) query = hash in parents
        query = "name='" + FolderName + "'"
        query = query + " AND mimeType = 'application/vnd.google-apps.folder'"
        result = self.SendQuery(input=query)
        
        fileList = self.MakeFInfoList(result, isFile=False)

        return fileList

    #input이 포함된 모든 폴더 리스트를 반환한다.
    def GetFolderListContain(self, input):
        query = "fullText contains '" + input + "'"
        query = query + ' and ' + 'mimeType = \'application/vnd.google-apps.folder\''
        #print(query)
        result = self.SendQuery(input=query)
        fileList = self.MakeFInfoList(result)
        return fileList

    def DownloadByInfo(self, outName, info, filePath=None) :
        self.DownloadByFileId( outName=outName, fId=info.hash, outPath=filePath)
        return

    def DownloadByFileId(self,  outName, fId, outPath = None) :
        print( '[Downlaod] Start')
        request = self.service.files().get_media(fileId=fId)
        #fh = io.BytesIO()

        outFile = None
        if outPath is not None :
            bExist = os.path.isdir(outPath)
            if bExist != True:
                os.mkdir(outPath)
            outFile = outPath + outName
        else :
            outFile = outName

        fh = io.FileIO(outFile, mode='wb')
        downLoader = MediaIoBaseDownload(fh, request )#, chunksize=1024*1024)
        done = False

        while done is False:
            status, done = downLoader.next_chunk()
            #print (status.progress())
            print( "Download %d%%" %int(status.progress()* 100) ) 

        print( '[Downlaod] End')
        return

    #주어진 쿼리에 맞는 조건의 폴더/파일 리스트 반환
    # return : list
    def SendQuery(self, input):
        page_token = None

        print('QUERY : ' + input + '\n')

        while True:
            # 딕션너리  {'name' = '' , 'id' = ''} 의 리스트.
            response = self.service.files().list(
                                            q=input,
                                            spaces='drive',
                                            fields='nextPageToken, files(id, name, createdTime, modifiedTime, size)',
                                            pageToken=page_token).execute()

            # for file in response.get('files', []):
            #     #print ('Found file: %s (%s)' % (file.get('name'), file.get('id')))
            #     #FileInfo (name, path, hash, timestamp, isFile)
            #     result.append(file.get('name'))
            #     result.append(file.get('id'))
            #     page_token = response.get('nextPageToken', None)
                #print (result)


            if page_token is None:
                break
        
        return response
    
    def MakeFInfoList(self, queryResult, isFile = True) :
        fileList = queryResult['files']
        infoList = []
        
        for file in fileList:
            #print(file)
            info = FInfo(file['name'], 'path', file['id'], file['createdTime'], file['modifiedTime'], isFile)
            infoList.append(info)
            #info.print()

        return infoList


def main() :
    conn = GoogleDriver()
    #result = conn.GetFolderList()
    #result = conn.GetFileList()
    
    # TEST ExistDir
    #isExistDir = conn.ExistDir('ComeupJordy.png')
    # isExistDir = conn.ExistDir('Jordy2')
    # if isExistDir == True:
    #     print('TRUE')
    # else:
    #     print('FALSE')

    # TEST ExistFile
    #isEixstFile = conn.ExistFile('ComeupJordy.png')
    # isEixstFile = conn.ExistFile('Jordy2')
    # if isEixstFile == True:
    #     print('TRUE')
    # else:
    #     print('FALSE')

    #TEST GetType #Done
    # target = 'PickMeJordy.jpg'
    # fType = conn.GetType(target)
    # if fType is not None:
    #     answer = fType
    # else :
    #     answer = 'None'
    # print(target + ' Type : ' + answer)

    #TEST GetFileInfo  #Done
    #infoList = conn.GetFileInfo("DokiDokiJordy.jpg")
    # for info in infoList:
    #     print(info)

    #TEST GetFileInfoContain #Done
    infoList = conn.GetFileListContain('Jordy')
    
    #TEST GetFileUpdateAfter #Done
    #infoList = conn.GetFileUpdateAfter('2022-05-12T12:00:00')
    
    #TEST GetFolderInfo #Done
    #infoList = conn.GetFolderInfo('Jordy')
    
    #TEST getFolderInfoContain #done
    #infoList = conn.GetFolderListContain('Jordy')

    i = 0
    for info in infoList:
        
        info.print()
        path = str('C:\\Users\\diffe\\Documents\\GitHub\\contents_curator\\img\\')
        conn.DownloadByInfo( info=info , outName=info.name, filePath=path )
        
#    result = conn.GetFolderList()
    
    # 'files'라는 키 검색. 없으면 빈 딕션너리 리턴
    # for file in result.get('files', []):
    #     print(file)
    
    print('[LOG] DONE')

    return

if __name__ == '__main__':
    main()
elif __name__ == 'GoogleDriverConnector' :
    print('imported')
else:
    raise Exception('Invalid Name!!!')



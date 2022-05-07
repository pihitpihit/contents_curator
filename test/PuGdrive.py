import os
import sys
import pickle
import hashlib

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

class HashFinder:
	def __init__(self, dataPath):
		self.dataPath = dataPath
		if os.path.exists(dataPath):
			self.dict = self.load(dataPath)
		else:
			self.dict = {
				'root':{'hash':'root','dirs':None},
				'HashToPath':{}
			}
		return

	def cleanup(self):
		os.remove(self.dataPath)
		return

	def save(self):
		with open(self.dataPath, 'wb') as f:
			pickle.dump(self.dict, f, pickle.HIGHEST_PROTOCOL)
			print('[HashFinder] saved!')
		return

	def load(self, dataPath):
		with open(dataPath, 'rb') as f:
			return pickle.load(f)

	def get(self, path):
		dict = self.dict['root']
		found = ''

		dirs = []
		if path not in ['', '/']:
			dirs = path.split('/')

		for node in dirs:
			if dict['dirs'] is None or node not in dict['dirs']:
				return (dict['hash'], False, found)
			dict = dict['dirs'][node]
			if len(found):
				found += '/'
			found += node

		return (dict['hash'], True, found)

	def set(self, path, hash):
		#print('[CACHE][SET] %s = %s' % (hash, path))
		(complete, foundHash, _) = self.get(path)
		if complete and hash == foundHash:
			return False

		dirs = []
		if path not in ['', '/']:
			dirs = path.split('/')
		dict = self.dict['root']

		if len(dirs) == 0:
			raise Exception('[HashFinder][set] root has cannot be set')

		for node in dirs[:-1]:
			if node not in dict['dirs']:
				raise Exception('[HashFinder][set] parent \'%s\' not found' % node)
			dict = dict['dirs'][node]

		baseDir = dirs[-1]
		if dict['dirs'] is None:
			dict['dirs'] = {}
		dict['dirs'][baseDir] = {'hash':hash, 'dirs':None}
		return True

	def hashToPath(self, hash):
		return self.dict['HashToPath'][hash]

	def pathToHash(self, path):
		hash = hashlib.md5(path).hexdigest()
		if 'HashToPath' not in self.dict:
			self.dict['HashToPath'] = {}
		if hash in self.dict['HashToPath']:
			if self.dict['HashToPath'][hash] == path:
				return hash
			# debug
			print('[PathToHash] CONFLICT!!' % path)
			print(' e:', self.dict['HashToPath'][hash].decode('utf-8'))
			print(' n:', path.decode('utf-8'))
			return None
				
		self.dict['HashToPath'][hash] = path
		return hash

	def show(self):
		print('[HashFinder-start]')
		print(self.dict)
		print('[HashFinder-end]')
		return

class gdrv:
	def __init__(self):
		self.SCOPES = ['https://www.googleapis.com/auth/drive.readonly']
		self.tokenJson = 'token.json'
		self.clientJson = 'client_secret_drive.json'
		self.creds = None

		if os.path.exists(self.tokenJson):
			self.creds = Credentials.from_authorized_user_file(self.tokenJson, self.SCOPES)
		else:
			print('[LOG] Client Json does not exists.')

		if not self.creds or not self.creds.valid:
			if self.creds and self.creds.expired and self.creds.refresh_token:
				self.creds.refresh(Request())
			else:
				flow = InstalledAppFlow.from_client_secrets_file(clientJson, self.SCOPES)
				self.creds = flow.run_local_server(port=0)
			with open(self.tokenJson, 'w') as token:
				token.write(self.creds.to_json())

		self.service = build('drive', 'v3', credentials=self.creds)
		self.cache = HashFinder(os.path.join('.', 'PuPlexData', 'GDrvHash.pkl'))
		return

	def showCache(self):
		self.cache.show()
		return

	def hashToPath(self, hash):
		return self.cache.hashToPath(hash)

	def pathToHash(self, path):
		return self.cache.pathToHash(path)

	def getId(self, path):
		if not path.startswith('Storage'):
			raise Exception('Invalid Path')
		(foundHash, found, foundPath) = self.cache.get(path)
		#print('[CACHE][GET][%5s] %s = %s' % (found, foundHash, foundPath))
		#print(foundPath, len(foundPath))

		# cache hit
		if found:
			return foundHash

		# cache miss
		remainPath = path[len(foundPath):]
		if remainPath[0] == '/':
			remainPath = remainPath[1:]
		toFind = remainPath.split('/')
		#print('toFind :', toFind)
		for node in toFind:
			entryList = self.getListByHash(foundHash)
			nextFoundHash = None
			for item in entryList:
				if len(foundPath):
					setPath = foundPath + '/' + item
				else:
					setPath = item
				self.cache.set(setPath, entryList[item])
				if item == node:
					nextFoundHash = entryList[item]

			if nextFoundHash is None:
				raise Exception('Hash Retrieve Failed ER:%s'%(node))
			foundHash = nextFoundHash
			if len(foundPath):
				foundPath += '/'
			foundPath += node

		self.cache.save()
		return foundHash

	def getListByHash(self, findInHash = 'root'):

		dictFound = {}
		pToken = None

		while True:
			result = self.service.files().list(
				pageSize=100,
				q='\'%s\' in parents' % findInHash,
				pageToken=pToken,
				fields='nextPageToken, files(name, id)'
			).execute()

			items = result.get('files', [])
			for item in items:
				name = item['name']
				id = item['id']
				dictFound[item['name']] = item['id']

			pToken = result.get('nextPageToken')
			if pToken is None:
				break;
			print(pToken)

		return dictFound 

	def test(self, hash = None):
		if hash is None:
			results = self.service.files().list(
				q='\'root\' in parents', fields='nextPageToken, files(name, id)').execute()
				#q='root', fields='files(id, name)').execute()
		else:
			results = self.service.files().list(
				q='\'%s\' in parents' % hash).execute()
				#q='root', fields='files(id, name)').execute()

		items = results.get('files', [])

		for item in items:
			st#print(u'{0} ({1})'.format(item['name'], item['id']))
			print('[Result]', item)

		print(len(items))
		item = results.get('nextPageToken')
		print('NextPageToken: ', item)
		return

def main():

	if True:
		g = gdrv()
		#g.showCache()
		hash = g.getId('Storage/MOWM/Video/Animation/_미정리')
		print(hash)
	

	if False:
		hf = HashFinder(os.path.join('.', 'PuPlexData', 'GDrvHashTest.pkl'))
		hf.show()
		print(hf.get(''))
		
		hf.set('a', 'A')
		hf.show()
		hf.set('b', 'B')
		hf.show()
		hf.set('a/b', 'B')
		hf.show()
		#print(hf.get(''))
		#print(hf.get('a'))
		#print(hf.get('a/b'))
		#print(hf.get('a/b/c'))
		#hf.set('a/b/c', 'C')
		#hf.cleanup()

	return


if __name__ == '__main__':
	main()


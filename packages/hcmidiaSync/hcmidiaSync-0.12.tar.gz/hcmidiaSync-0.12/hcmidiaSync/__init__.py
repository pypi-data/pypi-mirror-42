import requests
import simplejson as json
import re
from datetime import datetime  
from datetime import timedelta 

HOST = 'http://192.168.0.11'
HCMIDIA_HOST = 'http://192.168.0.76/hcmedia'

def getAssets() :
	r = requests.get(HOST + '/api/v1.2/assets');
	print 'GET '+ HOST +'/api/v1.2/assets: ' + str(r.status_code)
	data = json.loads(r.text)
	#print data
	return data
	
def showAssets(data) :
	for a in data:
		print a['asset_id'] + " - " + a['uri'] + " - " + str(a['is_enabled'])

def getTodayMovies(uri) :
	r = requests.get(uri);
	print 'GET ' + uri + ': ' + str(r.status_code)
	data = json.loads(r.text)	
	#print data
	return data

def createAsset(uri, name) :
	now = datetime.now()
	asset = {}
	asset['duration'] = 0
	asset['end_date'] = str (now + timedelta(days=30))
	asset['is_active'] = 1
	asset['is_enabled'] = 0
	asset['is_processing'] = 0
	asset['mimetype'] = "video"
	asset['name'] = name
	asset['nocache'] = 0
	asset['play_order'] = 0
	asset['skip_asset_check'] = 0
	asset['start_date'] = str(now)
	asset['uri'] = uri
	return asset


def addAsset(asset) :
	r = requests.post(HOST + '/api/v1.2/assets', data= json.dumps(asset))
	print 'POST '+ HOST +'/api/v1.2/assets: ' + str(r.status_code)
	print 'request result text ' + r.text
	data = json.loads(r.text)
	return data

def enableAsset(asset) :
	asset['is_enabled'] = 1
	r = requests.put(HOST + '/api/v1.2/assets/' + asset['asset_id'], data= json.dumps(asset))
	print 'PUT '+ HOST +'/api/v1.2/assets/' + asset['asset_id'] +': ' + str(r.status_code)
	print 'request result text ' + r.text
	data = json.loads(r.text)
	return data

def disableAsset(asset) :
	asset['is_enabled'] = 0
	r = requests.put(HOST + '/api/v1.2/assets/' + asset['asset_id'], data= json.dumps(asset))
	print 'PUT '+ HOST +'/api/v1.2/assets/' + asset['asset_id'] +': ' + str(r.status_code)
	print 'request result text ' + r.text
	data = json.loads(r.text)
	return data

def deleteAsset(asset):
	r = requests.delete(HOST + '/api/v1.2/assets/' + asset['asset_id'])
	print 'DEL '+ HOST +'/api/v1.2/assets/' + asset['asset_id'] +': ' + str(r.status_code)
	print 'request result text ' + r.text


def addTodayMovies(todayMovies) :
	for m in todayMovies:
		print 'Adding: ' +  m['path']
		asset = createAsset(m['path'], m['filename'])
		newAsset = addAsset(asset)
		if newAsset['asset_id'] is None:
			print 'error adding: ' +  m['path']
		else:
			print m['path'] + ' was successfully added'
		enableAsset(newAsset)

def test_disable(assets, id):
	asset1 = next((x for x in assets if x['asset_id'] == id), None)
	disableAsset(asset1)

def test_delete(assets, id):
	asset1 = next((x for x in assets if x['asset_id'] == id), None)
	deleteAsset(asset1)

def findMoviesToSync(assets):
	foldersToSync = []
	for a in assets:
		pattern = "^"+ HCMIDIA_HOST +"/.*movies[.]php$"
		#print pattern
		x = re.search(pattern, a['uri'])
		if x :
			foldersToSync.append(a)
	return foldersToSync

def syncMovies(assets, moviesToSync) :
	for m in moviesToSync:
		syncMoviesByURI(assets, m['uri'])

def syncMoviesByURI(assets, uri):
	baseUri = uri.replace('movies.php', '')

	todayMovies = getTodayMovies(uri)
	assetsWithBaseURI = getAssetsWithBaseURI(assets, baseUri)
#	showAssets(assetsWithBaseURI)

	assetsToDelete = getMoviesToDelete(assetsWithBaseURI, todayMovies)
	showAssets(assetsToDelete)
	deleteAssets(assetsToDelete)
	moviesToAdd = getMoviesToAdd(assetsWithBaseURI, todayMovies)
	print moviesToAdd

	addTodayMovies(moviesToAdd)
	#test_disable(assets, '381d7a2643a84a24bd233c182037adb0')
	#test_delete(assets, '381d7a2643a84a24bd233c182037adb0')

def getAssetsWithBaseURI (assets, baseUri):
	assetsWithBaseURI = []
	for a in assets:
		pattern = "^"+ baseUri
		x = re.search(pattern, a['uri'])
		idx = a['uri'].find('movies.php')
		if ( x is not None )  & ( idx == -1 ) :
			assetsWithBaseURI.append(a)
	return assetsWithBaseURI

def getMoviesToDelete(assetsWithBaseURI, todayMovies):
	moviesToDelete = []
	for a in assetsWithBaseURI:
		todayMovie = next((x for x in todayMovies['arquivos'] if x['path'] == a['uri']), None)
		if todayMovie is None:
			moviesToDelete.append(a)
	return moviesToDelete

def getMoviesToAdd(assetsWithBaseURI, todayMovies):
	moviesToAdd = []
	for m in todayMovies['arquivos']:
		newAsset = next((x for x in assetsWithBaseURI if m['path'] == x['uri']), None)
		if newAsset is None:
			moviesToAdd.append(m)
	return moviesToAdd


def deleteAssets(assets):
	for a in assets:
		deleteAsset(a)

def main():	
	assets = getAssets()
	#showAssets(assets)

	#print 'foldersToSync:'
	moviesToSync = findMoviesToSync(assets)
	#showAssets(moviesToSync)
	syncMovies(assets, moviesToSync)

if __name__== "__main__":
	main()	


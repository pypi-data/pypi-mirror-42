import requests
import json

r = requests.get('http://localhost:8080/');
print r.text
data = r.json()
print data
print json.loads(r.text)
print data['foo']
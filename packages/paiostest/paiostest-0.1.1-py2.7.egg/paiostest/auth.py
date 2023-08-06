import json
import urllib
import urllib2

url = "http://127.0.0.1:8888/"

def authen(name,secretId):
	values = {'name': name,'secretId': secretId}
	data = urllib.urlencode(values)
	req = urllib2.Request(url+"auth", data)
	response = urllib2.urlopen(req)
	print(response.getcode())
	dict = response.read()
	print dict
	dict_info = json.loads(dict)
	print "dict_info['secretId']:", dict_info['secretId']
	G.secretId = dict_info['secretId']
	
class G:
	secretId = ""
	
	
def printMessage():
	print "hi,welcome to authentication page!"
	
	
if __name__ == '__main__':
	printMessage()
	
import json
import urllib
import urllib2

url = "http://192.168.2.102:8080/"

def authen(key,secretId):
	values = {'key': key,'secretId': secretId}
	print values
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
	authen("yab","123451111qqq")		
import httplib, urllib, base64, json

# API can only process chunks shorter than 5k characters
def fiveThousandChunks(longstring):
	strings = []
	while len(longstring) > 5000:
		strings.append(longstring[:4999])
		longstring = longstring[5000:]
	strings.append(longstring)
	return strings

# make submittable json
def convertLongTextToJSON(long_text):
	strings = fiveThousandChunks(long_text)
	data = {}
	data["documents"] = []
	idnumber = 1
	for string in strings:	
		data_entry = {}
		data_entry["text"] = string
		data_entry["id"] = str(idnumber)
		data_entry["language"] = "en"
		data["documents"].append(data_entry)
		idnumber = idnumber + 1
	json_data = json.dumps(data)
	return json_data

# actually makes the API call
def callAPIwithJSON(json_to_submit,access_key="7fae8fc1feb540e4bc24bd0ea357e836"):	
	headers = {
		# Request headers
		'Content-Type': 'application/json',
		'Ocp-Apim-Subscription-Key': access_key,
	}
	params = urllib.urlencode({})
	try:
		conn = httplib.HTTPSConnection('westeurope.api.cognitive.microsoft.com')
		conn.request("POST", "/text/analytics/v2.0/keyPhrases?%s" % params, json_to_submit, headers)
		response = conn.getresponse()
		data = response.read()
		conn.close()
	except Exception as e:
		print("[Errno {0}] {1}".format(e.errno, e.strerror))
	return data

# wrapper for ease of use
def getKeyWords(string_to_process,access_key="7fae8fc1feb540e4bc24bd0ea357e836"):
	json_to_submit = convertLongTextToJSON(string_to_process)
	apiResponse = json.loads(callAPIwithJSON(json_to_submit,access_key))
	keyPhrases = apiResponse['documents'][0]['keyPhrases']
	return keyPhrases



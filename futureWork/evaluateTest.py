#!/usr/bin/env python
#import evaluate
import httplib, urllib, base64, json

key1 = "9d982e22afa04d38be00c1680f9657ee"
key2 = "e687b95c09454cfd817e7f59bfce1711"

headers = {
		# Request headers
		'Content-Type': 'application/x-www-form-urlencoded',
		'Ocp-Apim-Subscription-Key': key1,
}
params = urllib.urlencode({
})
    
try: 
    conn = httplib.HTTPSConnection('westus.api.cognitive.microsoft.com')
    conn.request("POST", "/academic/v1.0/evaluate?%s" % params, "expr=Composite(AA.AuN='albert einstein')&count=10&orderby=CC:desc&attributes=CC,Ti,Y,F.FN", headers)
    response = conn.getresponse()
    data = response.read()
    print(data)
    conn.close()
except Exception as e:
    print("[Errno {0}] {1}".format(e.errno, e.strerror))

#!/usr/bin/python

import httplib
import base64
import string
import json
import urllib2
import ConfigParser


json_introspect='{ "jsonrpc": "2.0", "method": "JSONRPC.Introspect", "id": 1 }'
cache={}

config = ConfigParser.RawConfigParser()

config.read(os.path.expanduser('~') + '/.xbmcjsonapi')
username=config.get('http','username')
password=config.get('http','password')
json_url=config.get('http','json_url')
host=config.get('http','host')

class xmbcjsonapitransport:
    def __init__(self):
        pass

def http_json_request(json_request):
    # base64 encode the username and password
    auth = base64.encodestring('%s:%s' % (username, password)).replace('\n', '')
    url = 'http://%s%s%s' % (host, json_url, json_request)

    # write the Authorization header like: 'Basic base64encode(username + ':' + password)
    headers = {'Authorization' : 'Basic %s' % auth, 
               'Content-Type' : 'application/json',
               'Content-Length' : '%s' % len(json_request)}
    
        # get the response
    req = urllib2.Request( 'http://%s%s' % (host,json_url), json_request, headers)
    response = urllib2.urlopen(req)
    json = response.read()
    return json


class xbmcjsonapi:
    def __init__(self):
        pass


def namespaces():
    namespaces=[]
    for method in json.loads(http_json_request(json_introspect))['result']['methods']:
        if method.split('.')[0] not in namespaces:
            namespaces.append(method.split('.')[0])
    return namespaces


for namespace in namespaces():
    s = """class %s(xbmcjsonapi):
    \"\"\"XBMC %s namespace. \"\"\"
    pass
    """%(namespace,namespace)
    exec (s)

cache=json.loads(http_json_request(json_introspect))['result']['methods']
for namespace in namespaces():
    for key in cache:
        if namespace in key:
            function_name=key.split('.')[1]
            s="""def %s(self, *args, **kwargs):
            \"\"\"
            Description : %s 
            Parameters : %s
            Returns : %s
            \"\"\"
            json_request='{ "jsonrpc": "2.0", "method": "%s.%s"'
            if kwargs=={}:
                json_request=json_request+'}'
            else:
                json_request=json_request+json.dumps(kwargs)+'}'
            return http_json_request(json_request)
            """ % (function_name, cache[key]['description'], cache[key]['params'], cache[key]['returns'], namespace, function_name)
            exec(s)
            s="""setattr(%s,'%s',%s)""" % (namespace, function_name, function_name)
            exec(s)

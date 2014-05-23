#!/usr/bin/python

import httplib
import base64
import string
import json
import urllib2
import ConfigParser
import os

cache={}


class xbmcjsonapitransport:
    def __init__(self):
        pass
    def request(self,jsonrequest):
        pass
        

class HTTPtransport(xbmcjsonapitransport):
    json_introspect='{ "jsonrpc": "2.0", "method": "JSONRPC.Introspect", "id": 1 }'
    config = ConfigParser.RawConfigParser()
    config.read(os.path.expanduser('~') + '/.xbmcjsonapi')
    username=config.get('http','username')
    password=config.get('http','password')
    port=config.get('http','port')
    json_url=config.get('http','json_url')
    host=config.get('http','host')

    def __init__(self):
      pass  
        
    def request(self, json_request):
        # base64 encode the username and password
        auth = base64.encodestring('%s:%s' % (self.username, self.password)).replace('\n', '')
        url = 'http://%s:%s%s%s' % (self.host, self.port, self.json_url, json_request)
        # write the Authorization header like: 'Basic base64encode(username + ':' + password)
        headers = {'Authorization' : 'Basic %s' % auth, 
                   'Content-Type' : 'application/json',
                   'Content-Length' : '%s' % len(json_request)}
    
        # get the response
        req = urllib2.Request( url, json_request, headers)
        response = urllib2.urlopen(req)
        json = response.read()
        return json


class xbmcjsonapi:
    def __init__(self):
        pass

transport_instance=HTTPtransport()

def namespaces():
    namespaces=[]
    for method in json.loads(transport_instance.request(transport_instance.json_introspect))['result']['methods']:
        if method.split('.')[0] not in namespaces:
            namespaces.append(method.split('.')[0])
    return namespaces


for namespace in namespaces():
    s = """class %s(xbmcjsonapi):
    \"\"\"XBMC %s namespace. \"\"\"
    pass
    """%(namespace,namespace)
    exec (s)

cache=json.loads(transport_instance.request(transport_instance.json_introspect))['result']['methods']
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
            return transport_instance.request(json_request)
            """ % (function_name, cache[key]['description'], cache[key]['params'], cache[key]['returns'], namespace, function_name)
            exec(s)
            s="""setattr(%s,'%s',%s)""" % (namespace, function_name, function_name)
            exec(s)

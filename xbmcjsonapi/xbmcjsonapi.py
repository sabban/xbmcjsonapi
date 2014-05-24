#!/usr/bin/python

import string
import json
import os
import ConfigParser
import transports

cache={}




class xbmcjsonapi:
    def __init__(self):
        pass


# config = ConfigParser.RawConfigParser()
# config.read(os.path.expanduser('~') + '/.xbmcjsonapi')
# username=config.get('http','username')
# password=config.get('http','password')
# port=config.get('http','port')
# json_url=config.get('http','json_url')
# host=config.get('http','host')

config = ConfigParser.RawConfigParser()
config.read(os.path.expanduser('~') + '/.xbmcjsonapi')
port=config.get('tcp','port')
buffer_size=config.get('tcp','buffer_size')
host=config.get('tcp','host')



# transport_instance=transports.HTTPtransport(**{'port': port, 'host': host, 'username': username, 'password': password})
transport_instance=transports.TCPtransport(**{'port': port, 'host': host, 'buffer_size': buffer_size})


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

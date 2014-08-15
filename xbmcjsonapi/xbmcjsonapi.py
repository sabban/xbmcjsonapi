#!/usr/bin/python

import string
import json
import os
import transports

cache={}

class xbmcjsonapi:
    def __init__(self, *args, **kwargs):
        self.type_transport = kwargs.get('type_transport', "TCP")
        self.port = kwargs.get('port', 9090)
        self.host = kwargs.get('host', "localhost")
        self.username = kwargs.get('username', "username")
        self.password = kwargs.get('password', "password")
        self.buffer_size = kwargs.get('buffer_size', 1024)
        if self.type_transport == 'TCP':
            self.transport_instance=transports.TCPtransport(**{'port': self.port, 'host': self.host, 'buffer_size': self.buffer_size})
        if self.type_transport == 'HTTP':
            self.transport_instance=transports.HTTPtransport(**{'port': self.port, 'host': self.host, 'username': self.username, 'password': self.password})
        cache=json.loads(self.transport_instance.request(self.transport_instance.json_introspect))['result']['methods']
        xbmcjsonapi_create_subclasses(self)

    def namespaces(self):
        namespaces=[]
        for method in json.loads(self.transport_instance.request(self.transport_instance.json_introspect))['result']['methods']:
            if method.split('.')[0] not in namespaces:
                namespaces.append(method.split('.')[0])
        return namespaces

    def parameters(self):
        return {'type_transport': self.type_transport,
                'port' : self.port,
                'host' : self.host,
                'username' : self.username,
                'password' : self.password,
                'buffer_size' : self.buffer_size}

def xbmcjsonapi_create_subclasses(instance):
    namespaces = instance.namespaces()
    for namespace in namespaces:
        s = """class %s(object):
    \"\"\"XBMC %s namespace. \"\"\"
    def __init__(self, *args, **kwargs):
        self.type_transport = kwargs.get('type_transport', "TCP")
        self.port = kwargs.get('port', 9090)
        self.host = kwargs.get('host', "localhost")
        self.username = kwargs.get('username', "username")
        self.password = kwargs.get('password', "password")
        self.buffer_size = kwargs.get('buffer_size', 1024)
        if self.type_transport == 'TCP':
            self.transport_instance=transports.TCPtransport(**{'port': self.port, 'host': self.host, 'buffer_size': self.buffer_size})
        if self.type_transport == 'HTTP':
            self.transport_instance=transports.HTTPtransport(**{'port': self.port, 'host': self.host, 'username': self.username, 'password': self.password})

    """%(namespace,namespace)
        exec (s)
        s="""setattr(xbmcjsonapi,'%s',%s)""" % (namespace, namespace)
        exec (s)
    
    cache=json.loads(instance.transport_instance.request(instance.transport_instance.json_introspect))['result']['methods']
    for namespace in namespaces:
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
                json_request=json_request + ',' + json.dumps(kwargs)[1:-1]+'}'
            return self.transport_instance.request(json_request)
            """ % (function_name, cache[key]['description'], cache[key]['params'], cache[key]['returns'], namespace, function_name)
                exec(s)
                s="""setattr(%s,'%s',%s)""" % (namespace, function_name, function_name)
                exec(s)

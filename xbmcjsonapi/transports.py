#!/usr/bin/python

import httplib
import base64
import string
import json
import urllib2
import os
import ConfigParser
import socket

class xbmcjsonapitransport:
    json_introspect='{ "jsonrpc": "2.0", "method": "JSONRPC.Introspect", "id": 1 }'

    def request(self,jsonrequest):
        pass
        

class HTTPtransport(xbmcjsonapitransport):
    def __init__(self, *args, **kwargs):
        self.port=kwargs['port']
        self.username=kwargs['username']
        self.password=kwargs['password']
        self.host=kwargs['host']
        self.json_url='/jsonrpc?request='

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

class TCPtransport(xbmcjsonapitransport):
    def __init__(self, *args, **kwargs):
        self.port=kwargs['port']
        self.host=kwargs['host']
        self.buffer_size=kwargs['buffer_size']

    def request(self, json_request):
        s = socket.socket(socket.AF_INET, 
                          socket.SOCK_STREAM)
        s.connect((self.host, int(self.port)))
        s.send(json_request)
        json=s.recv(int(self.buffer_size))
        print json
        return json

import os, ConfigParser, socket, json
from transports import *
from multiprocessing import Process, Manager, Lock

config = ConfigParser.RawConfigParser()
config.read(os.path.expanduser('~') + '/.xbmcjsonapi')
port=config.get('tcp','port')
buffer_size=config.get('tcp','buffer_size')
host=config.get('tcp','host')


class notifications(TCPtransport):

    def __init__(self, *args, **kwargs):
        TCPtransport.__init__(self, **{'port': port, 'host': host, 'buffer_size': '1'})
        self.request_configuration=('{"id":"1","jsonrpc":"2.0","result":'
                                    '{"notifications":{"Application":true,"AudioLibrary":true,'
                                    '"GUI":true,"Input":true,"Other":true,"PVR":false,'
                                    '"Player":true,"Playlist":true,"System":true,"VideoLibrary":true}}}')        
        self.list_notifications=[]
        self.request(self.request_configuration)
        self.fork_listen_notifications()
    
    def fork_listen_notifications(self):
        manager = Manager()
        self.json_list = manager.list()
        lock = Lock()
        self.p = Process(target=self.__get_notifications, args=(self.json_list, lock))
        self.p.start()
        self.list_notifications=self.json_list

    def __get_notifications(self, json_list, lock):
        s = socket.socket(socket.AF_INET, 
                          socket.SOCK_STREAM)
        s.connect((self.host, int(self.port)))
        string=''
        while True:
            braces=0
            string=s.recv(1) 
            braces=string.count('{')
            braces=braces-string.count('}')
            while braces!=0:
                tmp=s.recv(1)
                string=string+tmp.strip('\n')
                braces=braces+tmp.count('{')
                braces=braces-tmp.count('}')
            self.json_list.append(json.loads(string))

    def last_notifications(self):
        try:
            return self.list_notifications.pop()
        except:
            return ''

    def __del__(self):
        self.p.terminate()

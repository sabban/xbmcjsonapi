xbmcjsonapi is an API for JSON connection to XBMC
written in python

TCP and HTTP connections are implemented for the
moment.

Invocation is quite ugly for the moment:

This example show how to perform a update of the
Video Library
import xbmcjsonapi.xbmcjsonapi
x=xbmcjsonapi.xbmcjsonapi.xbmcjsonapi(**{'port': 9090, 'host': 'hostname', 'buffer_size': 1024})
y=x.VideoLibrary(**x.parameters()
y.Scan()

All functions are autodocumented:
help(y.Scan())

All functions documented by XBMC are also implemented.

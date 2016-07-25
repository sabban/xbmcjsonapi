#1 xbmcjsonapi is an API for JSON connection to XBMC written in python

Only TCP and HTTP connections are implemented for the moment.

Invocation is quite ugly for the moment:

This example show how to perform a update of the Video Library:
```python
import xbmcjsonapi.xbmcjsonapi
x=xbmcjsonapi.xbmcjsonapi.xbmcjsonapi(**{'port': 9090, 'host': 'hostname', 'buffer_size': 1024})
y=x.VideoLibrary(**x.parameters()
y.Scan()
```

All functions are self-documented:
```python
help(y.Scan())
```

All functions documented in XBMC json api are implemented.
[http://wiki.xbmc.org/index.php?title=JSON-RPC_API/v6](XBMC JSON API reference)
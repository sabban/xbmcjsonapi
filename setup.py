from distutils.core import setup, Extension
from xbmcjsonapi import VERSION

if __name__ == "__main__":
    setup(name="xbmcjsonapi",
          version=VERSION,
          url='https://github.com/sabban/xbmcjsonapi',
          description='python implementation of XBMC JSON interface',
          author='Manuel Sabban',
          author_email="sabban@sabban.eu",
          license="OpenBSD",
          platform="Linux",
          packages=["xbmcjsonapi"])

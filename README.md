pytor
=====

Pytor is a Python wrapper for scraping over the Tor network. This is useful if you've been blocked, either locally or remotely, from the server you're attempting to scrape, or if it's otherwise important to not reaveal your identity.

Pytor allows you to channel simple http requests through a Tor proxy. And it allows you to route mechanize requests through the proxy, meaning you can still have all the benefits of a virtual browser. Pytor also allows you to periodically establish a new Tor identity.

requirements
============
* A functioning (and running) instance of Tor. This could be the basic Tor Browser Bundle. For more configuration options, consider using the Tor Expert Bundle, available from https://www.torproject.org/download/download.html.en. 
* SocksiPy for handling socks requests (unpack to lib/site-packages), available from http://sourceforge.net/projects/socksipy/.
* Mechanize (install through pip)
* Stem (install through pip)


usage 
=====

'''py
from pytor import pytor

tor = pytor()
html = tor.get('http://bradheath.org')
print tor.ip()
tor.new_identity()
print tor.ip()
'''

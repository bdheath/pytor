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

assumptions
===========
For now, Pytor assumes that your Tor control port is set to 9051. If your configuration is different, you can edit the global variables at the top to adjust. **Future versions** will acommodate different ports and authentication passwords.

usage 
=====
Create a basic Pytor instance and send a simple http request:
```Python
from pytor import pytor

tor = pytor()
html = tor.get('http://bradheath.org')
```
Or, if your Tor configuration requires a different host or port:
```python
from pytor import pytor
tor = pytor(host='localhost', port=9055)
html = tor.get('http://bradheath.org')
```

Check the IP address that remote servers will see:
```python
print tor.ip()
```

Download a file:
```python
tor.downloadFile(url, local_filename)
```

Request a new identity from Tor: (Note that the network won't always assign you one, and even when it does, you may end up with the same exit node and therefore the same IP address. Also note that you shouldn't change your identity too ofen to avoid stressing the network.)
```python
tor.newIdentity()
```

Have Pytor periodically assign a new identity. (Note that this currently works with get() and download_file() requests, but does not currently force a new identity when using a mechanize browser. More on that later.)
```python
tor.identityTime(1200)  # Request a new identity every 1200 seconds
```

To create a new instance of a mechanize browser:
```python
br = tor.mechanizeBrowser()
br.open('http://bradheath.org')
# continue using br just like any other mechanize object
```
or
```
tor.mechanizeBrowser()
tor.browser.open('http://bradheath.org')
# etc.
```

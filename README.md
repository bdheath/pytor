Pytor
=====

Pytor is a Python wrapper for scraping over the Tor network. This is useful if you've been blocked (either locally or remotely) from the server you're attempting to scrape, or if it's otherwise important to not reveal your identity.

Pytor allows you to channel simple http requests through a Tor proxy. It also allows you to route more complex Mechanize requests through the proxy if your script needs to emulate a browser. Pytor also allows you to periodically establish a new Tor identity, either directly or by setting a custom interval for the use of a particular identity.

Requirements
============
* A functioning (and running) instance of Tor. This could be the basic Tor Browser Bundle. For more configuration options, consider using the Tor Expert Bundle, available from https://www.torproject.org/download/download.html.en. 
* Mechanize (install through pip)
* Stem (install through pip or apt-get)

Basic usage
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
You can also configure Pytor to set up a control connection to your Tor instance. That enables you to do things like ask Tor to change your circuit. 

```python
tor = pytor( port = 9050, controller = True, controlPort = 9051, password='Your-non-hashed-password')
```

Request a new identity from Tor: (Note that the network won't always assign you one, and even when it does, you may end up with the same exit node and therefore the same IP address. Also note that you shouldn't change your identity too ofen to avoid stressing the network.)
```python
tor.newIdentity()
```

Have Pytor periodically assign a new identity. (Note that this currently works with get() and download_file() requests, but does not currently force a new identity when using a mechanize browser. More on that later.)
```python
tor.identityTime(1200)  # Request a new identity every 1,200 seconds (20 minutes)
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

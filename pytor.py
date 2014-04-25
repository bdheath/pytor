#	PYTOR
#	Lightweight wrapper for web scraping on the Tor network
#	Brad Heath, brad.heath@gmail.com, @bradheath
#
# 	REQUIREMENTS
#	- Functioning (and active) TOR proxy
#	- SocksiPy (socks.py installed to lib/site-packages)
#	- Stem (pip install stem)
#	- Mechanize
#
#

import socks
import socket
import stem
import urllib2
from stem.control import Controller
from stem import Signal
import mechanize
import datetime

class pytor:

	controlPort = 9051
	port = 9050
	host = 'localhost'
	_version = 0.1
	_last_result = None
	_last_request = None
	_id_time = None
	_last_id_time = None
	_ip = None
	_connected = False
	browser = None
	
	try:
		torControl = Controller.from_port(port=controlPort)
		_connected = True
	except:
		_connected = False

	def __init__(self, host='localhost', port=9050):
		if self._connected:
			socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, host, port)
			socket.socket = socks.socksocket
			self._last_id_time = datetime.datetime.now()
		else:
			print "### ERROR: Could not establish a Tor connection!"
		return
		
	def get(self, url):		
		self._checkIdentityTime()
		request = urllib2.Request(url)
		request.add_header('Cache-Control','max-age=0')
		response = urllib2.urlopen(request)
		self._last_result = response.read()
		self._last_request = url
		return self._last_result

	def ip(self):
		self._ip = self.get('http://bradheath.org/ip')
		return self._ip

	def downloadFile(self, url, file):
		self._checkIdentityTime()
		request = urllib2.Request(url)
		request.add_header('Cache-Control','max-age=0')
		request.add_header('User-agent', 'Mozilla/5.0')
		response = urllib2.urlopen(request)
		with open(file, 'wb') as local_file:
			local_file.write(response.read())
		return True

	def newIdentity(self):
		self.torControl.authenticate()
		self.torControl.signal(Signal.NEWNYM)
		self._last_id_time = datetime.datetime.now()
		return True

	def _checkIdentityTime(self):
		if self._id_time != None and self._last_id_time != None:
			if (datetime.datetime.now() - self._last_id_time).seconds >= self._id_time:
				print 'Getting new identity'
				self.newIdentity()
		return
		
	def identityTime(self, time = 600):
		self._id_time = time
		return
		
	def mechanizeBrowser(self):
		self.browser = mechanize.Browser()
		return self.browser


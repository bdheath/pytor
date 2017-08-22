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

import stem
from stem.control import Controller
from stem import Signal
import mechanize
import datetime
import requests

class pytor:

	controlPort = 9051
	port = 9050
	host = 'localhost'
	password = ''
	_version = 0.1
	_last_result = None
	_last_request = None
	_id_time = None
	_last_id_time = None
	_ip = None
	_connected = False
	browser = None
	controller = False
	
	_proxies = {}

	def __init__(self, host='localhost', port=9050, controller=False, controlPort = 9051, password=''):
		self.controlPort = controlPort
		self.port = port
		self.controller = controller
		self._proxies['http'] = 'socks5://localhost:' + str(self.port)
		self._proxies['https'] = 'socks5://localhost:' + str(self.port)
		if self.controller:
			self.torControl = Controller.from_port(port=controlPort)
			self.torControl.authenticate(self.password)
			self._connected = True
		self._last_id_time = datetime.datetime.now()
		return
	
	def request(self, url, timeout = 30):
		self._checkIdentityTime()
		r = requests.get(url, timeout=timeout, proxies=self._proxies)
		self._last_request = url
		self._last_result = r.text
		return r
	
	def get(self, url, t=30):		
		self._checkIdentityTime()

		r = self.request(url, timeout = t)
		
		if r.status_code == 200:
			self._last_result = r.text
			self._last_request = url
			return self._last_result
		else:
			return False

	def ip(self):
		self._ip = self.get('http://bradheath.org/ip')
		return self._ip

	def timeForNew(self):
		self._checkIdentityTime()
		return		
		
	def saveLastResult(file):
		with open(file, 'wb') as local_file:
			local_file.write(self._last_result)
		return
		
	def downloadFile(self, url, file):
		self._checkIdentityTime()
		r = requests.get(url, stream = True, proxies = self._proxies)
		with open(file, 'wb') as local_file:
			for chunk in r.iter_content ( chunk_size = 1024)
				if chunk:
					local_file.write(chunk)
		self._last_request = url
		return True

	def newIdentity(self):
		print "## NEW IDENTITY ## "
		if not self._connected:
			self.torControl = Controller.from_port(port=self.controlPort)
			self.torControl.authenticate(self.password)
			self._connected = True
		self.torControl.authenticate(self.password)
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


#	PYTOR
#	Lightweight wrapper for web scraping on the Tor network
#	Brad Heath, brad.heath@gmail.com, @bradheath
#
# 	REQUIREMENTS
#	- Functioning (and active) TOR proxy
#	- SocksiPy (socks.py installed to lib/site-packages)
#	- Stem (pip install stem)
#	- Mechanize


import socks
import socket
import stem
import urllib2
from stem.control import Controller
from stem import Signal
import mechanize
import datetime

class pytor:

	version = 0.1
	port = 9050
	host = 'localhost'
	last_result = None
	last_request = None
	id_time = None
	last_id_time = None
	ip = None
	browser = None
	
	torControl = Controller.from_port(port=9051)

	def __init__(self, host='localhost', port=9050):
		socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, host, port)
		socket.socket = socks.socksocket
		self.last_id_time = datetime.datetime.now()
		return
		
	def get(self, url):		
		self.check_identity_time()
		request = urllib2.Request(url)
		request.add_header('Cache-Control','max-age=0')
		response = urllib2.urlopen(request)
		self.last_result = response.read()
		self.last_request = url
		return self.last_result

	def ip(self):
		self.ip = self.get('http://ifconfig.me/ip')
		return self.ip

	def download_file(self, url, file):
		self.check_identity_time()
		request = urllib2.Request(url)
		request.add_header('Cache-Control','max-age=0')
		request.add_header('User-agent', 'Mozilla/5.0')
		response = urllib2.urlopen(request)
		with open(file, 'wb') as local_file:
			local_file.write(response.read())
		return True

	def new_identity(self):
		self.torControl.authenticate()
		self.torControl.signal(Signal.NEWNYM)
		self.last_id_time = datetime.datetime.now()
		return True

	def check_identity_time(self):
		if self.id_time != None and self.last_id_time != None:
			if (datetime.datetime.now() - self.last_id_time).seconds >= self.id_time:
				print 'Getting new identity'
				self.new_identity()
		return
		
	def identity_time(self, time = 600):
		self.id_time = time
		return
		
	def mechanize_browser(self):
		self.browser = mechanize.Browser()
		return self.browser
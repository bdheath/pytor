from pytor import pytor
import urllib2

ip = urllib2.urlopen('http://bradheath.org/ip').read()
tor = pytor(controller=True, controlPort = 9051, port = 9060, password='YOURPASSWORD')

print "Without Tor, my IP address is     : " + ip
print "With Tor, my IP address is        : " + tor.ip()
tor.newIdentity()
print "Now my IP address is              : " + tor.ip()


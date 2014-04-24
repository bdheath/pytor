from pytor import pytor

tor = pytor()

print "My IP address is: " + tor.ip()
tor.newIdentity()
print "Now my IP address is: " + tor.ip()


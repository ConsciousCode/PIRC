import irc
import time

user=irc.User("Test")
server=irc.Server("jq.dyndns-free.com")
server.connect(user)
server.join("#u413")

while True:
	for sent in server.channels["#u413"].get_data():
		if sent["cmd"]=="MSG":
			print "<%s> %s"%(sent["user"],sent["params"])
		elif sent["cmd"]=="ME":
			print "*** %s %s"%(sent["user"],sent["params"])
		else:
			print sent["params"]
	time.sleep(0.5)
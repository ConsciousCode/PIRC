class metadata:
	name="output"
	version="1.0.0.0"
	description="Outputs the received data into the console."
	type="Reaction"

def action(bot,data):
	if data["cmd"]=="MSG":
		print "<%s> %s"%(data["user"],data["params"])
	elif data["cmd"]=="ME":
		print "*** %s %s"%(data["user"],data["params"])
	else:
		print "%s sent %s %s"%(data["user"],data["cmd"],data["params"])
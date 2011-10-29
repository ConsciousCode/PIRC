class metadata:
	name="sendraw"
	version="1.0.0.0"
	description="Send a raw command to the server"
	type="Command"
	usage="SENDRAW <raw command>"
	params={"raw command":"The raw command to send to the server"}

def action(bot,io,data):
	io.sendraw(data["params"])
class metadata:
	name="say"
	version="1.0.0.0"
	description="Makes the bot say something."
	type="Command"
	usage="SAY <text>"
	params={"text":"Text to output"}

def action(bot,io,data):
	return data["params"]
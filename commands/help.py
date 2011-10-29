class metadata:
	name="help"
	version="1.0.0.0"
	description="Prints the help data"
	type="Command"
	usage="HELP [command]"
	params={"command":"The command to give in-depth information about"}

def action(bot,io,data):
	if data["params"]=="":
		s="%s Help\r\n----------------\r\n"%bot.name
		if len(bot.types["Command"][0])>0:
			s+="Commands:\r\n"
			for name in bot.types["Command"][0]:
				s+="    %s - %s\r\n"%(name,bot.types["Command"][0][name].description)
		if len(bot.types["Reaction"][0])>0:
			s+="\r\n    Reactions:\r\n"
			for name in bot.types["Reaction"][0]:
				s+="    %s - %s\r\n"%(name,bot.types["Reaction"][0][name].description)
		if len(bot.types["Modifier"][0])>0:
			s+="\r\n    Modifiers:\r\n"
			for name in bot.types["Modifier"][0]:
				s+="    %s - %s\r\n"%(name,bot.types["Modifier"][0][name].description)
		if len(bot.types["Service"][0])>0:
			s+="\r\n    Services:\r\n"
			for name in bot.types["Service"][0]:
				s+="    %s - %s\r\n"%(name,bot.types["Service"][0][name].description)
	else:
		cmd=data.split()[0]
		if cmd in bot.types["Command"]:
			s=bot.types["Command"][0][cmd].usage
			for arg in bot.types["Command"][0][cmd].params:
				s+="\r\n    %s - %s"%(arg,bot.types["Command"][0][cmd].params[arg])
		else:
			s="Non-command help not yet implemented"
	return s
class metadata:
	name="mode"
	version="1.0.0.0"
	description="Toggle a modifier"
	type="Command"
	usage="ON <mode>"
	params={"mode":"The mode to turn on"}
	
def action(bot,io,data):
	data["params"]=data["params"].lower()
	if data["params"] in bot.types["Modifier"][0]:
		if bot.types["Modifier"][0][data["params"]].active:
			bot.types["Modifier"][0][data["params"]].active=False
			return data["params"].title()+" modifier has been deactivated."
		else:
			bot.types["Modifier"][0][data["params"]].active=True
			return data["params"].title()+" modifier has been activated."
	else:
		return data["params"].title()+" is not a modifier."
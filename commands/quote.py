import random

class metadata:
	name="quote"
	version="1.0.0.0"
	description="quote"
	type="Command"
	usage="QUOTE [newquote]"
	params={"newquote":"A new quote to add to the quote database"}

def init(bot):
	quotefile=open("quotes.txt","r+")
	bot.quotes=quotefile.readlines()
	quotefile.close()

def action(bot,io,data):
	with open("quotes.txt","r+") as quotefile:
		bot.quotes=quotefile.readlines()
		if data["params"]=="":
			return bot.quotes[random.randrange(0,len(bot.quotes))-1]
		else:
			bot.quotes.append('"'+data["params"]+'" ~ '+data["user"])
			quotefile.write('\n"'+data["params"]+'" ~ '+data["user"])
			return "Quote has been added"
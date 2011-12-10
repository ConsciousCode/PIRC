import bot
import types
import string
import os

class metadata:
	name="command"
	version="1.0.0.0"
	description="Provides a system through which commands can be implemented."
	type="Reaction"

deliminator="@"

class Command(bot.Bot.Module):
	def __init__(self,fname):
		super(Command,self).__init__(fname)
		if "usage" in dir(self.mod.metadata):
			self.usage=self.mod.metadata.usage
		else:
			self.usage=self.name.upper()
		if "params" in dir(self.mod.metadata):
			self.params=self.mod.metadata.params
		else:
			self.params={}

def init(bot):
	if "Command" not in bot.types:
		bot.types.update({"Command":({},Command)})

def action(bot,io,data):
	words=data["params"].split()
	if words[0][0]==deliminator:
		if words[0][1:] in bot.types["Command"][0]:
			try:
				data["params"]=string.join(words[1:])
				return bot.types["Command"][0][words[0][1:]].action(bot,io,data)
			except Exception as e:
				print e

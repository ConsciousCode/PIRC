import bot
import types
import string
import os

class metadata:
	name="command"
	version="1.0.0.0"
	description="Provides a system through which commands can be implemented."
	type="Reaction"

deliminator="!"

class Command(bot.Bot.Module):
	def __init__(self,fname):
		super(Command,self).__init__(fname)
		if "action" not in dir(self.mod):
			raise NameError("action not defined in Command module")
		self.action=self.mod.action

def add_command(self,fname):
	cmd=Command(fname)
	self.commands.update({cmd.name:cmd})
	if "init" in dir(cmd.mod):
		cmd.mod.init(self)

def load_commands(self):
	#load commands
	listing=os.listdir(cmddir)
	for f in listing:
		path=os.path.splitext(f)
		if path[1]==".py":
			mod=imp.load_source(path[0])
			if mod.metadata.type=="Command":
				self.add_command(path[0])
			else:
				self.load_module(path[0])

def init(bot):
	global add_command
	#bind add_command to bot
	add_command=types.MethodType(add_command,bot,type(bot))
	bot.add_command=add_command
	#bind load_commands to bot
	load_commands=types.MethodType(load_commands,bot,type(bot))
	bot.load_commands=load_commands
	#create a dictionary of commands
	bot.commands={}

def action(bot,data):
	words=data["params"].split()
	if words[0][0]==deliminator:
		if words[0][1:] in bot.commands:
			return bot.commands[words[0][1:]].action(bot,string.join(words[1:]))

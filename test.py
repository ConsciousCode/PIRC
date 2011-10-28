import time
import irc

user=irc.User("PIbot")
server=irc.Server("jq.dyndns-free.com")
server.connect(user)
server.join("#u413")

import bot

bot=bot.Bot("PIbot","","A bot test")
bot.add_stream(server.channels["#u413"])
bot.load_module("output")
bot.load_module("command")
bot.add_command("say")
bot.run()
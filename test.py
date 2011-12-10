import time
import irc

user=irc.User("PIbot")
jqserver=irc.Server("jq.dyndns-free.com")
jqserver.connect(user)
jqserver.join("#u413")

import bot

bot=bot.Bot("PIbot","1.0.0.0","A multi-purpose chat bot.")
bot.add_stream(jqserver.channels["#u413"])

bot.load_modules("modifiers/")
bot.load_modules("reactions/")
bot.load_modules("services/")
bot.load_modules("commands/")

bot.run()
# -*- coding: utf-8 -*-

"""
MIT License

Copyright (c) 2019 J16N

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""


import discord, coc
import asyncio, os, asyncpg
import configparser
from discord.ext.commands import Bot
from coc import Client



# +++++++++ Configurations ++++++++++++

config = configparser.RawConfigParser()
config.read("config.txt")

# +++++++++++++++++++++++++++++++++++++


# Command prefix for using the bot
BOT_PREFIX = [
	't- ', 'T- ', 
	't-', 'T-', 
	'<@554689083289632781> ', '<@554689083289632781>'
]

cogs = ['cogs.translate', 'cogs.coc', 'cogs.utils', 'cogs.help', 'cogs.game', 'cogs.entertainment']



async def run():
	'''Run the bot and connect to the database'''

	bot = Bot(
		description="I am your next generation discord bot.",
		command_prefix=BOT_PREFIX,
		case_insensitive=True
	)

	# +++++++++++++++++++++++++++++++++ COC Client +++++++++++++++++++++++++++++++++++++++++++++++++++

	bot.coc = Client()
	bot.coc.create_cache
	await bot.coc.login(config.get("my-config", "coc_email"), config.get("my-config", "coc_password"))

	# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

	
	# %%%%%%%%%%%%% Database Setup %%%%%%%%%%%%%%%%%%

	bot.pool = await asyncpg.create_pool(
		host=config.get("my-config", "host"), 
		database=config.get("my-config", "database"), 
		user=config.get("my-config", "user"), 
		password=config.get("my-config", "password")
	)

	# &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&

	for cog in cogs:
		bot.load_extension(cog)


	#these things are absolutely for help command
	# -------------------------------------------

	bot.temp_user = {}
	bot.categories = list(set([cog for cog in bot.cogs])) # this is to remove duplicates
	bot.allcommands = list(set([command.qualified_name for command in bot.walk_commands() if not command.hidden]))
	bot.help_prefix = (
		't- help', 'T- help', 
		't-help', 'T-help', 
		'<@554689083289632781> help', '<@554689083289632781>help'
	)

	# +++++++++++++++++++++++++++++++++++++++++++


	# running our bot with the token finally
	try:
		await bot.start(config.get("my-config", "TOKEN"))
	
	except:
		# Make sure to do these steps if you use a command to exit the bot
		await bot.pool.close()
		await bot.logout()


loop = asyncio.get_event_loop()
loop.run_until_complete(run())

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


import discord
from discord.ext import commands
import asyncio
import os
import asyncpg
import configparser

# Command prefix for using the bot
BOT_PREFIX = [
	't- ', 'T- ', 
	't-', 'T-', 
	'<@554689083289632781> ', '<@554689083289632781>'
]

cogs = ['cogs.translate', 'cogs.coc', 'cogs.utils', 'cogs.help', 'cogs.game', 'cogs.fun']

async def run():
	'''Runs the bot and connect to the database'''

	bot = commands.Bot(command_prefix=BOT_PREFIX, case_insensitive=True)

	bot.config = configparser.RawConfigParser()
	bot.config.read("config.txt")

	bot.pool = await asyncpg.create_pool(
		host=bot.config.get("my-config", "host"), 
		database=bot.config.get("my-config", "database"), 
		user=bot.config.get("my-config", "user"), 
		password=bot.config.get("my-config", "password")
	)

	for cog in cogs:
		bot.load_extension(cog)

	# bot token, VERY IMPORTANT
	token = bot.config.get("my-config", "TOKEN")

	# running our bot with the token finally
	try:
		await bot.start(token)
	except:
		# Make sure to do these steps if you use a command to exit the bot
		await db.close()
		await bot.logout()


loop = asyncio.get_event_loop()
loop.run_until_complete(run())

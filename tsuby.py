import discord
from discord.ext import commands
import asyncio
import os

# Command prefix for using the bot
BOT_PREFIX = [
	't-', 'T-', 
	't -', 'T -',
	't- ', 'T- ',
]

bot = commands.Bot(command_prefix=BOT_PREFIX, case_insensitive=True)

cogs = ['cogs.translate', 'cogs.coc', 'cogs.utils', 'cogs.help', 'cogs.game', 'cogs.fun']

for cog in cogs:
	bot.load_extension(cog)


# bot token, VERY IMPORTANT
token = os.environ.get("TOKEN")
# running our bot with the token finally
bot.run(token)
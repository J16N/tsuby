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
from discord.ext.commands.cooldowns import BucketType
import asyncio

class Help(commands.Cog):

	def __init__(self, bot):
		self.bot = bot

	@commands.command()
	@commands.cooldown(10,600,type=BucketType.member)
	async def help(self, ctx):
		'''Displays the help command'''

		embed = discord.Embed(description="*I found the following list of commands. The prefix and commands are case-insensitive.*", color=0xA78BE1)
		embed.set_author(name="Help")
		
		embed.add_field(name="**t-clear <number>(int) <mentioned_user>(optional)**", value="`└─ Deletes all the messages of a channel. The <number> is used to search the total number of messages. Put 0 if you want me to search through all the messages.\nThe optional <mentioned_user> is given to delete the message of that particular user. Remember that the <number> used will not necessarily delete the total number of messages of the <mentioned_user>.`", inline=False)
		embed.add_field(name="**t-feedback <your_feedback>**", value="`└─ Sends feedback to my owner.`", inline=False)
		embed.add_field(name="**t-info**", value="`└─ Lists some general info about me.`", inline=False)
		embed.add_field(name="**t-invite**", value="`└─ Invite me to your server.`", inline=False)
		embed.add_field(name="**t-nitromojis**", value="`└─ Lists all my nitromojis.`", inline=False)
		embed.add_field(name="**t-ne [<nitromoji>, <nitromoji> ... <nitromoji>]**", value="`└─ Sends all the list of nitromojis. The alias of this command is 't-nitro'`", inline=False)
		embed.add_field(name="**t-ping**", value="`└─ Ping me.`", inline=False)
		embed.add_field(name="**t-react [<emoji>, <emoji> ... <nitromoji>]**", value="`└─ Reacts to the last message of any user with the following list of emojis.` \n\n**─── Main Commands ───**", inline=False)
		
		embed.add_field(name="**t-9gag help**", value="`└─ 1 command. All my available memes related commands.`", inline=False)
		embed.add_field(name="**t-coc help**", value="`└─ 2 commands. All my Clash Of Clans related commands.`", inline=False)
		embed.add_field(name="**t-game help**", value="`└─ 2 command. All my available games and their related commands.`", inline=False)
		embed.add_field(name="**t-jokes help**", value="`└─ 1 command. All my available jokes related commands.`", inline=False)
		embed.add_field(name="**t-tr help**", value="`└─ 7 commands. All my translation related commands.`", inline=False)
		embed.set_footer(text="I am glad to help you out :D", icon_url="https://raw.githubusercontent.com/J16N/tsuby/master/assets/tsuby-footer.png")

		if ctx.message.guild is not None:
			await ctx.message.add_reaction("📧")

		await ctx.author.send(embed=embed)

def setup(bot):
	# Add the cog
	bot.remove_command("help")
	bot.add_cog(Help(bot))
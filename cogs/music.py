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


import os
import discord
from discord.ext import commands
from discord.ext.commands.cooldowns import BucketType
import spotify

class Music(commands.Cog):

	def __init__(self, bot):

		self.bot = bot

		self.client_id = os.environ.get("spotify_client")
		self.client_secret = os.environ.get("spotify_secret")
		self.client_token = None


	@commands.group(case_insensitive=True)
	@commands.cooldown(10,600,type=BucketType.member)
	@commands.guild_only()
	async def music(self, ctx):
		'''This is our main music command. Other commands are just sub-commands of this.'''

		if ctx.invoked_subcommand is None:
			await ctx.send('`t-music help`')


	@music.command()
	@commands.guild_only()
	async def spotify(self, ctx, song_data):
		'''Streams directly from spotify'''





		



def setup(bot):
	bot.add_cog(Music(bot))
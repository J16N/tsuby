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
import traceback
import re
import os
from datetime import datetime
import pytz

start_time = datetime.utcnow() # Timestamp of when Tsuby comes online

class Utils(commands.Cog):

	def __init__(self, bot):

		self.bot = bot

		#react regex
		self.react_regex = open('emoji_regex.txt', 'r').read()

		#feedback file if present then load the feedback number from it
		if os.path.isfile("feedback.txt") and os.stat("feedback.txt").st_size != 0:
			self.feedback = int(open("feedback.txt").read())
		else:
			self.feedback = 1

	async def status_task(self):
		'''Change the bot presence every time'''
		while True:
			await self.bot.change_presence(status=discord.Status.do_not_disturb, activity=discord.Activity(type=discord.ActivityType.playing, name='Hello I Am Tsuby'))
			await asyncio.sleep(10)
			
			await self.bot.change_presence(status=discord.Status.do_not_disturb, activity=discord.Activity(type=discord.ActivityType.playing, name='Default prefix: \'t-\''))
			await asyncio.sleep(10)
			
			await self.bot.change_presence(status=discord.Status.do_not_disturb, activity=discord.Activity(type=discord.ActivityType.watching, name='Everyone!'))
			await asyncio.sleep(15)

			await self.bot.change_presence(status=discord.Status.do_not_disturb, activity=discord.Activity(type=discord.ActivityType.listening, name='Everyone!'))
			await asyncio.sleep(15)

	@commands.Cog.listener()
	async def on_ready(self):
		'''Things to perform when the bot gets ready'''

		print(f"The api version is {discord.__version__}")
		print("I'm in")
		print(self.bot.user)
		print(f"Guilds: {len(self.bot.guilds)}")
		print("\nInvite Link: https://discordapp.com/api/oauth2/authorize?client_id=554689083289632781&permissions=8&scope=bot")
		self.bot.loop.create_task(self.status_task())	


	

	@commands.command()
	@commands.cooldown(10,600,type=BucketType.member)
	async def ping(self, ctx):
		'''Pings the bot'''
		
		if ctx.message.guild is not None:
			await ctx.send(f"{ctx.author.mention}, ***PONG!*** (~{round(self.bot.latency*1000)}ms)", delete_after=3.0)

			if ctx.me.permissions_in(ctx.message.channel).manage_messages:
				# delete the message command
				await ctx.message.delete(delay=3.0)

		else:
			await ctx.send(f"***PONG!*** (~{round(self.bot.latency*1000)}ms)")


	

	@commands.command(name='nitromojis', aliases=['nitroemojis'])
	@commands.cooldown(10,600,type=BucketType.member)
	async def nitromojis(self, ctx):
		'''Lists all the nitromojis'''

		await ctx.message.channel.trigger_typing()

		# list of names of custom animated emojis
		emoji_list = [emoji.name for emoji in self.bot.get_guild(372348786917507074).emojis if emoji.animated] + \
			[emoji.name for emoji in self.bot.get_guild(611086977457979403).emojis if emoji.animated] + \
			[emoji.name for emoji in self.bot.get_guild(576442836157857792).emojis if emoji.animated]

		emoji_list = sorted(emoji_list)


		# I have to split this because no field must contain more than 1024 characters
		emoji_help1 = ''
		emoji_help2 = ''
		emoji_help3 = ''
		emoji_help4 = ''
		emoji_help5 = ''
		emoji_help6 = ''

		for emoji in emoji_list[:18]:
			emoji_help1 += f"*{emoji}* : {discord.utils.get(self.bot.emojis, name=emoji)}\n\n"

		for emoji in emoji_list[18:36]:
			emoji_help2 += f"*{emoji}* : {discord.utils.get(self.bot.emojis, name=emoji)}\n\n"

		for emoji in emoji_list[36:54]:
			emoji_help3 += f"*{emoji}* : {discord.utils.get(self.bot.emojis, name=emoji)}\n\n"

		for emoji in emoji_list[54:72]:
			emoji_help4 += f"*{emoji}* : {discord.utils.get(self.bot.emojis, name=emoji)}\n\n"

		for emoji in emoji_list[72:90]:
			emoji_help5 += f"*{emoji}* : {discord.utils.get(self.bot.emojis, name=emoji)}\n\n"

		for emoji in emoji_list[90:]:
			emoji_help6 += f"*{emoji}* : {discord.utils.get(self.bot.emojis, name=emoji)}\n\n"

		embed = discord.Embed(description='***NITROMOJIS***', color=0xF5C46F)
		embed.add_field(name='\u200b', value = emoji_help1, inline=True)
		embed.add_field(name='\u200b', value = emoji_help2, inline=True)
		embed.add_field(name='\u200b', value = emoji_help3, inline=True)
		embed.add_field(name='\u200b', value = emoji_help4, inline=True)
		embed.add_field(name='\u200b', value = emoji_help5, inline=True)
		embed.add_field(name='\u200b', value = emoji_help6, inline=True)
		embed.set_footer(text="The prefix of every nitromojis is 't'.", icon_url="https://raw.githubusercontent.com/J16N/tsuby/master/assets/tsuby-footer.png")
		
		await ctx.send(embed=embed, delete_after=120.0)

		if ctx.me.permissions_in(ctx.message.channel).manage_messages:
			# delete the message command
			await ctx.message.delete(delay=120.0)


	

	@commands.command(name="ne", aliases=['nitro', 'nitroemoji', 'nitromoji'])
	@commands.cooldown(10,600,type=BucketType.member)
	async def nitromoji(self, ctx, *names):
		'''Send the nitromoji'''

		await ctx.message.channel.trigger_typing()

		if names:

			if ctx.me.permissions_in(ctx.message.channel).manage_messages:
				# delete the message command
				await ctx.message.delete()

			# make all the names lowercase
			#names = [name.lower().replace(":", "") for name in names]
			
			# list of names of custom animated emojis
			#emoji_list = [emoji.name for emoji in self.bot.get_guild(372348786917507074).emojis if emoji.animated] + \
				#[emoji.name for emoji in self.bot.get_guild(611086977457979403).emojis if emoji.animated] + \
				#[emoji.name for emoji in self.bot.get_guild(576442836157857792).emojis if emoji.animated]

			# here I could have used set intersection but I didn't because that won't work for repititive emojis 
			#emoji_names = [name for name in names if name in emoji_list]

			#if emoji_names:

				#emoji_message = [str(discord.utils.get(self.bot.emojis, name=name)) for name in emoji_names]

				# now send the message
				#await ctx.send(''.join(emoji_message))


			emojis = []

			for name in names:
				# literally from here we will going to seperate out all the unicode emojis from custom ones so that bot
				# can send both

				unicode_emoji = re.search(self.react_regex, name)

				if not unicode_emoji:
					try:
						emoji = await commands.EmojiConverter().convert(ctx, name)
					except:
						continue
				else:
					emoji = name

				emojis.append(str(emoji))


			if emojis:
				await ctx.send(''.join(emojis))

			else:
				await ctx.send('*The emoji with that name does not exist.* \nType `t-nitromojis` to get the list.', delete_after=5.0)
		
		else:
			await ctx.send('Type `t-nitromojis` to get the list of nitromojis. \n**Usage: ** `t-ne [<nitromoji> <nitromoji> ... <nitromoji>]`', delete_after=10.0)

			if ctx.me.permissions_in(ctx.message.channel).manage_messages:
				# delete the message command
				await ctx.message.delete(delay=10.0)




	

	@commands.command()
	@commands.cooldown(10,600,type=BucketType.member)
	async def react(self, ctx, number, *reactions):
		'''Reacts to the last message'''

		if reactions:

			if ctx.me.permissions_in(ctx.message.channel).manage_messages:
				# delete the message command
				await ctx.message.delete()

			try:
				message = await commands.MessageConverter().convert(ctx, number)
			except:
				message = None
				try:
					number = int(number)
					message_list = await ctx.message.channel.history(limit=number+1, before=ctx.message).flatten()
				except:
					await ctx.send("*I don't see any message to react in this channel.*", delete_after=3.0)

			#react = re.findall(self.react_regex, ' '.join(reactions))
			#reactions = set(reactions) - set(react)

			#if reactions: # here the bot will react with custom emotes

				#emoji_list = [emoji.name for emoji in self.bot.get_guild(372348786917507074).emojis if emoji.animated] + \
					#[emoji.name for emoji in self.bot.get_guild(611086977457979403).emojis if emoji.animated] + \
					#[emoji.name for emoji in self.bot.get_guild(576442836157857792).emojis if emoji.animated]
				#reactions = list(reactions.intersection(reactions)) #removing duplicates
				#emoji_names = [name.replace(":", "") for name in reactions if name.replace(":", "") in emoji_list]
				#react = react + [discord.utils.get(self.bot.emojis, name=name) for name in emoji_names]

				#for reaction in react:
					#await message[0].add_reaction(reaction)

			#else:
				
				#for reaction in react:
					#await message[0].add_reaction(reaction)


			reactions = list(set(reactions) & set(reactions))
			react = []

			for reaction in reactions:

				unicode_emoji = re.search(self.react_regex, reaction)

				if not unicode_emoji:
					try:
						emoji = await commands.EmojiConverter().convert(ctx, reaction)
					except:
						continue
				else:
					emoji = reaction

				
				react.append(str(emoji))

			
			for reaction in react:
				if not message:
					await message_list[number].add_reaction(reaction)
				else:
					await message.add_reaction(reaction)


		else:
			await ctx.send('`t-react [<emoji> <emoji> ... <nitromoji> <nitromoji>]`', delete_after=10.0)

			if ctx.me.permissions_in(ctx.message.channel).manage_messages:
				# delete the message command
				await ctx.message.delete(delay=10.0)



	




	@commands.command()
	@commands.cooldown(10,600,type=BucketType.member)
	@commands.guild_only()
	async def feedback(self, ctx, *, message=None):
		'''Sends feedback to the developer'''
		
		if message:

			if ctx.me.permissions_in(ctx.message.channel).manage_messages:
				# delete the message command
				await ctx.message.delete()

			await ctx.message.channel.trigger_typing()

			tz = pytz.timezone ("Asia/Kolkata")
			utc_time = datetime.utcnow()
			date_time = pytz.utc.localize(utc_time, is_dst=None).astimezone(tz).strftime("%m-%d-%Y, %I:%M:%S %p")

			channel = self.bot.get_channel(586473048841125889)

			message = f"*{date_time}*\n\n"+message

			embed = discord.Embed(color=0x9BD362)
			embed.set_author(name=ctx.author.name+"#"+ctx.author.discriminator, icon_url=ctx.author.avatar_url)
			embed.add_field(name=f"**Feedback #{self.feedback}**", value=message)
			embed.set_footer(text = f"From {ctx.guild.name}", icon_url=ctx.guild.icon_url)
			await channel.send(embed=embed)
			
			#notify user that their feedback has been sent
			await ctx.send("*Your feedback has been sent successfully.* :white_check_mark:", delete_after=5.0)

			self.feedback += 1 #updating our feedback number

			# saving the contents in a file.
			feedback_file = open("feedback.txt", "w")
			feedback_file.write(str(self.feedback))
			feedback_file.close()

		else:
			await ctx.send("`t-feedback <feedback_message>`", delete_after=5.0)

			if ctx.me.permissions_in(ctx.message.channel).manage_messages:
				# delete the message command
				await ctx.message.delete(delay=5.0)


	




	@commands.command()
	@commands.cooldown(10,600,type=BucketType.member)
	async def invite(self, ctx):
		'''Returns an invite url'''

		url = "https://discordapp.com/api/oauth2/authorize?client_id=554689083289632781&permissions=8&scope=bot"
		await ctx.send(f"*Invite me using this url*\n{url}")


	




	@commands.command()
	@commands.cooldown(10,600,type=BucketType.member)
	async def about(self, ctx):
		'''Lists some info about Tsuby'''

		url = "https://discordapp.com/api/oauth2/authorize?client_id=554689083289632781&permissions=8&scope=bot"

		now = datetime.utcnow()
		delta = now - start_time
		hours, remainder = divmod(int(delta.total_seconds()), 3600)
		minutes, seconds = divmod(remainder, 60)
		days, hours = divmod(hours, 24)
		
		if days:
			time_format = "**{d}** `days` **{h}** `hours` **{m}** `minutes` **{s}** `seconds`"
		else:
			time_format = "**{h}** `hours` **{m}** `minutes` **{s}** `seconds`"
		
		uptime_stamp = time_format.format(d=days, h=hours, m=minutes, s=seconds)

		embed = discord.Embed(description=f"Hey there {ctx.author.name}!\n*Seems like you're getting interested in me.* <a:tcowboy:581728970483957761>\nYou can [`invite`]({url}) me to your server. <a:tpandarun:574530725475516432>", color=0x9FFA99)
		embed.set_author(name="About Me")
		embed.set_footer(text="I believe every Humans and bots can mutually thrive on this planet.", icon_url="https://raw.githubusercontent.com/J16N/tsuby/master/assets/tsuby-footer.png")
		embed.add_field(name="**My Creator**", value="`Tsubasa#7917`")
		embed.add_field(name="**My Supporter**", value="`Linus#0002`")
		embed.add_field(name="**My Name-Giver**", value="`Zaxs Souven#4045`")
		embed.add_field(name="**Watching Servers**", value=f"`{len(self.bot.guilds)}`")
		embed.add_field(name="**Uptime**", value=f"{uptime_stamp}")
		embed.add_field(name="**Remark**", value="I am getting smarter everyday...\nI hope will do the welfare to the mankind soon.")

		await ctx.send(embed=embed)


	@commands.command()
	@commands.guild_only()
	@commands.has_permissions(manage_messages=True)
	@commands.cooldown(10,600,type=BucketType.member)
	async def clear(self, ctx, number=None, mention=None):
		'''Clears the given number of messages'''

		try:
			number = int(number)

			if mention:
				member = await commands.MemberConverter().convert(ctx, mention)

			def check_user(user):
				if mention:
					return user.author == member
				else:
					return True

			if number == 0:
				await ctx.message.channel.purge(check=check_user)
			else:
				number += 1
				await ctx.message.channel.purge(limit=number, check=check_user)

		except:
			ctx.send("`t-clear <total_messages_to_search_through>(int) <mentioned_users>(optional)`", delete_after=5.0)

			if ctx.me.permissions_in(ctx.message.channel).manage_messages:
				# delete the message command
				await ctx.message.delete(delay=5.0)



	



	def owner():	
		def bot_owner(ctx):
			return ctx.message.author.id == 302467968095223820 

		return commands.check(bot_owner)


	


	@commands.command()
	@owner()
	async def announce(self, ctx, *, message):
		'''Announce new features to all the servers'''

		for guild in self.bot.guilds:
			
			general = discord.utils.get(guild.text_channels, name='general')
			announcement = discord.utils.get(guild.text_channels, name='announcement')

			if announcement and announcement.permissions_for(guild.me).send_messages:
				await announcement.send(message)

			elif general and general.permissions_for(guild.me).send_messages:
				await general.send(message)

			else:
				for channel in guild.text_channels:
					try:
						await channel.send(message)
						break
					except:
						continue


	


	@commands.Cog.listener()
	async def on_guild_join(self, guild):
		'''When the bot joins the guild'''

		general = discord.utils.get(guild.text_channels, name='general')
		welcome = discord.utils.get(guild.text_channels, name='welcome')

		if welcome and welcome.permissions_for(guild.me).send_messages:
			await welcome.send('**Thanks for inviting me to your server.** <a:tsmileface:581728033967177744>')

		elif general and general.permissions_for(guild.me).send_messages:
			await general.send('**Thanks for inviting me to your server.** <a:tsmileface:581728033967177744>')

		else:	
			for channel in guild.text_channels:
				try:
					await channel.send('**Thanks for inviting me to your server.** <a:tsmileface:581728033967177744>')
					break
				except:
					continue


	
	@commands.Cog.listener()
	async def on_message(self, message):
		'''When someone mentions Tsuby'''

		ctx = await self.bot.get_context(message)

		if not ctx.valid:
			if message.guild:
				if message.guild.me.mentioned_in(message):
					await message.add_reaction('<a:tsparklingheart:594132183669538826>')
			else:
				if self.bot.user.mentioned_in(message):
					await message.add_reaction('<a:tsparklingheart:594132183669538826>')

def setup(bot):
	bot.add_cog(Utils(bot))
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


# Load important modules
import discord
from discord.ext import commands
from discord.ext.commands.cooldowns import BucketType
from aiogoogletrans import Translator, LANGUAGES, LANGCODES
import asyncio
import random
import re
import os
import asyncpg

class Translate(commands.Cog):

	def __init__(self, bot):

		self.bot = bot
		
		# Instantiates a translator client
		self.translator = Translator()

		# making a list of languages and codes
		# i am making this into two halves because there is a sent message limit in discord
		self.first_half_codes = ""
		self.second_half_codes = ""
		self.third_half_codes = ""

		for key, value in list(LANGCODES.items())[:36]:
			self.first_half_codes += "\n*{}*\n`{}`\n".format(key.capitalize(), value)

		for key, value in list(LANGCODES.items())[36:72]:
			self.second_half_codes += "\n*{}*\n`{}`\n".format(key.capitalize(), value)

		for key, value in list(LANGCODES.items())[72:]:
			self.third_half_codes += "\n*{}*\n`{}`\n".format(key.capitalize(), value)

		#emoji regex
		self.emoji_regex = open('emoji_regex.txt', 'r').read()

		# if the message starts with these things, we'll ignore translating them. they usually
		# contain bot prefixes
		if os.path.isfile("ignore.txt") and os.stat("ignore.txt").st_size != 0:
			self.ignore = open("ignore.txt").read().splitlines()

		else:
			self.ignore = [
				't-', 'T-', 't -', 'T -',
				't- ', 'T- ', '-', '.', '?', 
				'tr?', '+', '^', '*', '='
			]


	@commands.group(case_insensitive=True)
	@commands.cooldown(10,600,type=BucketType.member)
	async def tr(self, ctx):
		'''The main translation command. Other commands are just sub commands of this'''
		if ctx.invoked_subcommand is None:
			temp = await ctx.send('`t-tr help`')

			await temp.delete(delay=3.0)

			if ctx.me.permissions_in(ctx.message.channel).manage_messages:
				# delete the message command
				await ctx.message.delete(delay=3.0)

	@tr.group(case_insensitive=True)
	async def auto(self, ctx):
		'''This is a sub-sub command'''
		if str(ctx.invoked_subcommand) == 'tr auto':
			temp = await ctx.send('`t-tr auto help`')

			await temp.delete(delay=3.0)

			if ctx.me.permissions_in(ctx.message.channel).manage_messages:
				# delete the message command
				await ctx.message.delete(delay=3.0)

	@tr.group(case_insensitive=True)
	async def ch(self, ctx):
		'''This is a sub-sub command'''
		if str(ctx.invoked_subcommand) == 'tr ch':
			temp = await ctx.send('`t-tr ch help`')

			await temp.delete(delay=3.0)

			if ctx.me.permissions_in(ctx.message.channel).manage_messages:
				# delete the message command
				await ctx.message.delete(delay=3.0)


	@tr.command()
	async def help(self, ctx):
		'''Help command for translate'''

		embed = discord.Embed(description="*I found the following list of commands.*", color=0xC0C0C0)
		
		embed.set_author(name="Help")
		embed.add_field(name="**t-tr codes**", value="`└─ Displays the list of language codes.`", inline=False)
		embed.add_field(name="**t-tr fr <dest.> <src> [<user> <user> ... <user>] (Admin-only)**", value="`└─ Enables auto translation of the messages to the 'dest.' language from the 'src' language of all the mentioned 'user'`", inline=False)
		embed.add_field(name="**t-tr ignore [<word> <word> ... <word>] (Admin-only)**", value="`└─ Ignores auto-translating the message when started with the given words. Usually 'word' contain other bot's prefixes. \nWarning: Once the words is added, it cannot be removed.`", inline=False)
		embed.add_field(name="**t-tr remove [<user> <user> ... <user>] (Admin-only)**", value="`└─ Disables auto translation of all the mentioned 'user'.`", inline=False)
		embed.add_field(name="**t-tr to <dest.> <src> <message>**", value="`└─ Translates the message to the 'dest.' language from the 'src' language.` \n\n**─── Sub Commands ───**", inline=False)
		embed.add_field(name="**t-tr auto**", value="`└─ 2 commands.`", inline=True)
		embed.add_field(name="**t-tr ch**", value="`└─ 2 commands.`", inline=True)

		embed.set_footer(text="Type t-help to get the list of all commands", icon_url="https://raw.githubusercontent.com/J16N/tsuby/master/assets/tsuby-footer.png")

		if ctx.message.guild is not None:
			await ctx.message.add_reaction("📧")

		await ctx.author.send(embed=embed)


	@auto.command(name="help")
	async def auto_help(self, ctx):
		'''Help command for auto-translate'''

		embed = discord.Embed(description="*I found the following list of commands.*", color=0xC0C0C0)
		embed.set_author(name="Help")
		embed.add_field(name="**t-tr auto on <dest.> <src>**", value="`└─ Enables server-wide auto-translation of your message to the 'dest.' language from the 'src' language.`", inline=False)
		embed.add_field(name="**t-tr auto off**", value="`└─ Disables your server-wide auto-translation`", inline=False)

		embed.set_footer(text="Type t-help to get the list of all commands", icon_url="https://raw.githubusercontent.com/J16N/tsuby/master/assets/tsuby-footer.png")

		if ctx.message.guild is not None:
			await ctx.message.add_reaction("📧")

		await ctx.author.send(embed=embed)


	@ch.command(name="help")
	async def ch_help(self, ctx):
		'''Help command for channel-translate'''

		embed = discord.Embed(description="*I found the following list of commands.*", color=0xC0C0C0)
		embed.set_author(name="Help")
		embed.add_field(name="**t-tr ch on <dest.> <src>**", value="`└─ Enables channel-wide auto-translation of your message to the 'dest.' language from the 'src' language.`", inline=False)
		embed.add_field(name="**t-tr ch off**", value="`└─ Disables your channel-wide auto-translation`", inline=False)

		embed.set_footer(text="Type t-help to get the list of all commands", icon_url="https://raw.githubusercontent.com/J16N/tsuby/master/assets/tsuby-footer.png")

		if ctx.message.guild is not None:
			await ctx.message.add_reaction("📧")
			
		await ctx.author.send(embed=embed)


	@tr.command()
	async def to(self, ctx, to, frm, *, message):
		'''Translate the message'''

		links = ' '
		emojis = ' '

		'''
		Verify if the message any kind of mentions only.
		If it does, ignore translating it.
		'''

		if set(message.split()) == set(re.findall(r"(<[@|#]!?&? ?\d+>|@everyone|@here)", message)):
			return

		
		'''
		Okay so we also don't want to translate those messages that contain only numbers.
		1) We removed mentions (if any) from the message.
		2) Verifying if the message.content is a number. If it is, then we won't translate.
		'''
		temp = re.sub("<[@|#]!?&? ?\d+>", '', message)
		if set(temp.split()) == set(re.findall(r"\b\d+\b", temp)):
			return


		'''
		Alright so again some kind of restrictions before translating the message like if user share any
		urls ignore, or any bot commands, or any emojis etc etc.
		'''
		if message == links.join(re.findall("(?P<url>https?://[^\s]+)", message)) or \
		message == emojis.join(re.findall(self.emoji_regex, message)):
			return

		# saving our new old message :-3
		old_message_content = message

		# okay we don't want any markdowns. So let's remove them
		old_message_content = old_message_content.replace('*', '')
		old_message_content = old_message_content.strip(' ')
		old_message_content = re.sub(' +', ' ', old_message_content) #removes extra space

		# stripping off the emojis
		message = message.translate(message.maketrans('', '', ''.join(re.findall(self.emoji_regex, message))))
		message = message.replace('*', '')
		message = re.sub(' +', ' ', message)

		# with more confidence means perfect translation xD
		language_confidence = await self.translator.detect(message)
		if language_confidence.confidence < 0.9:
			src = frm
		else:
			src = language_confidence.lang

		# to_lang
		dest = to

		if src != dest:
			# lets just send typing status to the user while the bot do some of his important tasks in background 
			await ctx.message.channel.trigger_typing()

			translated_message = await self.translator.translate(message, dest = dest, src = src)

			# here I found that few things get changed after translating the message
			# so I just replace them with their original formats
			if "<@ " in translated_message.text or "<@! " in translated_message.text:
				translated_message.text = translated_message.text.replace("<@ ", "<@")
				translated_message.text = translated_message.text.replace("<@! ", "<@")

			if "<# " in translated_message.text or "<@! " in translated_message.text:
				translated_message.text = translated_message.text.replace("<# ", "<#")

			# Discord embeds, no big deal xD
			embed = discord.Embed(description = '*'+old_message_content+'*', color=0xC0C0C0)
			embed.set_author(name=ctx.message.author.name, icon_url=ctx.message.author.avatar_url)
			embed.add_field(name="**Translated**", value = translated_message.text, inline=True)
			embed.set_footer(text=u"{} ({}) → {} ({})".format(LANGUAGES[src].capitalize(), \
				src, LANGUAGES[dest].capitalize(), dest), icon_url="https://raw.githubusercontent.com/J16N/tsuby/master/assets/tsuby-footer.png")

			await ctx.message.channel.send(embed=embed)



	# verify if the user is the server mod or the bot creator
	def has_power():
		def predicate(ctx):
			if ctx.author.id == 302467968095223820 or ctx.author.permissions_in(ctx.message.channel).manage_messages:
				return True
			else:
				return False
		
		return commands.check(predicate)





	@auto.command(name="for")
	@commands.guild_only()
	@has_power() # command only for server mod and bot creator
	async def afr(self, ctx, to, frm, *args):
		'''Setting up the translation for others'''
		
		if ctx.me.permissions_in(ctx.message.channel).manage_messages:
			# delete the message command
			await ctx.message.delete(delay=3.0)

		to = to.lower()
		frm = frm.lower()

		con = await self.bot.pool.acquire()
		
		if to in list(LANGUAGES.keys()) and frm in list(LANGUAGES.keys()):

			updated_user = []
			
			try:
				for user in args:
					try:
						member = await commands.MemberConverter().convert(ctx, user)
					except:
						continue
					
					user_id = member.id

					check_user = "SELECT * FROM translation_table WHERE user_id = '{}' \
					AND ser_id = '{}' AND ch_id=0".format(user_id, ctx.guild.id)
						
					user_data = await con.fetchrow(check_user)

					if not user_data:
						
						ins_user = "INSERT INTO translation_table (user_id, ser_id, translate_to, translate_from) VALUES ('{}', '{}', '{}', '{}')".format(user_id, ctx.guild.id, to, frm)

						await con.execute(ins_user)
						updated_user.append(member.mention)

					else:
						#update the translation system for the given users
						if user_data['translate_from'] != frm or user_data['translate_to'] != to:
							
							update_user = "UPDATE translation_table SET translate_to = '{}', translate_from = '{}' \
							WHERE user_id = '{}' AND ser_id = '{}' AND ch_id=0".format(to, frm, user_id, ctx.guild.id)

							await con.execute(update_user)
							updated_user.append(member.mention)

			
			finally:
				await self.bot.pool.release(con)


			if updated_user:
				await ctx.send(f"{', '.join(updated_user)}, *your automatic translation to* `{to}` *has successfully been updated.*")
			else:
				await ctx.send("I do not see any user to add into the translation table. The user(s) may be present already.", delete_after=3.0)

		
		else:
			await ctx.send("Sorry I didn't understand the language codes. Please type `t-tr codes` to get the list of supported languages.", delete_after=3.0)







	@auto.command(name="remove")
	@commands.guild_only()
	@has_power() # command only for server admins and bot creators
	async def aremove(self, ctx, *args):
		'''Removes user from translation table.'''

		if ctx.me.permissions_in(ctx.message.channel).manage_messages:
			# delete the message command
			await ctx.message.delete(delay=3.0)

		removed_user = []

		con = await self.bot.pool.acquire()

		try:
			for user in args:
				try:
					member = await commands.MemberConverter().convert(ctx, user)
				except:
					continue

				user_id = member.id

				check_user = "SELECT * FROM translation_table WHERE user_id = '{}' \
				AND ser_id = '{}' AND ch_id=0".format(user_id, ctx.guild.id)

				if await con.fetchrow(check_user):
					del_user = "DELETE FROM translation_table WHERE user_id = '{}' AND \
					ser_id = '{}' AND ch_id=0".format(user_id, ctx.guild.id)

					await con.execute(del_user)
					removed_user.append(member.mention)
		
		finally:
			await self.bot.pool.release(con)
			

		if removed_user:
			await ctx.send(f"{', '.join(removed_user)}, you will no longer be auto translated.")
		else:
			await ctx.send("I do not see any user to remove from the translation table. The user(s) may already been removed.", delete_after=3.0)






	



	@auto.command(name="on")
	@commands.guild_only()
	async def auto_on(self, ctx, to, frm):
		'''Setting the translation'''

		if ctx.me.permissions_in(ctx.message.channel).manage_messages:
			# delete the message command
			await ctx.message.delete(delay=3.0)
		
		to = to.lower()
		frm = frm.lower()

		con = await self.bot.pool.acquire()

		# check if user passed the right argument
		if to in list(LANGUAGES.keys()) and frm in list(LANGUAGES.keys()):

			check_user = "SELECT * FROM translation_table WHERE user_id = '{}' \
			AND ser_id = '{}' AND ch_id=0".format(ctx.author.id, ctx.guild.id)

			user_data = await con.fetchrow(check_user)

			if user_data:

				if user_data['translate_from'] == frm and user_data['translate_to'] == to:
					
					await ctx.send(f"{ctx.author.mention}, your automatic translation is already enabled")

				else:
					update_user = "UPDATE translation_table SET translate_to = '{}', translate_from = '{}' WHERE user_id = '{}' AND ser_id = '{}' AND ch_id=0".format(to, frm, ctx.author.id, ctx.guild.id)

					try:
						await con.execute(update_user)

						await ctx.send(f"{ctx.author.mention}, your automatic translation has successfully been updated.", delete_after=3.0)

					finally:
						await self.bot.pool.release(con)

			

			else:

				ins_user = "INSERT INTO translation_table (user_id, ser_id, translate_to, translate_from) VALUES \
				('{}', '{}', '{}', '{}')".format(ctx.author.id, ctx.guild.id, to, frm)

				try:
					await con.execute(ins_user)

					await ctx.send(f"{ctx.author.mention}, your automatic translation to `{to}` has successfully been enabled.", delete_after=3.0)
				
				finally:
					await self.bot.pool.release(con)

		else:
			await ctx.send("Sorry I didn't understand the language codes. Please type `t-tr codes` to get the list of supported languages.", delete_after=3.0)




	@auto.command(name="off")
	@commands.guild_only()
	async def auto_off(self, ctx):
		'''Turns off the auto translation'''

		if ctx.me.permissions_in(ctx.message.channel).manage_messages:
			# delete the message command
			await ctx.message.delete(delay=3.0)

		con = await self.bot.pool.acquire()
		
		check_user = "SELECT * FROM translation_table WHERE user_id = '{}' \
		AND ser_id = '{}' AND ch_id=0".format(ctx.author.id, ctx.guild.id)

		if await con.fetchrow(check_user):

			del_user = "DELETE FROM translation_table WHERE user_id = '{}' AND \
			ser_id = '{}' AND ch_id=0".format(ctx.author.id, ctx.guild.id)

			try:
				await con.execute(del_user)

				await ctx.send(f"{ctx.author.mention}, you will no longer be auto translated.", delete_after=3.0)

			finally:
					await self.bot.pool.release(con)

		else:
			await ctx.send(f"{ctx.author.mention}, your server-wide auto-translation is already disabled. Try `t-tr auto <dest.> <src>` to enable it.", delete_after=3.0)




	@ch.command(name="for")
	@commands.guild_only()
	@has_power() # command only for server mod and bot creator
	async def cfr(self, ctx, to, frm, *args):
		'''Setting up the channel translation for others'''
		
		if ctx.me.permissions_in(ctx.message.channel).manage_messages:
			# delete the message command
			await ctx.message.delete(delay=3.0)

		to = to.lower()
		frm = frm.lower()

		con = await self.bot.pool.acquire()
		
		if to in list(LANGUAGES.keys()) and frm in list(LANGUAGES.keys()):

			updated_user = []
			
			try:
				for user in args:
					try:
						member = await commands.MemberConverter().convert(ctx, user)
					except:
						continue
					
					user_id = member.id

					check_user = "SELECT * FROM translation_table WHERE user_id = '{}' \
					AND ch_id = '{}'".format(user_id, ctx.channel.id)

					user_data = await con.fetchrow(check_user)
					
					if not user_data:
						
						ins_user = "INSERT INTO translation_table (user_id, ser_id, ch_id, translate_to, translate_from) VALUES ('{}', '{}', '{}', '{}', '{}')".format(user_id, ctx.guild.id, ctx.channel.id, to, frm)

						await con.execute(ins_user)
						updated_user.append(member.mention)

					else:
						#update the translation system for the given users
						if user_data['translate_from'] != frm or user_data['translate_to'] != to:
							
							update_user = "UPDATE translation_table SET translate_to = '{}', translate_from = '{}' WHERE user_id = '{}' AND ch_id = '{}'".format(to, frm, user_id, ctx.channel.id)

							await con.execute(update_user)
							updated_user.append(member.mention)

			
			finally:
				await self.bot.pool.release(con)


			if updated_user:
				await ctx.send(f"{', '.join(updated_user)}, *your automatic translation to* `{to}` *has successfully been updated for this channel.*")
			else:
				await ctx.send("I do not see any user to add into the translation table. The user(s) may be present already.", delete_after=3.0)

		
		else:
			await ctx.send("Sorry I didn't understand the language codes. Please type `t-tr codes` to get the list of supported languages.", delete_after=3.0)





	

	@ch.command(name="remove")
	@commands.guild_only()
	@has_power() # command only for server admins and bot creators
	async def cremove(self, ctx, *args):
		'''Removes user from translation table.'''

		if ctx.me.permissions_in(ctx.message.channel).manage_messages:
			# delete the message command
			await ctx.message.delete(delay=3.0)

		removed_user = []

		con = await self.bot.pool.acquire()

		try:
			for user in args:
				try:
					member = await commands.MemberConverter().convert(ctx, user)
				except:
					continue

				user_id = member.id

				check_user = "SELECT * FROM translation_table WHERE user_id = '{}' \
				AND ch_id = '{}'".format(user_id, ctx.channel.id)

				if await con.fetchrow(check_user):
					del_user = "DELETE FROM translation_table WHERE user_id = '{}' AND ch_id = '{}'".format(user_id, ctx.channel.id)

					await con.execute(del_user)
					removed_user.append(member.mention)
		
		finally:
			await self.bot.pool.release(con)
			

		if removed_user:
			await ctx.send(f"{', '.join(removed_user)}, you will no longer be auto translated here.")
		else:
			await ctx.send("I do not see any user to remove from the translation table. The user(s) may already been removed.", delete_after=3.0)







	

	@ch.command(name="on")
	@commands.guild_only()
	async def ch_on(self, ctx, to, frm):
		'''Turns on auto translation for the given channel'''

		if ctx.me.permissions_in(ctx.message.channel).manage_messages:
			# delete the message command
			await ctx.message.delete(delay=3.0)

		to = to.lower()
		frm = frm.lower()

		con = await self.bot.pool.acquire()

		if to in list(LANGUAGES.keys()) and frm in list(LANGUAGES.keys()):

			check_channel_user = "SELECT * FROM translation_table WHERE user_id = '{}' \
			AND ch_id = '{}'".format(ctx.author.id, ctx.channel.id)

			# let's just check out if the user is present...
			user_data = await con.fetchrow(check_channel_user)
			
			if user_data:

				if user_data['translate_from'] == frm and user_data['translate_to'] == to:
					await ctx.send(f"{ctx.author.mention}, your automatic translation here is already enabled", delete_after=3.0)


				else:
					update_user = "UPDATE translation_table SET translate_to = '{}', translate_from = '{}' \
					WHERE user_id = '{}' AND ch_id = '{}'".format(to, frm, ctx.author.id, ctx.channel.id)

					try:
						await con.execute(update_user)
						await ctx.send(f"{ctx.author.mention}, your automatic translation here has successfully been updated.", delete_after=3.0)


					finally:
						await self.bot.pool.release(con)


			
			else:
				ins_user = "INSERT INTO translation_table (user_id, ser_id, ch_id, translate_to, translate_from) VALUES \
				('{}', '{}', '{}', '{}', '{}')".format(ctx.author.id, ctx.guild.id, ctx.channel.id, to, frm)

				try:
					await con.execute(ins_user)
					await ctx.send(f"{ctx.author.mention}, your automatic translation to `{to}` has successfully been enabled for this channel.", delete_after=3.0)
				
				
				finally:
					await self.bot.pool.release(con)

		else:
			await ctx.send("Sorry I didn't understand the language codes. Please type `t-tr codes` to get the list of supported languages.", delete_after=3.0)





	@ch.command(name="off")
	@commands.guild_only()
	async def ch_off(self, ctx):

		if ctx.me.permissions_in(ctx.message.channel).manage_messages:
			# delete the message command
			await ctx.message.delete(delay=3.0)

		con = await self.bot.pool.acquire()
		
		check_user = "SELECT * FROM translation_table WHERE user_id = '{}' \
		AND ch_id = '{}'".format(ctx.author.id, ctx.message.channel.id)

		if await con.fetchrow(check_user):
			del_user = "DELETE FROM translation_table WHERE user_id = '{}' AND ch_id = '{}'".format(ctx.author.id, ctx.channel.id)

			try:
				await con.execute(del_user)
				await ctx.send(f"{ctx.author.mention}, you will no longer be auto translated here.", delete_after=3.0)


			finally:
				await self.bot.pool.release(con)


		else:
			await ctx.send(f"{ctx.author.mention}, your automatic translation here is already disabled. Try `t-tr ch <dest.> <src>` to enable it.", delete_after=3.0)





	

	@tr.command()
	async def codes(self, ctx):
		'''Getting the language codes'''

		embed = discord.Embed(description='***Language Codes***', color=0x800000)
		embed.add_field(name='\u200b', value = self.first_half_codes, inline=True)
		embed.add_field(name='\u200b', value = self.second_half_codes, inline=True)
		embed.add_field(name='\u200b', value = self.third_half_codes, inline=True)
		await ctx.send(embed=embed, delete_after=120.0)

		if ctx.me.permissions_in(ctx.message.channel).manage_messages:
			# delete the message command
			await ctx.message.delete(delay=120.0)






	@tr.command()
	@commands.guild_only()
	@has_power()
	async def ignore(self, ctx, *keyword):
		'''This will ignore translating the message starting with the keyword'''
		if set(keyword).issubset(set(self.ignore)):
			if len(keyword) > 1:
				await ctx.send("*No need. I already ignore these words.*")
			elif len(keyword) == 1:
				await ctx.send("*No need. I already ignore this word.*")

		else:
			self.ignore = list(set(self.ignore + list(keyword)))

			with open('ignore.txt', 'w') as ignore_file:
				for item in self.ignore:
					ignore_file.write("%s\n" % item)


			await ctx.send(f"*Any message starting with *\'{', '.join(keyword)}\'* will not be translated.*")






	@tr.command()
	@commands.guild_only()
	async def block(self, ctx, *channels):
		'''Block auto-translation in given channels'''
		
		if ctx.me.permissions_in(ctx.message.channel).manage_messages:
			# delete the message command
			await ctx.message.delete(delay=3.0)


		con = await self.bot.pool.acquire()

		# check if the auto translation is enabled for the user
		check_user = "SELECT * FROM translation_table WHERE user_id = '{}' \
		AND ser_id = '{}' AND ch_id=0".format(ctx.author.id, ctx.guild.id)

		if await con.fetchrow(check_user):
			try:
				if channels:
					updated_channels = []

					for channel in channels:
						try:
							ch = await commands.TextChannelConverter().convert(ctx, channel)
						except:
							continue

						ch_id = ch.id

						# we will check out if any translation-enabled channel is provided
						duplicate_ch = "SELECT * FROM translation_table WHERE user_id = '{}' \
						AND ch_id = '{}' AND ch_block = 'N'".format(ctx.author.id, ch_id)

						ch_data = await con.execute(duplicate_ch)

						if ch_data:
							update_ch = "UPDATE translation_table SET ch_block = 'Y' \
							WHERE user_id = '{}' AND ch_id = '{}'".format(ctx.author.id, ch_id)

							await con.execute(update_ch)
							updated_channels.append(ch.mention)

						else:
							ins_ch = "INSERT INTO translation_table (user_id, ser_id, ch_id, ch_block) \
							VALUES ('{}', '{}', '{}', 'Y')".format(ctx.author.id, ctx.guild.id, ch_id)

							await con.execute(ins_ch)
							updated_channels.append(ch.mention)


					if updated_channels:
						await ctx.send(f"{ctx.author.mention}, *you will no longer be auto-translated in* {', '.join(updated_channels)}")

				else:
					# we will check out if the command is run in translation-enabled channel
					duplicate_ch = "SELECT * FROM translation_table WHERE user_id = '{}' \
					AND ch_id = '{}' AND ch_block = 'N'".format(ctx.author.id, ctx.channel.id)

					ch_data = await con.execute(duplicate_ch)

					if ch_data:
						update_ch = "UPDATE translation_table SET ch_block = 'Y' \
						WHERE user_id = '{}' AND ch_id = '{}'".format(to, frm, ctx.author.id, ctx.channel.id)

						await con.execute(update_ch)

					else:
						ins_ch = "INSERT INTO translation_table (user_id, ser_id, ch_id, ch_block) \
						VALUES ('{}', '{}', '{}', 'Y')".format(ctx.author.id, ctx.guild.id, ctx.channel.id)

						await con.execute(ins_ch)


					await ctx.send(f"{ctx.author.mention}, you will no longer be auto-translated here.")

			finally:
				await self.bot.pool.release(con)


		else:
			await ctx.send("You do not have server-wide auto-translation enabled. Try `t-tr auto on <dest.> <src>` to enable it.", delete_after=3.0)







	@tr.command()
	@commands.guild_only()
	async def unblock(self, ctx, *channels):
		'''Block auto-translation in given channels'''
		
		if ctx.me.permissions_in(ctx.message.channel).manage_messages:
			# delete the message command
			await ctx.message.delete(delay=3.0)


		con = await self.bot.pool.acquire()

		try:
			if channels:
				updated_channels = []

				for channel in channels:
					try:
						ch = await commands.TextChannelConverter().convert(ctx, channel)
					except:
						continue

					ch_id = ch.id

					# we will check out if any translation-enabled channel is provided
					duplicate_ch = "SELECT * FROM translation_table WHERE user_id = '{}' \
					AND ch_id = '{}' AND ch_block = 'Y' AND translate_to IS NOT NONE".format(ctx.author.id, ch_id)

					ch_data = await con.execute(duplicate_ch)

					if ch_data:
						update_ch = "UPDATE translation_table SET ch_block = 'N' \
						WHERE user_id = '{}' AND ch_id = '{}'".format(ctx.author.id, ch_id)

						await con.execute(update_ch)
						updated_channels.append(ch.mention)

					else:
						del_ch = "DELETE FROM translation_table WHERE \
						user_id = '{}' AND ch_id = '{}' AND ch_block = 'Y'".format(ctx.author.id, ch_id)

						await con.execute(del_ch)
						updated_channels.append(ch.mention)


				if updated_channels:
					await ctx.send(f"{ctx.author.mention}, *you will again be auto-translated in* {', '.join(updated_channels)}")

			else:
				# we will check out if the command is run in translation-disabled channel
				duplicate_ch = "SELECT * FROM translation_table WHERE user_id = '{}' \
				AND ch_id = '{}' AND ch_block = 'Y' AND translate_to IS NOT NONE".format(ctx.author.id, ctx.channel.id)

				ch_data = await con.execute(duplicate_ch)

				if ch_data:
					update_ch = "UPDATE translation_table SET ch_block = 'N' \
					WHERE user_id = '{}' AND ch_id = '{}'".format(ctx.author.id, ctx.channel.id)

					await con.execute(update_ch)
					updated_channels.append(ch.mention)

				else:
					del_ch = "DELETE FROM translation_table WHERE \
					user_id = '{}' AND ch_id = '{}' AND ch_block = 'Y'".format(ctx.author.id, ctx.channel.id)

					await con.execute(del_ch)


				await ctx.send(f"{ctx.author.mention}, you will again be auto-translated here.")

		finally:
			await self.bot.pool.release(con)





	

	@commands.Cog.listener()
	async def on_message_edit(self, old_message, new_message):
		'''Editing the translation when the user edit their message'''

		# If someone has enabled the translation for some channel
		# then we are gonna verify them too. Similar logic for one who has enabled server wide translation
		# let's initialize the user as none

		user = None

		if old_message.guild:
			check_channel_block = "SELECT * FROM translation_table WHERE user_id = '{}' AND \
			ch_id = '{}' AND ch_block = 'Y'".format(new_message.author.id, new_message.channel.id)

			check_guild_user = "SELECT * FROM translation_table WHERE user_id = '{}' AND ser_id = '{}' AND ch_id=0".format(new_message.author.id, new_message.guild.id)

			check_channel_user = "SELECT * FROM translation_table WHERE \
			user_id = '{}' AND ch_id = '{}' AND ch_block = 'N'".format(new_message.author.id, new_message.channel.id)

			con = await self.bot.pool.acquire()

			try:
				channel_not_block = await con.fetchrow(check_channel_block)

				if not channel_not_block:
					user = await con.fetchrow(check_channel_user)

					if not user:
						user = await con.fetchrow(check_guild_user)

			finally:
				await self.bot.pool.release(con)


		if user:
			
			links = ' '
			emojis = ' '

			# search for the bot's message and then edit it
			async for message in old_message.channel.history():
				if message.embeds:
					if message.author.id == self.bot.user.id and message.embeds[0].description.strip('*') == old_message.content:

						'''
						Verify if the message any kind of mentions only.
						If it does, ignore translating it.
						'''

						if set(new_message.content.split()) == set(re.findall(r"(<[@|#]!?&? ?\d+>|@everyone|@here)", new_message.content)):
							await message.delete()
							break

						
						'''
						Okay so we also don't want to translate those messages that contain only numbers.
						1) We removed mentions (if any) from the message.
						2) Verifying if the message.content is a number. If it is, then we won't translate.
						'''
						temp = re.sub("<[@|#]!?&? ?\d+>", '', new_message.content)
						if set(temp.split()) == set(re.findall(r"\b\d+\b", temp)):
							await message.delete()
							break


						'''
						Alright so some kind of restrictions before editing the message like if user share any
						urls ignore, or any bot commands, or any emojis etc etc.
						'''

						if new_message.content == links.join(re.findall("(?P<url>https?://[^\s]+)", new_message.content)) or \
						new_message.content.startswith(tuple(self.ignore)) or \
						new_message.content == emojis.join(re.findall(self.emoji_regex, new_message.content)) or \
						new_message.content.startswith('```'):
							await message.delete()
							break


						# saving our new old message
						updated_message = new_message.clean_content

						# okay we don't want any markdowns. So let's remove them
						updated_message = updated_message.replace('*', '')
						updated_message = updated_message.strip(' ')
						updated_message = re.sub(' +', ' ', updated_message) #removes extra space


						# stripping off the emojis
						new_message_content = new_message.clean_content.translate(new_message.clean_content.maketrans('', '', ''.join(re.findall(self.emoji_regex, new_message.clean_content))))
						new_message_content = new_message.clean_content.replace('*', '')
						new_message_content = re.sub(' +', ' ', new_message_content)


						# with more confidence means perfect translation xD
						language_confidence = await self.translator.detect(new_message_content)
						if language_confidence.confidence < 0.8:
							src = user['translate_from']
						else:
							src = language_confidence.lang

						# to_lang
						dest = user['translate_to']


						if src != dest:

							translated_message = await self.translator.translate(new_message_content, dest=dest, src=src)

							# here I found that few things get changed after translating the message
							# so I just replace them with their original formats
							if "<@ " in translated_message.text or "<@! " in translated_message.text:
								translated_message.text = translated_message.text.replace("<@ ", "<@")
								translated_message.text = translated_message.text.replace("<@! ", "<@")

							if "<# " in translated_message.text or "<@! " in translated_message.text:
								translated_message.text = translated_message.text.replace("<# ", "<#")

							# Discord embeds, no big deal xD
							embed = discord.Embed(description = '*'+updated_message+'*', color=0xC0C0C0)
							embed.set_author(name=new_message.author.name, icon_url=new_message.author.avatar_url)
							embed.add_field(name="**Translated**", value = translated_message.text, inline=True)
							embed.set_footer(text=u"{} ({}) → {} ({})".format(LANGUAGES[src].capitalize(), \
								src, LANGUAGES[dest].capitalize(), dest), icon_url="https://raw.githubusercontent.com/J16N/tsuby/master/assets/tsuby-footer.png")

							await message.edit(embed=embed)

							break

						else:
							await message.delete()
							break



	

	@commands.Cog.listener()
	async def on_message_delete(self, deleted_message):
		'''Delete the translated message when the user delete their message'''

		async for message in deleted_message.channel.history():
			if message.embeds and message.embeds[0].description:
				if message.author.id == self.bot.user.id and message.embeds[0].description.strip('*') == deleted_message.clean_content:
					await message.delete()
					break



	

	@commands.Cog.listener()
	async def on_message(self, message):
		'''Translating the registered user'''

		# Ignore translating the message from bot itself
		if message.author.id == self.bot.user.id:
			return


		# If someone has enabled the translation for some channel
		# then we are gonna verify them too. Similar logic for one who has enabled server wide translation
		# let's initialize the user as none

		user = None

		if message.guild:
			check_channel_block = "SELECT * FROM translation_table WHERE user_id = '{}' AND \
			ch_id = '{}' AND ch_block = 'Y'".format(message.author.id, message.channel.id)

			check_guild_user = "SELECT * FROM translation_table WHERE user_id = '{}' AND ser_id = '{}' AND ch_id=0".format(message.author.id, message.guild.id)

			check_channel_user = "SELECT * FROM translation_table WHERE user_id = '{}' AND ch_id = '{}'".format(message.author.id, message.channel.id)

			con = await self.bot.pool.acquire()

			try:
				channel_not_block = await con.fetchrow(check_channel_block)

				if not channel_not_block:
					user = await con.fetchrow(check_channel_user)

					if not user:
						user = await con.fetchrow(check_guild_user)

			finally:
				await self.bot.pool.release(con)

		
		if user:

			'''
			Verify if the message any kind of mentions only.
			If it does, ignore translating it.
			'''

			if set(message.content.split()) == set(re.findall(r"(<[@|#]!?&? ?\d+>|@everyone|@here)", message.content)):
				return

			
			'''
			Okay so we also don't want to translate those messages that contain only numbers.
			1) We removed mentions (if any) from the message.
			2) Verifying if the message.content is a number. If it is, then we won't translate.
			'''
			temp = re.sub("<[@|#]!?&? ?\d+>", '', message.content)
			if set(temp.split()) == set(re.findall(r"\b\d+\b", temp)):
				return


			'''
			Alright so again some kind of restrictions before translating the message like if user share any
			urls ignore, or any bot commands, or any emojis etc etc.
			'''
			links = ' '
			emojis = ' '

			if message.content != links.join(re.findall("(?P<url>https?://[^\s]+)", message.content)) and \
			not message.content.startswith(tuple(self.ignore)) and \
			message.content != emojis.join(re.findall(self.emoji_regex, message.content)) and \
			not message.content.startswith('```'):

				# saving our new old message :-3
				old_message_content = message.clean_content

				# okay we don't want any markdowns. So let's remove them
				old_message_content = old_message_content.replace('*', '')
				old_message_content = old_message_content.strip(' ')
				old_message_content = re.sub(' +', ' ', old_message_content) #removes extra space

				# stripping off the emojis
				message_content = message.clean_content.translate(message.clean_content.maketrans('', '', ''.join(re.findall(self.emoji_regex, message.clean_content))))
				message_content = message_content.replace('*', '')
				message_content = re.sub(' +', ' ', message_content)

				# with more confidence means perfect translation
				language_confidence = await self.translator.detect(message_content)
				if language_confidence.confidence < 0.8:
					src = user['translate_from']
				else:
					src = language_confidence.lang

				# to_lang
				dest = user['translate_to']

				if src != dest:

					# lets just send typing status to the user while the bot do some of his important tasks in background 
					await message.channel.trigger_typing()

					translated_message = await self.translator.translate(message_content, dest=dest, src=src)

					# here I found that few things get changed after translating the message
					# so I just replace them with their original formats
					if "<@ " in translated_message.text or "<@! " in translated_message.text:
						translated_message.text = translated_message.text.replace("<@ ", "<@")
						translated_message.text = translated_message.text.replace("<@! ", "<@")

					if "<# " in translated_message.text or "<#! " in translated_message.text:
						translated_message.text = translated_message.text.replace("<# ", "<#")

					if "<@& " in translated_message.text or "<@&! " in translated_message.text:
						translated_message.text = translated_message.text.replace("<@& ", "<@&")

					# Discord embeds, no big deal xD
					embed = discord.Embed(description = '*'+old_message_content+'*', color=0xC0C0C0)
					embed.set_author(name=message.author.name, icon_url=message.author.avatar_url)
					embed.add_field(name="**Translated**", value = translated_message.text, inline=True)
					embed.set_footer(text=u"{} ({}) → {} ({})".format(LANGUAGES[src].capitalize(), \
						src, LANGUAGES[dest].capitalize(), dest), icon_url="https://raw.githubusercontent.com/J16N/tsuby/master/assets/tsuby-footer.png")

					await message.channel.send(embed=embed)




	@commands.command()
	@commands.cooldown(10,600,type=BucketType.member)
	@has_power()
	async def leave(self, ctx):
		'''Removes all the translation setup (if enabled) and leaves the server'''

		message = await ctx.send("Cleaning up...")

		con = await self.bot.pool.acquire()

		check_guild = "SELECT * FROM translation_table WHERE ser_id = '{}'".format(ctx.guild.id)

		if await con.fetchrow(check_guild):
			del_server = "DELETE FROM translation_table WHERE ser_id = '{}'".format(ctx.guild.id)

			try:
				await con.execute(del_server)

			finally:
				await self.bot.pool.release(con)


		await message.edit(content="**GOODBYE EVERYONE !!** :wave:")
		await ctx.guild.leave()



def setup(bot):
	bot.add_cog(Translate(bot))
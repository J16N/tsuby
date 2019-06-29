# Load important modules
import discord
from discord.ext import commands
from discord.ext.commands.cooldowns import BucketType
from googletrans import Translator, LANGUAGES, LANGCODES
import asyncio
import random
import re
import os
import pymysql

class Translate(commands.Cog):

	def __init__(self, bot):

		self.bot = bot
		
		# Instantiates a translator client
		self.translator = Translator()

		#url, username & password
		self.database_url = os.environ.get("url")
		self.username = os.environ.get("user")
		self.password = os.environ.get("password")

		#open database connection
		self.tr_db = pymysql.connect(self.database_url, self.username, self.password, self.username, cursorclass=pymysql.cursors.DictCursor)

		#a cursor object using cursor method
		self.tr_cur = self.tr_db.cursor()

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
			await ctx.send('`t-tr help`')

	@tr.group(case_insensitive=True)
	async def auto(self, ctx):
		'''This is a sub-sub command'''
		if str(ctx.invoked_subcommand) == 'tr auto':
			await ctx.send('`t-tr auto help`')

	@tr.group(case_insensitive=True)
	async def ch(self, ctx):
		'''This is a sub-sub command'''
		if str(ctx.invoked_subcommand) == 'tr ch':
			await ctx.send('`t-tr ch help`')


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

		embed.set_footer(text="Type t-help to get the list of all commands", icon_url="https://raw.githubusercontent.com/J16N/tsuby/master/cogs/tsuby.png")

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

		embed.set_footer(text="Type t-help to get the list of all commands", icon_url="https://raw.githubusercontent.com/J16N/tsuby/master/cogs/tsuby.png")

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

		embed.set_footer(text="Type t-help to get the list of all commands", icon_url="https://raw.githubusercontent.com/J16N/tsuby/master/cogs/tsuby.png")

		if ctx.message.guild is not None:
			await ctx.message.add_reaction("📧")
			
		await ctx.author.send(embed=embed)


	@tr.command()
	async def to(self, ctx, to, frm, *message):
		'''Translate the message'''

		message = ' '.join(list(message))

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
		if self.translator.detect(message).confidence < 0.9:
			src = frm
		else:
			src = self.translator.detect(message).lang

		# to_lang
		dest = to

		if src != dest:
			# lets just send typing status to the user while the bot do some of his important tasks in background 
			await ctx.message.channel.trigger_typing()

			translated_message = self.translator.translate(message, dest = dest, src = src)

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
				src, LANGUAGES[dest].capitalize(), dest), icon_url="https://raw.githubusercontent.com/J16N/tsuby/master/cogs/tsuby.png")

			await ctx.message.channel.send(embed=embed)



	# verify if the user is the server admin or the bot creator
	def has_power():
		def predicate(ctx):
			if ctx.author.id == 302467968095223820 or ctx.message.author.guild_permissions.administrator:
				return True
			else:
				return False
		
		return commands.check(predicate)



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


			await ctx.send("*Any message starting with* '{}' *will not be translated.*".format(', '.join(keyword)))



	@tr.command()
	@commands.guild_only()
	@has_power() # command only for server admins and bot creators
	async def fr(self, ctx, to, frm, *args):
		'''Setting up the translation for others'''
		
		to = to.lower()
		frm = frm.lower()

		self.tr_db.ping(reconnect=True) # Check if the server is alive. If the connection is closed, reconnect.

		# get the list of channels in the server
		channels = [channel.id for channel in ctx.guild.channels]
		
		if to in list(LANGUAGES.keys()) and frm in list(LANGUAGES.keys()):
			
			added_user = []

			updated_user = []
			
			for user in args:
				user_id = int(re.search(r'\d+', user).group(0))

				check_user = "SELECT * FROM translation_table WHERE user_id = '{}' \
				AND ser_id = '{}'".format(user_id, ctx.guild.id)
				
				if int(user_id) not in channels:
					if not self.tr_cur.execute(check_user):
						
						ins_user = "INSERT INTO translation_table (user_id, ser_id, translate_to, translate_from) VALUES \
						('{}', '{}', '{}', '{}')".format(user_id, ctx.guild.id, to, frm)

						try:
							self.tr_cur.execute(ins_user)
							self.tr_db.commit()
							added_user.append(user)
						except:
							self.tr_db.rollback()

					else:
						#update the translation system for the given users
						user_data = self.tr_cur.fetchone()

						if user_data['translate_from'] != frm or user_data['translate_to'] != to:
							update_user = "UPDATE translation_table SET translate_to = '{}', translate_from = '{}' WHERE user_id = '{}' \
							AND ser_id = '{}'".format(to, frm, user_id, ctx.guild.id)

							try:
								self.tr_cur.execute(update_user)
								self.tr_db.commit()
								updated_user.append(user)

							except:
								self.tr_db.rollback()


			if added_user:
				await ctx.send("{}, your automatic translation to `{}` has successfully been updated.".format(', '.join(added_user), to))
			elif updated_user:
				await ctx.send("{}, your automatic translation to `{}` has successfully been updated.".format(', '.join(updated_user), to))
			else:
				bot_message = await ctx.send("I do not see any user to add into the translation table. The user(s) may be present already.")

				await bot_message.delete(delay=5.0)

				if ctx.me.permissions_in(ctx.message.channel).manage_messages:
					# delete the message command
					await ctx.message.delete(delay=5.0)

		else:
			bot_message = await ctx.send("Sorry I didn't understand the language codes. Please type `?tr codes` to get the list of supported languages.")

			await bot_message.delete(delay=5.0)

			if ctx.me.permissions_in(ctx.message.channel).manage_messages:
				# delete the message command
				await ctx.message.delete(delay=5.0)



	@tr.command()
	@commands.guild_only()
	@has_power() # command only for server admins and bot creators
	async def remove(self, ctx, *args):
		'''Removes user from translation table.'''

		removed_user = []

		self.tr_db.ping(reconnect=True)

		for user in args:
			
			user_id = int(re.search(r'\d+', user).group(0))

			check_user = "SELECT * FROM translation_table WHERE user_id = '{}' \
			AND ser_id = '{}'".format(user_id, ctx.guild.id)

			if self.tr_cur.execute(check_user):
				del_user = "DELETE FROM translation_table WHERE user_id = '{}' AND ser_id = '{}'".format(user_id, ctx.guild.id)

				try:
					self.tr_cur.execute(del_user)
					self.tr_db.commit()
					removed_user.append(user)
				except:
					self.tr_db.rollback()
			

		if removed_user:
			await ctx.send("{}, you will no longer be auto translated".format(', '.join(removed_user)))
		else:
			bot_message = await ctx.send("I do not see any user to remove from the translation table. The user(s) may already been removed.")

			await bot_message.delete(delay=5.0)

			if ctx.me.permissions_in(ctx.message.channel).manage_messages:
				# delete the message command
				await ctx.message.delete(delay=5.0)



	@auto.command(name="on")
	@commands.guild_only()
	async def auto_on(self, ctx, to, frm):
		'''Setting the translation'''
		
		to = to.lower()
		frm = frm.lower()

		self.tr_db.ping(reconnect=True)

		# check if user passed the right argument
		if to in list(LANGUAGES.keys()) and frm in list(LANGUAGES.keys()):

			check_user = "SELECT * FROM translation_table WHERE user_id = '{}' \
			AND ser_id = '{}' AND ch_id IS NULL".format(ctx.author.id, ctx.guild.id)

			if self.tr_cur.execute(check_user):

				user_data = self.tr_cur.fetchone()

				if user_data['translate_from'] == frm and user_data['translate_to'] == to:
					
					await ctx.send("{0.author.mention}, your automatic translation is already enabled".format(ctx))

				else:
					update_user = "UPDATE translation_table SET translate_to = '{}', translate_from = '{}' WHERE user_id = '{}' \
					AND ser_id = '{}'".format(to, frm, ctx.author.id, ctx.guild.id)

					try:
						self.tr_cur.execute(update_user)
						self.tr_db.commit()

						bot_message = await ctx.send("{0.author.mention}, your automatic translation has successfully been updated.".format(ctx))

						await bot_message.delete(delay=5.0)

						if ctx.me.permissions_in(ctx.message.channel).manage_messages:
							# delete the message command
							await ctx.message.delete(delay=5.0)

					except:
						self.tr_db.rollback()

						bot_message = await ctx.send("{0.author.mention}, failed to add you into translation table. An unknown error has occured".format(ctx))

						await bot_message.delete(delay=5.0)

						if ctx.me.permissions_in(ctx.message.channel).manage_messages:
							# delete the message command
							await ctx.message.delete(delay=5.0)

			

			else:

				'''When enabling server wide translation, we will delete that user's channel translation in that server'''
				del_channel_user = "DELETE FROM translation_table WHERE user_id = '{}' AND ser_id = '{}'".format(ctx.author.id, ctx.guild.id)

				try:
					self.tr_cur.execute(del_channel_user)
					self.tr_db.commit()
				except:
					self.tr_db.rollback()

				ins_user = "INSERT INTO translation_table (user_id, ser_id, translate_to, translate_from) VALUES \
				('{}', '{}', '{}', '{}')".format(ctx.author.id, ctx.guild.id, to, frm)

				try:
					self.tr_cur.execute(ins_user)
					self.tr_db.commit()

					await ctx.send("{0.author.mention}, your automatic translation to `{1}` has successfully been enabled.".format(ctx, to))

					bot_message = await bot_message.delete(delay=5.0)

					if ctx.me.permissions_in(ctx.message.channel).manage_messages:
						# delete the message command
						await ctx.message.delete(delay=5.0)
				
				except:
					self.tr_db.rollback()

					bot_message = await ctx.send("{0.author.mention}, failed to add you into translation table. An unknown error has occured".format(ctx))

					await bot_message.delete(delay=5.0)

					if ctx.me.permissions_in(ctx.message.channel).manage_messages:
						# delete the message command
						await ctx.message.delete(delay=5.0)

		else:
			bot_message = await ctx.send("Sorry I didn't understand the language codes. Please type `?tr codes` to get the list of supported languages.")

			await bot_message.delete(delay=5.0)

			if ctx.me.permissions_in(ctx.message.channel).manage_messages:
				# delete the message command
				await ctx.message.delete(delay=5.0)




	@auto.command(name="off")
	@commands.guild_only()
	async def auto_off(self, ctx):
		'''Turns off the auto translation'''

		self.tr_db.ping(reconnect=True)
		
		check_user = "SELECT * FROM translation_table WHERE user_id = '{}' \
		AND ser_id = '{}' AND ch_id IS NULL".format(ctx.author.id, ctx.guild.id)

		if self.tr_cur.execute(check_user):

			del_user = "DELETE FROM translation_table WHERE user_id = '{}' AND ser_id = '{}' AND ch_id is NULL".format(ctx.author.id, \
				ctx.guild.id)

			try:
				self.tr_cur.execute(del_user)
				self.tr_db.commit()

				bot_message = await ctx.send("{0.author.mention}, you will no longer be auto translated.".format(ctx))

				await bot_message.delete(delay=5.0)

				if ctx.me.permissions_in(ctx.message.channel).manage_messages:
					# delete the message command
					await ctx.message.delete(delay=5.0)

			except:
				self.tr_db.rollback()

				bot_message = await ctx.send("{0.author.mention}, failed to remove you from translation table. An unknown error has occured".format(ctx))

				await bot_message.delete(delay=5.0)

				if ctx.me.permissions_in(ctx.message.channel).manage_messages:
					# delete the message command
					await ctx.message.delete(delay=5.0)

		else:

			bot_message = await ctx.send("{0.author.mention}, your automatic translation is already disabled. Try `?tr auto <dest> <src>` to enable it.".format(ctx))

			await bot_message.delete(delay=5.0)

			if ctx.me.permissions_in(ctx.message.channel).manage_messages:
				# delete the message command
				await ctx.message.delete(delay=5.0)




	@ch.command(name="on")
	@commands.guild_only()
	async def ch_on(self, ctx, to, frm):
		'''Turns on auto translation for the given channel'''

		to = to.lower()
		frm = frm.lower()

		self.tr_db.ping(reconnect=True)

		if to in list(LANGUAGES.keys()) and frm in list(LANGUAGES.keys()):

			check_guild_user = "SELECT * FROM translation_table WHERE user_id = '{}' \
			AND ser_id = '{}' AND ch_id IS NULL".format(ctx.author.id, ctx.guild.id)

			check_channel_user = "SELECT * FROM translation_table WHERE user_id = '{}' \
			AND ch_id = '{}'".format(ctx.author.id, ctx.message.channel.id)

			if self.tr_cur.execute(check_guild_user):
				bot_message = await ctx.send("No need {0.author.mention}. Server wide auto-translation is already enabled for you".format(ctx))

				await bot_message.delete(delay=5.0)

				if ctx.me.permissions_in(ctx.message.channel).manage_messages:
					# delete the message command
					await ctx.message.delete(delay=5.0)

			elif self.tr_cur.execute(check_channel_user):
				user_data = self.tr_cur.fetchone()

				if user_data['translate_from'] == frm and user_data['translate_to'] == to:
					bot_message = await ctx.send("{0.author.mention}, your automatic translation here is already enabled".format(ctx))

					await bot_message.delete(delay=5.0)

					if ctx.me.permissions_in(ctx.message.channel).manage_messages:
						# delete the message command
						await ctx.message.delete(delay=5.0)

				else:
					update_user = "UPDATE translation_table SET translate_to = '{}', translate_from = '{}' WHERE user_id = '{}' \
					AND ch_id = '{}'".format(to, frm, ctx.author.id, ctx.message.channel.id)

					try:
						self.tr_cur.execute(update_user)
						self.tr_db.commit()

						bot_message = await ctx.send("{0.author.mention}, your automatic translation here has successfully been updated.".format(ctx))

						await bot_message.delete(delay=5.0)

						if ctx.me.permissions_in(ctx.message.channel).manage_messages:
							# delete the message command
							await ctx.message.delete(delay=5.0)

					except:
						self.tr_db.rollback()

						bot_message = await ctx.send("{0.author.mention}, failed to add you into translation table. An unknown error has occured".format(ctx))

						await bot_message.delete(delay=5.0)

						if ctx.me.permissions_in(ctx.message.channel).manage_messages:
							# delete the message command
							await ctx.message.delete(delay=5.0)


			else:
				ins_user = "INSERT INTO translation_table (user_id, ser_id, ch_id, translate_to, translate_from) VALUES \
				('{}', '{}', '{}', '{}', '{}')".format(ctx.author.id, ctx.guild.id, ctx.message.channel.id, to, frm)

				try:
					self.tr_cur.execute(ins_user)
					self.tr_db.commit()

					bot_message = await ctx.send("{0.author.mention}, your automatic translation to `{1}` has successfully been enabled for this channel.".format(ctx, to))

					await bot_message.delete(delay=5.0)

					if ctx.me.permissions_in(ctx.message.channel).manage_messages:
						# delete the message command
						await ctx.message.delete(delay=5.0)
				
				except:
					self.tr_db.rollback()

					bot_message = await ctx.send("{0.author.mention}, failed to add you into translation table. An unknown error has occured".format(ctx))

					await bot_message.delete(delay=5.0)

					if ctx.me.permissions_in(ctx.message.channel).manage_messages:
						# delete the message command
						await ctx.message.delete(delay=5.0)

		else:
			bot_message = await ctx.send("Sorry I didn't understand the language codes. Please type `?tr codes` to get the list of supported languages.")

			await bot_message.delete(delay=5.0)

			if ctx.me.permissions_in(ctx.message.channel).manage_messages:
				# delete the message command
				await ctx.message.delete(delay=5.0)





	@ch.command(name="off")
	@commands.guild_only()
	async def ch_off(self, ctx):

		self.tr_db.ping(reconnect=True)
		
		check_user = "SELECT * FROM translation_table WHERE user_id = '{}' \
		AND ch_id = '{}'".format(ctx.author.id, ctx.message.channel.id)

		if self.tr_cur.execute(check_user):
			del_user = "DELETE FROM translation_table WHERE user_id = '{}' AND ch_id = '{}'".format(ctx.author.id, ctx.message.channel.id)

			try:
				self.tr_cur.execute(del_user)
				self.tr_db.commit()

				bot_message = await ctx.send("{0.author.mention}, you will no longer be auto translated here.".format(ctx))

				await bot_message.delete(delay=5.0)

				if ctx.me.permissions_in(ctx.message.channel).manage_messages:
					# delete the message command
					await ctx.message.delete(delay=5.0)

			except:
				self.tr_db.rollback()

				bot_message = await ctx.send("{0.author.mention}, failed to remove you from translation table. An unknown error has occured".format(ctx))

				await bot_message.delete(delay=5.0)

				if ctx.me.permissions_in(ctx.message.channel).manage_messages:
					# delete the message command
					await ctx.message.delete(delay=5.0)


		else:
			bot_message = await ctx.send("{0.author.mention}, your automatic translation is already disabled. Try `?tr ch <dest> <src>` to enable it.".format(ctx))

			await bot_message.delete(delay=5.0)

			if ctx.me.permissions_in(ctx.message.channel).manage_messages:
				# delete the message command
				await ctx.message.delete(delay=5.0)




	@tr.command()
	async def codes(self, ctx):
		'''Getting the language codes'''

		embed = discord.Embed(description='***Language Codes***', color=0x800000)
		embed.add_field(name='\u200b', value = self.first_half_codes, inline=True)
		embed.add_field(name='\u200b', value = self.second_half_codes, inline=True)
		embed.add_field(name='\u200b', value = self.third_half_codes, inline=True)
		await ctx.send(embed=embed)



	@commands.Cog.listener()
	async def on_message_edit(self, old_message, new_message):
		'''Editing the translation when the user edit their message'''

		# If someone has enabled the translation for some channel
		# then we are gonna verify them too. Similar logic for one who has enabled server wide translation
		# let's initialize the user as none

		user = None

		if old_message.guild:
			check_guild_user = "SELECT * FROM translation_table WHERE user_id = '{}' AND ser_id = '{}' AND ch_id IS NULL".format(new_message.author.id, new_message.guild.id)

			check_channel_user = "SELECT * FROM translation_table WHERE user_id = '{}' AND ch_id = '{}'".format(new_message.author.id, new_message.channel.id)

			self.tr_db.ping(reconnect=True)

			if self.tr_cur.execute(check_guild_user) or self.tr_cur.execute(check_channel_user):
				user = self.tr_cur.fetchone()


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
						updated_message = new_message.content

						# okay we don't want any markdowns. So let's remove them
						updated_message = updated_message.replace('*', '')
						updated_message = updated_message.strip(' ')
						updated_message = re.sub(' +', ' ', updated_message) #removes extra space


						# stripping off the emojis
						new_message.content = new_message.content.translate(new_message.content.maketrans('', '', ''.join(re.findall(self.emoji_regex, new_message.content))))
						new_message.content = new_message.content.replace('*', '')
						new_message.content = re.sub(' +', ' ', new_message.content)


						# with more confidence means perfect translation xD
						if self.translator.detect(new_message.content).confidence < 0.8:
							src = user['translate_from']
						else:
							src = self.translator.detect(new_message.content).lang

						# to_lang
						dest = user['translate_to']


						if src != dest:

							translated_message = self.translator.translate(new_message.content, dest = dest, src = src)

							# here I found that few things get changed after translating the message
							# so I just replace them with their original formats
							if "<@ " in translated_message.text or "<@! " in translated_message.text:
								translated_message.text = translated_message.text.replace("<@ ", "<@")
								translated_message.text = translated_message.text.replace("<@! ", "<@")

							if "<# " in translated_message.text or "<@! " in translated_message.text:
								translated_message.text = translated_message.text.replace("<# ", "<#")

							# Discord embeds, no big deal xD
							embed = discord.Embed(description = '*'+updated_message+'*', color=0xC0C0C0)
							embed.set_author(name=message.author.name, icon_url=message.author.avatar_url)
							embed.add_field(name="**Translated**", value = translated_message.text, inline=True)
							embed.set_footer(text=u"{} ({}) → {} ({})".format(LANGUAGES[src].capitalize(), \
								src, LANGUAGES[dest].capitalize(), dest), icon_url="https://raw.githubusercontent.com/J16N/tsuby/master/cogs/tsuby.png")

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
				if message.author.id == self.bot.user.id and message.embeds[0].description.strip('*') == deleted_message.content:
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
			check_guild_user = "SELECT * FROM translation_table WHERE user_id = '{}' AND ser_id = '{}' AND ch_id IS NULL".format(message.author.id, message.guild.id)

			check_channel_user = "SELECT * FROM translation_table WHERE user_id = '{}' AND ch_id = '{}'".format(message.author.id, message.channel.id)

			self.tr_db.ping(reconnect=True)

			if self.tr_cur.execute(check_guild_user) or self.tr_cur.execute(check_channel_user):
				user = self.tr_cur.fetchone()

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
				old_message_content = message.content

				# okay we don't want any markdowns. So let's remove them
				old_message_content = old_message_content.replace('*', '')
				old_message_content = old_message_content.strip(' ')
				old_message_content = re.sub(' +', ' ', old_message_content) #removes extra space

				# stripping off the emojis
				message.content = message.content.translate(message.content.maketrans('', '', ''.join(re.findall(self.emoji_regex, message.content))))
				message.content = message.content.replace('*', '')
				message.content = re.sub(' +', ' ', message.content)

				# with more confidence means perfect translation xD
				if self.translator.detect(message.content).confidence < 0.8:
					src = user['translate_from']
				else:
					src = self.translator.detect(message.content).lang

				# to_lang
				dest = user['translate_to']

				if src != dest:

					# lets just send typing status to the user while the bot do some of his important tasks in background 
					await message.channel.trigger_typing()

					translated_message = self.translator.translate(message.content, dest = dest, src = src)

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
						src, LANGUAGES[dest].capitalize(), dest), icon_url="https://raw.githubusercontent.com/J16N/tsuby/master/cogs/tsuby.png")

					await message.channel.send(embed=embed)




	@commands.command()
	@commands.cooldown(10,600,type=BucketType.member)
	@has_power()
	async def leave(self, ctx):
		'''Removes all the translation setup (if enabled) and leaves the server'''

		message = await ctx.send("Cleaning up...")

		self.tr_db.ping(reconnect=True)

		check_guild = "SELECT * FROM translation_table WHERE ser_id = '{}'".format(ctx.guild.id)

		if self.tr_cur.execute(check_guild):
			del_server = "DELETE FROM translation_table WHERE ser_id = '{}'".format(ctx.guild.id)

			try:
				self.tr_cur.execute(del_server)
				self.tr_db.commit()

			except:
				self.tr_db.rollback()

				await message.edit(content="Clean up failed.")


		await message.edit(content="**GOODBYE EVERYONE !!** :wave:")

		await ctx.guild.leave()



def setup(bot):
	bot.add_cog(Translate(bot))
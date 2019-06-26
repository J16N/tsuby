import discord
from discord.ext import commands
from discord.ext.commands.cooldowns import BucketType
from akinator.async_aki import Akinator
import akinator
import asyncio

class Games(commands.Cog):

	def __init__(self, bot):

		self.bot = bot
		self.aki = Akinator()


	@commands.group(case_insensitive=True)
	@commands.cooldown(10,600,type=BucketType.member)
	async def game(self, ctx):
		'''Our main game command. Other commands are just sub commands of this'''
		if ctx.invoked_subcommand is None:
			await ctx.send('`t-game help`')


	@game.command()
	async def help(self, ctx):
		'''Help command for games'''
		embed = discord.Embed(description="*I found the following list of commands*", color=0x86BFF4)
		embed.set_author(name="Help")
		embed.add_field(name="**t-game guess [language_code (optional)]**", value="`└─ Starts the game where I will try to guess the character you think of. If the optional language is given then the questions are provided in that particular language. This defaults to English. \n\nCurrently supported languages are:\nEnglish (en)\nArabic (ar)\nChinese (cn)\nGerman (de)\nSpanish (es)\nFrench (fr)\nHebrew (il)\nItalian (it)\nJapanese (jp)\nKorean (kr)\nDutch (nl)\nPolish (pl)\nPortuguese (pt)\nRussian (ru)\nTurkish (tr)`", inline=False)
		embed.set_footer(text="Type t-help to get the list of all commands", icon_url="https://raw.githubusercontent.com/J16N/tsuby/master/cogs/tsuby.png")

		if ctx.message.guild is not None:
			await ctx.message.add_reaction("📧")
			
		await ctx.author.send(embed=embed)


	@game.command(name="guess")
	async def aki(self, ctx, lang="en2"):
		'''Starts the game Akinator'''

		#if ctx.author.id not in self.gamer:
		
		lang = lang.lower()

		# buttons we'll be using in embed as reaction
		buttons = [
				'<:myA:584978563204120577>', 
				'<:myB:592285509863211009>', 
				'<:myC:584978564521263127>', 
				'<:myD:584978564009426964>',
				'<:myE:584998291901644836>', 
				'<:myleft:584972740595810304>',
				'<:myright:584973342793138197>'
		]

		def check(reaction, user):
			return user == ctx.message.author and str(reaction.emoji) in buttons and (reaction.message.id == message.id)

		description = "**You all know the King of Guessing, Akinator right? Well I've had happened to meet him one day. :blush:\nWe enjoyed a lot and at the end of the day, he taught me his secret. :wink:\n\nGuess what? Now I can also tell any character you think of, regardless of that person be real or fictitious. :sunglasses:\n\nBelow are the basic instructions to play this game.**\n\n**__How To Play__**\n*React with the supported reactions to make a way through the game.*\n\n<:myleft:584972740595810304> *Takes you to the previous question.*\n\n*React to any one of your choosen options to proceed.*\n\n<:myA:584978563204120577>\t\t<:myB:592285509863211009>\t\t<:myC:584978564521263127>\t\t<:myD:584978564009426964>\t\t<:myE:584998291901644836>\n\n**Now it's your turn to think of a character and answer my questions honestly. \nSo what are you waiting for? Go, react to proceed!**"

		options = "\n\n<:myA:584978563204120577> *YES*\n<:myB:592285509863211009> *NO*\n<:myC:584978564521263127> *I DON'T KNOW*\n<:myD:584978564009426964> *PROBABLY*\n<:myE:584998291901644836> *PROBABLY NOT*"

		embed = discord.Embed(description=description, color=0x86BFF4)
		embed.set_author(name="──── Guess Who? ────")

		message = await ctx.send(embed=embed)
		await message.add_reaction('<:myright:584973342793138197>')

		try:
			reaction, user = await self.bot.wait_for('reaction_add', timeout=120.0, check=check)

			if str(reaction.emoji) == '<:myright:584973342793138197>':

				await message.clear_reactions()

				try:
					if lang == "fr":
						try:
							question = await self.aki.start_game(language=lang)
						except:
							try:
								question = await self.aki.start_game(language="fr2")
							except:
								await message.edit(content="Servers are down in this region. Try again later or use a different language. :slight_frown:", embed=None)

								await message.delete(delay=5.0)

								if ctx.me.permissions_in(ctx.message.channel).manage_messages:
									# delete the message command
									await ctx.message.delete(delay=5.0)
					else:
						try:
							question = await self.aki.start_game(language=lang)
						except:
							await message.edit(content="Servers are down in this region. Try again later or use a different language. :slight_frown:", embed=None)

							await message.delete(delay=5.0)

							if ctx.me.permissions_in(ctx.message.channel).manage_messages:
								# delete the message command
								await ctx.message.delete(delay=5.0)
				except:
					try:
						question = await self.aki.start_game(language="en")
					except:
						await message.edit(content="Servers are down in this region. Try again later or use a different language. :slight_frown:", embed=None)

						await message.delete(delay=5.0)

						if ctx.me.permissions_in(ctx.message.channel).manage_messages:
							# delete the message command
							await ctx.message.delete(delay=5.0)

				question = '**'+question+'**'+options

				embed = discord.Embed(description=question, color=0x86BFF4)
				embed.set_author(name="──── Guess Who? ────")

				await message.edit(embed=embed)

				for button in buttons[:6]:
					await message.add_reaction(button)

				while self.aki.progression <= 90:
					try:
						reaction, user = await self.bot.wait_for('reaction_add', timeout=20.0, check=check)

						if str(reaction.emoji) == '<:myA:584978563204120577>':
							await message.remove_reaction(reaction, user)
							question = await self.aki.answer("y")
							question = '**'+question+'**'+options

							embed = discord.Embed(description=question, color=0x86BFF4)
							embed.set_author(name="──── Guess Who? ────")

							await message.edit(embed=embed)

						elif str(reaction.emoji) == '<:myB:592285509863211009>':
							await message.remove_reaction(reaction, user)
							question = await self.aki.answer("n")
							question = '**'+question+'**'+options

							embed = discord.Embed(description=question, color=0x86BFF4)
							embed.set_author(name="──── Guess Who? ────")

							await message.edit(embed=embed)

						elif str(reaction.emoji) == '<:myC:584978564521263127>':
							await message.remove_reaction(reaction, user)
							question = await self.aki.answer("idk")
							question = '**'+question+'**'+options

							embed = discord.Embed(description=question, color=0x86BFF4)
							embed.set_author(name="──── Guess Who? ────")

							await message.edit(embed=embed)

						elif str(reaction.emoji) == '<:myD:584978564009426964>':
							await message.remove_reaction(reaction, user)
							question = await self.aki.answer("p")
							question = '**'+question+'**'+options

							embed = discord.Embed(description=question, color=0x86BFF4)
							embed.set_author(name="──── Guess Who? ────")

							await message.edit(embed=embed)

						elif str(reaction.emoji) == '<:myE:584998291901644836>':
							await message.remove_reaction(reaction, user)
							question = await self.aki.answer("pn")
							question = '**'+question+'**'+options

							embed = discord.Embed(description=question, color=0x86BFF4)
							embed.set_author(name="──── Guess Who? ────")

							await message.edit(embed=embed)

						elif str(reaction.emoji) == '<:myleft:584972740595810304>':
							await message.remove_reaction(reaction, user)
							try:	
								question = await self.aki.back()
								question = '**'+question+'**'+options

								embed = discord.Embed(description=question, color=0x86BFF4)
								embed.set_author(name="──── Guess Who? ────")

								await message.edit(embed=embed)

							except:
								pass

						else:
							await message.remove_reaction(reaction, user)
					
					except asyncio.TimeoutError:
						await message.delete()
						message = None
						await ctx.send("*You failed to respond.*\n**GAME OVER!**")
						break


				if message:
					await message.clear_reactions()
					await self.aki.win()

					answer = f"It's **{self.aki.name}** \n*{self.aki.description}*!\n\nWas I correct?\n<:myA:584978563204120577> *YES*\t<:myB:592285509863211009> *NO*"
					
					embed = discord.Embed(description=answer, color=0x86BFF4)
					embed.set_author(name="──── Guess Who? ────")
					embed.set_image(url=self.aki.picture)
					
					await message.edit(embed=embed)

					for button in buttons[:2]:
						await message.add_reaction(button)


					try:
						reaction, user = await self.bot.wait_for('reaction_add', timeout=20.0, check=check)

						if str(reaction.emoji) == '<:myA:584978563204120577>':
							await message.edit(content="**Hurray!!! I made it.** :sunglasses:")

						elif str(reaction.emoji) == '<:myB:592285509863211009>':
							await message.edit(content="**I might try my best next time. Thanks for playing** :pensive:")

						else:
							await message.clear_reactions()

					except asyncio.TimeoutError:
						await message.clear_reactions()
						await message.edit(content="Well you didn't respond in time. :slight_frown: ")

			else:
				await message.clear_reactions()

		
		except asyncio.TimeoutError:
			await message.clear_reactions()
			await message.edit(content="Sorry but I've also other things to do than waiting for you to respond. :sweat_smile:", embed=None)



def setup(bot):
	bot.add_cog(Games(bot))
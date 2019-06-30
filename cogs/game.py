import discord
from discord.ext import commands
from discord.ext.commands.cooldowns import BucketType
from akinator.async_aki import Akinator
import akinator
import asyncio
import random
import re

class Games(commands.Cog):

	def __init__(self, bot):

		self.bot = bot
		self.aki = Akinator()


	@commands.group(case_insensitive=True)
	@commands.cooldown(10,600,type=BucketType.member)
	@commands.guild_only()
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

		embed.add_field(name="**t-game tictactoe <@user>**", value="`└─ Starts the tictactoe game with the mentioned user.`", inline=False)
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




	@game.command()
	async def tictactoe(self, ctx, player=None):
		'''Starts a tic-tac-toe game'''

		buttons = [
			'<:mys1:593695781194694669>',
			'<:mys2:593696851165839380>',
			'<:mys3:593696876587515914>',
			'<:mys4:593696927426805779>',
			'<:mys5:593696937061122058>',
			'<:mys6:593696945059659777>',
			'<:mys7:593696953569640460>',
			'<:mys8:593696962411495475>',
			'<:mys9:593696973782253598>'
		]

		noughts = {
			'mys1': '<:myo1:593751555484680212>',
			'mys2': '<:myo2:593751565475643393>',
			'mys3': '<:myo3:593751576145952791>',
			'mys4': '<:myo4:593751590582747137>',
			'mys5': '<:myo5:593751601873944576>',
			'mys6': '<:myo6:593751613081124864>',
			'mys7': '<:myo7:593751769218023437>',
			'mys8': '<:myo8:593751780374872075>',
			'mys9': '<:myo9:593751796900691978>'
		}

		crosses = {
			'mys1': '<:myx1:593751813170266117>',
			'mys2': '<:myx2:593751826696896512>',
			'mys3': '<:myx3:593751990635462666>',
			'mys4': '<:myx4:593752084206059539>',
			'mys5': '<:myx5:593752097959313418>',
			'mys6': '<:myx6:593752111917826049>',
			'mys7': '<:myx7:593752127554322462>',
			'mys8': '<:myx8:593752144654368768>',
			'mys9': '<:myx9:593752156285304851>'
		}

		board = "<:s1:593739203771236372> <:s2:593739203561390113> <:s3:593747848068202525>\n<:s4:593747859187171331> <:s5:593745794415329290> <:s6:593744480797065216>\n<:s7:593744500334264320> <:s8:593744516763090954> <:s9:593744531732824094>"

		if player is not None:
			# let's play a game with the player

			player = await commands.MemberConverter().convert(ctx, player)

			who_s_turn = [ctx.author, player]
			tictac = [noughts, crosses]
			
			# let tsuby decide who will go first
			player1 =  random.choice(who_s_turn)
			who_s_turn.remove(player1)
			player2 = who_s_turn[0]

			#let computer decide what to choose for player_1 and player_2
			# X or O ?
			player_1 = random.choice(tictac)
			tictac.remove(player_1)
			player_2 = tictac[0]


			def check_move_player1(reaction, user):
				return user == player1 and str(reaction.emoji) in buttons and (reaction.message.id == message.id)

			def check_move_player2(reaction, user):
				return user == player2 and str(reaction.emoji) in buttons and (reaction.message.id == message.id)

			'''def check(reaction, user):
				return (user == ctx.message.author or user == player) and str(reaction.emoji) == "<a:tcrossedfinger:592291117215645697>" and (reaction.message.id == message.id)'''


			tictactoe = board

			embed = discord.Embed(description=f"*It's {player1.name}'s turn.*", color=0x86BFF4)
			embed.set_author(name="Tic-Tac-Toe")
			embed.set_thumbnail(url="https://raw.githubusercontent.com/J16N/tsuby/master/tictactoe-thumbnail.png")
			embed.add_field(name="**How To Play**", value="`React to a number to mark on that particular field.`\n", inline=False)
			embed.add_field(name="**Game**", value=tictactoe, inline=False)
			embed.set_footer(text=f"Currently Playing | {player1.name} vs {player2.name}", icon_url="https://raw.githubusercontent.com/J16N/tsuby/master/cogs/tsuby.png")

			message = await ctx.send(embed=embed)
			
			for button in buttons:
				await message.add_reaction(button)

			initial_move = 0

			while initial_move < 9:

				if not initial_move % 2:

					try:
						reaction, user = await self.bot.wait_for('reaction_add', timeout=60.0, check=check_move_player1)
						
						tictactoe = re.sub("<:"+reaction.emoji.name[2:]+":\d+>", player_1[reaction.emoji.name], tictactoe)

						initial_move += 1

						embed = discord.Embed(description=f"*It's {player2.name}'s turn.*", color=0x86BFF4)
						embed.set_author(name="Tic-Tac-Toe")
						embed.set_thumbnail(url="https://raw.githubusercontent.com/J16N/tsuby/master/tictactoe-thumbnail.png")
						embed.add_field(name="**How To Play**", value="`React to a number to mark on that particular field.`\n", inline=False)
						embed.add_field(name="**Game**", value=tictactoe, inline=False)
						embed.set_footer(text=f"Currently Playing | {player1.name} vs {player2.name}", icon_url="https://raw.githubusercontent.com/J16N/tsuby/master/cogs/tsuby.png")

						await message.edit(embed=embed)

						await message.remove_reaction(reaction, user)
						await message.remove_reaction(reaction, ctx.me)


						winning_string = tictactoe.replace('\n', ' ').split()

						if winning_string[0][2:5] == winning_string[1][2:5] == winning_string[2][2:5] or \
						winning_string[3][2:5] == winning_string[4][2:5] == winning_string[5][2:5] or \
						winning_string[6][2:5] == winning_string[7][2:5] == winning_string[8][2:5] or \
						winning_string[0][2:5] == winning_string[3][2:5] == winning_string[6][2:5] or \
						winning_string[1][2:5] == winning_string[4][2:5] == winning_string[7][2:5] or \
						winning_string[2][2:5] == winning_string[5][2:5] == winning_string[8][2:5] or \
						winning_string[0][2:5] == winning_string[4][2:5] == winning_string[8][2:5] or \
						winning_string[2][2:5] == winning_string[4][2:5] == winning_string[6][2:5]:
							await message.clear_reactions()
							await message.edit(content=f"**Congratulation !!**\n{player1.mention} won. <a:trainbowconfetti:572049858643623956>", embed=None)
							break


					except asyncio.TimeoutError:
						await message.clear_reactions()
						await message.edit(content=f"{player1.mention} missed the turn. What a noob! :laughing:", embed=None)
						break

				else:
								
					try:
						reaction, user = await self.bot.wait_for('reaction_add', timeout=60.0, check=check_move_player2)
						
						tictactoe = re.sub("<:"+reaction.emoji.name[2:]+":\d+>", player_2[reaction.emoji.name], tictactoe)

						initial_move += 1

						embed = discord.Embed(description=f"*It's {player1.name}'s turn.*", color=0x86BFF4)
						embed.set_author(name="Tic-Tac-Toe")
						embed.set_thumbnail(url="https://raw.githubusercontent.com/J16N/tsuby/master/tictactoe-thumbnail.png")
						embed.add_field(name="**How To Play**", value="`React to a number to mark on that particular field.`\n", inline=False)
						embed.add_field(name="**Game**", value=tictactoe, inline=False)
						embed.set_footer(text=f"Currently Playing | {player1.name} vs {player2.name}", icon_url="https://raw.githubusercontent.com/J16N/tsuby/master/cogs/tsuby.png")

						await message.edit(embed=embed)

						await message.remove_reaction(reaction, user)
						await message.remove_reaction(reaction, ctx.me)


						winning_string = tictactoe.replace('\n', ' ').split()

						if winning_string[0][2:5] == winning_string[1][2:5] == winning_string[2][2:5] or \
						winning_string[3][2:5] == winning_string[4][2:5] == winning_string[5][2:5] or \
						winning_string[6][2:5] == winning_string[7][2:5] == winning_string[8][2:5] or \
						winning_string[0][2:5] == winning_string[3][2:5] == winning_string[6][2:5] or \
						winning_string[1][2:5] == winning_string[4][2:5] == winning_string[7][2:5] or \
						winning_string[2][2:5] == winning_string[5][2:5] == winning_string[8][2:5] or \
						winning_string[0][2:5] == winning_string[4][2:5] == winning_string[8][2:5] or \
						winning_string[2][2:5] == winning_string[4][2:5] == winning_string[6][2:5]:
							await message.clear_reactions()
							await message.edit(content=f"**Congratulation !!**\n{player2.mention} won. <a:trainbowconfetti:572049858643623956>", embed=None)
							break


					except asyncio.TimeoutError:
						await message.clear_reactions()
						await message.edit(content=f"{player2.mention} missed the turn. What a noob! :laughing:", embed=None)
						break


			if initial_move == 9:
				winning_string = tictactoe.replace('\n', ' ').split()

				if winning_string[0][2:5] == winning_string[1][2:5] == winning_string[2][2:5] or \
				winning_string[3][2:5] == winning_string[4][2:5] == winning_string[5][2:5] or \
				winning_string[6][2:5] == winning_string[7][2:5] == winning_string[8][2:5] or \
				winning_string[0][2:5] == winning_string[3][2:5] == winning_string[6][2:5] or \
				winning_string[1][2:5] == winning_string[4][2:5] == winning_string[7][2:5] or \
				winning_string[2][2:5] == winning_string[5][2:5] == winning_string[8][2:5] or \
				winning_string[0][2:5] == winning_string[4][2:5] == winning_string[8][2:5] or \
				winning_string[2][2:5] == winning_string[4][2:5] == winning_string[6][2:5]:
					await message.clear_reactions()
					await message.edit(content=f"**Congratulation !!**\n{player1.mention} won. <a:trainbowconfetti:572049858643623956>", embed=None)
				else:
					await message.clear_reactions()
					await message.edit(content=f"*It's a draw...* <a:tcheers:574536125037805568>", embed=None)


		else:
			if ctx.author.id == 302467968095223820:
				'''let's play with Tsuby'''

				who_s_turn = [ctx.me, ctx.author]
				tictac = [noughts, crosses]
				
				# let tsuby decide who will go first
				player1 =  random.choice(who_s_turn)
				who_s_turn.remove(player1)
				player2 = who_s_turn[0]

				#let computer decide what to choose for player_1 and player_2
				# X or O ?
				player_1 = random.choice(tictac)
				tictac.remove(player_1)
				player_2 = tictac[0]

				tictactoe = board
				winning_string = tictactoe.replace('\n', ' ').split()

				def check_move_human(reaction, user):
					return user == ctx.author and str(reaction.emoji) in buttons and (reaction.message.id == message.id)

				available_moves = [0, 1, 2, 3, 4, 5, 6, 7, 8]

				player1 = ctx.author
				player2 = ctx.me

				if player1 == ctx.me:
					embed = discord.Embed(description=f"*It's my turn.*", color=0x86BFF4)
					embed.set_author(name="Tic-Tac-Toe")
					embed.set_thumbnail(url="https://raw.githubusercontent.com/J16N/tsuby/master/tictactoe-thumbnail.png")
					embed.add_field(name="**How To Play**", value="`React to a number to mark on that particular field.`\n", inline=False)
					embed.add_field(name="**Game**", value=tictactoe, inline=False)
					embed.set_footer(text=f"Currently Playing | {player1.name} vs {player2.name}", icon_url="https://raw.githubusercontent.com/J16N/tsuby/master/cogs/tsuby.png")

					message = await ctx.send(embed=embed)
					
					for button in buttons:
						await message.add_reaction(button)

					initial_move = 0

					while initial_move < 9:

						if not initial_move % 2:
							if initial_move == 0:
								# bot move
								bot_position = random.randrange(0, 10, 2)
								available_moves.remove(bot_position)
								
								#get the reaction name to remove
								reaction_name = buttons[int(winning_string[bot_position][3]) - 1]
								print(reaction_name)
								emoji = await commands.EmojiConverter().convert(ctx, reaction_name)
								#make a move
								winning_string[bot_position] = player_1[list(player_1.keys())[bot_position]]

								tictactoe = ' '.join(winning_string[:3])+"\n"+' '.join(winning_string[3:6])+"\n"+' '.join(winning_string[6:])

								embed = discord.Embed(description=f"*It's your turn.*", color=0x86BFF4)
								embed.set_author(name="Tic-Tac-Toe")
								embed.set_thumbnail(url="https://raw.githubusercontent.com/J16N/tsuby/master/tictactoe-thumbnail.png")
								embed.add_field(name="**How To Play**", value="`React to a number to mark on that particular field.`\n", inline=False)
								embed.add_field(name="**Game**", value=tictactoe, inline=False)
								embed.set_footer(text=f"Currently Playing | {player1.name} vs {player2.name}", icon_url="https://raw.githubusercontent.com/J16N/tsuby/master/cogs/tsuby.png")

								await message.edit(embed=embed)

								await message.remove_reaction(emoji, ctx.me)

								initial_move += 1


							elif initial_move == 2:

								old_bot_position = bot_position
								old_human_position = human_position

								if bot_position == 4:

									if human_position in [1, 3, 5, 7]:
										bot_position = random.choice([0, 2, 6, 8])

									else:
										bot_position = 8 - human_position
									
								elif human_position == 4:
									bot_position = 8 - bot_position

								elif not (abs(human_position - bot_position) % 3):
									mapping = {'0' : '2', '2': '0', '6': '8', '8': '6'}
									bot_position = int(mapping[str(bot_position)])

								elif abs(human_position - bot_position) == 1:
									mapping = {'0' : '6', '2': '8', '6': '0', '8': '2'}
									bot_position = int(mapping[str(bot_position)])

								else:
									corners = [0, 2, 6, 8]
									if human_position not in corners:
										mapping = {'0' : ['2', '6'], '2': ['0', '8'], '6': ['0', '8'], '8': ['2', '6']}
										bot_position = int(random.choice(mapping[str(bot_position)]))

									else:
										corners.remove(human_position)
										corners.remove(bot_position)

										bot_position = random.choice(corners)

								available_moves.remove(bot_position)

								#get the reaction name to remove
								reaction_name = buttons[int(winning_string[bot_position][3]) - 1]
								emoji = await commands.EmojiConverter().convert(ctx, reaction_name)
								#make a move
								winning_string[bot_position] = player_1[list(player_1.keys())[bot_position]]

								tictactoe = ' '.join(winning_string[:3])+"\n"+' '.join(winning_string[3:6])+"\n"+' '.join(winning_string[6:])

								embed = discord.Embed(description=f"*It's your turn.*", color=0x86BFF4)
								embed.set_author(name="Tic-Tac-Toe")
								embed.set_thumbnail(url="https://raw.githubusercontent.com/J16N/tsuby/master/tictactoe-thumbnail.png")
								embed.add_field(name="**How To Play**", value="`React to a number to mark on that particular field.`\n", inline=False)
								embed.add_field(name="**Game**", value=tictactoe, inline=False)
								embed.set_footer(text=f"Currently Playing | {player1.name} vs {player2.name}", icon_url="https://raw.githubusercontent.com/J16N/tsuby/master/cogs/tsuby.png")

								await message.edit(embed=embed)

								await message.remove_reaction(emoji, ctx.me)

								initial_move += 1


							elif initial_move == 4:

								old_bot_position = bot_position
								old_human_position = human_position


								if winning_string[0][2:5] == winning_string[1][2:5]:
									if 2 in available_moves: bot_position = 2

								if winning_string[1][2:5] == winning_string[2][2:5]:
									if 0 in available_moves: bot_position = 0

								if winning_string[0][2:5] == winning_string[2][2:5]:
									if 1 in available_moves: bot_position = 1

								if winning_string[3][2:5] == winning_string[4][2:5]:
									if 5 in available_moves: bot_position = 5

								if winning_string[4][2:5] == winning_string[5][2:5]:
									if 3 in available_moves: bot_position = 3

								if winning_string[3][2:5] == winning_string[5][2:5]:
									if 4 in available_moves: bot_position = 4

								if winning_string[6][2:5] == winning_string[7][2:5]:
									if 8 in available_moves: bot_position = 8

								if winning_string[7][2:5] == winning_string[8][2:5]:
									if 6 in available_moves: bot_position = 6

								if winning_string[6][2:5] == winning_string[8][2:5]:
									if 7 in available_moves: bot_position = 7

								if winning_string[0][2:5] == winning_string[3][2:5]:
									if 6 in available_moves: bot_position = 6

								if winning_string[3][2:5] == winning_string[6][2:5]:
									if 0 in available_moves: bot_position = 0

								if winning_string[0][2:5] == winning_string[6][2:5]:
									if 3 in available_moves: bot_position = 3

								if winning_string[1][2:5] == winning_string[4][2:5]:
									if 7 in available_moves: bot_position = 7

								if winning_string[4][2:5] == winning_string[7][2:5]:
									if 1 in available_moves: bot_position = 1

								if winning_string[1][2:5] == winning_string[7][2:5]:
									if 4 in available_moves: bot_position = 4

								if winning_string[2][2:5] == winning_string[5][2:5]:
									if 8 in available_moves: bot_position = 8

								if winning_string[5][2:5] == winning_string[8][2:5]:
									if 2 in available_moves: bot_position = 2

								if winning_string[2][2:5] == winning_string[8][2:5]:
									if 5 in available_moves: bot_position = 5

								if winning_string[0][2:5] == winning_string[4][2:5]:
									if 8 in available_moves: bot_position = 8

								if winning_string[4][2:5] == winning_string[8][2:5]:
									if 0 in available_moves: bot_position = 0

								if winning_string[0][2:5] == winning_string[8][2:5]:
									if 4 in available_moves: bot_position = 4

								if winning_string[2][2:5] == winning_string[4][2:5]:
									if 6 in available_moves: bot_position = 6

								if winning_string[4][2:5] == winning_string[6][2:5]:
									if 2 in available_moves: bot_position = 2

								if winning_string[2][2:5] == winning_string[6][2:5]:
									if 4 in available_moves: bot_position = 4

								if old_bot_position == bot_position:
									corners = [0, 2, 6, 8]

									if bot_position in corners:
										corners.remove(bot_position)

									if old_bot_position in corners:
										corners.remove(old_bot_position)

									if human_position in corners:
										corners.remove(human_position)

									if old_human_position in corners:
										corners.remove(old_human_position)

									if corners:
										if abs(old_human_position - old_bot_position) == 1:
											mapping = {'0' : '6', '2': '8', '6': '0', '8': '2'}
											bot_position = int(mapping[str(bot_position)])

										elif not (abs(old_human_position - old_bot_position) % 3):
											mapping = {'0' : '6', '2': '8', '6': '0', '8': '2'}
											bot_position = int(mapping[str(bot_position)])

										else:
											bot_position = random.choice(corners)


									else:

										bot_position = random.choice(available_moves)

								available_moves.remove(bot_position)

								#get the reaction name to remove
								print(winning_string[bot_position][3])
								print(winning_string)
								reaction_name = buttons[int(winning_string[bot_position][3]) - 1]
								emoji = await commands.EmojiConverter().convert(ctx, reaction_name)
								#make a move
								winning_string[bot_position] = player_1[list(player_1.keys())[bot_position]]

								tictactoe = ' '.join(winning_string[:3])+"\n"+' '.join(winning_string[3:6])+"\n"+' '.join(winning_string[6:])

								embed = discord.Embed(description=f"*It's your turn.*", color=0x86BFF4)
								embed.set_author(name="Tic-Tac-Toe")
								embed.set_thumbnail(url="https://raw.githubusercontent.com/J16N/tsuby/master/tictactoe-thumbnail.png")
								embed.add_field(name="**How To Play**", value="`React to a number to mark on that particular field.`\n", inline=False)
								embed.add_field(name="**Game**", value=tictactoe, inline=False)
								embed.set_footer(text=f"Currently Playing | {player1.name} vs {player2.name}", icon_url="https://raw.githubusercontent.com/J16N/tsuby/master/cogs/tsuby.png")

								await message.edit(embed=embed)

								await message.remove_reaction(emoji, ctx.me)

								initial_move += 1

								if winning_string[0][2:5] == winning_string[1][2:5] == winning_string[2][2:5] or \
								winning_string[3][2:5] == winning_string[4][2:5] == winning_string[5][2:5] or \
								winning_string[6][2:5] == winning_string[7][2:5] == winning_string[8][2:5] or \
								winning_string[0][2:5] == winning_string[3][2:5] == winning_string[6][2:5] or \
								winning_string[1][2:5] == winning_string[4][2:5] == winning_string[7][2:5] or \
								winning_string[2][2:5] == winning_string[5][2:5] == winning_string[8][2:5] or \
								winning_string[0][2:5] == winning_string[4][2:5] == winning_string[8][2:5] or \
								winning_string[2][2:5] == winning_string[4][2:5] == winning_string[6][2:5]:
									await message.clear_reactions()
									await message.edit(content=f"**Hurray !!**\nI won. <a:trainbowconfetti:572049858643623956>", embed=None)
									break

							
							elif initial_move == 6:

								old_bot_position = bot_position

								if winning_string[0][2:5] == winning_string[1][2:5]:
									if 2 in available_moves: bot_position = 2

								if winning_string[1][2:5] == winning_string[2][2:5]:
									if 0 in available_moves: bot_position = 0

								if winning_string[0][2:5] == winning_string[2][2:5]:
									if 1 in available_moves: bot_position = 1

								if winning_string[3][2:5] == winning_string[4][2:5]:
									if 5 in available_moves: bot_position = 5

								if winning_string[4][2:5] == winning_string[5][2:5]:
									if 3 in available_moves: bot_position = 3

								if winning_string[3][2:5] == winning_string[5][2:5]:
									if 4 in available_moves: bot_position = 4

								if winning_string[6][2:5] == winning_string[7][2:5]:
									if 8 in available_moves: bot_position = 8

								if winning_string[7][2:5] == winning_string[8][2:5]:
									if 6 in available_moves: bot_position = 6

								if winning_string[6][2:5] == winning_string[8][2:5]:
									if 7 in available_moves: bot_position = 7

								if winning_string[0][2:5] == winning_string[3][2:5]:
									if 6 in available_moves: bot_position = 6

								if winning_string[3][2:5] == winning_string[6][2:5]:
									if 0 in available_moves: bot_position = 0

								if winning_string[0][2:5] == winning_string[6][2:5]:
									if 3 in available_moves: bot_position = 3

								if winning_string[1][2:5] == winning_string[4][2:5]:
									if 7 in available_moves: bot_position = 7

								if winning_string[4][2:5] == winning_string[7][2:5]:
									if 1 in available_moves: bot_position = 1

								if winning_string[1][2:5] == winning_string[7][2:5]:
									if 4 in available_moves: bot_position = 4

								if winning_string[2][2:5] == winning_string[5][2:5]:
									if 8 in available_moves: bot_position = 8

								if winning_string[5][2:5] == winning_string[8][2:5]:
									if 2 in available_moves: bot_position = 2

								if winning_string[2][2:5] == winning_string[8][2:5]:
									if 5 in available_moves: bot_position = 5

								if winning_string[0][2:5] == winning_string[4][2:5]:
									if 8 in available_moves: bot_position = 8

								if winning_string[4][2:5] == winning_string[8][2:5]:
									if 0 in available_moves: bot_position = 0

								if winning_string[0][2:5] == winning_string[8][2:5]:
									if 4 in available_moves: bot_position = 4

								if winning_string[2][2:5] == winning_string[4][2:5]:
									if 6 in available_moves: bot_position = 6

								if winning_string[4][2:5] == winning_string[6][2:5]:
									if 2 in available_moves: bot_position = 2

								if winning_string[2][2:5] == winning_string[6][2:5]:
									if 4 in available_moves: bot_position = 4

								if old_bot_position == bot_position:
									bot_position = random.choice(available_moves)

								available_moves.remove(bot_position)
								
								#get the reaction name to remove
								reaction_name = buttons[int(winning_string[bot_position][3]) - 1]
								emoji = await commands.EmojiConverter().convert(ctx, reaction_name)
								#make a move
								winning_string[bot_position] = player_1[list(player_1.keys())[bot_position]]

								tictactoe = ' '.join(winning_string[:3])+"\n"+' '.join(winning_string[3:6])+"\n"+' '.join(winning_string[6:])

								embed = discord.Embed(description=f"*It's your turn.*", color=0x86BFF4)
								embed.set_author(name="Tic-Tac-Toe")
								embed.set_thumbnail(url="https://raw.githubusercontent.com/J16N/tsuby/master/tictactoe-thumbnail.png")
								embed.add_field(name="**How To Play**", value="`React to a number to mark on that particular field.`\n", inline=False)
								embed.add_field(name="**Game**", value=tictactoe, inline=False)
								embed.set_footer(text=f"Currently Playing | {player1.name} vs {player2.name}", icon_url="https://raw.githubusercontent.com/J16N/tsuby/master/cogs/tsuby.png")

								await message.edit(embed=embed)

								await message.remove_reaction(emoji, ctx.me)

								initial_move += 1

								if winning_string[0][2:5] == winning_string[1][2:5] == winning_string[2][2:5] or \
								winning_string[3][2:5] == winning_string[4][2:5] == winning_string[5][2:5] or \
								winning_string[6][2:5] == winning_string[7][2:5] == winning_string[8][2:5] or \
								winning_string[0][2:5] == winning_string[3][2:5] == winning_string[6][2:5] or \
								winning_string[1][2:5] == winning_string[4][2:5] == winning_string[7][2:5] or \
								winning_string[2][2:5] == winning_string[5][2:5] == winning_string[8][2:5] or \
								winning_string[0][2:5] == winning_string[4][2:5] == winning_string[8][2:5] or \
								winning_string[2][2:5] == winning_string[4][2:5] == winning_string[6][2:5]:
									await message.clear_reactions()
									await message.edit(content=f"**Hurray !!**\nI won. <a:trainbowconfetti:572049858643623956>", embed=None)
									break


							elif initial_move == 8:

								old_bot_position = bot_position

								if winning_string[0][2:5] == winning_string[1][2:5]:
									if 2 in available_moves: bot_position = 2

								if winning_string[1][2:5] == winning_string[2][2:5]:
									if 0 in available_moves: bot_position = 0

								if winning_string[0][2:5] == winning_string[2][2:5]:
									if 1 in available_moves: bot_position = 1

								if winning_string[3][2:5] == winning_string[4][2:5]:
									if 5 in available_moves: bot_position = 5

								if winning_string[4][2:5] == winning_string[5][2:5]:
									if 3 in available_moves: bot_position = 3

								if winning_string[3][2:5] == winning_string[5][2:5]:
									if 4 in available_moves: bot_position = 4

								if winning_string[6][2:5] == winning_string[7][2:5]:
									if 8 in available_moves: bot_position = 8

								if winning_string[7][2:5] == winning_string[8][2:5]:
									if 6 in available_moves: bot_position = 6

								if winning_string[6][2:5] == winning_string[8][2:5]:
									if 7 in available_moves: bot_position = 7

								if winning_string[0][2:5] == winning_string[3][2:5]:
									if 6 in available_moves: bot_position = 6

								if winning_string[3][2:5] == winning_string[6][2:5]:
									if 0 in available_moves: bot_position = 0

								if winning_string[0][2:5] == winning_string[6][2:5]:
									if 3 in available_moves: bot_position = 3

								if winning_string[1][2:5] == winning_string[4][2:5]:
									if 7 in available_moves: bot_position = 7

								if winning_string[4][2:5] == winning_string[7][2:5]:
									if 1 in available_moves: bot_position = 1

								if winning_string[1][2:5] == winning_string[7][2:5]:
									if 4 in available_moves: bot_position = 4

								if winning_string[2][2:5] == winning_string[5][2:5]:
									if 8 in available_moves: bot_position = 8

								if winning_string[5][2:5] == winning_string[8][2:5]:
									if 2 in available_moves: bot_position = 2

								if winning_string[2][2:5] == winning_string[8][2:5]:
									if 5 in available_moves: bot_position = 5

								if winning_string[0][2:5] == winning_string[4][2:5]:
									if 8 in available_moves: bot_position = 8

								if winning_string[4][2:5] == winning_string[8][2:5]:
									if 0 in available_moves: bot_position = 0

								if winning_string[0][2:5] == winning_string[8][2:5]:
									if 4 in available_moves: bot_position = 4

								if winning_string[2][2:5] == winning_string[4][2:5]:
									if 6 in available_moves: bot_position = 6

								if winning_string[4][2:5] == winning_string[6][2:5]:
									if 2 in available_moves: bot_position = 2

								if winning_string[2][2:5] == winning_string[6][2:5]:
									if 4 in available_moves: bot_position = 4

								if old_bot_position == bot_position:
									bot_position = random.choice(available_moves)

								
								available_moves.remove(bot_position)


								#get the reaction name to remove
								reaction_name = buttons[int(winning_string[bot_position][3]) - 1]
								emoji = await commands.EmojiConverter().convert(ctx, reaction_name)
								#make a move
								winning_string[bot_position] = player_1[list(player_1.keys())[bot_position]]

								tictactoe = ' '.join(winning_string[:3])+"\n"+' '.join(winning_string[3:6])+"\n"+' '.join(winning_string[6:])

								embed = discord.Embed(description=f"*It's your turn.*", color=0x86BFF4)
								embed.set_author(name="Tic-Tac-Toe")
								embed.set_thumbnail(url="https://raw.githubusercontent.com/J16N/tsuby/master/tictactoe-thumbnail.png")
								embed.add_field(name="**How To Play**", value="`React to a number to mark on that particular field.`\n", inline=False)
								embed.add_field(name="**Game**", value=tictactoe, inline=False)
								embed.set_footer(text=f"Currently Playing | {player1.name} vs {player2.name}", icon_url="https://raw.githubusercontent.com/J16N/tsuby/master/cogs/tsuby.png")

								await message.edit(embed=embed)

								await message.remove_reaction(emoji, ctx.me)

								initial_move += 1

								if winning_string[0][2:5] == winning_string[1][2:5] == winning_string[2][2:5] or \
								winning_string[3][2:5] == winning_string[4][2:5] == winning_string[5][2:5] or \
								winning_string[6][2:5] == winning_string[7][2:5] == winning_string[8][2:5] or \
								winning_string[0][2:5] == winning_string[3][2:5] == winning_string[6][2:5] or \
								winning_string[1][2:5] == winning_string[4][2:5] == winning_string[7][2:5] or \
								winning_string[2][2:5] == winning_string[5][2:5] == winning_string[8][2:5] or \
								winning_string[0][2:5] == winning_string[4][2:5] == winning_string[8][2:5] or \
								winning_string[2][2:5] == winning_string[4][2:5] == winning_string[6][2:5]:
									await message.clear_reactions()
									await message.edit(content=f"**Hurray !!**\nI won. <a:trainbowconfetti:572049858643623956>", embed=None)
									break


						else:
							try:
								reaction, user = await self.bot.wait_for('reaction_add', timeout=60.0, check=check_move_human)

								tictactoe = re.sub("<:"+reaction.emoji.name[2:]+":\d+>", player_2[reaction.emoji.name], tictactoe)

								# get the human's move
								human_position = int(reaction.emoji.name[3]) - 1

								available_moves.remove(human_position)

								initial_move += 1

								embed = discord.Embed(description=f"*It's my turn.*", color=0x86BFF4)
								embed.set_author(name="Tic-Tac-Toe")
								embed.set_thumbnail(url="https://raw.githubusercontent.com/J16N/tsuby/master/tictactoe-thumbnail.png")
								embed.add_field(name="**How To Play**", value="`React to a number to mark on that particular field.`\n", inline=False)
								embed.add_field(name="**Game**", value=tictactoe, inline=False)
								embed.set_footer(text=f"Currently Playing | {player1.name} vs {player2.name}", icon_url="https://raw.githubusercontent.com/J16N/tsuby/master/cogs/tsuby.png")

								await message.edit(embed=embed)

								await message.remove_reaction(reaction, user)
								await message.remove_reaction(reaction, ctx.me)


								winning_string = tictactoe.replace('\n', ' ').split()

								if winning_string[0][2:5] == winning_string[1][2:5] == winning_string[2][2:5] or \
								winning_string[3][2:5] == winning_string[4][2:5] == winning_string[5][2:5] or \
								winning_string[6][2:5] == winning_string[7][2:5] == winning_string[8][2:5] or \
								winning_string[0][2:5] == winning_string[3][2:5] == winning_string[6][2:5] or \
								winning_string[1][2:5] == winning_string[4][2:5] == winning_string[7][2:5] or \
								winning_string[2][2:5] == winning_string[5][2:5] == winning_string[8][2:5] or \
								winning_string[0][2:5] == winning_string[4][2:5] == winning_string[8][2:5] or \
								winning_string[2][2:5] == winning_string[4][2:5] == winning_string[6][2:5]:
									await message.clear_reactions()
									await message.edit(content=f"**Congratulation !!**\nYou won. <a:trainbowconfetti:572049858643623956>", embed=None)
									break

							except asyncio.TimeoutError:
								await message.clear_reactions()
								await message.edit(content=f"You missed your turn. What a noob! :laughing:", embed=None)
								break

					if initial_move == 9:

						print("I ran")

						if winning_string[0][2:5] == winning_string[1][2:5] == winning_string[2][2:5] or \
							winning_string[3][2:5] == winning_string[4][2:5] == winning_string[5][2:5] or \
							winning_string[6][2:5] == winning_string[7][2:5] == winning_string[8][2:5] or \
							winning_string[0][2:5] == winning_string[3][2:5] == winning_string[6][2:5] or \
							winning_string[1][2:5] == winning_string[4][2:5] == winning_string[7][2:5] or \
							winning_string[2][2:5] == winning_string[5][2:5] == winning_string[8][2:5] or \
							winning_string[0][2:5] == winning_string[4][2:5] == winning_string[8][2:5] or \
							winning_string[2][2:5] == winning_string[4][2:5] == winning_string[6][2:5]:
								await message.clear_reactions()
								await message.edit(content=f"**Hurray !!**\nI won. <a:trainbowconfetti:572049858643623956>", embed=None)

						else:
							await message.clear_reactions()
							await message.edit(content=f"*It's a draw...Well played!* <a:tcheers:574536125037805568>", embed=None)


				
				else:
					embed = discord.Embed(description=f"*It's your turn.*", color=0x86BFF4)
					embed.set_author(name="Tic-Tac-Toe")
					embed.set_thumbnail(url="https://raw.githubusercontent.com/J16N/tsuby/master/tictactoe-thumbnail.png")
					embed.add_field(name="**How To Play**", value="`React to a number to mark on that particular field.`\n", inline=False)
					embed.add_field(name="**Game**", value=tictactoe, inline=False)
					embed.set_footer(text=f"Currently Playing | {player1.name} vs {player2.name}", icon_url="https://raw.githubusercontent.com/J16N/tsuby/master/cogs/tsuby.png")

					message = await ctx.send(embed=embed)
					
					for button in buttons:
						await message.add_reaction(button)

					initial_move = 0

					while initial_move < 9:

						if initial_move % 2:
							if initial_move == 1:
								if human_position == 4:
									bot_position = random.choice([0, 2, 6, 8])
								else:
									bot_position = 4
								
								#get the reaction name to remove
								reaction_name = buttons[int(winning_string[bot_position][5]) - 1]
								emoji = await commands.EmojiConverter().convert(ctx, reaction_name)
								#make a move
								winning_string[bot_position] = player_1[list(player_1.keys())[bot_position]]

								tictactoe = ' '.join(winning_string[:3])+"\n"+' '.join(winning_string[3:6])+"\n"+' '.join(winning_string[6:])

								embed = discord.Embed(description=f"*It's your turn.*", color=0x86BFF4)
								embed.set_author(name="Tic-Tac-Toe")
								embed.set_thumbnail(url="https://raw.githubusercontent.com/J16N/tsuby/master/tictactoe-thumbnail.png")
								embed.add_field(name="**How To Play**", value="`React to a number to mark on that particular field.`\n", inline=False)
								embed.add_field(name="**Game**", value=tictactoe, inline=False)
								embed.set_footer(text=f"Currently Playing | {player1.name} vs {player2.name}", icon_url="https://raw.githubusercontent.com/J16N/tsuby/master/cogs/tsuby.png")

								await message.edit(embed=embed)

								await message.remove_reaction(emoji, ctx.me)

								initial_move += 1


							elif initial_move == 3:

								old_bot_position = bot_position
								old_human_position = human_position

								if winning_string[0][2:5] == winning_string[1][2:5]:
									if 2 in available_moves: bot_position = 2

								if winning_string[1][2:5] == winning_string[2][2:5]:
									if 0 in available_moves: bot_position = 0

								if winning_string[0][2:5] == winning_string[2][2:5]:
									if 1 in available_moves: bot_position = 1

								if winning_string[3][2:5] == winning_string[4][2:5]:
									if 5 in available_moves: bot_position = 5

								if winning_string[4][2:5] == winning_string[5][2:5]:
									if 3 in available_moves: bot_position = 3

								if winning_string[3][2:5] == winning_string[5][2:5]:
									if 4 in available_moves: bot_position = 4

								if winning_string[6][2:5] == winning_string[7][2:5]:
									if 8 in available_moves: bot_position = 8

								if winning_string[7][2:5] == winning_string[8][2:5]:
									if 6 in available_moves: bot_position = 6

								if winning_string[6][2:5] == winning_string[8][2:5]:
									if 7 in available_moves: bot_position = 7

								if winning_string[0][2:5] == winning_string[3][2:5]:
									if 6 in available_moves: bot_position = 6

								if winning_string[3][2:5] == winning_string[6][2:5]:
									if 0 in available_moves: bot_position = 0

								if winning_string[0][2:5] == winning_string[6][2:5]:
									if 3 in available_moves: bot_position = 3

								if winning_string[1][2:5] == winning_string[4][2:5]:
									if 7 in available_moves: bot_position = 7

								if winning_string[4][2:5] == winning_string[7][2:5]:
									if 1 in available_moves: bot_position = 1

								if winning_string[1][2:5] == winning_string[7][2:5]:
									if 4 in available_moves: bot_position = 4

								if winning_string[2][2:5] == winning_string[5][2:5]:
									if 8 in available_moves: bot_position = 8

								if winning_string[5][2:5] == winning_string[8][2:5]:
									if 2 in available_moves: bot_position = 2

								if winning_string[2][2:5] == winning_string[8][2:5]:
									if 5 in available_moves: bot_position = 5

								if winning_string[0][2:5] == winning_string[4][2:5]:
									if 8 in available_moves: bot_position = 8

								if winning_string[4][2:5] == winning_string[8][2:5]:
									if 0 in available_moves: bot_position = 0

								if winning_string[0][2:5] == winning_string[8][2:5]:
									if 4 in available_moves: bot_position = 4

								if winning_string[2][2:5] == winning_string[4][2:5]:
									if 6 in available_moves: bot_position = 6

								if winning_string[4][2:5] == winning_string[6][2:5]:
									if 2 in available_moves: bot_position = 2

								if winning_string[2][2:5] == winning_string[6][2:5]:
									if 4 in available_moves: bot_position = 4

								if old_bot_position == bot_position:
									corners = [0, 2, 6, 8]

									if bot_position in corners:
										corners.remove(bot_position)

									if old_bot_position in corners:
										corners.remove(old_bot_position)

									if human_position in corners:
										corners.remove(human_position)

									if old_human_position in corners:
										corners.remove(old_human_position)

									if corners:
										if abs(old_human_position - old_bot_position) == 1:
											mapping = {'0' : '6', '2': '8', '6': '0', '8': '2'}
											bot_position = int(mapping[str(bot_position)])

										elif not (abs(old_human_position - old_bot_position) % 3):
											mapping = {'0' : '6', '2': '8', '6': '0', '8': '2'}
											bot_position = int(mapping[str(bot_position)])

										else:
											bot_position = random.choice(corners)


									else:

										bot_position = random.choice(available_moves)

								available_moves.remove(bot_position)

								#get the reaction name to remove
								print(winning_string[bot_position][3])
								print(winning_string)
								reaction_name = buttons[int(winning_string[bot_position][5]) - 1]
								emoji = await commands.EmojiConverter().convert(ctx, reaction_name)
								#make a move
								winning_string[bot_position] = player_1[list(player_1.keys())[bot_position]]

								tictactoe = ' '.join(winning_string[:3])+"\n"+' '.join(winning_string[3:6])+"\n"+' '.join(winning_string[6:])

								embed = discord.Embed(description=f"*It's your turn.*", color=0x86BFF4)
								embed.set_author(name="Tic-Tac-Toe")
								embed.set_thumbnail(url="https://raw.githubusercontent.com/J16N/tsuby/master/tictactoe-thumbnail.png")
								embed.add_field(name="**How To Play**", value="`React to a number to mark on that particular field.`\n", inline=False)
								embed.add_field(name="**Game**", value=tictactoe, inline=False)
								embed.set_footer(text=f"Currently Playing | {player1.name} vs {player2.name}", icon_url="https://raw.githubusercontent.com/J16N/tsuby/master/cogs/tsuby.png")

								await message.edit(embed=embed)

								await message.remove_reaction(emoji, ctx.me)

								initial_move += 1

								if winning_string[0][2:5] == winning_string[1][2:5] == winning_string[2][2:5] or \
								winning_string[3][2:5] == winning_string[4][2:5] == winning_string[5][2:5] or \
								winning_string[6][2:5] == winning_string[7][2:5] == winning_string[8][2:5] or \
								winning_string[0][2:5] == winning_string[3][2:5] == winning_string[6][2:5] or \
								winning_string[1][2:5] == winning_string[4][2:5] == winning_string[7][2:5] or \
								winning_string[2][2:5] == winning_string[5][2:5] == winning_string[8][2:5] or \
								winning_string[0][2:5] == winning_string[4][2:5] == winning_string[8][2:5] or \
								winning_string[2][2:5] == winning_string[4][2:5] == winning_string[6][2:5]:
									await message.clear_reactions()
									await message.edit(content=f"**Hurray !!**\nI won. <a:trainbowconfetti:572049858643623956>", embed=None)
									break


							elif initial_move == 5:

								old_bot_position = bot_position

								print(bot_position)

								if winning_string[0][2:5] == winning_string[1][2:5]:
									if 2 in available_moves: bot_position = 2

								if winning_string[1][2:5] == winning_string[2][2:5]:
									if 0 in available_moves: bot_position = 0

								if winning_string[0][2:5] == winning_string[2][2:5]:
									if 1 in available_moves: bot_position = 1

								if winning_string[3][2:5] == winning_string[4][2:5]:
									if 5 in available_moves: bot_position = 5

								if winning_string[4][2:5] == winning_string[5][2:5]:
									if 3 in available_moves: bot_position = 3

								if winning_string[3][2:5] == winning_string[5][2:5]:
									if 4 in available_moves: bot_position = 4

								if winning_string[6][2:5] == winning_string[7][2:5]:
									if 8 in available_moves: bot_position = 8

								if winning_string[7][2:5] == winning_string[8][2:5]:
									if 6 in available_moves: bot_position = 6

								if winning_string[6][2:5] == winning_string[8][2:5]:
									if 7 in available_moves: bot_position = 7

								if winning_string[0][2:5] == winning_string[3][2:5]:
									if 6 in available_moves: bot_position = 6

								if winning_string[3][2:5] == winning_string[6][2:5]:
									if 0 in available_moves: bot_position = 0

								if winning_string[0][2:5] == winning_string[6][2:5]:
									if 3 in available_moves: bot_position = 3

								if winning_string[1][2:5] == winning_string[4][2:5]:
									if 7 in available_moves: bot_position = 7

								if winning_string[4][2:5] == winning_string[7][2:5]:
									if 1 in available_moves: bot_position = 1

								if winning_string[1][2:5] == winning_string[7][2:5]:
									if 4 in available_moves: bot_position = 4

								if winning_string[2][2:5] == winning_string[5][2:5]:
									if 8 in available_moves: bot_position = 8

								if winning_string[5][2:5] == winning_string[8][2:5]:
									if 2 in available_moves: bot_position = 2

								if winning_string[2][2:5] == winning_string[8][2:5]:
									if 5 in available_moves: bot_position = 5

								if winning_string[0][2:5] == winning_string[4][2:5]:
									if 8 in available_moves: bot_position = 8

								if winning_string[4][2:5] == winning_string[8][2:5]:
									if 0 in available_moves: bot_position = 0

								if winning_string[0][2:5] == winning_string[8][2:5]:
									if 4 in available_moves: bot_position = 4

								if winning_string[2][2:5] == winning_string[4][2:5]:
									if 6 in available_moves: bot_position = 6

								if winning_string[4][2:5] == winning_string[6][2:5]:
									if 2 in available_moves: bot_position = 2

								if winning_string[2][2:5] == winning_string[6][2:5]:
									if 4 in available_moves: bot_position = 4

								if old_bot_position == bot_position:
									bot_position = random.choice(available_moves)

								print(bot_position)

								available_moves.remove(bot_position)

								#get the reaction name to remove
								reaction_name = buttons[int(winning_string[bot_position][5]) - 1]
								emoji = await commands.EmojiConverter().convert(ctx, reaction_name)
								#make a move
								winning_string[bot_position] = player_1[list(player_1.keys())[bot_position]]

								tictactoe = ' '.join(winning_string[:3])+"\n"+' '.join(winning_string[3:6])+"\n"+' '.join(winning_string[6:])

								embed = discord.Embed(description=f"*It's your turn.*", color=0x86BFF4)
								embed.set_author(name="Tic-Tac-Toe")
								embed.set_thumbnail(url="https://raw.githubusercontent.com/J16N/tsuby/master/tictactoe-thumbnail.png")
								embed.add_field(name="**How To Play**", value="`React to a number to mark on that particular field.`\n", inline=False)
								embed.add_field(name="**Game**", value=tictactoe, inline=False)
								embed.set_footer(text=f"Currently Playing | {player1.name} vs {player2.name}", icon_url="https://raw.githubusercontent.com/J16N/tsuby/master/cogs/tsuby.png")

								await message.edit(embed=embed)

								await message.remove_reaction(emoji, ctx.me)

								initial_move += 1

								if winning_string[0][2:5] == winning_string[1][2:5] == winning_string[2][2:5] or \
								winning_string[3][2:5] == winning_string[4][2:5] == winning_string[5][2:5] or \
								winning_string[6][2:5] == winning_string[7][2:5] == winning_string[8][2:5] or \
								winning_string[0][2:5] == winning_string[3][2:5] == winning_string[6][2:5] or \
								winning_string[1][2:5] == winning_string[4][2:5] == winning_string[7][2:5] or \
								winning_string[2][2:5] == winning_string[5][2:5] == winning_string[8][2:5] or \
								winning_string[0][2:5] == winning_string[4][2:5] == winning_string[8][2:5] or \
								winning_string[2][2:5] == winning_string[4][2:5] == winning_string[6][2:5]:
									await message.clear_reactions()
									await message.edit(content=f"**Hurray !!**\nI won. <a:trainbowconfetti:572049858643623956>", embed=None)
									break

							
							elif initial_move == 7:

								old_bot_position = bot_position

								if winning_string[0][2:5] == winning_string[1][2:5]:
									if 2 in available_moves: bot_position = 2

								if winning_string[1][2:5] == winning_string[2][2:5]:
									if 0 in available_moves: bot_position = 0

								if winning_string[0][2:5] == winning_string[2][2:5]:
									if 1 in available_moves: bot_position = 1

								if winning_string[3][2:5] == winning_string[4][2:5]:
									if 5 in available_moves: bot_position = 5

								if winning_string[4][2:5] == winning_string[5][2:5]:
									if 3 in available_moves: bot_position = 3

								if winning_string[3][2:5] == winning_string[5][2:5]:
									if 4 in available_moves: bot_position = 4

								if winning_string[6][2:5] == winning_string[7][2:5]:
									if 8 in available_moves: bot_position = 8

								if winning_string[7][2:5] == winning_string[8][2:5]:
									if 6 in available_moves: bot_position = 6

								if winning_string[6][2:5] == winning_string[8][2:5]:
									if 7 in available_moves: bot_position = 7

								if winning_string[0][2:5] == winning_string[3][2:5]:
									if 6 in available_moves: bot_position = 6

								if winning_string[3][2:5] == winning_string[6][2:5]:
									if 0 in available_moves: bot_position = 0

								if winning_string[0][2:5] == winning_string[6][2:5]:
									if 3 in available_moves: bot_position = 3

								if winning_string[1][2:5] == winning_string[4][2:5]:
									if 7 in available_moves: bot_position = 7

								if winning_string[4][2:5] == winning_string[7][2:5]:
									if 1 in available_moves: bot_position = 1

								if winning_string[1][2:5] == winning_string[7][2:5]:
									if 4 in available_moves: bot_position = 4

								if winning_string[2][2:5] == winning_string[5][2:5]:
									if 8 in available_moves: bot_position = 8

								if winning_string[5][2:5] == winning_string[8][2:5]:
									if 2 in available_moves: bot_position = 2

								if winning_string[2][2:5] == winning_string[8][2:5]:
									if 5 in available_moves: bot_position = 5

								if winning_string[0][2:5] == winning_string[4][2:5]:
									if 8 in available_moves: bot_position = 8

								if winning_string[4][2:5] == winning_string[8][2:5]:
									if 0 in available_moves: bot_position = 0

								if winning_string[0][2:5] == winning_string[8][2:5]:
									if 4 in available_moves: bot_position = 4

								if winning_string[2][2:5] == winning_string[4][2:5]:
									if 6 in available_moves: bot_position = 6

								if winning_string[4][2:5] == winning_string[6][2:5]:
									if 2 in available_moves: bot_position = 2

								if winning_string[2][2:5] == winning_string[6][2:5]:
									if 4 in available_moves: bot_position = 4

								if old_bot_position == bot_position:
									bot_position = random.choice(available_moves)

								available_moves.remove(bot_position)


								#get the reaction name to remove
								reaction_name = buttons[int(winning_string[bot_position][5]) - 1]
								emoji = await commands.EmojiConverter().convert(ctx, reaction_name)
								#make a move
								winning_string[bot_position] = player_1[list(player_1.keys())[bot_position]]

								tictactoe = ' '.join(winning_string[:3])+"\n"+' '.join(winning_string[3:6])+"\n"+' '.join(winning_string[6:])

								embed = discord.Embed(description=f"*It's your turn.*", color=0x86BFF4)
								embed.set_author(name="Tic-Tac-Toe")
								embed.set_thumbnail(url="https://raw.githubusercontent.com/J16N/tsuby/master/tictactoe-thumbnail.png")
								embed.add_field(name="**How To Play**", value="`React to a number to mark on that particular field.`\n", inline=False)
								embed.add_field(name="**Game**", value=tictactoe, inline=False)
								embed.set_footer(text=f"Currently Playing | {player1.name} vs {player2.name}", icon_url="https://raw.githubusercontent.com/J16N/tsuby/master/cogs/tsuby.png")

								await message.edit(embed=embed)

								await message.remove_reaction(emoji, ctx.me)

								initial_move += 1

								if winning_string[0][2:5] == winning_string[1][2:5] == winning_string[2][2:5] or \
								winning_string[3][2:5] == winning_string[4][2:5] == winning_string[5][2:5] or \
								winning_string[6][2:5] == winning_string[7][2:5] == winning_string[8][2:5] or \
								winning_string[0][2:5] == winning_string[3][2:5] == winning_string[6][2:5] or \
								winning_string[1][2:5] == winning_string[4][2:5] == winning_string[7][2:5] or \
								winning_string[2][2:5] == winning_string[5][2:5] == winning_string[8][2:5] or \
								winning_string[0][2:5] == winning_string[4][2:5] == winning_string[8][2:5] or \
								winning_string[2][2:5] == winning_string[4][2:5] == winning_string[6][2:5]:
									await message.clear_reactions()
									await message.edit(content=f"**Hurray !!**\nI won. <a:trainbowconfetti:572049858643623956>", embed=None)
									break


						else:
							try:
								reaction, user = await self.bot.wait_for('reaction_add', timeout=60.0, check=check_move_human)

								tictactoe = re.sub("<:"+reaction.emoji.name[2:]+":\d+>", player_2[reaction.emoji.name], tictactoe)

								# get the human's move
								human_position = int(reaction.emoji.name[3]) - 1
								available_moves.remove(human_position)

								initial_move += 1

								embed = discord.Embed(description=f"*It's my turn.*", color=0x86BFF4)
								embed.set_author(name="Tic-Tac-Toe")
								embed.set_thumbnail(url="https://raw.githubusercontent.com/J16N/tsuby/master/tictactoe-thumbnail.png")
								embed.add_field(name="**How To Play**", value="`React to a number to mark on that particular field.`\n", inline=False)
								embed.add_field(name="**Game**", value=tictactoe, inline=False)
								embed.set_footer(text=f"Currently Playing | {player1.name} vs {player2.name}", icon_url="https://raw.githubusercontent.com/J16N/tsuby/master/cogs/tsuby.png")

								await message.edit(embed=embed)

								await message.remove_reaction(reaction, user)
								await message.remove_reaction(reaction, ctx.me)


								winning_string = tictactoe.replace('\n', ' ').split()

								if winning_string[0][2:5] == winning_string[1][2:5] == winning_string[2][2:5] or \
								winning_string[3][2:5] == winning_string[4][2:5] == winning_string[5][2:5] or \
								winning_string[6][2:5] == winning_string[7][2:5] == winning_string[8][2:5] or \
								winning_string[0][2:5] == winning_string[3][2:5] == winning_string[6][2:5] or \
								winning_string[1][2:5] == winning_string[4][2:5] == winning_string[7][2:5] or \
								winning_string[2][2:5] == winning_string[5][2:5] == winning_string[8][2:5] or \
								winning_string[0][2:5] == winning_string[4][2:5] == winning_string[8][2:5] or \
								winning_string[2][2:5] == winning_string[4][2:5] == winning_string[6][2:5]:
									await message.clear_reactions()
									await message.edit(content=f"**Congratulation !!**\nYou won. <a:trainbowconfetti:572049858643623956>", embed=None)
									break

							except asyncio.TimeoutError:
								await message.clear_reactions()
								await message.edit(content=f"You missed your turn. What a noob! :laughing:", embed=None)
								break

			else:
				await ctx.send("You need to mention a user to play with.")





def setup(bot):
	bot.add_cog(Games(bot))
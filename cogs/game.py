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
from akinator.async_aki import Akinator
import akinator
import asyncio
import random
import re
import itertools

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
			temp = await ctx.send('`t-game help`')

			await temp.delete(delay=3.0)

			if ctx.me.permissions_in(ctx.message.channel).manage_messages:
				# delete the message command
				await ctx.message.delete(delay=3.0)


	@game.command()
	async def help(self, ctx):
		'''Help command for games'''
		embed = discord.Embed(description="*I found the following list of commands.*", color=0x86BFF4)
		embed.set_author(name="Help")
		embed.add_field(name="**t-game guess [language_code (optional)]**", value="`└─ Starts the game where I will try to guess the character you think of. If the optional language is given then the questions are provided in that particular language. This defaults to English. \n\nCurrently supported languages are:\nEnglish (en)\nArabic (ar)\nChinese (cn)\nGerman (de)\nSpanish (es)\nFrench (fr)\nHebrew (il)\nItalian (it)\nJapanese (jp)\nKorean (kr)\nDutch (nl)\nPolish (pl)\nPortuguese (pt)\nRussian (ru)\nTurkish (tr)`", inline=False)

		embed.add_field(name="**t-game tictactoe <@user> (optional)**", value="`└─ Starts the tictactoe game with the mentioned user. Not mentioning any user makes me as your opponent.`", inline=False)
		embed.set_footer(text="Type t-help to get the list of all commands", icon_url="https://raw.githubusercontent.com/J16N/tsuby/master/assets/tsuby-footer.png")

		if ctx.message.guild is not None:
			await ctx.message.add_reaction("📧")
			
		await ctx.author.send(embed=embed)


	@game.command(name="guess")
	async def aki(self, ctx, lang="en2"):
		'''Starts the game Akinator'''

		await ctx.message.channel.trigger_typing()

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

		description = "**You all know the King of Guessing, Akinator right? Well I've had happened to meet him one day. <a:tcowboy:581728970483957761>\nWe enjoyed a lot and at the end of the day, he taught me his secret. <a:twink:611083686959382528>\n\nGuess what? Now I can also tell any character you think of, regardless of that person be real or fictitious. <a:tsunglasses:611083717762351104>\n\nBelow are the basic instructions to play this game.**\n\n**__How To Play__**\n*React with the supported reactions to make a way through the game.*\n\n<:myleft:584972740595810304> *Takes you to the previous question.*\n\n*React to any one of your choosen options to proceed.*\n\n<:myA:584978563204120577>\t\t<:myB:592285509863211009>\t\t<:myC:584978564521263127>\t\t<:myD:584978564009426964>\t\t<:myE:584998291901644836>\n\n**Now it's your turn to think of a character and answer my questions honestly. \nSo what are you waiting for? Go, react to proceed!**"

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

						elif str(reaction.emoji) == '<:myB:592285509863211009>':
							await message.remove_reaction(reaction, user)
							question = await self.aki.answer("n")

						elif str(reaction.emoji) == '<:myC:584978564521263127>':
							await message.remove_reaction(reaction, user)
							question = await self.aki.answer("idk")

						elif str(reaction.emoji) == '<:myD:584978564009426964>':
							await message.remove_reaction(reaction, user)
							question = await self.aki.answer("p")

						elif str(reaction.emoji) == '<:myE:584998291901644836>':
							await message.remove_reaction(reaction, user)
							question = await self.aki.answer("pn")

						elif str(reaction.emoji) == '<:myleft:584972740595810304>':
							await message.remove_reaction(reaction, user)
							try:	
								question = await self.aki.back()
							except:
								pass
						else:
							await message.remove_reaction(reaction, user)

						question = '**'+question+'**'+options

						embed = discord.Embed(description=question, color=0x86BFF4)
						embed.set_author(name="──── Guess Who? ────")

						await message.edit(embed=embed)
					
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
							await message.edit(content="**Hurray!!! I made it.** <a:tsunglasses:611083717762351104>")

						elif str(reaction.emoji) == '<:myB:592285509863211009>':
							await message.edit(content="**I might try my best next time. Thanks for playing** <a:tcry:581729105230168068>")

						else:
							await message.clear_reactions()

					except asyncio.TimeoutError:
						await message.clear_reactions()
						await message.edit(content="Well you didn't respond in time. <a:trollingeyes:581731869847060500>")

			else:
				await message.clear_reactions()

		
		except asyncio.TimeoutError:
			await message.clear_reactions()
			await message.edit(content="Sorry but I've also other things to do than waiting for you to respond. :sweat_smile:", embed=None)




	def check_win(self, winning_string):
		'''Check if the player won tic-tac-toe'''

		winning_string = [i[2:5] for i in winning_string]

		# here the algorithm is to check row, column and diagonal simultaneously

		result = False

		for i in [0, 1, 2]:
			get_row = 3*i
			row = winning_string[get_row:(get_row+3)]
			if row[1:] == row[:-1]:
				result = True
				break

			column = winning_string[i::3]
			if column[1:] == column[:-1]:
				result = True
				break

			if not i % 2:
				diagonal = winning_string[i:9-i:4-i]
				if diagonal[1:] == diagonal[:-1]:
					result = True
					break

		return result




	def about_to_win(self, winning_string, available_moves, botsign):
		'''Check if the bot or the human is winning'''

		# Forget about [2:5] thing. This one is exclusively for discord and nothing to add up in the algorithm
		winning_string = [i[2:6] for i in winning_string]

		botsign = botsign['mys1'][2:5]

		result = False
		position = 0

		for i in [0, 1, 2]:
			get_row = 3*i
			row = winning_string[get_row:(get_row+3)]
			row_check = list(itertools.combinations(row, 2))
			
			for item in row_check:
				if item[0][:3] == item[1][:3] and item[0][:3] == botsign:
					if (int(item[0][3]) + int(item[1][3])) % 3 == 0:
						position = int(item[0][3]) + int(item[1][3]) - get_row

					else:
						position = abs(int(item[0][3]) - int(item[1][3])) + get_row
					
					if (position-1) in available_moves:
						result = True
						break

			if result:
				break

			column = winning_string[i::3]
			column_check = list(itertools.combinations(column, 2))
			
			for item in column_check:
				if item[0][:3] == item[1][:3] and item[0][:3] == botsign:
					if int(item[0][3]) + int(item[1][3]) <= (7+i):
						position = int(item[0][3]) + int(item[1][3]) + (2-i)
					else:
						position = abs(int(item[0][3]) - int(item[1][3])) - (2-i)

					if (position-1) in available_moves:
						result = True
						break

			if result:
				break

			if not i % 2:
				diagonal = winning_string[i:9-i:4-i]
				diagonal_check = list(itertools.combinations(diagonal, 2))
				
				for item in diagonal_check:
					if item[0][:3] == item[1][:3] and item[0][:3] == botsign:
						if i == 0:
							if (int(item[0][3]) + int(item[1][3])) % 3 == 0:
								position = int(item[0][3]) + int(item[1][3]) + 3

							else:
								position = abs(int(item[0][3]) - int(item[1][3])) - 3
						
						else:
							if int(item[0][3]) + int(item[1][3]) == 8:
								position = 7

							else:
								position = abs(int(item[0][3]) - int(item[1][3])) + 1

						if (position-1) in available_moves:
							result = True
							break

			if result:
				break


		if result:
			return position

		else:
			for i in [0, 1, 2]:
				get_row = 3*i
				row = winning_string[get_row:(get_row+3)]
				row_check = list(itertools.combinations(row, 2))
				
				for item in row_check:
					if item[0][:3] == item[1][:3]:					
						if (int(item[0][3]) + int(item[1][3])) % 3 == 0:
							position = int(item[0][3]) + int(item[1][3]) - get_row

						else:
							position = abs(int(item[0][3]) - int(item[1][3])) + get_row
						
						if (position-1) in available_moves:
							result = True
							break

				if result:
					break

				column = winning_string[i::3]
				column_check = list(itertools.combinations(column, 2))
				
				for item in column_check:
					if item[0][:3] == item[1][:3]:
						if int(item[0][3]) + int(item[1][3]) <= (7+i):
							position = int(item[0][3]) + int(item[1][3]) + (2-i)
						else:
							position = abs(int(item[0][3]) - int(item[1][3])) - (2-i)

						if (position-1) in available_moves:
							result = True
							break

				if result:
					break

				if not i % 2:
					diagonal = winning_string[i:9-i:4-i]
					diagonal_check = list(itertools.combinations(diagonal, 2))
					
					for item in diagonal_check:
						if item[0][:3] == item[1][:3]:
							if i == 0:
								if (int(item[0][3]) + int(item[1][3])) % 3 == 0:
									position = int(item[0][3]) + int(item[1][3]) + 3

								else:
									position = abs(int(item[0][3]) - int(item[1][3])) - 3
							
							else:
								if int(item[0][3]) + int(item[1][3]) == 8:
									position = 7

								else:
									position = abs(int(item[0][3]) - int(item[1][3])) + 1

							if (position-1) in available_moves:
								result = True
								break

				if result:
					break


			if result:
				return position

			else:
				return result






	def do_move(self, initial_move=0, bot_position=0, human_position=0, \
		old_bot_position=0, old_human_position=0, winning_string=None, available_moves=None, botsign=None):
		'''Calculates what move to make. In the example X is a bot move and O is of human's'''

		corners = [0, 2, 6, 8]
		edges = [1, 3, 5, 7]

		if initial_move == 0:

			# make the bot place in either corners or center
			return random.randrange(0, 10, 2)

		

		# this means that the opponent goes first
		elif initial_move == 1:

			# when human chooses the center, the bot chooses the random corners
			if human_position == 4:
				return random.choice([0, 2, 6, 8])

			# if not then the bot chooses the center immediately
			else:
				return 4




		elif initial_move == 2:

			# if the bot placed in center
			if bot_position == 4:

				# humans placed in any one of the edges
				if human_position in [1, 3, 5, 7]:
					return random.choice([0, 2, 6, 8])

				else:
					return (8 - human_position)



			
			
			# 0  1  2
			# 3  O  5
			# X  7  8

			# As a smart opponent, place it next to the opposite square, ie, 2

			elif human_position == 4:
				return (8 - bot_position)

			

			# This one is quite interesting
				
			# 0  1  2
			# 3  4  5
			# X  7  8

			# This means that human has either given in either 3 or 0

			elif not (abs(human_position - bot_position) % 3):
				# I am using mapping here because I can't make any algorithm that would
				# follow the pattern (as shown in the mapping). For ex.
				# if the previous bot_position is 0 then the new bot_position will be 2,
				# if the previous bot_position is 2 then the new bot_position will be 0 and
				# so on...

				mapping = {0 : 2, 2: 0, 6: 8, 8: 6}
				return mapping[bot_position]

			

			# This one is also quite interesting
				
			# 0  1  2
			# 3  4  5
			# X  7  8

			# This means that human has either given in 7
			# So if the human_position is just corresponding of bot_position...

			elif abs(human_position - bot_position) == 1:
				mapping = {0 : 6, 2: 8, 6: 0, 8: 2}
				return mapping[bot_position]

			


			# if the human is given in either 1, 2, 5 or 8 then...

			else:

				# Okay once again, if the human has not given in the corners,

				# 0  1  2
				# 3  4  5
				# X  7  8

				# Can be anything among 1, 2 or 5 then, we have 2 possibilities,
				# either to put in 0 or in 8

				if human_position not in corners:
					mapping = {0 : [2, 6], 2: [0, 8], 6: [0, 8], 8: [2, 6]}
					return random.choice(mapping[bot_position])

				

				# Else just put it in any
				# of the corners.

				else:
					unwanted_move = [bot_position, human_position]
					choose_move = [move for move in corners if move not in unwanted_move]

					return random.choice(choose_move)




		elif initial_move == 3:

			# if the human goes first, then from this move, there is good possibility on who will
			# be about to win

			is_winning = self.about_to_win(winning_string, available_moves, botsign)

			if is_winning:
				return (is_winning-1)


			else:

				# X  1  2
				# 3  O  5
				# 6  7  O

				# When this is the case....choosing just any of the two other corners is a safe move

				if (human_position in corners and bot_position in corners):

					unwanted_move = [bot_position, human_position]
					choose_move = [move for move in corners if move not in unwanted_move]

					return random.choice(choose_move)


				
				# O  1  2
				# 3  X  5
				# 6  7  O

				# When this is the case....choosing just any of the 4 edges is a safe move


				elif (human_position in corners and old_human_position in corners):

					return random.choice(edges)

				
				
				# 0  1  2      0  O  2
				# O  X  O  OR  3  X  5
				# 6  7  8      6  O  8

				# When this is the case....choosing any of the 4 corners is a winning move


				elif (old_human_position + human_position) == 8:
					return random.choice(corners)

				
				
				
				# 0  O  2      0  1  2
				# O  X  5      3  4  5
				# 6  7  8      6  7  8

				# When this is the case....

				elif human_position in edges and old_human_position in edges:
					
					mapping = {4: [0, 2, 6], 6: [0, 2, 8], 10: [0, 6, 8], 12: [2, 6, 8]}

					return random.choice(mapping[old_human_position + human_position])

				

				# 0  1  O
				# O  X  5
				# 6  7  8

				# When this is the case....

				else:

					mapping = {1: [0, 2], 3: [0, 6], 5: [2, 8], 7: [6, 8]}

					if old_human_position in edges:
						return random.choice(mapping[old_human_position])

					else:
						return random.choice(mapping[human_position])

							





		elif initial_move == 4:
			# from this move, bot or human might make a winning move, so we'll check them

			is_winning = self.about_to_win(winning_string, available_moves, botsign)
			
			if is_winning:
				return (is_winning-1)

			else:
				unwanted_move = [bot_position, human_position, old_bot_position, old_human_position]
				choose_move = [move for move in corners if move not in unwanted_move]

				if choose_move:

					# 0  1  O
					# 3  X  5
					# X  O  8

					# For these conditions, here it must be placed either in 3 or 0
				
					if old_bot_position == 4 and old_human_position in edges:
						if not abs(bot_position - old_human_position) % 3:
							mapping = {0: [1, 2], 2: [0, 1], 6: [7, 8], 8: [6, 7]}
							return random.choice(mapping[bot_position])

						else:
							mapping = {0: [3, 6], 2: [5, 8], 6: [0, 3], 8: [2, 5]}
							return random.choice(mapping[bot_position])
					

					# X  1  2    O  1  2
					# O  4  5    3  4  5
					# X  O  8    X  O  X

					# For these conditions, the one only move the bot should make in is 2.

					elif abs(old_human_position - old_bot_position) == 1:
						return (8 - old_bot_position)

					elif not (abs(old_human_position - old_bot_position) % 3):
						return (8 - old_bot_position)

					else:
						return random.choice(choose_move)

				else:
					return random.choice(available_moves)



		elif initial_move == 5:

			is_winning = self.about_to_win(winning_string, available_moves, botsign)
			
			if is_winning:
				return (is_winning-1)

			else:

				# in most of the time, game must be over by or before this move. If not, then draw
				# just keep clam and continue playing :p
				
				return random.choice(available_moves)



		


		elif initial_move == 6:

			# in most cases the game should be finished by now, if not, then it'll surely be a draw

			is_winning = self.about_to_win(winning_string, available_moves, botsign)

			if is_winning:
				return (is_winning-1)
			else:
				return random.choice(available_moves)


		

		elif initial_move == 7:

			is_winning = self.about_to_win(winning_string, available_moves, botsign)
			
			if is_winning:
				return (is_winning-1)

			else:
				return random.choice(available_moves)
		



		elif initial_move == 8:

			is_winning = self.about_to_win(winning_string, available_moves, botsign)
			
			if is_winning:
				return (is_winning-1)
			
			else:
				return random.choice(available_moves)







	@game.command(name="tictactoe", aliases=['ttt'])
	async def tictactoe(self, ctx, player=None):
		'''Starts a tic-tac-toe game'''

		await ctx.message.channel.trigger_typing()

		if ctx.me.permissions_in(ctx.message.channel).manage_messages:
			# delete the message command
			await ctx.message.delete(delay=60.0)


		buttons = [
			'<:mys1:593695781194694669>',
			'<:mys2:593696851165839380>',
			'<:mys3:593696876587515914>',
			'<:mys4:593696927426805779>',
			'<:mys5:593696937061122058>',
			'<:mys6:593696945059659777>',
			'<:mys7:593696953569640460>',
			'<:mys8:593696962411495475>',
			'<:mys9:593696973782253598>',
			'<:tquit:611086600243249152>'
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

			if not player.bot:

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

				score = {ctx.author: 0, player: 0}


				def check_move_player1(reaction, user):
					return user == player1 and str(reaction.emoji) in buttons and (reaction.message.id == message.id)

				def check_move_player2(reaction, user):
					return user == player2 and str(reaction.emoji) in buttons and (reaction.message.id == message.id)

				def check_both_player(reaction, user):
					return (user == ctx.author or user == player) and str(reaction.emoji) == '<:treplay:593851739170668595>' and (reaction.message.id == message.id)


				tictactoe = board

				embed = discord.Embed(description=f"***```yaml\nIt's {player1.display_name}'s turn.```***", color=0x86BFF4)
				embed.set_author(name="Tic-Tac-Toe")
				embed.set_thumbnail(url="https://raw.githubusercontent.com/J16N/tsuby/master/tictactoe-thumbnail.png")
				embed.add_field(name="**How To Play**", value="`React to a number to mark on that particular field.`", inline=False)
				embed.add_field(name="**Scoreboard**", value=f"**`{player1.display_name}: {score[player1]}`**\n**`{player2.display_name}: {score[player2]}`**", inline=False)
				embed.add_field(name="**Game**", value=tictactoe, inline=False)
				embed.set_footer(text=f"Currently Playing | {player1.display_name} vs {player2.display_name}", icon_url="https://raw.githubusercontent.com/J16N/tsuby/master/assets/tsuby-footer.png")

				message = await ctx.send(embed=embed)
				
				for button in buttons:
					await message.add_reaction(button)

				initial_move = 0

				while True:

					if not initial_move % 2 and not initial_move == 9:

						try:
							reaction, user = await self.bot.wait_for('reaction_add', timeout=60.0, check=check_move_player1)
							
							if reaction.emoji.name == "tquit":
								score[player2] += 1
								await message.clear_reactions()
								await message.edit(content=f"***Oh no, {player1.display_name} left the game.*** <a:tcry:581729105230168068>\n**{player2.display_name}: {score[player2]}**\n**{player1.display_name}: {score[player1]}**", embed=None)



								break

						except asyncio.TimeoutError:
							score[player2] += 1
							await message.clear_reactions()
							await message.edit(content=f"***{player1.mention} missed the turn. What a noob!*** <a:tlol:611083720543174656>\n**{player2.display_name}: {score[player2]}**\n**{player1.display_name}: {score[player1]}**", embed=None)
							break

						
						tictactoe = re.sub("<:"+reaction.emoji.name[2:]+":\d+>", player_1[reaction.emoji.name], tictactoe)

						initial_move += 1

						embed = discord.Embed(description=f"***```yaml\nIt's {player2.display_name}'s turn.```***", color=0x86BFF4)
						embed.set_author(name="Tic-Tac-Toe")
						embed.set_thumbnail(url="https://raw.githubusercontent.com/J16N/tsuby/master/tictactoe-thumbnail.png")
						embed.add_field(name="**How To Play**", value="`React to a number to mark on that particular field.`\n", inline=False)
						embed.add_field(name="**Scoreboard**", value=f"**`{player1.display_name}: {score[player1]}`**\n**`{player2.display_name}: {score[player2]}`**", inline=False)
						embed.add_field(name="**Game**", value=tictactoe, inline=False)
						embed.set_footer(text=f"Currently Playing | {player1.display_name} vs {player2.display_name}", icon_url="https://raw.githubusercontent.com/J16N/tsuby/master/assets/tsuby-footer.png")

						await message.edit(embed=embed)

						await message.remove_reaction(reaction, user)
						await message.remove_reaction(reaction, ctx.me)


						winning_string = tictactoe.replace('\n', ' ').split()

						if self.check_win(winning_string):
							score[player1] += 1
							await message.clear_reactions()
							await message.edit(content=f"***Congratulation {player1.mention}!*** <a:ttada:572049858643623956>\n*In order to play again, react both of you.*", embed=None)
							
							await message.add_reaction('<:treplay:593851739170668595>')

							try:
								reaction, user = await self.bot.wait_for('reaction_add', timeout=15.0, check=check_both_player)
								reaction, user = await self.bot.wait_for('reaction_add', timeout=15.0, check=check_both_player)

								await message.clear_reactions()

							except:
								await message.clear_reactions()
								await message.edit(content=f"***Congratulation {player1.mention}!*** <a:ttada:572049858643623956>\n**{player1.display_name}: {score[player1]}**\n**{player2.display_name}: {score[player2]}**")
								break

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

							tictactoe = board

							embed = discord.Embed(description=f"***```yaml\nIt's {player1.display_name}'s turn.```***", color=0x86BFF4)
							embed.set_author(name="Tic-Tac-Toe")
							embed.set_thumbnail(url="https://raw.githubusercontent.com/J16N/tsuby/master/tictactoe-thumbnail.png")
							embed.add_field(name="**How To Play**", value="`React to a number to mark on that particular field.`", inline=False)
							embed.add_field(name="**Scoreboard**", value=f"**`{player1.display_name}: {score[player1]}`**\n**`{player2.display_name}: {score[player2]}`**", inline=False)
							embed.add_field(name="**Game**", value=tictactoe, inline=False)
							embed.set_footer(text=f"Currently Playing | {player1.display_name} vs {player2.display_name}", icon_url="https://raw.githubusercontent.com/J16N/tsuby/master/assets/tsuby-footer.png")

							await message.edit(content=None, embed=embed)
							
							for button in buttons:
								await message.add_reaction(button)

							initial_move = 0


					elif initial_move == 9:
						winning_string = tictactoe.replace('\n', ' ').split()

						await message.clear_reactions()

						if self.check_win(winning_string):
							score[player1] += 1
							await message.edit(content=f"***Congratulation {player1.mention}!*** <a:ttada:572049858643623956>\n*In order to play again, react both of you.*", embed=None)
						else:
							await message.edit(content=f"***It's a draw...*** <a:tcheers:574536125037805568>\n*In order to play again, react both of you.*", embed=None)
						
						await message.add_reaction('<:treplay:593851739170668595>')

						try:
							reaction, user = await self.bot.wait_for('reaction_add', timeout=15.0, check=check_both_player)
							reaction, user = await self.bot.wait_for('reaction_add', timeout=15.0, check=check_both_player)

							await message.clear_reactions()

						except:
							await message.clear_reactions()
							
							if score[player1] > score[player2]:
								await message.edit(content=f"***Congratulation {player1.mention}!*** <a:ttada:572049858643623956>\n**{player1.display_name}: {score[player1]}**\n**{player2.display_name}: {score[player2]}**", embed=None)
							elif score[player1] < score[player2]:
								await message.edit(content=f"***Congratulation {player2.mention}!*** <a:ttada:572049858643623956>\n**{player2.display_name}: {score[player2]}**\n**{player1.display_name}: {score[player1]}**", embed=None)
							else:
								await message.edit(content=f"***It's a draw...*** <a:tcheers:574536125037805568>\n**{player1.display_name}: {score[player1]}**\n**{player2.display_name}: {score[player2]}**")
							
							break

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

						tictactoe = board

						embed = discord.Embed(description=f"***```yaml\nIt's {player1.display_name}'s turn.```***", color=0x86BFF4)
						embed.set_author(name="Tic-Tac-Toe")
						embed.set_thumbnail(url="https://raw.githubusercontent.com/J16N/tsuby/master/tictactoe-thumbnail.png")
						embed.add_field(name="**How To Play**", value="`React to a number to mark on that particular field.`\n", inline=False)
						embed.add_field(name="**Scoreboard**", value=f"**`{player1.display_name}: {score[player1]}`**\n**`{player2.display_name}: {score[player2]}`**", inline=False)
						embed.add_field(name="**Game**", value=tictactoe, inline=False)
						embed.set_footer(text=f"Currently Playing | {player1.display_name} vs {player2.display_name}", icon_url="https://raw.githubusercontent.com/J16N/tsuby/master/assets/tsuby-footer.png")

						await message.edit(content=None, embed=embed)
						
						for button in buttons:
							await message.add_reaction(button)

						initial_move = 0


					else:
									
						try:
							reaction, user = await self.bot.wait_for('reaction_add', timeout=60.0, check=check_move_player2)
							
							if reaction.emoji.name == "tquit":
								score[player1] += 1
								await message.clear_reactions()
								await message.edit(content=f"***Oh no, {player2.display_name} left the game.*** <a:tcry:581729105230168068>\n**{player1.display_name}: {score[player1]}**\n**{player2.display_name}: {score[player2]}**", embed=None)
								break


						except asyncio.TimeoutError:
							score[player1] += 1
							await message.clear_reactions()
							await message.edit(content=f"***{player2.mention} missed the turn. What a noob!*** <a:tlol:611083720543174656>\n**{player1.display_name}: {score[player1]}**\n**{player2.display_name}: {score[player2]}**", embed=None)
							break

						
						tictactoe = re.sub("<:"+reaction.emoji.name[2:]+":\d+>", player_2[reaction.emoji.name], tictactoe)

						initial_move += 1

						embed = discord.Embed(description=f"***```yaml\nIt's {player1.display_name}'s turn.```***", color=0x86BFF4)
						embed.set_author(name="Tic-Tac-Toe")
						embed.set_thumbnail(url="https://raw.githubusercontent.com/J16N/tsuby/master/tictactoe-thumbnail.png")
						embed.add_field(name="**How To Play**", value="`React to a number to mark on that particular field.`", inline=False)
						embed.add_field(name="**Scoreboard**", value=f"**`{player1.display_name}: {score[player1]}`**\n**`{player2.display_name}: {score[player2]}`**", inline=False)
						embed.add_field(name="**Game**", value=tictactoe, inline=False)
						embed.set_footer(text=f"Currently Playing | {player1.display_name} vs {player2.display_name}", icon_url="https://raw.githubusercontent.com/J16N/tsuby/master/assets/tsuby-footer.png")

						await message.edit(embed=embed)

						await message.remove_reaction(reaction, user)
						await message.remove_reaction(reaction, ctx.me)


						winning_string = tictactoe.replace('\n', ' ').split()

						if self.check_win(winning_string):
							score[player2] += 1
							await message.clear_reactions()
							await message.edit(content=f"***Congratulation {player2.mention}!*** <a:ttada:572049858643623956>\n*In order to play again, react both of you.*", embed=None)
							
							await message.add_reaction('<:treplay:593851739170668595>')

							try:
								reaction, user = await self.bot.wait_for('reaction_add', timeout=15.0, check=check_both_player)
								reaction, user = await self.bot.wait_for('reaction_add', timeout=15.0, check=check_both_player)

								await message.clear_reactions()


							except:
								await message.clear_reactions()
								await message.edit(content=f"***Congratulation {player2.mention}!*** <a:ttada:572049858643623956>\n**{player2.display_name}: {score[player2]}**\n**{player1.display_name}: {score[player1]}**")
								break

							
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

							tictactoe = board

							embed = discord.Embed(description=f"***```yaml\nIt's {player1.display_name}'s turn.```***", color=0x86BFF4)
							embed.set_author(name="Tic-Tac-Toe")
							embed.set_thumbnail(url="https://raw.githubusercontent.com/J16N/tsuby/master/tictactoe-thumbnail.png")
							embed.add_field(name="**How To Play**", value="`React to a number to mark on that particular field.`", inline=False)
							embed.add_field(name="**Scoreboard**", value=f"**`{player1.display_name}: {score[player1]}`**\n**`{player2.display_name}: {score[player2]}`**", inline=False)
							embed.add_field(name="**Game**", value=tictactoe, inline=False)
							embed.set_footer(text=f"Currently Playing | {player1.display_name} vs {player2.display_name}", icon_url="https://raw.githubusercontent.com/J16N/tsuby/master/assets/tsuby-footer.png")

							await message.edit(content=None, embed=embed)
							
							for button in buttons:
								await message.add_reaction(button)

							initial_move = 0


			else:

				if player == ctx.me:
					await ctx.send("*If you want to play with me, no need to mention. I can understand you better...*", delete_after=3.0)

				else:
					await ctx.send("*Ehh....stop mentioning other bots. You need to mention a real user.*", delete_after=3.0)

				if ctx.me.permissions_in(ctx.message.channel).manage_messages:
					# delete the message command
					await ctx.message.delete(delay=3.0)



		else:
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

			score = {ctx.me: 0, ctx.author: 0}

			tictactoe = board
			winning_string = tictactoe.replace('\n', ' ').split()

			def check_move_human(reaction, user):
				return user == ctx.author and str(reaction.emoji) in buttons and (reaction.message.id == message.id)


			def check_player(reaction, user):
				return user == ctx.author and str(reaction.emoji) == '<:treplay:593851739170668595>' and (reaction.message.id == message.id)

			
			available_moves = [0, 1, 2, 3, 4, 5, 6, 7, 8]


			if player1 == ctx.me:
				bot_turn = 1
				embed = discord.Embed(description=f"***```yaml\nIt's my turn.```***", color=0x86BFF4)
					
			else:
				bot_turn = 0
				embed = discord.Embed(description=f"***```yaml\nIt's your turn.```***", color=0x86BFF4)
						
			embed.set_author(name="Tic-Tac-Toe")
			embed.set_thumbnail(url="https://raw.githubusercontent.com/J16N/tsuby/master/tictactoe-thumbnail.png")
			embed.add_field(name="**How To Play**", value="`React to a number to mark on that particular field.`\n", inline=False)
			embed.add_field(name="**Scoreboard**", value=f"**`{player1.display_name}: {score[player1]}`**\n**`{player2.display_name}: {score[player2]}`**", inline=False)
			embed.add_field(name="**Game**", value=tictactoe, inline=False)
			embed.set_footer(text=f"Currently Playing | {player1.display_name} vs {player2.display_name}", icon_url="https://raw.githubusercontent.com/J16N/tsuby/master/assets/tsuby-footer.png")

			
			message = await ctx.send(embed=embed)
			
			for button in buttons:
				await message.add_reaction(button)

			initial_move = 0
			bot_position = 0
			human_position = 0

			while True:

				if bot_turn and initial_move != 9:

					if player1 == ctx.me:

						if initial_move == 0:

							bot_position = self.do_move(initial_move)
							old_bot_position = bot_position

						elif initial_move == 2:

							bot_position = self.do_move(initial_move, bot_position, human_position)

						elif initial_move == 4:

							bot_position = self.do_move(initial_move, bot_position, human_position, \
								old_bot_position, old_human_position, winning_string, available_moves, player_1)

						elif initial_move == 6:

							bot_position = self.do_move(initial_move=initial_move, \
								winning_string=winning_string, available_moves=available_moves, botsign=player_1)

						elif initial_move == 8:

							bot_position = self.do_move(initial_move=initial_move, \
								winning_string=winning_string, available_moves=available_moves, botsign=player_1)



					else:

						if initial_move == 1:
							bot_position = self.do_move(initial_move=initial_move, human_position=human_position)

						elif initial_move == 3:
							bot_position = self.do_move(initial_move=initial_move, human_position=human_position, \
								bot_position=bot_position, old_human_position=old_human_position, \
								winning_string=winning_string, available_moves=available_moves, botsign=player_2)

						elif initial_move == 5:
							bot_position = self.do_move(initial_move=initial_move, winning_string=winning_string, \
								available_moves=available_moves, botsign=player_2)

						elif initial_move == 7:
							bot_position = self.do_move(initial_move=initial_move, winning_string=winning_string, \
								available_moves=available_moves, botsign=player_2)

					
					available_moves.remove(bot_position)
					initial_move += 1
					bot_turn = 0
						
					#get the reaction name to remove
					reaction_name = buttons[int(winning_string[bot_position][3]) - 1]
					emoji = await commands.EmojiConverter().convert(ctx, reaction_name)
					#make a move
					if player1 == ctx.me:
						winning_string[bot_position] = player_1[list(player_1.keys())[bot_position]]
					else:
						winning_string[bot_position] = player_2[list(player_2.keys())[bot_position]]

					tictactoe = ' '.join(winning_string[:3])+"\n"+' '.join(winning_string[3:6])+"\n"+' '.join(winning_string[6:])

					embed = discord.Embed(description=f"***```yaml\nIt's your turn.```***", color=0x86BFF4)
					embed.set_author(name="Tic-Tac-Toe")
					embed.set_thumbnail(url="https://raw.githubusercontent.com/J16N/tsuby/master/tictactoe-thumbnail.png")
					embed.add_field(name="**How To Play**", value="`React to a number to mark on that particular field.`\n", inline=False)
					embed.add_field(name="**Scoreboard**", value=f"**`{player1.display_name}: {score[player1]}`**\n**`{player2.display_name}: {score[player2]}`**", inline=False)
					embed.add_field(name="**Game**", value=tictactoe, inline=False)
					embed.set_footer(text=f"Currently Playing | {player1.name} vs {player2.name}", icon_url="https://raw.githubusercontent.com/J16N/tsuby/master/assets/tsuby-footer.png")

					await message.edit(embed=embed)

					await message.remove_reaction(emoji, ctx.me)

					if self.check_win(winning_string):
					
						score[ctx.me] += 1

						await message.clear_reactions()
						await message.edit(content=f"***Hurray ! I won.*** <a:ttada:572049858643623956>\n*React, in order to play again. Hurry...*", embed=None)
						
						await message.add_reaction('<:treplay:593851739170668595>')

						try:
							reaction, user = await self.bot.wait_for('reaction_add', timeout=15.0, check=check_player)
							await message.clear_reactions()

						except:
							await message.clear_reactions()
							await message.edit(content=f"***Hurray ! I won.*** <a:ttada:572049858643623956>\n**{ctx.me.display_name}: {score[ctx.me]}**\n**{ctx.author.display_name}: {score[ctx.author]}**")
							break


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

						available_moves = [0, 1, 2, 3, 4, 5, 6, 7, 8]

						if player1 == ctx.me:
							bot_turn = 1
							embed = discord.Embed(description=f"***```yaml\nIt's my turn.```***", color=0x86BFF4)
						
						else:
							bot_turn = 0
							embed = discord.Embed(description=f"***```yaml\nIt's your turn.```***", color=0x86BFF4)
							
						embed.set_author(name="Tic-Tac-Toe")
						embed.set_thumbnail(url="https://raw.githubusercontent.com/J16N/tsuby/master/tictactoe-thumbnail.png")
						embed.add_field(name="**How To Play**", value="`React to a number to mark on that particular field.`\n", inline=False)
						embed.add_field(name="**Scoreboard**", value=f"**`{player1.display_name}: {score[player1]}`**\n**`{player2.display_name}: {score[player2]}`**", inline=False)
						embed.add_field(name="**Game**", value=tictactoe, inline=False)
						embed.set_footer(text=f"Currently Playing | {player1.name} vs {player2.name}", icon_url="https://raw.githubusercontent.com/J16N/tsuby/master/assets/tsuby-footer.png")

						
						await message.edit(content=None, embed=embed)
						
						for button in buttons:
							await message.add_reaction(button)

						initial_move = 0
						bot_position = 0
						human_position = 0
						



				

				elif initial_move == 9:

					if self.check_win(winning_string):
						await message.clear_reactions()
						
						score[player1] += 1

						if player1 == ctx.me:
							await message.edit(content=f"***Hurray ! I won.***\n*React, in order to play again. Hurry...*", embed=None)
						else:
							await message.edit(content=f"***Congratulation {player1.mention}!*** \nYou won. <a:ttada:572049858643623956>\n*React, in order to play again. Hurry...*", embed=None)

					else:
						await message.clear_reactions()
						await message.edit(content=f"***It's a draw...*** <a:tcheers:574536125037805568>\n*React, in order to play again. Hurry...*", embed=None)


					await message.add_reaction('<:treplay:593851739170668595>')

					try:
						reaction, user = await self.bot.wait_for('reaction_add', timeout=15.0, check=check_player)
						await message.clear_reactions()

					except:
						await message.clear_reactions()
						
						if score[ctx.me] > score[ctx.author]:
							await message.edit(content=f"***Hurray ! I won.***\n**{ctx.me.display_name}: {score[ctx.me]}**\n**{ctx.author.display_name}: {score[ctx.author]}**", embed=None)

						elif score[ctx.me] < score[ctx.author]:
							await message.edit(content=f"***Congratulation {player1.mention}!*** <a:ttada:572049858643623956>\n**{ctx.author.display_name}: {score[ctx.author]}**\n**{ctx.me.display_name}: {score[ctx.me]}**", embed=None)

						else:
							await message.edit(content=f"***It's a draw...*** <a:tcheers:574536125037805568>\n**{ctx.author.display_name}: {score[ctx.author]}**\n**{ctx.me.display_name}: {score[ctx.me]}**")
						
						break


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

					available_moves = [0, 1, 2, 3, 4, 5, 6, 7, 8]

					if player1 == ctx.me:
						bot_turn = 1
						embed = discord.Embed(description=f"***```yaml\nIt's my turn.```***", color=0x86BFF4)
					
					else:
						bot_turn = 0
						embed = discord.Embed(description=f"***```yaml\nIt's your turn.```***", color=0x86BFF4)
						
					embed.set_author(name="Tic-Tac-Toe")
					embed.set_thumbnail(url="https://raw.githubusercontent.com/J16N/tsuby/master/tictactoe-thumbnail.png")
					embed.add_field(name="**How To Play**", value="`React to a number to mark on that particular field.`", inline=False)
					embed.add_field(name="**Scoreboard**", value=f"**`{player1.display_name}: {score[player1]}`**\n**`{player2.display_name}: {score[player2]}`**", inline=False)
					embed.add_field(name="**Game**", value=tictactoe, inline=False)
					embed.set_footer(text=f"Currently Playing | {player1.name} vs {player2.name}", icon_url="https://raw.githubusercontent.com/J16N/tsuby/master/assets/tsuby-footer.png")

					
					await message.edit(content=None, embed=embed)
					
					for button in buttons:
						await message.add_reaction(button)

					initial_move = 0
					bot_position = 0
					human_position = 0


		

				else:

					old_human_position = human_position

					try:
						reaction, user = await self.bot.wait_for('reaction_add', timeout=60.0, check=check_move_human)

						if reaction.emoji.name == "tquit":
							score[ctx.me] += 1
							await message.clear_reactions()
							await message.edit(content=f"***Why did you leave?*** <a:tcry:581729105230168068>\n**{ctx.me.display_name}: {score[ctx.me]}**\n**{ctx.author.display_name}: {score[ctx.author]}**", embed=None)
							break

					except asyncio.TimeoutError:
						score[ctx.me] += 1
						await message.clear_reactions()
						await message.edit(content=f"***{player2.mention} missed the turn. What a noob!*** <a:tlol:611083720543174656>\n**{ctx.me.display_name}: {score[ctx.me]}**\n**{ctx.author.display_name}: {score[ctx.author]}**", embed=None)
						break

					if player2 == ctx.author:
						tictactoe = re.sub("<:"+reaction.emoji.name[2:]+":\d+>", player_2[reaction.emoji.name], tictactoe)
					else:
						tictactoe = re.sub("<:"+reaction.emoji.name[2:]+":\d+>", player_1[reaction.emoji.name], tictactoe)

					# get the human's move
					human_position = int(reaction.emoji.name[3]) - 1

					available_moves.remove(human_position)

					initial_move += 1
					bot_turn = 1

					embed = discord.Embed(description=f"***```yaml\nIt's my turn.```***", color=0x86BFF4)
					embed.set_author(name="Tic-Tac-Toe")
					embed.set_thumbnail(url="https://raw.githubusercontent.com/J16N/tsuby/master/tictactoe-thumbnail.png")
					embed.add_field(name="**How To Play**", value="`React to a number to mark on that particular field.`\n", inline=False)
					embed.add_field(name="**Scoreboard**", value=f"**`{player1.display_name}: {score[player1]}`**\n**`{player2.display_name}: {score[player2]}`**", inline=False)
					embed.add_field(name="**Game**", value=tictactoe, inline=False)
					embed.set_footer(text=f"Currently Playing | {player1.name} vs {player2.name}", icon_url="https://raw.githubusercontent.com/J16N/tsuby/master/assets/tsuby-footer.png")

					await message.edit(embed=embed)

					await message.remove_reaction(reaction, user)
					await message.remove_reaction(reaction, ctx.me)


					winning_string = tictactoe.replace('\n', ' ').split()

					if self.check_win(winning_string):
					
						score[ctx.author] += 1
						
						await message.clear_reactions()
						
						await message.edit(content=f"***Congratulation {ctx.author.mention}!*** <a:ttada:572049858643623956>\n*React in order to play again. Hurry...*", embed=None)
						
						await message.add_reaction('<:treplay:593851739170668595>')

						try:
							reaction, user = await self.bot.wait_for('reaction_add', timeout=15.0, check=check_player)
							await message.clear_reactions()

						except:
							await message.clear_reactions()

							await message.edit(content=f"***Congratulation {ctx.author.mention}!***<a:ttada:572049858643623956>\n**{ctx.author.display_name}: {score[ctx.author]}\n**{ctx.me.display_name}: {score[ctx.me]}**")
							
							break


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

						available_moves = [0, 1, 2, 3, 4, 5, 6, 7, 8]

						if player1 == ctx.me:
							bot_turn = 1
							embed = discord.Embed(description=f"***```yaml\nIt's my turn.```***", color=0x86BFF4)
						
						else:
							bot_turn = 0
							embed = discord.Embed(description=f"***```yaml\nIt's your turn.```***", color=0x86BFF4)
							
						embed.set_author(name="Tic-Tac-Toe")
						embed.set_thumbnail(url="https://raw.githubusercontent.com/J16N/tsuby/master/tictactoe-thumbnail.png")
						embed.add_field(name="**How To Play**", value="`React to a number to mark on that particular field.`", inline=False)
						embed.add_field(name="**Scoreboard**", value=f"**`{player1.display_name}: {score[player1]}`**\n**`{player2.display_name}: {score[player2]}`**", inline=False)
						embed.add_field(name="**Game**", value=tictactoe, inline=False)
						embed.set_footer(text=f"Currently Playing | {player1.name} vs {player2.name}", icon_url="https://raw.githubusercontent.com/J16N/tsuby/master/assets/tsuby-footer.png")

						
						await message.edit(content=None, embed=embed)
						
						for button in buttons:
							await message.add_reaction(button)

						initial_move = 0
						bot_position = 0
						human_position = 0





def setup(bot):
	bot.add_cog(Games(bot))
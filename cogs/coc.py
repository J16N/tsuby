import discord
from discord.ext import commands
from discord.ext.commands.cooldowns import BucketType
import asyncio
import os
import requests
import json
import urllib
import re

class Coc(commands.Cog):
	
	def __init__(self, bot):

		self.bot = bot

		#coc api token
		self.coc_token = os.environ.get("COC")

		self.headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer {0}'.format(self.coc_token)}


	async def paginator(self, ctx, pages, **footer):
		'''Paginates the given embeds into pages'''
		
		buttons = ['<:myleft:584972740595810304>', '<:myright:584973342793138197>']

		def check(reaction, user):
			return user == ctx.message.author and str(reaction.emoji) in buttons and (reaction.message.id == message.id)

		total_pages = len(pages)

		current_page = 0

		embed = pages[current_page]
		if footer['text'] is None and footer['url'] is None:
			embed.set_footer(text=f"Page: {current_page+1}/{total_pages}")
		else:
			embed.set_footer(text=footer['text']+f" | Page: {current_page+1}/{total_pages}", icon_url=footer['url'])
		message = await ctx.send(embed=embed)

		for button in buttons:
			await message.add_reaction(button)

		while True:
			try:
				reaction, user = await self.bot.wait_for('reaction_add', timeout=30.0, check=check)

				if str(reaction.emoji) == '<:myright:584973342793138197>' and (current_page + 1) < total_pages:
					await message.remove_reaction(reaction, user)
					current_page += 1
					embed = pages[current_page]
					
					if footer['text'] is None and footer['url'] is None:
						embed.set_footer(text=f"Page: {current_page+1}/{total_pages}")
					else:
						embed.set_footer(text=footer['text']+f" | Page: {current_page+1}/{total_pages}", icon_url=footer['url'])
					
					await message.edit(embed=embed)

				elif str(reaction.emoji) == '<:myleft:584972740595810304>' and current_page > 0:
					await message.remove_reaction(reaction, user)
					current_page -= 1
					embed = pages[current_page]
					if footer['text'] is None and footer['url'] is None:
						embed.set_footer(text=f"Page: {current_page+1}/{total_pages}")
					else:
						embed.set_footer(text=footer['text']+f" Page: {current_page+1}/{total_pages}", icon_url=footer['url'])
					await message.edit(embed=embed)

				else:
					await message.remove_reaction(reaction, user)
			
			except asyncio.TimeoutError:
				await message.clear_reactions()
				break




	@commands.group(case_insensitive=True)
	@commands.cooldown(10,600,type=BucketType.member)
	async def coc(self, ctx):
		'''Our main coc command. Other commands are just sub commands of this'''
		if ctx.invoked_subcommand is None:
			await ctx.send('`t-coc help`')


	@coc.command()
	async def help(self, ctx):
		'''Help command for COC'''

		embed = discord.Embed(description="*I found the following list of commands*", color=0xB47211)
		
		embed.set_author(name="Help")
		embed.add_field(name="**t-coc clan <clan_tag>**", value="`└─ Fetches information about the given clan.`", inline=False)
		embed.add_field(name="**t-coc player <player_tag>**", value="`└─ Fetches information about the given player.`", inline=False)
		embed.set_footer(text="Type t-help to get the list of all commands", icon_url="https://raw.githubusercontent.com/J16N/tsuby/master/cogs/tsuby.png")

		if ctx.message.guild is not None:
			await ctx.message.add_reaction("📧")
			
		await ctx.author.send(embed=embed)

	

	@coc.command()
	async def player(self, ctx, tag):
		'''Fetches coc player info with the given tag.'''

		tag = tag.upper()

		await ctx.message.channel.trigger_typing()

		if re.fullmatch("\A#[A-Z 0-9]{8,}", tag):
			
			url = "https://api.clashofclans.com/v1/players/" + urllib.parse.quote_plus(tag)

			response = requests.get(url, headers=self.headers)

			if response.status_code == 200:

				# retrieving the data from json
				data = json.loads(response.content.decode('utf-8'))

				space = ' \u200B '*8
				gen_info = "**TAG:** *{0}* {1} **XP:** *{2}* \u200B ".format(data['tag'], space, data['expLevel'])

				#discord embeds no big deal
				embed_1 = discord.Embed(description=gen_info, color=0xB47211)

				if 'league' in data:
					embed_1.set_author(name=data['name'], icon_url=data['league']['iconUrls']['medium'])
				else:
					embed_1.set_author(name=data['name'], icon_url="https://vignette.wikia.nocookie.net/clashofclans/images/c/c0/Unranked_League.png/revision/latest/scale-to-width-down/92?cb=20171003011534")

				if 'clan' in data:
					clan_info = "***Tag:*** \u200B {}\n ***Name:*** \u200B {}\n ***Level:*** \u200B {}".format(\
						data['clan']['tag'], data['clan']['name'], str(data['clan']['clanLevel']))

					embed_1.set_footer(text='From {} {}'.format(data['clan']['name'], data['clan']['tag']), \
						icon_url=data['clan']['badgeUrls']['large'])

					embed_1.add_field(name="**Clan**", value=clan_info, inline=False)
					embed_1.add_field(name="\u200B", value='\u200B', inline=False)

				if 'trophies' in data:
					embed_1.add_field(name="**Trophies**", value = str(data['trophies']), inline=True)
				if 'versusTrophies' in data:
					embed_1.add_field(name="**Versus Trophies**", value = str(data['versusTrophies']), inline=True)
				if 'attackWins' in data:
					embed_1.add_field(name="**Attacks Won**", value = str(data['attackWins']), inline=True)
				if 'defenseWins' in data:
					embed_1.add_field(name="**Defense Won**", value = str(data['defenseWins']), inline=True)
				if 'bestTrophies' in data:
					embed_1.add_field(name="**Best Trophies**", value = str(data['bestTrophies']), inline=True)
				if 'donations' in data:
					embed_1.add_field(name="**Donations**", value = str(data['donations']), inline=True)
				if 'donationsReceived' in data:
					embed_1.add_field(name="**Donations Received**", value = str(data['donationsReceived']), inline=True)
				if 'warStars' in data:
					embed_1.add_field(name="**War Stars**", value = str(data['warStars']), inline=True)
				if 'role' in data:
					embed_1.add_field(name="**Role**", value = data['role'], inline=True)
				if 'townHallLevel' in data:
					embed_1.add_field(name="**TownHall Level**", value = str(data['townHallLevel']), inline=True)
				if 'builderHallLevel' in data:
					embed_1.add_field(name="**BuilderHall Level**", value = str(data['builderHallLevel']), inline=True)
				if 'bestVersusTrophies' in data:
					embed_1.add_field(name="**Best Versus Trophies**", value = str(data['bestVersusTrophies']), inline=True)
				if 'versusBattleWins' in data:
					embed_1.add_field(name="**Versus Battles Won**", value = str(data['versusBattleWins']), inline=True)


				if 'legendStatistics' in data:

					embed_1.add_field(name="\u200B", value='\u200B', inline=False)

					embed_1.add_field(name="**Legend Statistics**", value = str(data['legendStatistics']['legendTrophies']), inline=False)

					if 'rank'  in data['legendStatistics']['currentSeason']:
						cSeason = f"***Rank:*** \u200B {data['legendStatistics']['currentSeason']['rank']}\n"
					else:
						cSeason = ""

					if 'trophies' in data['legendStatistics']['currentSeason']:
						cSeason += f"***Trophies:*** \u200B {data['legendStatistics']['currentSeason']['trophies']}"
					else:
						cSeason = ""

					if cSeason:
						embed_1.add_field(name="**Current Season**", value=cSeason, inline=True)

					
					if 'rank'  in data['legendStatistics']['previousVersusSeason']:
						pSeason = f"***Rank:*** \u200B {data['legendStatistics']['previousVersusSeason']['rank']}\n"
					else:
						pSeason = ""

					if 'trophies' in data['legendStatistics']['previousVersusSeason']:
						pSeason += f"***Trophies:*** \u200B {data['legendStatistics']['previousVersusSeason']['trophies']}"
					else:
						pSeason = ""

					if pSeason:
						embed_1.add_field(name="**Previous Season**", value=pSeason, inline=True)


					if 'rank'  in data['legendStatistics']['bestVersusSeason']:
						bSeason = f"***Rank:*** \u200B {data['legendStatistics']['bestVersusSeason']['rank']}\n"
					else:
						bSeason = ""

					if 'trophies' in data['legendStatistics']['bestVersusSeason']:
						bSeason += f"***Trophies:*** \u200B {data['legendStatistics']['bestVersusSeason']['trophies']}"
					else:
						bSeason = ""

					if bSeason:
						embed_1.add_field(name="**Best Season**", value=bSeason, inline=True)



				if 'achievements' in data and len(data['achievements']) <= 25:
					embed_2 = discord.Embed(description=gen_info, color=0xB47211)

					if 'league' in data:
						embed_2.set_author(name=data['name']+' - Achievements', icon_url=data['league']['iconUrls']['medium'])
					else:
						embed_2.set_author(name=data['name']+' - Achievements', icon_url="https://vignette.wikia.nocookie.net/clashofclans/images/c/c0/Unranked_League.png/revision/latest/scale-to-width-down/92?cb=20171003011534")

					for achievement in data['achievements']:
						embed_2.add_field(name=f"**{achievement['name']}**", value=f"*{achievement['info']}*\n**Stars:** {str(achievement['stars'])}\n\u200B\n", inline=False)


					embed_3 = None



				if 'achievements' in data and len(data['achievements']) > 25:
					embed_2 = discord.Embed(description=gen_info, color=0xB47211)

					if 'league' in data:
						embed_2.set_author(name=data['name']+' - Achievements', icon_url=data['league']['iconUrls']['medium'])
					else:
						embed_2.set_author(name=data['name']+' - Achievements', icon_url="https://vignette.wikia.nocookie.net/clashofclans/images/c/c0/Unranked_League.png/revision/latest/scale-to-width-down/92?cb=20171003011534")

					for achievement in data['achievements'][:25]:
						embed_2.add_field(name=f"**{achievement['name']}**", value=f"*{achievement['info']}*\n**Stars:** {str(achievement['stars'])}\n\u200B\n", inline=False)


					embed_3 = discord.Embed(description=gen_info, color=0xB47211)

					if 'league' in data:
						embed_3.set_author(name=data['name']+' - Achievements', icon_url=data['league']['iconUrls']['medium'])
					else:
						embed_3.set_author(name=data['name']+' - Achievements', icon_url="https://vignette.wikia.nocookie.net/clashofclans/images/c/c0/Unranked_League.png/revision/latest/scale-to-width-down/92?cb=20171003011534")

					for achievement in data['achievements'][25:]:
						embed_3.add_field(name=f"**{achievement['name']}**", value=f"*{achievement['info']}*\n**Stars:** {str(achievement['stars'])}\n\u200B\n", inline=False)



				if 'troops' in data and len(data['troops']) <= 25:
					embed_4 = discord.Embed(description=gen_info, color=0xB47211)

					if 'league' in data:
						embed_4.set_author(name=data['name']+' - Troops', icon_url=data['league']['iconUrls']['medium'])
					else:
						embed_4.set_author(name=data['name']+' - Troops', icon_url="https://vignette.wikia.nocookie.net/clashofclans/images/c/c0/Unranked_League.png/revision/latest/scale-to-width-down/92?cb=20171003011534")

					for troop in data['troops']:
						embed_4.add_field(name=f"**{troop['name']}**", value=f"**Level:** {troop['level']}\n**Max Level:** {troop['maxLevel']}\n\u200B\n", inline=True)

					
					embed_5 = None


				if 'troops' in data and len(data['troops']) > 25:
					embed_4 = discord.Embed(description=gen_info, color=0xB47211)

					if 'league' in data:
						embed_4.set_author(name=data['name']+' - Troops', icon_url=data['league']['iconUrls']['medium'])
					else:
						embed_4.set_author(name=data['name']+' - Troops', icon_url="https://vignette.wikia.nocookie.net/clashofclans/images/c/c0/Unranked_League.png/revision/latest/scale-to-width-down/92?cb=20171003011534")

					for troop in data['troops'][:25]:
						embed_4.add_field(name=f"**{troop['name']}**", value=f"**Level:** {troop['level']}\n**Max Level:** {troop['maxLevel']}\n\u200B\n", inline=True)


					embed_5 = discord.Embed(description=gen_info, color=0xB47211)

					if 'league' in data:
						embed_5.set_author(name=data['name']+' - Troops', icon_url=data['league']['iconUrls']['medium'])
					else:
						embed_5.set_author(name=data['name']+' - Troops', icon_url="https://vignette.wikia.nocookie.net/clashofclans/images/c/c0/Unranked_League.png/revision/latest/scale-to-width-down/92?cb=20171003011534")

					for troop in data['troops'][25:]:
						embed_5.add_field(name=f"**{troop['name']}**", value=f"**Level:** {troop['level']}\n**Max Level:** {troop['maxLevel']}\n\u200B\n", inline=True)


				if 'heroes' in data:
					embed_6 = discord.Embed(description=gen_info, color=0xB47211)

					if 'league' in data:
						embed_6.set_author(name=data['name']+' - Heroes', icon_url=data['league']['iconUrls']['medium'])
					else:
						embed_6.set_author(name=data['name']+' - Heroes', icon_url="https://vignette.wikia.nocookie.net/clashofclans/images/c/c0/Unranked_League.png/revision/latest/scale-to-width-down/92?cb=20171003011534")

					for hero in data['heroes']:
						embed_6.add_field(name=f"**{hero['name']}**", value=f"**Level:** {hero['level']}\n**Max Level:** {hero['maxLevel']}\n\u200B\n", inline=True)

				else:
					embed_6 = None


				if 'spells' in data:
					embed_7 = discord.Embed(description=gen_info, color=0xB47211)

					if 'league' in data:
						embed_7.set_author(name=data['name']+' - Spells', icon_url=data['league']['iconUrls']['medium'])
					else:
						embed_7.set_author(name=data['name']+' - Spells', icon_url="https://vignette.wikia.nocookie.net/clashofclans/images/c/c0/Unranked_League.png/revision/latest/scale-to-width-down/92?cb=20171003011534")

					for spell in data['spells']:
						embed_7.add_field(name=f"**{spell['name']}**", value=f"**Level:** {spell['level']}\n**Max Level:** {spell['maxLevel']}\n\u200B\n", inline=True)

				else:
					embed_7 = None


				# we need to filter the embed list since we don't know which embed will not be None
				embed_list = [embed_1, embed_2, embed_3, embed_4, embed_5, embed_6, embed_7]
				filtered_embed_list = list(filter(None, embed_list))

				print(filtered_embed_list)
				
				if 'clan' in data:
					await self.paginator(ctx, filtered_embed_list, text=embed_1.footer.text, url=embed_1.footer.icon_url)
				else:
					await self.paginator(ctx, filtered_embed_list, text=None, url=None)




			else:
				# let's just handle the error and show the user what server respons
				await ctx.send("`The server responds`\n**ERROR {}:**\n*{}*".format(response.status_code, json.loads(response.content.decode('utf-8'))['reason']))

		else:

			await ctx.send("`t-coc player <valid_player_tag>`")


	@coc.command()
	async def clan(self, ctx, tag):
		'''Fetches the clan info with the given tag'''

		tag = tag.upper()

		await ctx.message.channel.trigger_typing()

		if re.fullmatch("\A#[A-Z 0-9]{8,}", tag):
			
			url = "https://api.clashofclans.com/v1/clans/" + urllib.parse.quote_plus(tag)

			response = requests.get(url, headers=self.headers)

			if response.status_code == 200:
				data = json.loads(response.content.decode('utf-8'))

				gen_info = "**TAG:** {}\n{}".format(data['tag'], data['description'])

				if 'description' in data:
					gen_info = "**TAG:** {}\n\n*{}*\n".format(data['tag'], data['description'])
					embed_1 = discord.Embed(description=gen_info, color=0xB47211)

				else:
					gen_info = "**TAG:** {}\n".format(data['tag'])
					embed_1 = discord.Embed(description=gen_info, color=0xB47211)
				
				embed_1.set_author(name=data['name'], icon_url=data['badgeUrls']['large'])

				if 'location' in data:
					embed_1.add_field(name="**Location**", value=data['location']['name'], inline=True)
				if 'clanLevel' in data:
					embed_1.add_field(name="**Clan Level**", value=str(data['clanLevel']), inline=True)
				if 'clanPoints' in data:
					embed_1.add_field(name="**Clan Points**", value=str(data['clanPoints']), inline=True)
				if 'clanVersusPoints' in data:
					embed_1.add_field(name="**Clan Versus Points**", value=str(data['clanVersusPoints']), inline=True)
				if 'members' in data:
					embed_1.add_field(name="**Members**", value=str(data['members']), inline=True)
				if 'type' in data:
					embed_1.add_field(name="**Type**", value=data['type'], inline=True)
				if 'requiredTrophies' in data:
					embed_1.add_field(name="**Required Trophies**", value=str(data['requiredTrophies']), inline=True)
				if 'warFrequency' in data:
					embed_1.add_field(name="**War Frequency**", value=data['warFrequency'], inline=True)
				if 'warWinStreak' in data:
					embed_1.add_field(name="**War Win Streak**", value=str(data['warWinStreak']), inline=True)
				if 'warWins' in data:
					embed_1.add_field(name="**Wars Won**", value=str(data['warWins']), inline=True)
				if 'warLosses' in data:
					embed_1.add_field(name="**Wars Lost**", value=str(data['warLosses']), inline=True)
				if 'warTies' in data:
					embed_1.add_field(name="**Wars Draw**", value=str(data['warTies']), inline=True)

				
				if 'memberList' in data and len(data['memberList']) <= 25:
					embed_2 = discord.Embed(description=gen_info, color=0xB47211)

					embed_2.set_author(name=data['name']+' - Members', icon_url=data['badgeUrls']['large'])

					for member in data['memberList']:
						embed_2.add_field(name=member['name'], value='`'+member['tag']+'`')

					embed_3 = None

				elif 'memberList' in data and len(data['memberList']) > 25:
					embed_2 = discord.Embed(description=gen_info, color=0xB47211)

					embed_2.set_author(name=data['name']+' - Members', icon_url=data['badgeUrls']['large'])

					for member in data['memberList'][:25]:
						embed_2.add_field(name=member['name'], value='`'+member['tag']+'`')


					embed_3 = discord.Embed(description=gen_info, color=0xB47211)

					embed_3.set_author(name=data['name']+' - Members', icon_url=data['badgeUrls']['large'])

					for member in data['memberList'][25:]:
						embed_3.add_field(name=member['name'], value='`'+member['tag']+'`')

				else:
					embed_2 = None
					embed_3 = None

				embed_list = [embed_1, embed_2, embed_3]
				filtered_embed_list = list(filter(None, embed_list))

				await self.paginator(ctx, filtered_embed_list, text=None, url=None)


			else:
				# let's just handle the error and show the user what server respons
				await ctx.send("`The server responds`\n**ERROR {}:**\n*{}*".format(response.status_code, json.loads(response.content.decode('utf-8'))['reason']))

		
		else:
			await ctx.send("`t-coc clan <valid_clan_tag>`")



def setup(bot):
	bot.add_cog(Coc(bot))
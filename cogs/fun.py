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
import requests
import urllib
from bs4 import BeautifulSoup
import random
import json

class Fun(commands.Cog):

	def __init__(self, bot):

		self.bot = bot

		self.headers = [
			{'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'},
			{'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'},
			{'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'},
			{'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36'},
			{'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'},
			
			{'User-Agent': 'Mozilla/5.0 (Windows NT 5.1; rv:7.0.1) Gecko/20100101 Firefox/7.0.1'},
			{'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0'},
			{'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1'},
			{'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:18.0) Gecko/20100101 Firefox/18.0'},
			{'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0'},
			
			{'User-Agent': 'Opera/9.80 (Windows NT 6.1; WOW64) Presto/2.12.388 Version/12.18'},
			{'User-Agent': 'Opera/9.80 (Windows NT 6.0) Presto/2.12.388 Version/12.14'}
		]

		self.jokes_category = [
			'animal jokes', 'dirty jokes', 'disabled jokes', 'general jokes',
			'pick up lines', 'political jokes', 'racist jokes', 'relationship jokes',
			'religious jokes', 'sports jokes', 'surreal jokes', 'yo mama jokes'
		]


		self.meme_category = {
			"India": "india",
			"USA": "usa",
			"Philippines": "philippines",
			"Italy": "italy",
			"Germany": "germany",
			"Pakistan": "pakistan",
			"Sri Lanka": "srilanka",
			"Hong Kong": "hongkong",
			"Japan": "japan",
			"Funny": "funny",
			"Animals": "cute",
			"Anime & Manga": "anime-manga",
			"Anime Waifu": "animefanart",
			"Anime Wallpaper": "animewallpaper",
			"Apex Legends": "apexlegends",
			"Ask 9GAG": "ask9gag",
			"Awesome": "awesome",
			"Basketball": "basketball",
			"Car": "car",
			"Comic": "comic",
			"Cosplay": "cosplay",
			"Countryballs": "country",
			"Crappy Design": "crappydesign",
			"Drawing & Crafts": "imadedis",
			"Endgame": "endgame",
			"Food": "food",
			"Football": "football",
			"Fortnite": "fortnite",
			"Game of Thrones": "got",
			"Gaming": "gaming",
			"GIF": "gif",
			"Girl": "girl",
			"Girl Celebrity": "goddess",
			"Guy": "guy",
			"Happy Poo": "happypoo",
			"History": "history",
			"Horror": "horror",
			"Home": "home",
			"K-Pop": "kpop",
			"League of Legends": "leagueoflegends",
			"LEGO": "lego",
			"Meme": "meme",
			"Movies & TV": "movie-tv",
			"Music": "music",
			"NSFW": "nsfw",
			"Rate My Outfit": "outfits",
			"Overwatch": "overwatch",
			"PC Master Race": "pcmr",
			"Pokemon": "pokemon",
			"Politics": "politics",
			"Relationship": "relationship",
			"PUBG": "pubg",
			"Savage": "savage",
			"Satisfying": "satisfying",
			"School": "school",
			"Science": "science",
			"Star Wars": "starwars",
			"Superhero": "superhero",
			"Sport": "sport",
			"Travel": "travel",
			"Timely": "timely",
			"Video": "video",
			"Warhammer": "warhammer",
			"Wallpaper": "wallpaper",
			"WTF": "wtf",
			"Dark Humor": "darkhumor"
		}

		self.meme_categories = {key.lower(): value for key, value in self.meme_category.items()}

		self.like = '<a:tthumbsup:594132184202346516>'
		self.dislike = '<a:tthumbsdown:594132184315461632>'

	

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







	@commands.group(case_insensitive=True, invoke_without_command=True)
	@commands.cooldown(10,600,type=BucketType.member)
	@commands.guild_only()
	async def jokes(self, ctx, *category):
		'''Our main jokes command. This posts random jokes'''
		
		await ctx.message.channel.trigger_typing()
		category = ' '.join(category).lower()

		if category not in self.jokes_category and category:
			temp = await ctx.send("`t-jokes help`")
			await temp.delete(delay=5.0)

			if ctx.me.permissions_in(ctx.message.channel).manage_messages:
				# delete the message command
				await ctx.message.delete(delay=5.0)
		
		else:

			if category in self.jokes_category:
				url = "http://www.funnyshortjokes.com/c/"+category.replace(' ', '-')
			else:
				url = "http://www.funnyshortjokes.com/"

			page = requests.get(url=url, headers=self.headers[random.randint(0, 11)])

			if page.status_code == 200:
				soup = BeautifulSoup(page.content, 'html.parser')
				lastpage = int(soup.select("div.navigation-pages span.item")[-1].get_text()) #getting the last page number

				if category in self.jokes_category:
					url = "http://www.funnyshortjokes.com/c/"+category.replace(' ', '-')+"/page/"+str(random.randint(1, lastpage))
				else:
					url = "http://www.funnyshortjokes.com/page/"+str(random.randint(1, lastpage))

				page = requests.get(url=url, headers=self.headers[random.randint(0, 11)])

				if page.status_code == 200:
					soup = BeautifulSoup(page.content, 'html.parser')

					#getting all the jokes from the random page
					joke_heading_list = soup.select("h3")
					joke_content_list = soup.select("div.post-text")
					likes = soup.select("span.thumbs-rating-up")
					dislikes = soup.select("span.thumbs-rating-down")
					
					total_jokes = len(joke_heading_list)
					initial_joke = 0

					ratings = f"\n\n{self.like} **{likes[initial_joke].get_text()}** \u200B \u200B \u200B \u200B \u200B {self.dislike} **{dislikes[initial_joke].get_text()}**"

					embed = discord.Embed(color=0xE18BAD)
					embed.add_field(name=joke_heading_list[initial_joke].get_text(), value=joke_content_list[initial_joke].get_text().strip() + ratings)
					embed.set_footer(text="From FunnyShortJokes.com", icon_url="http://www.funnyshortjokes.com/wp-content/uploads/2014/02/favicon-Copy1.ico")
					bot_post = await ctx.send(embed=embed)
					await bot_post.add_reaction('<:myright:584973342793138197>')

					def check(reaction, user):
						return user == ctx.message.author and str(reaction.emoji) == '<:myright:584973342793138197>' and (reaction.message.id == bot_post.id)

					while True:
						try:
							reaction, user = await self.bot.wait_for('reaction_add', timeout=60.0, check=check)
							
							initial_joke += 1

							if str(reaction.emoji) == '<:myright:584973342793138197>':
								await bot_post.clear_reactions()

								if initial_joke < total_jokes:
									
									ratings = f"\n\n{self.like} **{likes[initial_joke].get_text()}** \u200B \u200B \u200B \u200B \u200B {self.dislike} **{dislikes[initial_joke].get_text()}**"

									#preparing our next joke
									embed = discord.Embed(color=0xE18BAD)
									embed.add_field(name=joke_heading_list[initial_joke].get_text(), value=joke_content_list[initial_joke].get_text().strip() + ratings)
									embed.set_footer(text="From FunnyShortJokes.com", icon_url="http://www.funnyshortjokes.com/wp-content/uploads/2014/02/favicon-Copy1.ico")
									bot_post = await ctx.send(embed=embed)
									await bot_post.add_reaction('<:myright:584973342793138197>')

								else:
									if category in self.jokes_category:
										url = "http://www.funnyshortjokes.com/c/"+category.replace(' ', '-')+"/page/"+str(random.randint(1, lastpage))
									else:
										url = "http://www.funnyshortjokes.com/page/"+str(random.randint(1, lastpage))

									page = requests.get(url=url, headers=self.headers[random.randint(0, 11)])

									if page.status_code == 200:
										soup = BeautifulSoup(page.content, 'html.parser')

										#getting all the jokes from the random page
										joke_heading_list = soup.select("h3")
										joke_content_list = soup.select("div.post-text")
										likes = soup.select("span.thumbs-rating-up")
										dislikes = soup.select("span.thumbs-rating-down")

										total_jokes = len(joke_heading_list)
										initial_joke = 0

										ratings = f"\n\n{self.like} **{likes[initial_joke].get_text()}** \u200B \u200B \u200B \u200B \u200B {self.dislike} **{dislikes[initial_joke].get_text()}**"

										embed = discord.Embed(color=0xE18BAD)
										embed.add_field(name=joke_heading_list[initial_joke].get_text(), value=joke_content_list[initial_joke].get_text().strip() + ratings)
										embed.set_footer(text="From FunnyShortJokes.com", icon_url="http://www.funnyshortjokes.com/wp-content/uploads/2014/02/favicon-Copy1.ico")
										bot_post = await ctx.send(embed=embed)
										await bot_post.add_reaction('<:myright:584973342793138197>')

									else:
										await bot_post.clear_reactions()
										temp = await ctx.send(f"`The server responds`\n**ERROR {page.status_code}**")
										await temp.delete(delay=5.0)
										break


							else:
								await bot_post.remove_reaction(reaction, user)



						except asyncio.TimeoutError:
							await bot_post.clear_reactions()
							break
				

				else:
					temp = await ctx.send(f"`The server responds`\n**ERROR {page.status_code}**")
					await temp.delete(delay=5.0)

					if ctx.me.permissions_in(ctx.message.channel).manage_messages:
						# delete the message command
						await ctx.message.delete(delay=5.0)
			
			else:
				temp = await ctx.send(f"`The server responds`\n**ERROR {page.status_code}**")
				await temp.delete(delay=5.0)

				if ctx.me.permissions_in(ctx.message.channel).manage_messages:
					# delete the message command
					await ctx.message.delete(delay=5.0)


	




	@jokes.command(name="category")
	async def category_jokes(self, ctx):
		'''Lists Jokes category'''
		
		embed = discord.Embed(description='\n\u200b\n', color=0xE18BAD)
		embed.set_author(name="Jokes Categories")
		for category in self.jokes_category:
			embed.add_field(name=category.title(), value='\u200b')

		embed.set_footer(text="From FunnyShortJokes.com", icon_url="http://www.funnyshortjokes.com/wp-content/uploads/2014/02/favicon-Copy1.ico")

		await ctx.send(embed=embed)







	@commands.group(case_insensitive=True, invoke_without_command=True, name="9gag")
	@commands.guild_only()
	@commands.cooldown(10,600,type=BucketType.member)
	async def ninegag(self, ctx, *category):
		'''Posts random meme'''

		await ctx.message.channel.trigger_typing()

		category = ' '.join(category).lower()

		if category not in list(self.meme_categories.keys()) and category:
			temp = await ctx.send("`t-9gag sections`")
			await temp.delete(delay=5.0)

			if ctx.me.permissions_in(ctx.message.channel).manage_messages:
				# delete the message command
				await ctx.message.delete(delay=5.0)

		else:

			if category in list(self.meme_categories.keys()):
				url = "https://9gag.com/v1/group-posts/group/"+self.meme_categories[category]+"/type/hot?"
			else:
				url = "https://9gag.com/v1/group-posts/group/default/type/hot?"

			response = requests.get(url=url, headers=self.headers[random.randint(0, 11)])

			if response.status_code == 200:
				resource = json.loads(response.content.decode('utf-8'))

				posts = resource['data']['posts']
				total_posts = len(posts)
				initial_post = 0

				# preparing our first post
				upvote = posts[initial_post]['upVoteCount']
				downvote = posts[initial_post]['downVoteCount']
				ratings = f"\n{self.like} **+{upvote}** \u200B \u200B \u200B \u200B \u200B {self.dislike} **-{downvote}**\n"

				if posts[initial_post]["type"] == "Animated":
					post = "**" + posts[initial_post]["title"] + "**" + ratings + posts[initial_post]["images"]["image460sv"]["url"]
					bot_post = await ctx.send(post)
					await bot_post.add_reaction('<:myright:584973342793138197>')

				else:
					embed = discord.Embed(description=ratings, color=0xE18BAD)
					embed.set_author(name=posts[initial_post]["title"])
					embed.set_image(url=posts[initial_post]["images"]["image700"]["url"])
					embed.set_footer(text="From 9GAG.com", icon_url="https://assets-9gag-fun.9cache.com/s/fab0aa49/07824eb881f5709a9e226d08f5b6c6201a21d414/static/dist/core/img/favicon.ico")

					bot_post = await ctx.send(embed=embed)
					await bot_post.add_reaction('<:myright:584973342793138197>')


				def check(reaction, user):
					return user == ctx.message.author and str(reaction.emoji) == '<:myright:584973342793138197>' and (reaction.message.id == bot_post.id)


				while True:
					try:
						reaction, user = await self.bot.wait_for('reaction_add', timeout=300.0, check=check)
						
						initial_post += 1

						if str(reaction.emoji) == '<:myright:584973342793138197>':
							await bot_post.clear_reactions()

							if initial_post < total_posts:
								# preparing our next post
								upvote = posts[initial_post]['upVoteCount']
								downvote = posts[initial_post]['downVoteCount']
								ratings = f"\n{self.like} **+{upvote}** \u200B \u200B \u200B \u200B \u200B {self.dislike} **-{downvote}**\n"

								if posts[initial_post]["type"] == "Animated":
									post = "**" + posts[initial_post]["title"] + "**" + ratings + posts[initial_post]["images"]["image460sv"]["url"]
									bot_post = await ctx.send(post)
									await bot_post.add_reaction('<:myright:584973342793138197>')

								else:
									embed = discord.Embed(description=ratings, color=0xE18BAD)
									embed.set_author(name=posts[initial_post]["title"])
									embed.set_image(url=posts[initial_post]["images"]["image700"]["url"])
									embed.set_footer(text="From 9GAG.com", icon_url="https://assets-9gag-fun.9cache.com/s/fab0aa49/07824eb881f5709a9e226d08f5b6c6201a21d414/static/dist/core/img/favicon.ico")

									bot_post = await ctx.send(embed=embed)
									await bot_post.add_reaction('<:myright:584973342793138197>')

							else:

								url = url.split("?")[0] + "?" + resource['data']["nextCursor"]

								response = requests.get(url=url, headers=self.headers[random.randint(0, 11)])

								if response.status_code == 200:
									resource = json.loads(response.content.decode('utf-8'))

									posts = resource['data']['posts']
									total_posts = len(posts)
									initial_post = 0

									# preparing our more post
									upvote = posts[initial_post]['upVoteCount']
									downvote = posts[initial_post]['downVoteCount']
									ratings = f"\n{self.like} **+{upvote}** \u200B \u200B \u200B \u200B \u200B {self.dislike} **-{downvote}**\n"

									if posts[initial_post]["type"] == "Animated":
										post = "**" + posts[initial_post]["title"] + "**" + ratings + posts[initial_post]["images"]["image460sv"]["url"]
										bot_post = await ctx.send(post)
										await bot_post.add_reaction('<:myright:584973342793138197>')

									else:
										embed = discord.Embed(description=ratings, color=0xE18BAD)
										embed.set_author(name=posts[initial_post]["title"])
										embed.set_image(url=posts[initial_post]["images"]["image700"]["url"])
										embed.set_footer(text="From 9GAG.com", icon_url="https://assets-9gag-fun.9cache.com/s/fab0aa49/07824eb881f5709a9e226d08f5b6c6201a21d414/static/dist/core/img/favicon.ico")

										bot_post = await ctx.send(embed=embed)
										await bot_post.add_reaction('<:myright:584973342793138197>')

								else:
									await bot_post.clear_reactions()
									temp = await ctx.send(f"`The server responds`\n**ERROR {response.status_code}**")
									await temp.delete(delay=5.0)
									break

						else:
							await bot_post.remove_reaction(reaction, user)



					except asyncio.TimeoutError:
						await bot_post.clear_reactions()
						break


			else:
				temp = await ctx.send(f"`The server responds`\n**ERROR {response.status_code}**")
				await temp.delete(delay=5.0)

				if ctx.me.permissions_in(ctx.message.channel).manage_messages:
					# delete the message command
					await ctx.message.delete(delay=5.0)


	



	@ninegag.command()
	async def trending(self, ctx, *category):
		'''Fetches trends from 9GAG.com'''

		await ctx.message.channel.trigger_typing()

		category = ' '.join(category).lower()

		if category not in list(self.meme_categories.keys()) and category:
			temp = await ctx.send("`t-9gag sections`")
			await temp.delete(delay=5.0)

			if ctx.me.permissions_in(ctx.message.channel).manage_messages:
				# delete the message command
				await ctx.message.delete(delay=5.0)

		else:

			if category in list(self.meme_categories.keys()):
				url = "https://9gag.com/v1/group-posts/group/"+self.meme_categories[category]+"/type/trending?"
			else:
				url = "https://9gag.com/v1/group-posts/group/default/type/trending?"

			response = requests.get(url=url, headers=self.headers[random.randint(0, 11)])

			if response.status_code == 200:
				resource = json.loads(response.content.decode('utf-8'))

				posts = resource['data']['posts']
				total_posts = len(posts)
				initial_post = 0

				# preparing our first post
				upvote = posts[initial_post]['upVoteCount']
				downvote = posts[initial_post]['downVoteCount']
				ratings = f"\n{self.like} **+{upvote}** \u200B \u200B \u200B \u200B \u200B {self.dislike} **-{downvote}**\n"

				if posts[initial_post]["type"] == "Animated":
					post = "**" + posts[initial_post]["title"] + "**" + ratings + posts[initial_post]["images"]["image460sv"]["url"]
					bot_post = await ctx.send(post)
					await bot_post.add_reaction('<:myright:584973342793138197>')

				else:
					embed = discord.Embed(description=ratings, color=0xE18BAD)
					embed.set_author(name=posts[initial_post]["title"])
					embed.set_image(url=posts[initial_post]["images"]["image700"]["url"])
					embed.set_footer(text="From 9GAG.com", icon_url="https://assets-9gag-fun.9cache.com/s/fab0aa49/07824eb881f5709a9e226d08f5b6c6201a21d414/static/dist/core/img/favicon.ico")

					bot_post = await ctx.send(embed=embed)
					await bot_post.add_reaction('<:myright:584973342793138197>')


				def check(reaction, user):
					return user == ctx.message.author and str(reaction.emoji) == '<:myright:584973342793138197>' and (reaction.message.id == bot_post.id)


				while True:
					try:
						reaction, user = await self.bot.wait_for('reaction_add', timeout=300.0, check=check)
						
						initial_post += 1

						if str(reaction.emoji) == '<:myright:584973342793138197>':
							await bot_post.clear_reactions()

							if initial_post < total_posts:
								# preparing our next post
								upvote = posts[initial_post]['upVoteCount']
								downvote = posts[initial_post]['downVoteCount']
								ratings = f"\n{self.like} **+{upvote}** \u200B \u200B \u200B \u200B \u200B {self.dislike} **-{downvote}**\n"

								if posts[initial_post]["type"] == "Animated":
									post = "**" + posts[initial_post]["title"] + "**" + ratings + posts[initial_post]["images"]["image460sv"]["url"]
									bot_post = await ctx.send(post)
									await bot_post.add_reaction('<:myright:584973342793138197>')

								else:
									embed = discord.Embed(description=ratings, color=0xE18BAD)
									embed.set_author(name=posts[initial_post]["title"])
									embed.set_image(url=posts[initial_post]["images"]["image700"]["url"])
									embed.set_footer(text="From 9GAG.com", icon_url="https://assets-9gag-fun.9cache.com/s/fab0aa49/07824eb881f5709a9e226d08f5b6c6201a21d414/static/dist/core/img/favicon.ico")

									bot_post = await ctx.send(embed=embed)
									await bot_post.add_reaction('<:myright:584973342793138197>')

							else:

								url = url.split("?")[0] + "?" + resource['data']["nextCursor"]

								response = requests.get(url=url, headers=self.headers[random.randint(0, 11)])

								if response.status_code == 200:
									resource = json.loads(response.content.decode('utf-8'))

									posts = resource['data']['posts']
									total_posts = len(posts)
									initial_post = 0

									# preparing our more post
									upvote = posts[initial_post]['upVoteCount']
									downvote = posts[initial_post]['downVoteCount']
									ratings = f"\n{self.like} **+{upvote}** \u200B \u200B \u200B \u200B \u200B {self.dislike} **-{downvote}**\n"

									if posts[initial_post]["type"] == "Animated":
										post = "**" + posts[initial_post]["title"] + "**" + ratings + posts[initial_post]["images"]["image460sv"]["url"]
										bot_post = await ctx.send(post)
										await bot_post.add_reaction('<:myright:584973342793138197>')

									else:
										embed = discord.Embed(description=ratings, color=0xE18BAD)
										embed.set_author(name=posts[initial_post]["title"])
										embed.set_image(url=posts[initial_post]["images"]["image700"]["url"])
										embed.set_footer(text="From 9GAG.com", icon_url="https://assets-9gag-fun.9cache.com/s/fab0aa49/07824eb881f5709a9e226d08f5b6c6201a21d414/static/dist/core/img/favicon.ico")

										bot_post = await ctx.send(embed=embed)
										await bot_post.add_reaction('<:myright:584973342793138197>')

								else:
									await bot_post.clear_reactions()
									temp = await ctx.send(f"`The server responds`\n**ERROR {response.status_code}**")
									await temp.delete(delay=5.0)
									break

						else:
							await bot_post.remove_reaction(reaction, user)



					except asyncio.TimeoutError:
						await bot_post.clear_reactions()
						break


			else:
				temp = await ctx.send(f"`The server responds`\n**ERROR {response.status_code}**")
				await temp.delete(delay=5.0)

				if ctx.me.permissions_in(ctx.message.channel).manage_messages:
					# delete the message command
					await ctx.message.delete(delay=5.0)



	



	@ninegag.command()
	async def fresh(self, ctx, *category):
		'''Fetches fresh from 9GAG.com'''

		await ctx.message.channel.trigger_typing()
		
		category = ' '.join(category).lower()

		if category not in list(self.meme_categories.keys()) and category:
			temp = await ctx.send("`t-9gag sections`")
			await temp.delete(delay=5.0)

			if ctx.me.permissions_in(ctx.message.channel).manage_messages:
				# delete the message command
				await ctx.message.delete(delay=5.0)

		else:

			if category in list(self.meme_categories.keys()):
				url = "https://9gag.com/v1/group-posts/group/"+self.meme_categories[category]+"/type/fresh?"
			else:
				url = "https://9gag.com/v1/group-posts/group/default/type/fresh?"

			response = requests.get(url=url, headers=self.headers[random.randint(0, 11)])

			if response.status_code == 200:
				resource = json.loads(response.content.decode('utf-8'))

				posts = resource['data']['posts']
				total_posts = len(posts)
				initial_post = 0

				# preparing our first post
				upvote = posts[initial_post]['upVoteCount']
				downvote = posts[initial_post]['downVoteCount']
				ratings = f"\n{self.like} **+{upvote}** \u200B \u200B \u200B \u200B \u200B {self.dislike} **-{downvote}**\n"

				if posts[initial_post]["type"] == "Animated":
					post = "**" + posts[initial_post]["title"] + "**" + ratings + posts[initial_post]["images"]["image460sv"]["url"]
					bot_post = await ctx.send(post)
					await bot_post.add_reaction('<:myright:584973342793138197>')

				else:
					embed = discord.Embed(description=ratings, color=0xE18BAD)
					embed.set_author(name=posts[initial_post]["title"])
					embed.set_image(url=posts[initial_post]["images"]["image700"]["url"])
					embed.set_footer(text="From 9GAG.com", icon_url="https://assets-9gag-fun.9cache.com/s/fab0aa49/07824eb881f5709a9e226d08f5b6c6201a21d414/static/dist/core/img/favicon.ico")

					bot_post = await ctx.send(embed=embed)
					await bot_post.add_reaction('<:myright:584973342793138197>')


				def check(reaction, user):
					return user == ctx.message.author and str(reaction.emoji) == '<:myright:584973342793138197>' and (reaction.message.id == bot_post.id)


				while True:
					try:
						reaction, user = await self.bot.wait_for('reaction_add', timeout=300.0, check=check)
						
						initial_post += 1

						if str(reaction.emoji) == '<:myright:584973342793138197>':
							await bot_post.clear_reactions()

							if initial_post < total_posts:
								# preparing our next post
								upvote = posts[initial_post]['upVoteCount']
								downvote = posts[initial_post]['downVoteCount']
								ratings = f"\n{self.like} **+{upvote}** \u200B \u200B \u200B \u200B \u200B {self.dislike} **-{downvote}**\n"

								if posts[initial_post]["type"] == "Animated":
									post = "**" + posts[initial_post]["title"] + "**" + ratings + posts[initial_post]["images"]["image460sv"]["url"]
									bot_post = await ctx.send(post)
									await bot_post.add_reaction('<:myright:584973342793138197>')

								else:
									embed = discord.Embed(description=ratings, color=0xE18BAD)
									embed.set_author(name=posts[initial_post]["title"])
									embed.set_image(url=posts[initial_post]["images"]["image700"]["url"])
									embed.set_footer(text="From 9GAG.com", icon_url="https://assets-9gag-fun.9cache.com/s/fab0aa49/07824eb881f5709a9e226d08f5b6c6201a21d414/static/dist/core/img/favicon.ico")

									bot_post = await ctx.send(embed=embed)
									await bot_post.add_reaction('<:myright:584973342793138197>')

							else:

								url = url.split("?")[0] + "?" + resource['data']["nextCursor"]

								response = requests.get(url=url, headers=self.headers[random.randint(0, 11)])

								if response.status_code == 200:
									resource = json.loads(response.content.decode('utf-8'))

									posts = resource['data']['posts']
									total_posts = len(posts)
									initial_post = 0

									# preparing our more post
									upvote = posts[initial_post]['upVoteCount']
									downvote = posts[initial_post]['downVoteCount']
									ratings = f"\n{self.like} **+{upvote}** \u200B \u200B \u200B \u200B \u200B {self.dislike} **-{downvote}**\n"

									if posts[initial_post]["type"] == "Animated":
										post = "**" + posts[initial_post]["title"] + "**" + ratings + posts[initial_post]["images"]["image460sv"]["url"]
										bot_post = await ctx.send(post)
										await bot_post.add_reaction('<:myright:584973342793138197>')

									else:
										embed = discord.Embed(description=ratings, color=0xE18BAD)
										embed.set_author(name=posts[initial_post]["title"])
										embed.set_image(url=posts[initial_post]["images"]["image700"]["url"])
										embed.set_footer(text="From 9GAG.com", icon_url="https://assets-9gag-fun.9cache.com/s/fab0aa49/07824eb881f5709a9e226d08f5b6c6201a21d414/static/dist/core/img/favicon.ico")

										bot_post = await ctx.send(embed=embed)
										await bot_post.add_reaction('<:myright:584973342793138197>')

								else:
									await bot_post.clear_reactions()
									temp = await ctx.send(f"`The server responds`\n**ERROR {response.status_code}**")
									await temp.delete(delay=5.0)
									break

						else:
							await bot_post.remove_reaction(reaction, user)



					except asyncio.TimeoutError:
						await bot_post.clear_reactions()
						break


			else:
				temp = await ctx.send(f"`The server responds`\n**ERROR {response.status_code}**")
				await temp.delete(delay=5.0)

				if ctx.me.permissions_in(ctx.message.channel).manage_messages:
					# delete the message command
					await ctx.message.delete(delay=5.0)




	@ninegag.command()
	async def search(self, ctx, query=None):
		'''Fetches trends from 9GAG.com'''

		await ctx.message.channel.trigger_typing()

		if query is None:
			temp = await ctx.send("*You need to tell me a query.*\n`t-9gag search <query>`")
			await temp.delete(delay=5.0)

			if ctx.me.permissions_in(ctx.message.channel).manage_messages:
				# delete the message command
				await ctx.message.delete(delay=5.0)

		else:

			url = "https://9gag.com/v1/search-posts?query=" + query

			response = requests.get(url=url, headers=self.headers[random.randint(0, 11)])

			if response.status_code == 200:
				resource = json.loads(response.content.decode('utf-8'))

				posts = resource['data']['posts']
				total_posts = len(posts)
				initial_post = 0

				# preparing our first post
				upvote = posts[initial_post]['upVoteCount']
				downvote = posts[initial_post]['downVoteCount']
				ratings = f"\n{self.like} **+{upvote}** \u200B \u200B \u200B \u200B \u200B {self.dislike} **-{downvote}**\n"

				if posts[initial_post]["type"] == "Animated":
					post = "**" + posts[initial_post]["title"] + "**" + ratings + posts[initial_post]["images"]["image460sv"]["url"]
					bot_post = await ctx.send(post)
					await bot_post.add_reaction('<:myright:584973342793138197>')

				else:
					embed = discord.Embed(description=ratings, color=0xE18BAD)
					embed.set_author(name=posts[initial_post]["title"])
					embed.set_image(url=posts[initial_post]["images"]["image700"]["url"])
					embed.set_footer(text="From 9GAG.com", icon_url="https://assets-9gag-fun.9cache.com/s/fab0aa49/07824eb881f5709a9e226d08f5b6c6201a21d414/static/dist/core/img/favicon.ico")

					bot_post = await ctx.send(embed=embed)
					await bot_post.add_reaction('<:myright:584973342793138197>')


				def check(reaction, user):
					return user == ctx.message.author and str(reaction.emoji) == '<:myright:584973342793138197>' and (reaction.message.id == bot_post.id)


				while True:
					try:
						reaction, user = await self.bot.wait_for('reaction_add', timeout=300.0, check=check)
						
						initial_post += 1

						if str(reaction.emoji) == '<:myright:584973342793138197>':
							await bot_post.clear_reactions()

							if initial_post < total_posts:
								# preparing our next post
								upvote = posts[initial_post]['upVoteCount']
								downvote = posts[initial_post]['downVoteCount']
								ratings = f"\n{self.like} **+{upvote}** \u200B \u200B \u200B \u200B \u200B {self.dislike} **-{downvote}**\n"

								if posts[initial_post]["type"] == "Animated":
									post = "**" + posts[initial_post]["title"] + "**" + ratings + posts[initial_post]["images"]["image460sv"]["url"]
									bot_post = await ctx.send(post)
									await bot_post.add_reaction('<:myright:584973342793138197>')

								else:
									embed = discord.Embed(description=ratings, color=0xE18BAD)
									embed.set_author(name=posts[initial_post]["title"])
									embed.set_image(url=posts[initial_post]["images"]["image700"]["url"])
									embed.set_footer(text="From 9GAG.com", icon_url="https://assets-9gag-fun.9cache.com/s/fab0aa49/07824eb881f5709a9e226d08f5b6c6201a21d414/static/dist/core/img/favicon.ico")

									bot_post = await ctx.send(embed=embed)
									await bot_post.add_reaction('<:myright:584973342793138197>')

							else:

								url = url.split("?")[0] + "?query=" + resource['data']["nextCursor"]

								response = requests.get(url=url, headers=self.headers[random.randint(0, 11)])

								if response.status_code == 200:
									resource = json.loads(response.content.decode('utf-8'))

									posts = resource['data']['posts']
									total_posts = len(posts)
									initial_post = 0

									# preparing our more post
									upvote = posts[initial_post]['upVoteCount']
									downvote = posts[initial_post]['downVoteCount']
									ratings = f"\n{self.like} **+{upvote}** \u200B \u200B \u200B \u200B \u200B {self.dislike} **-{downvote}**\n"

									if posts[initial_post]["type"] == "Animated":
										post = "**" + posts[initial_post]["title"] + "**" + ratings + posts[initial_post]["images"]["image460sv"]["url"]
										bot_post = await ctx.send(post)
										await bot_post.add_reaction('<:myright:584973342793138197>')

									else:
										embed = discord.Embed(description=ratings, color=0xE18BAD)
										embed.set_author(name=posts[initial_post]["title"])
										embed.set_image(url=posts[initial_post]["images"]["image700"]["url"])
										embed.set_footer(text="From 9GAG.com", icon_url="https://assets-9gag-fun.9cache.com/s/fab0aa49/07824eb881f5709a9e226d08f5b6c6201a21d414/static/dist/core/img/favicon.ico")

										bot_post = await ctx.send(embed=embed)
										await bot_post.add_reaction('<:myright:584973342793138197>')

								else:
									await bot_post.clear_reactions()
									temp = await ctx.send(f"`The server responds`\n**ERROR {response.status_code}**")
									await temp.delete(delay=5.0)
									break

						else:
							await bot_post.remove_reaction(reaction, user)



					except asyncio.TimeoutError:
						await bot_post.clear_reactions()
						break


			else:
				temp = await ctx.send(f"`The server responds`\n**ERROR {response.status_code}**")
				await temp.delete(delay=5.0)

				if ctx.me.permissions_in(ctx.message.channel).manage_messages:
					# delete the message command
					await ctx.message.delete(delay=5.0)




	




	@ninegag.command(name="sections")
	async def category_meme(self, ctx):
		'''Lists Meme Category'''

		'''
		   Okay so in this one since discord supports only 25 fields per embeds
		   we need 3 embeds to lists all out categories
		'''
		
		await ctx.message.channel.trigger_typing()

		embed_1 = discord.Embed(description='\n\u200b\n', color=0xE18BAD)
		embed_1.set_author(name="Sections")
		for category in list(self.meme_category.keys())[:25]:
			embed_1.add_field(name=category, value='\u200b')

		embed_2 = discord.Embed(description='\n\u200b\n', color=0xE18BAD)
		embed_2.set_author(name="Sections")
		for category in list(self.meme_category.keys())[25:50]:
			embed_2.add_field(name=category, value='\u200b')

		embed_3 = discord.Embed(description='\n\u200b\n', color=0xE18BAD)
		embed_3.set_author(name="Sections")
		for category in list(self.meme_category.keys())[50:]:
			embed_3.add_field(name=category, value='\u200b')

		embed_list = [embed_1, embed_2, embed_3]

		await self.paginator(ctx, embed_list, text="From 9GAG.com", url="https://assets-9gag-fun.9cache.com/s/fab0aa49/07824eb881f5709a9e226d08f5b6c6201a21d414/static/dist/core/img/favicon.ico")






	@jokes.command(name="help")
	async def joke_help(self, ctx):
		'''Sends the help command'''

		embed = discord.Embed(description="*I found the following list of commands.*", color=0xE18BAD)
		
		embed.set_author(name="Help")
		embed.add_field(name="**t-jokes <category> (optional)**", value="`└─ Get some random jokes.`", inline=False)
		embed.add_field(name="**t-jokes category**", value="`└─ Get the list of jokes categories.`", inline=False)
		embed.set_footer(text="Type t-help to get the list of all commands", icon_url="https://raw.githubusercontent.com/J16N/tsuby/master/cogs/tsuby.png")

		if ctx.message.guild is not None:
			await ctx.message.add_reaction("📧")

		await ctx.author.send(embed=embed)



	@ninegag.command(name="help")
	async def ninegag_help(self, ctx):
		'''Sends the help command'''

		embed = discord.Embed(description="*I found the following list of commands.*", color=0xE18BAD)
		
		embed.set_author(name="Help")
		embed.add_field(name="**t-9gag <popular> (optional) <sections> (optional)**", value="`└─ Get some random posts from 9gag.com.`", inline=False)
		embed.add_field(name="**t-9gag sections**", value="`└─ Get the list of 9gag sections. \nNOTE: If your country is not in the 'sections' and can still able to view it on 9gag.com use 't-feedback' to inform about it. \n\nThe 'popular' includes: \nTrending\nFresh`", inline=False)
		embed.add_field(name="**t-9gag search <query>**", value="`└─ Search 9gag and get your search result.`", inline=False)
		embed.set_footer(text="Type t-help to get the list of all commands", icon_url="https://raw.githubusercontent.com/J16N/tsuby/master/cogs/tsuby.png")

		if ctx.message.guild is not None:
			await ctx.message.add_reaction("📧")

		await ctx.author.send(embed=embed)


def setup(bot):
	bot.add_cog(Fun(bot))

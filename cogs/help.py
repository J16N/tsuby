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
		
		embed.add_field(name="**t-feedback <your_feedback>**", value="`└─ Sends feedback to the bot owner.`", inline=False)
		embed.add_field(name="**t-nitromojis**", value="`└─ Lists all the nitromojis.`", inline=False)
		embed.add_field(name="**t-ne [<nitromoji>, <nitromoji> ... <nitromoji>]**", value="`└─ Sends all the list of nitromojis. The aliases of this command is 't-nitro'`", inline=False)
		embed.add_field(name="**t-ping**", value="`└─ Pings the bot`", inline=False)
		embed.add_field(name="**t-react [<emoji>, <emoji> ... <nitromoji>]**", value="`└─ Reacts to the last message of any user with the following list of emojis.` \n\n**─── Main Commands ───**", inline=False)
		
		embed.add_field(name="**t-9gag help**", value="`└─ 1 command. All the available memes related commands.`", inline=False)
		embed.add_field(name="**t-coc help**", value="`└─ 2 commands. All the Clash Of Clans related commands.`", inline=False)
		embed.add_field(name="**t-game help**", value="`└─ 2 command. All the available games and their related commands.`", inline=False)
		embed.add_field(name="**t-jokes help**", value="`└─ 1 command. All the available jokes related commands.`", inline=False)
		embed.add_field(name="**t-tr help**", value="`└─ 7 commands. All the translation related commands.`", inline=False)
		embed.set_footer(text="I am created by Tsubasa#7917.", icon_url="https://raw.githubusercontent.com/J16N/tsuby/master/cogs/tsuby.png")

		if ctx.message.guild is not None:
			await ctx.message.add_reaction("📧")

		await ctx.author.send(embed=embed)

def setup(bot):
	# Add the cog
	bot.remove_command("help")
	bot.add_cog(Help(bot))
from discord.ext import commands

# verify if the user in the message has manage_message permission or the bot creator
def has_power():
	def predicate(ctx):
		if ctx.author.id == 302467968095223820 or ctx.author.permissions_in(ctx.channel).manage_messages:
			return True
		else:
			return False
	
	return commands.check(predicate)


def admin():
	def predicate(ctx):
		if ctx.author.id == 302467968095223820 or ctx.author.permissions_in(ctx.channel).administrator:
			return True
		else:
			return False
	
	return commands.check(predicate)	
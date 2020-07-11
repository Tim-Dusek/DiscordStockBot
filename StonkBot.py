#Timothy Dusek
#7/11/20

#import statements
import discord
from random import randint
from discord.ext import commands

#prefix for command. Example: /command or !command
client = commands.Bot(command_prefix = '/')

###events

@client.event
async def on_ready():
	print("The bot is up and running")
#end event

@client.event
async def on_member_join(member):
	print(f'[{member} has joined the server')
#end event

@client.event
async def on_member_remove(member):
	print(f'[{member} has left the server')
#end event

###commands

 #test the bots ping
@client.command()
async def ping(ctx):
	await ctx.send(f'Ping is {round(client.latency * 1000)}ms')
#end command

#magic 8 ball to tell you what to buy!
@client.command(aliases=['8ball','magic8ball'])
async def _8ball(ctx, *, message):
	responses = ['Tesla, TSLA.',
				'Nasdaq, NQAQ',
				'Nintendo, NTDOY',
				'General Motors, GM',
				'Ford, F',
				'American Airlines, AAL',
				'Delta Air Lines, DAL',
				'Advanced Micro Devices, AMD',
				'Apple, AAPL',
				'Alphabet Class A, GOOGL']

	await ctx.send (f'{message}! The magic 8 ball wants you to buy 1 share of {responses[randint(0, len(responses))]}!')
#end command

#clears 1-20 messages from the chat. Defaults to 5 if no input
@client.command()
async def clear(ctx, amount=5):
	if amount<=20 and amount>=1:
		await ctx.channel.purge(limit=amount+1)
	#end if

	else:
		await ctx.send (f'You must enter a number between 1-20.')
	#end else
#end command


#add bot token to this function
client.run('NzMxNTQ2NTk4OTc4NjE3Mzk2.XwnoKg.kgcxjr-tyilsjeKhGT3FMghYFPI')


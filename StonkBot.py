#Timothy Dusek
#7/13/20

#Bugs: None

#Todo:/topmovers /biggestloser

###
#import statements
###

import discord
import time
import os
import yfinance as yf
import datetime as datetime
from random import randint
from discord.ext import commands, tasks
from itertools import cycle
from googlesearch import search

#set the prefix for all commands
client = commands.Bot(command_prefix = '/')
client.remove_command('help')

#set a list of activities for the bot to 'be playing' on discord
activity_list = cycle(['The Stock Market','The Bull Market',
				'The Bear Market','The Kankgaroo Market'])

###
#Events
###

#runs when bot is ready
@client.event
async def on_ready():
	change_activity.start()
	print('Bot is ready.')
#end event

#runs when someone joins the server
@client.event
async def on_member_join(member):
	print(f'{member} has joined the server')
#end event

#runs when someone leaves the server
@client.event
async def on_member_remove(member):
	print(f'{member} has left the server')
#end event

#handles errors when they come up
@client.event
async def on_command_error(ctx, error):
	if isinstance(error, commands.MissingRequiredArgument):
		await ctx.send(f'You seem to be missing a required argument.')
	#end if

	elif isinstance(error, commands.MissingPermissions):
		await ctx.send(f'You do not have permission to do that.')
		await ctx.send(f'Please consult server owner.')
	#end elif

###
#Commands
###

@client.command()
async def help(ctx):
	await ctx.author.send('Base User Commands:\n'+\
		'/help - Get info on bot commands you can access.\n'+\
		'/ping - Shows the latency of the bot.\n'+\
		'/news <Optional: Company> - Shows the top 3 relevant market articles.\n'+\
		'/price <Ticker Symbol> - Gives you price information about a ticker symbol.\n'+\
		'/whois <Ticker Symbol> - Gives you general information about a ticker symbol.\n'+\
		'/8ball - Shake the Magic 8 Ball and be told what stock to buy.\n')

	if ctx.message.author.guild_permissions.administrator:
		await ctx.author.send('My records show you are an admin!\n'+\
		'Here are the admin commands:\n'+\
		'/clear <Number> - Clears 1-10 messages from the chat permanently.\n'+\
		'/kick <User> <Optional: Reason> - Kicks a user from the discord.\n'+\
		'/ban <User> <Optional: Reason> - Bans a user from the discord.\n'+\
		'/unban <User> - Unbans a User. To use this you must use their name and 4 digit code.\n\n')
	#end if
#end command

#test the bots ping
@client.command()
async def ping(ctx):
	await ctx.send(f'Ping is {round(client.latency * 1000)}ms')
#end command

#takes a company name and returns 3 news articles related to their stock
@client.command()
async def news(ctx, *, company = ''):
	if company != '':
		company = company + ' '
	#end if

	query = 'stock market news'+ company
	await ctx.send(f'Let me check the internet for the latest {company}financial news...')

	for results in search(query, tld='com', lang='en', num=3, start=0, stop=3, pause=2.0):
		await ctx.send(results)
		time.sleep(1)
	#end for
#end command

@client.command() #gives price for any ticker symbol
async def price(ctx, company):
	ticker = yf.Ticker(company)
	ticker_info = ticker.info
	await ctx.send(f'Latest ask price for '+company+': '+str(ticker_info['ask'])+'\n'+\
		'Latest bid price for '+company+': '+str(ticker_info['bid'])+'\n')
#end command

@client.command() #gives information about any ticker symbol
async def whois(ctx, company):
	ticker = yf.Ticker(company)
	ticker_info = ticker.info
	market_cap_dollars= "${:,}".format(ticker_info['marketCap'])
	full_time_employees= "{:,}".format(ticker_info['fullTimeEmployees'])
	await ctx.send(f'Name: '+ticker_info['longName'])
	await ctx.send(f'Sector: '+ ticker_info['sector'])
	await ctx.send(f'Phone Number: '+ticker_info['phone'])
	await ctx.send(f'Full Time Employees: '+ full_time_employees)
	await ctx.send(f'Market Cap: '+ market_cap_dollars)
	await ctx.send(f'Summary: '+ticker_info['longBusinessSummary'])
#end command

#magic 8 ball to tell you what to buy
@client.command(aliases=['8ball','magic8ball'])
async def _8ball(ctx, *, message = ''):
	responses = ['Tesla, TSLA',
				'Nasdaq, NQAQ',
				'Nintendo, NTDOY',
				'General Motors, GM',
				'Ford, F',
				'American Airlines, AAL',
				'Delta Air Lines, DAL',
				'Advanced Micro Devices, AMD',
				'Apple, AAPL',
				'Alphabet Class A, GOOGL']
	if message == '':
		await ctx.send (f'The magic 8 ball wants you to buy 1 share of {responses[randint(0, len(responses))]}!')
	#end if

	else:
		await ctx.send (f'{message}! The magic 8 ball wants you to buy 1 share of {responses[randint(0, len(responses))]}!')
	#end else
#end command

#clears 1-10 messages from the chat if user has manag messages permissions
@client.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount : int):
	if amount<=10 and amount>=1:
		await ctx.channel.purge(limit=amount+1)
	#end if

	else:
		await ctx.send (f'You must enter a number between 1-10.')
	#end else
#end command

#kick a user
@client.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member : discord.Member, *, reason=None):
	await member.kick(reason=reason)
	await ctx.send(f'Kicked {member.mention}.')
#end command

#ban a user
@client.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member : discord.Member, *, reason=None):
	await member.ban(reason=reason)
	await ctx.send(f'Banned {member.mention}.')
#end command

#unban a user
@client.command()
@commands.has_permissions(ban_members=True)
async def unban(ctx, *, member):
	banned_users = await ctx.guild.bans()
	member_name, member_discriminator = member.split('#')

	for ban_entry in banned_users:
		user = ban_entry.user

		if (user.name, user.discriminator) == (member_name, member_discriminator):
			await ctx.guild.unban(user)
			await ctx.send(f'Unbanned {user.mention}.')
			return
		#end if
	#end for
#end command

###
#Tasks
###

@tasks.loop(minutes=30)
async def change_activity():
	await client.change_presence(activity=discord.Game(next(activity_list)),status=discord.Status.idle)
#end task

###
### Experimental beyond this point
###

###
#Cogs
###
'''
#load cog command
@client.command()
async def load(ctx, extension):
	client.load_extension(f'Cogs.{extension}')

#unload cog command
@client.command()
async def unload(ctx, extension):
	client.unload_extension(f'Cogs.{extension}')

for filename in os.listdir('./Cogs'):
	if filename.endswith('.py'):
		client.load_extension(f'Cogs.{filename[:-3]}')
	#end if
#end for 
'''

#add bot token to this function
client.run('*')


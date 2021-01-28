#Timothy Dusek
#1/03/21

#Bugs: None

'''
Patch Notes:

Stonk Bot Version: 
- V-1.9.1

Bug Fixes / Minor Changes:
- Added a small message when using any /graph command so users know to wait

New Features:
- Added /monthgraph to show stock prices for 1 month of a company
- Added /daygraph to show daily stock prices

To Do:
- Hello Wall-e gif when Bot turns on
- Create /biggestlosers command.
- Create /topmovers command.
- Add commas for volume and avergea volume for /price
- Add a message for /graph comamnds so user knows to wait
- changed /price to show decimals following dollar ammount
- Add more relevant information to the /price and /whois commands.
- Add /dev command so users can see who is actively maintaining the program

For any additional feature requests or feedback please contact Tim Dusek
'''

###
#import statements
###

import time, os, sys, argparse, io
import discord, yfinance as yf, datetime as datetime, matplotlib.pyplot as plt
from datetime import datetime
from random import randint
from discord.ext import commands, tasks
from itertools import cycle
from googlesearch import search

parser = argparse.ArgumentParser()

parser.add_argument(
    "-k", 
    "--api_key", 
    help="The Discord API key Stonk Bot should use", 
    action="store",
    type=str
)

args = parser.parse_args()

env_var = os.environ
if "API_Key" in env_var:
	api_key = env_var["API_Key"]
else:
	api_key = ""
# End if/else block

if args.api_key:
	api_key = args.api_key
elif not api_key:
	print("Please provide a valid Discord API key via the \"-k\" flag or the \"API_Key\" environment variable!")
	sys.exit(1)
# End if

#set the prefix for all commands
client = commands.Bot(command_prefix = '/')
client.remove_command('help')

#set a list of activities for the bot to 'be playing' on discord
activity_list = cycle(['The Stock Market','The Bull Market',
				'The Bear Market','The Kankgaroo Market','The Wolf Market',
				'The Cryptocurrency Market', 'Theta Gang', 'It Bearish',
				'It Bullish','An Online Casino'])

###
#Events
###

#runs when bot is ready
@client.event
async def on_ready():
	change_activity.start()
	market_open.start()
	market_close.start()
	channel = client.get_channel(731225596100739224)
	#await channel.send(":robot: Stonk Bot is ready to maximize your gains :robot:")
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
		'/price <Ticker Symbol> - Gives you daily price information about a ticker symbol.\n'+\
		'/whois <Ticker Symbol> - Gives you general information about a ticker symbol.\n'+\
		'/expert <Ticker Symbol> - Gives you expert opinions on what a stock is doing.\n'+\
		'/maxgraph <Ticker Symbol> - Gives you a graph of a stocks entire price history.\n'+\
		'/yeargraph <Ticker Symbol> - Gives you a 1 year graph of a stocks price history.\n'+\
		'/monthgraph <Ticker Symbol> - Gives you a 1 month graph of a stocks price history.\n'+\
		'/daygraph <Ticker Symbol> - Gives you a 1 day graph of a stocks price history.\n'+\
		'/8ball - Shake the Magic 8 Ball and be told what stock to buy.\n')

	if ctx.message.author.guild_permissions.administrator:
		await ctx.author.send('My records show you are an admin!\n'+\
		'Here are the admin only commands:\n'+\
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

	for results in search(query, tld='com', lang='en', num=3, start=0, stop=3, pause=1.0):
		await ctx.send(results)
		time.sleep(1)
	#end for
#end command

@client.command() #gives price for any ticker symbol
async def price(ctx, company):
	await ctx.send(f'Getting price information for '+company+'...')
	ticker = yf.Ticker(company)
	ticker_info = ticker.info
	await ctx.send(f'Opening Price: $'+str(ticker_info['open'])+'\n'+\
		'Latest ask price: $'+str(ticker_info['ask'])+'\n'+\
		'Latest bid price: $'+str(ticker_info['bid'])+'\n'+\
		'Volume: '+str(ticker_info['volume'])+'\n'+\
		'Average volume: '+str(ticker_info['averageVolume'])+'\n'+\
		'Beta: '+str(ticker_info['beta'])[0:5]+'\n')
#end command

@client.command() #gives information about any ticker symbol
async def whois(ctx, company):
	await ctx.send(f'Getting general information for '+company+'...')
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

@client.command() #gives you expert thoughts on what a stock is doing
async def expert(ctx, company):
	await ctx.send(f'Let me get expert opinions on '+company+' for you...')
	ticker = yf.Ticker(company)
	expert = ticker.recommendations
	output = expert[len(expert)-5:len(expert)]
	output = str(output)
	output = output[75:]
	await ctx.send(output)
#end command

@client.command()#displays a graph of a stocks entire history
async def maxgraph(ctx,company):
	await ctx.send(f'Let me get a graph of '+company+' for you...')
	ticker = yf.Ticker(company)
	plotted_graph= ticker.history(period="max", interval="1d")
	plotted_graph['Close'].plot(title="Stock Price For "+company)
	plt.xlabel ('Date')
	plt.ylabel ('Price')
	plt.savefig('max_graph.png')
	await ctx.send(file=discord.File('max_graph.png'))
	plt.close()

@client.command()
async def yeargraph(ctx,company):
	await ctx.send(f'Let me get a graph of '+company+' for you...')
	ticker = yf.Ticker(company)
	plotted_graph= ticker.history(period="1y", interval="1d")
	plotted_graph['Close'].plot(title="Stock Price For "+company)
	plt.xlabel ('Date')
	plt.ylabel ('Price')
	plt.savefig('yr_graph.png')
	await ctx.send(file=discord.File('yr_graph.png'))
	plt.close()

@client.command()
async def monthgraph(ctx,company):
	await ctx.send(f'Let me get a graph of '+company+' for you...')
	ticker = yf.Ticker(company)
	plotted_graph= ticker.history(period="1mo", interval="1d")
	plotted_graph['Close'].plot(title="Stock Price For "+company)
	plt.xlabel ('Date')
	plt.ylabel ('Price')
	plt.savefig('mo_graph.png')
	await ctx.send(file=discord.File('mo_graph.png'))
	plt.close()

@client.command()#
async def weekgraph(ctx,company):
	#await ctx.send(f'Let me get a graph of '+company+' for you...')
	# Get stock data
	ticker = yf.Ticker(company)
	
	# Plot graph
	plotted_graph = ticker.history(period="5d", interval="1d")
	plotted_graph['Close'].plot(title="Stock Price For "+company)
	plt.xlabel ('Date & Military Time')
	plt.ylabel ('Price')

	# Save image to buffer
	image_buffer = io.BytesIO()
	plt.savefig(image_buffer, format="PNG")
	image_buffer.seek(0)
	
	# Push contents of image buffer to Discord
	await ctx.send("week_graph.png", file=discord.File(image_buffer))

	# Close plot and image buffer
	plt.close()
	image_buffer.close()

@client.command()#
async def daygraph(ctx,company):
	await ctx.send(f'Let me get a graph of '+company+' for you...')
	ticker = yf.Ticker(company)
	plotted_graph= ticker.history(period="1d", interval="1m", prepost=True)
	plotted_graph['Close'].plot(title="Stock Price For "+company)
	plt.xlabel ('Date & Military Time')
	plt.ylabel ('Price')
	plt.savefig('day_graph.png')
	await ctx.send(file=discord.File('day_graph.png'))
	plt.close()

#magic 8 ball to tell you what to buy
@client.command(aliases=['8ball','magic8ball'])
async def _8ball(ctx, *, message = ''):
	ammounts = ['1 share','a fractional share']

	responses = ['Agilent Technologies Inc, A', 'American Airlines Group, AAL', 'Advance Auto Parts, AAP', 'Apple Inc., AAPL',
	'AbbVie Inc., ABBV', 'AmerisourceBergen Corp, ABC', 'ABIOMED Inc, ABMD', 'Abbott Laboratories, ABT', 'Accenture plc, ACN',
	'Adobe Inc., ADBE', 'Analog Devices, Inc., ADI', 'Archer-Daniels-Midland Co, ADM', 'Automatic Data Processing, ADP', 'Alliance Data Systems, ADS',
	'Autodesk Inc., ADSK', 'Ameren Corp, AEE', 'American Electric Power, AEP', 'AES Corp, AES', 'AFLAC Inc, AFL', 'American International Group, AIG',
	'Apartment Investment & Management, AIV', 'Assurant, AIZ', 'Arthur J. Gallagher & Co., AJG', 'Akamai Technologies Inc, AKAM', 'Albemarle Corp, ALB',
	'Align Technology, ALGN', 'Alaska Air Group Inc, ALK', 'Allstate Corp, ALL', 'Allegion, ALLE', 'Alexion Pharmaceuticals, ALXN', 'Applied Materials Inc., AMAT',
	'Amcor plc, AMCR', 'Advanced Micro Devices Inc, AMD', 'AMETEK Inc., AME', 'Amgen Inc., AMGN', 'Ameriprise Financial, AMP', 'American Tower Corp., AMT',
	'Amazon.com Inc., AMZN', 'Arista Networks, ANET', 'ANSYS, ANSS', 'Anthem, ANTM', 'Aon plc, AON', 'A.O. Smith Corp, AOS', 'Apache Corporation, APA', 'Air Products & Chemicals Inc, APD',
	'Amphenol Corp, APH', 'Aptiv PLC, APTV', 'Alexandria Real Estate Equities, ARE', 'Atmos Energy, ATO', 'Activision Blizzard, ATVI', 'AvalonBay Communities, AVB', 'Broadcom Inc., AVGO',
	'Avery Dennison Corp, AVY', 'American Water Works Company Inc, AWK', 'American Express Co, AXP', 'AutoZone Inc, AZO', 'Boeing Company, BA', 'Bank of America Corp, BAC',
	'Baxter International Inc., BAX', 'Best Buy Co. Inc., BBY', 'Becton Dickinson, BDX', 'Franklin Resources, BEN', 'Brown-Forman Corp., BF.B', 'Biogen Inc., BIIB', 'The Bank of New York Mellon, BK',
	'Booking Holdings Inc, BKNG', 'Baker Hughes Co, BKR', 'BlackRock, BLK', 'Ball Corp, BLL', 'Bristol-Myers Squibb, BMY', 'Broadridge Financial Solutions, BR', 'Berkshire Hathaway, BRK.B', 'Boston Scientific, BSX',
	'BorgWarner, BWA', 'Boston Properties, BXP', 'Citigroup Inc., C', 'Conagra Brands, CAG', 'Cardinal Health Inc., CAH', 'Carrier Global, CARR', 'Caterpillar Inc., CAT', 'Chubb Limited, CB',
	'Cboe Global Markets, CBOE', 'CBRE Group, CBRE', 'Crown Castle International Corp., CCI', 'Carnival Corp., CCL', 'Cadence Design Systems, CDNS', 'CDW, CDW', 'Celanese, CE', 'Cerner, CERN',
	'CF Industries Holdings Inc, CF', 'Citizens Financial Group, CFG', 'Church & Dwight, CHD', 'C. H. Robinson Worldwide, CHRW', 'Charter Communications, CHTR', 'CIGNA Corp., CI', 'Cincinnati Financial, CINF',
	'Colgate-Palmolive, CL', 'The Clorox Company, CLX', 'Comerica Inc., CMA', 'Comcast Corp., CMCSA', 'CME Group Inc., CME', 'Chipotle Mexican Grill, CMG', 'Cummins Inc., CMI', 'CMS Energy, CMS',
	'Centene Corporation, CNC', 'CenterPoint Energy, CNP', 'Capital One Financial, COF', 'Cabot Oil & Gas, COG', 'The Cooper Companies, COO', 'ConocoPhillips, COP', 'Costco Wholesale Corp., COST',
	'Coty, Inc, COTY', 'Campbell Soup, CPB', 'Copart Inc, CPRT', 'Salesforce.com, CRM', 'Cisco Systems, CSCO', 'CSX Corp., CSX', 'Cintas Corporation, CTAS', 'CenturyLink Inc, CTL',
	'Cognizant Technology Solutions, CTSH', 'Corteva, CTVA', 'Citrix Systems, CTXS', 'CVS Health, CVS', 'Chevron Corp., CVX', 'Concho Resources, CXO', 'Dominion Energy, D',
	'Delta Air Lines Inc., DAL', 'DuPont de Nemours Inc, DD', 'Deere & Co., DE', 'Discover Financial Services, DFS', 'Dollar General, DG', 'Quest Diagnostics, DGX', 'D. R. Horton, DHI',
	'Danaher Corp., DHR', 'The Walt Disney Company, DIS', 'Discovery, Inc. (Class A), DISCA', 'Discovery, Inc. (Class C), DISCK', 'Dish Network, DISH', 'Digital Realty Trust Inc, DLR',
	'Dollar Tree, DLTR', 'Dover Corporation, DOV', 'Dow Inc., DOW', 'Dominos Pizza, DPZ', 'Duke Realty Corp, DRE', 'Darden Restaurants, DRI', 'DTE Energy Co., DTE', 'Duke Energy, DUK',
	'DaVita Inc., DVA', 'Devon Energy, DVN', 'DXC Technology, DXC', 'DexCom, DXCM', 'Electronic Arts, EA', 'eBay Inc., EBAY', 'Ecolab Inc., ECL', 'Consolidated Edison, ED', 'Equifax Inc., EFX',
	'Edison Intl, EIX', 'Estée Lauder Companies, EL', 'Eastman Chemical, EMN', 'Emerson Electric Company, EMR', 'EOG Resources, EOG', 'Equinix, EQIX', 'Equity Residential, EQR',
	'Eversource Energy, ES', 'Essex Property Trust, Inc., ESS', 'E*Trade, ETFC', 'Eaton Corporation, ETN', 'Entergy Corp., ETR', 'Evergy, EVRG', 'Edwards Lifesciences, EW', 'Exelon Corp., EXC',
	'Expeditors, EXPD', 'Expedia Group, EXPE', 'Extra Space Storage, EXR', 'Ford Motor Company, F', 'Diamondback Energy, FANG', 'Fastenal Co, FAST', 'Facebook, Inc., FB',
	'Fortune Brands Home & Security, FBHS', 'Freeport-McMoRan Inc., FCX', 'FedEx Corporation, FDX', 'FirstEnergy Corp, FE', 'F5 Networks, FFIV', 'Fidelity National Information Services, FIS',
	'Fiserv Inc, FISV', 'Fifth Third Bancorp, FITB', 'FLIR Systems, FLIR', 'Flowserve Corporation, FLS', 'FleetCor Technologies Inc, FLT', 'FMC Corporation, FMC',
	'Fox Corporation (Class B), FOX', 'Fox Corporation (Class A), FOXA', 'First Republic Bank, FRC', 'Federal Realty Investment Trust, FRT', 'TechnipFMC, FTI',
	'Fortinet, FTNT', 'Fortive Corp, FTV', 'General Dynamics, GD', 'General Electric, GE', 'Gilead Sciences, GILD', 'General Mills, GIS', 'Globe Life Inc., GL',
	'Corning Inc., GLW', 'General Motors, GM', 'Alphabet Inc. (Class C), GOOG', 'Alphabet Inc. (Class A), GOOGL', 'Genuine Parts, GPC', 'Global Payments Inc., GPN', 'Gap Inc., GPS',
	'Garmin Ltd., GRMN', 'Gowldman Sachs Group, GS', 'Grainger (W.W.) Inc., GWW', 'Halliburton Co., HAL', 'Hasbro Inc., HAS', 'Huntington Bancshares, HBAN', 'Hanesbrands Inc, HBI',
	'HCA Healthcare, HCA', 'Home Depot, HD', 'Hess Corporation, HES', 'HollyFrontier Corp, HFC', 'Hartford Financial Svc.Gp., HIG', 'Huntington Ingalls Industries, HII',
	'Hilton Worldwide Holdings Inc, HLT', 'Harley-Davidson, HOG', 'Hologic, HOLX', 'Honeywell Intl Inc., HON', 'Hewlett Packard Enterprise, HPE', 'HP Inc., HPQ', 'H&R Block, HRB',
	'Hormel Foods Corp., HRL', 'Henry Schein, HSIC', 'Host Hotels & Resorts, HST', 'The Hershey Company, HSY', 'Humana Inc., HUM', 'Howmet Aerospace, HWM', 'International Business Machines, IBM',
	'Intercontinental Exchange, ICE', 'IDEXX Laboratories, IDXX', 'IDEX Corporation, IEX', 'Intl Flavors & Fragrances, IFF', 'Illumina Inc, ILMN', 'Incyte, INCY', 'IHS Markit Ltd., INFO',
	'Intel Corp., INTC', 'Intuit Inc., INTU', 'International Paper, IP', 'Interpublic Group, IPG', 'IPG Photonics Corp., IPGP', 'IQVIA Holdings Inc., IQV', 'Ingersoll Rand, IR',
	'Iron Mountain Incorporated, IRM', 'Intuitive Surgical Inc., ISRG', 'Gartner Inc, IT', 'Illinois Tool Works, ITW', 'Invesco Ltd., IVZ', 'Jacobs Engineering Group, J',
	'J. B. Hunt Transport Services, JBHT', 'Johnson Controls International, JCI', 'Jack Henry & Associates, JKHY', 'Johnson & Johnson, JNJ', 'Juniper Networks, JNPR',
	'JPMorgan Chase & Co., JPM', 'Nordstrom, JWN', 'Kellogg Co., K', 'KeyCorp, KEY', 'Keysight Technologies, KEYS', 'Kraft Heinz Co, KHC', 'Kimco Realty, KIM', 'KLA Corporation, KLAC',
	'Kimberly-Clark, KMB', 'Kinder Morgan, KMI', 'Carmax Inc, KMX', 'Coca-Cola Company, KO', 'Kroger Co., KR', 'Kohls Corp., KSS', 'Kansas City Southern, KSU',
	'Loews Corp., L', 'L Brands Inc., LB', 'Leidos Holdings, LDOS', 'Leggett & Platt, LEG', 'Lennar Corp., LEN', 'Laboratory Corp. of America Holding, LH', 'L3Harris Technologies, LHX',
	'Linde plc, LIN', 'LKQ Corporation, LKQ', 'Lilly (Eli) & Co., LLY', 'Lockheed Martin Corp., LMT', 'Lincoln National, LNC', 'Alliant Energy Corp, LNT', 'Lowes Cos., LOW',
	'Lam Research, LRCX', 'Southwest Airlines, LUV', 'Las Vegas Sands, LVS', 'Lamb Weston Holdings Inc, LW', 'LyondellBasell, LYB', 'Live Nation Entertainment, LYV', 'Mastercard Inc., MA',
	'Mid-America Apartments, MAA', 'Marriott Intl., MAR', 'Masco Corp., MAS', 'McDonalds Corp., MCD', 'Microchip Technology, MCHP', 'McKesson Corp., MCK', 'Moodys Corp, MCO',
	'Mondelez International, MDLZ', 'Medtronic plc, MDT', 'MetLife Inc., MET', 'MGM Resorts International, MGM', 'Mohawk Industries, MHK', 'McCormick & Co., MKC', 'MarketAxess, MKTX',
	'Martin Marietta Materials, MLM', 'Marsh & McLennan, MMC', '3M Company, MMM', 'Monster Beverage, MNST', 'Altria Group Inc, MO', 'The Mosaic Company, MOS', 'Marathon Petroleum, MPC',
	'Merck & Co., MRK', 'Marathon Oil Corp., MRO', 'Morgan Stanley, MS', 'MSCI Inc, MSCI', 'Microsoft Corp., MSFT', 'Motorola Solutions Inc., MSI', 'M&T Bank Corp., MTB', 'Mettler Toledo, MTD',
	'Micron Technology, MU', 'Maxim Integrated Products Inc, MXIM', 'Mylan N.V., MYL', 'Noble Energy Inc, NBL', 'Norwegian Cruise Line Holdings, NCLH', 'Nasdaq, Inc., NDAQ', 'NextEra Energy, NEE', 'Newmont Corporation, NEM',
	'Netflix Inc., NFLX', 'NiSource Inc., NI', 'Nike, NKE', 'NortonLifeLock, NLOK', 'Nielsen Holdings, NLSN', 'Northrop Grumman, NOC', 'National Oilwell Varco Inc., NOV', 'ServiceNow, NOW', 'NRG Energy, NRG',
	'Norfolk Southern Corp., NSC', 'NetApp, NTAP', 'Northern Trust Corp., NTRS', 'Nucor Corp., NUE', 'Nvidia Corporation, NVDA', 'NVR Inc, NVR', 'Newell Brands, NWL', 'News Corp. Class B, NWS',
	'News Corp. Class A, NWSA', 'Realty Income Corporation, O', 'Old Dominion Freight Line, ODFL', 'ONEOK, OKE', 'Omnicom Group, OMC', 'Oracle Corp., ORCL', 'OReilly Automotive, ORLY', 'Otis Worldwide, OTIS',
	'Occidental Petroleum, OXY', 'Paycom, PAYC', 'Paychex Inc., PAYX', 'Peoples United Financial, PBCT', 'PACCAR Inc., PCAR', 'Healthpeak Properties, PEAK', 'Public Serv. Enterprise Inc., PEG',
	'PepsiCo Inc., PEP', 'Pfizer Inc., PFE', 'Principal Financial Group, PFG', 'Procter & Gamble, PG', 'Progressive Corp., PGR', 'Parker-Hannifin, PH', 'PulteGroup, PHM', 'Packaging Corporation of America, PKG',
	'PerkinElmer, PKI', 'Prologis, PLD', 'Philip Morris International, PM', 'PNC Financial Services, PNC', 'Pentair plc, PNR', 'Pinnacle West Capital, PNW', 'PPG Industries, PPG', 'PPL Corp., PPL', 'Perrigo, PRGO',
	'Prudential Financial, PRU', 'Public Storage, PSA', 'Phillips 66, PSX', 'PVH Corp., PVH', 'Quanta Services Inc., PWR', 'Pioneer Natural Resources, PXD', 'PayPal, PYPL', 'QUALCOMM Inc., QCOM', 'Qorvo, QRVO',
	'Royal Caribbean Cruises Ltd, RCL', 'Everest Re Group Ltd., RE', 'Regency Centers Corporation, REG', 'Regeneron Pharmaceuticals, REGN', 'Regions Financial Corp., RF', 'Robert Half International, RHI',
	'Raymond James Financial Inc., RJF', 'Ralph Lauren Corporation, RL', 'ResMed, RMD', 'Rockwell Automation Inc., ROK', 'Rollins Inc., ROL', 'Roper Technologies, ROP', 'Ross Stores, ROST', 'Republic Services Inc, RSG',
	'Raytheon Technologies, RTX', 'SBA Communications, SBAC', 'Starbucks Corp., SBUX', 'Charles Schwab Corporation, SCHW', 'Sealed Air, SEE', 'Sherwin-Williams, SHW', 'SVB Financial, SIVB', 'JM Smucker, SJM',
	'Schlumberger Ltd., SLB', 'SL Green Realty, SLG', 'Snap-on, SNA', 'Synopsys Inc., SNPS', 'Southern Company, SO', 'Simon Property Group Inc, SPG', 'S&P Global, Inc., SPGI', 'Sempra Energy, SRE',
	'STERIS plc, STE', 'State Street Corp., STT', 'Seagate Technology, STX', 'Constellation Brands, STZ', 'Stanley Black & Decker, SWK', 'Skyworks Solutions, SWKS', 'Synchrony Financial, SYF', 'Stryker Corp., SYK',
	'Sysco Corp., SYY', 'AT&T Inc., T', 'Molson Coors Brewing Company, TAP', 'TransDigm Group, TDG', 'TE Connectivity Ltd., TEL', 'Truist Financial, TFC', 'Teleflex, TFX', 'Target Corp., TGT',
	'Tiffany & Co., TIF', 'TJX Companies Inc., TJX', 'Thermo Fisher Scientific, TMO', 'T-Mobile US, TMUS', 'Tapestry, Inc., TPR', 'T. Rowe Price Group, TROW', 'The Travelers Companies Inc., TRV',
	'Tractor Supply Company, TSCO', 'Tyson Foods, TSN', 'Trane Technologies plc, TT', 'Take-Two Interactive, TTWO', 'Twitter, Inc., TWTR', 'Texas Instruments, TXN', 'Textron Inc., TXT', 'Under Armour (Class C), UA',
	'Under Armour (Class A), UAA', 'United Airlines Holdings, UAL', 'UDR, Inc., UDR', 'Universal Health Services, Inc., UHS', 'Ulta Beauty, ULTA', 'United Health Group Inc., UNH', 'Unum Group, UNM',
	'Union Pacific Corp, UNP', 'United Parcel Service, UPS', 'United Rentals, Inc., URI', 'U.S. Bancorp, USB', 'Visa Inc., V', 'Varian Medical Systems, VAR', 'V.F. Corp., VFC', 'ViacomCBS, VIAC', 'Valero Energy, VLO',
	'Vulcan Materials, VMC', 'Vornado Realty Trust, VNO', 'Verisk Analytics, VRSK', 'Verisign Inc., VRSN', 'Vertex Pharmaceuticals Inc, VRTX', 'Ventas Inc, VTR', 'Verizon Communications, VZ', 'Wabtec Corporation, WAB',
	'Waters Corporation, WAT', 'Walgreens Boots Alliance, WBA', 'Western Digital, WDC', 'WEC Energy Group, WEC', 'Welltower Inc., WELL', 'Wells Fargo, WFC', 'Whirlpool Corp., WHR', 'Willis Towers Watson, WLTW',
	'Waste Management Inc., WM', 'Williams Cos., WMB', 'Walmart, WMT', 'W. R. Berkley Corporation, WRB', 'WestRock, WRK', 'West Pharmaceutical Services, WST', 'Western Union Co, WU', 'Weyerhaeuser, WY',
	'Wynn Resorts Ltd, WYNN', 'Xcel Energy Inc, XEL', 'Xilinx, XLNX', 'Exxon Mobil Corp., XOM', 'Dentsply Sirona, XRAY', 'Xerox, XRX', 'Xylem Inc., XYL', 'Yum! Brands Inc, YUM', 'Zimmer Biomet Holdings, ZBH',
	'Zebra Technologies, ZBRA', 'Zions Bancorp, ZION', 'Zoetis, ZTS', 'Advanced Micro Devices, AMD', 'Amazon.com, AMZN', 'Amgen, AMGN', 'Analog Devices, ADI', 'Applied Materials, Inc., AMAT', 'ASML Holding, ASML',
	'Autodesk, ADSK', 'Automatic Data Processing, Inc., ADP', 'Baidu, BIDU', 'Biogen, BIIB', 'BioMarin Pharmaceutical, Inc., BMRN', 'Booking Holdings, BKNG', 'Cerner Corporation, CERN', 'Charter Communications, Inc., CHTR',
	'Check Point Software Technologies Ltd., CHKP', 'Cognizant Technology Solutions Corporation, CTSH', 'Comcast Corporation, CMCSA', 'Copart, CPRT', 'CoStar Group, CSGP', 'Costco Wholesale Corporation, COST',
	'CSX Corporation, CSX', 'DocuSign, DOCU', 'Dollar Tree, Inc., DLTR', 'Exelon Corporation, EXC', 'Fastenal Company, FAST', 'Fiserv, Inc., FISV', 'Gilead Sciences, Inc., GILD', 'Illumina, Inc., ILMN',
	'Incyte Corporation, INCY', 'Intel Corporation, INTC', 'Intuit, INTU', 'Intuitive Surgical, ISRG', 'JD.com, JD', 'Liberty Global (Class A), LBTYA', 'Liberty Global (Class C), LBTYK', 'Lululemon Athletica, LULU',
	'Marriott International, MAR', 'Maxim Integrated Products, MXIM', 'MercadoLibre, MELI', 'Micron Technology, Inc., MU', 'Microsoft Corporation, MSFT', 'Mondelēz International, MDLZ', 'Monster Beverage Corporation, MNST',
	'NetEase, Inc., NTES', 'Netflix, NFLX', 'NXP Semiconductors N.V., NXPI', 'OReilly Automotive, Inc., ORLY', 'Paychex, Inc., PAYX', 'PepsiCo, Inc., PEP', 'QUALCOMM, QCOM', 'Ross Stores Inc., ROST', 'Seattle Genetics, SGEN',
	'Sirius XM Radio, Inc., SIRI', 'Skyworks Solutions, Inc., SWKS', 'Splunk, SPLK', 'Starbucks Corporation, SBUX', 'Synopsys, Inc., SNPS', 'Take-Two Interactive, Inc., TTWO', 'Tesla, Inc., TSLA', 'Texas Instruments, Inc., TXN',
	'Trip.com Group, TCOM', 'Verisign, VRSN', 'Vertex Pharmaceuticals, VRTX', 'Walgreen Boots Alliance, Inc., WBA', 'Workday, Inc., WDAY', 'Xcel Energy, Inc., XEL', 'Xilinx, Inc., XLNX', 'Zoom Video Communications, ZM']
	
	if message == '':
		await ctx.send (f'The magic 8 ball wants you to buy {ammounts[randint(0,len(ammounts)-1)]} of {responses[randint(0, len(responses)-1)]}!')
	#end if

	else:
		await ctx.send (f'{message}! The magic 8 ball wants you to buy {ammounts[randint(0,len(ammounts)-1)]} of {responses[randint(0, len(responses)-1)]}!')
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

@tasks.loop(minutes=5) #
async def change_activity():
	await client.change_presence(activity=discord.Game(next(activity_list)),status=discord.Status.idle)
#end task

@tasks.loop(minutes=1) #sends a message when the market opens at 8:30 am EST
async def market_open():
	channel = client.get_channel(731225596100739224)
	eastern = arrow.utcnow.to('US/Eastern')
	if eastern.hour == 9 and eastern.minute == 30:
		await channel.send(":bell: The market is now open! :bell:")
	# End if
		
#end task

@tasks.loop(minutes=1) #sends a message when the market closes at 4:00 pm EST
async def market_close():
	channel = client.get_channel(731225596100739224)
	eastern = arrow.utcnow.to('US/Eastern')
	if eastern.hour == 16 and eastern.minute == 0:
		await channel.send(":bell: The market is now open! :bell:")
	# End if
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
client.run(api_key)
import discord
from discord.ext import commands
from db import is_in_database, dbupdate
import config
intents = discord.Intents()
intents.members = True
intents.guilds = True
intents.bans = True
intents.messages = True
intents.reactions = True


bot = commands.Bot(command_prefix='!', case_insensitive=True, intents=intents)
initCogs = ['cogs.error', 'cogs.events', 'cogs.moderation', 'cogs.log', 'cogs.info', 'cogs.misc'] #All default cogs that load on startup

#Event for when the bot comes online
@bot.event
async def on_ready():
    #Send a message when the comes online
    print('✅ Successfully logged in as {0.user}'.format(bot))

    #Verify all servers the bot is in are in the DB
    for guild in bot.guilds:
        if not await is_in_database(sql=f'SELECT server FROM servers WHERE Server={guild.id}'):
            await dbupdate('main.db', 'INSERT INTO servers (server, name) VALUES (?, ?)', (guild.id, guild.name))
            print(f'{guild.name} added to db!')

#Load all default cogs
counter = 0
for cog in initCogs:
    try:
        bot.load_extension(cog)
        print(f'✅ {cog} loaded successfully')
    except Exception as e:
        print(f'❌ {cog} failed to load')
        counter += 1
    else:
        if counter > 0:
            break
if counter == 0:
    print('✅ all cogs loaded successfully')

#Add ✅ reaction after a command was completed
@bot.event
async def on_command_completion(ctx):
    await ctx.message.add_reaction('✅')

#Manually load a cog
@bot.command()
@commands.is_owner()
async def load(ctx, extension):
    '''Load a specific cog'''
    bot.load_extension(f'cogs.{extension}')
    
#Manually unload a cog
@bot.command()
@commands.is_owner()
async def unload(ctx, extension):
    '''Unload a specific cog'''
    bot.unload_extension(f'cogs.{extension}')

#Manually reload a cog
@bot.command()
@commands.is_owner()
async def reload(ctx, extension):
    '''Reload a specific cog'''
    bot.unload_extension(f'cogs.{extension}')
    bot.load_extension(f'cogs.{extension}')

@bot.command()
async def ping(ctx):
    '''Get the bot's response time'''
    em = discord.Embed(color=0xEE7700)
    em.title = "Pong!"
    em.description = f'{round(bot.latency * 1000, 1)} ms'
    await ctx.send(embed=em) 

#Log bot into discord
bot.run(config.token)
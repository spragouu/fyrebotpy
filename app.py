import discord
from discord.ext import commands
import config

bot = commands.Bot(command_prefix='!', case_insensitive=True)
initCogs = ['cogs.error'] #All default cogs that load on startup

#Send confirmation message when logged into discord
@bot.event
async def on_ready():
    print('✅ Successfully logged in as {0.user}'.format(bot))

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
        else:
            print('✅ All cogs successfully loaded')

#Manually load a cog
@bot.command()
async def load(ctx, extension):
    """Load a cog"""
    bot.load_extension(f'cogs.{extension}')
    await ctx.message.add_reaction('✅')
    
#Manually unload a cog
@bot.command()
async def unload(ctx, extension):
    """Unload a cog"""
    bot.unload_extension(f'cogs.{extension}')
    await ctx.message.add_reaction('✅')

#Manually reload a cog
@bot.command()
async def reload(ctx, extension):
    """Reload a cog"""
    bot.unload_extension(f'cogs.{extension}')
    bot.load_extension(f'cogs.{extension}')
    await ctx.message.add_reaction('✅')

#Log bot into discord
bot.run(config.token)
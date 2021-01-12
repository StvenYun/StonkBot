import aiohttp
from discord.ext import commands
import os
from decouple import config



bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
    print('Bot is Ready')

@bot.command()
async def load(ctx, extension):
    bot.load_extension(f'cogs.{extension}')
    print(f'{extension} has been loaded')

@bot.command()
async def unload(ctx, extension):
    bot.unload_extension(f'cogs.{extension}')
    print(f'{extension} has been unloaded')

@bot.command()
async def reload(ctx, extension):
    bot.reload_extension(f'cogs.{extension}')
    print(f'{extension} has been reloaded')


for filename in os.listdir('./cogs'):
    #Check if file in directory is .py file
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')




Token = config('Token')


bot.run(Token)



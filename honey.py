#honey_bot.py
import os
import asyncio
import discord
from discord.ext import commands
from dotenv import load_dotenv

from honey.audiocontroller import *
###########################
#Honey Init
###########################
load_dotenv()

###########################
#Global
###########################
token = os.getenv('DISCORD_TOKEN')

###########################
#Honey Bot!
###########################

bot = commands.Bot(command_prefix=commands.when_mentioned_or("!"))

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))

if not discord.opus.is_loaded():   
    discord.opus.load_opus('libopus.so.0')

bot.remove_command("help")
bot.add_cog(AudioController(bot))
bot.run(token)

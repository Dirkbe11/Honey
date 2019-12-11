#honey_bot.py
import os
import asyncio

from discord.ext import commands
from dotenv import load_dotenv

from honey.sound.music import *
###########################
#Func Init
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

bot.add_cog(Music(bot))
bot.run(token)

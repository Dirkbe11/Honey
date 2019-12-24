import asyncio
import discord
from discord.ext import commands, tasks

from .sound.music import *
from .voice.voice_sink import *
print("Importing audiocontroller")


class AudioController(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.music = Music(bot)
        self.voice_sink = VoiceSink()
        
        self.voice_channel = None

        # self.S2TReader = None
        # Thread(target=SpeechReader, args=(self, self.buffer, self.voice_channel))
        # self.S2TReader.daemon = True
        # self.S2TReader.start()

    @commands.command()
    async def join(self, ctx):
        if ctx.author.voice:
            await ctx.author.voice.channel.connect()
            self.voice_channel = ctx.voice_client
            self.voice_channel.listen(self.voice_sink)
        else:
            await ctx.send("You are not in a voice channel!")

    @commands.command()
    async def clear(self, ctx):
        await self.music.clear(ctx)

    @commands.command()
    async def show(self, ctx):
        await self.music.show(ctx)

    @commands.command()
    async def queue(self, ctx, *, url):
        await self.music.queue(ctx, url)
    
    @commands.command()
    async def play(self, ctx, *, url):
        await self.music.play(ctx, url)
    
    @commands.command()
    async def volume(self, ctx, volume: int):
        await self.music.volume(ctx, volume)

    @commands.command()
    async def stop(self, ctx):
        await self.music.stop(ctx)
        await ctx.voice_client.disconnect()
        self.voice_channel.stop_listening()
        self.voice_channel = None

    #ensure_voice: Decorator for the 'play' command
    #If the command author is in a voice channel, then we join it
    @play.before_invoke
    async def ensure_voice(self, ctx):
        if ctx.voice_client is None:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect()
                self.voice_channel = ctx.voice_client
                self.voice_channel.listen(self.voice_sink)
            else:
                await ctx.send("You are not connected to a voice channel.")
                raise commands.CommandError("Author not connected to a voice channel.")
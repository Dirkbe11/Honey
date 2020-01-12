import asyncio
import discord
from discord.ext import commands, tasks

from .sound.music import *
from .voice.voice_sink import *
print("Importing audiocontroller")

loop = asyncio.get_event_loop()
help_command = "List of commands:\n\n**!join**: joins the voice channel\n\n**!clear**: clears the song queue\n\n**!queue**: shows the song queue\n\n**!queue_song [song]**: Adds given song to the queue\n\n**!play [song]**: plays the given song or adds to queue if honey is already playing one\n\n**!skip**: skips the current song\n\n**!stop**: stops honeybot and removes it from the voice channel"

class AudioController(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.music = Music(bot)
        self.voice_sink = VoiceSink(self.execute_verbal_command)
        self.voice_ctx = None
        self.async_event_loop = asyncio.get_event_loop()

    #==============================================
    #text-Command Functions
    #==============================================
    @commands.command()
    async def help(self, ctx):
        await ctx.send(help_command)

    @commands.command()
    async def join(self, ctx):
        if ctx.author.voice:
            await ctx.author.voice.channel.connect()
            self.voice_ctx = ctx
            self.voice_ctx.voice_client.listen(self.voice_sink)
        else:
            await ctx.send("You are not in a voice channel!")

    @commands.command()
    async def clear(self, ctx):
        await self.music.clear(ctx)

    @commands.command()
    async def queue(self, ctx):
        await self.music.show(ctx)

    @commands.command()
    async def queue_song(self, ctx, *, url):
        await self.music.queue(ctx, url)
    
    @commands.command()
    async def play(self, ctx, *, url):
        await self.music.play(ctx, url)
    
    @commands.command()
    async def volume(self, ctx, volume: int):
        await self.music.volume(ctx, volume)
    
    @commands.command()
    async def skip(self, ctx):
        await self.music.skip(ctx)

    @commands.command()
    async def stop(self, ctx):
        await self.music.stop(ctx)
        await ctx.voice_client.disconnect()

    #ensure_voice: Decorator for the 'play' command
    #If the command author is in a voice channel, then we join it
    @play.before_invoke
    async def ensure_voice(self, ctx):
        if ctx.voice_client is None:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect()
                self.voice_ctx = ctx
                self.voice_ctx.voice_client.listen(self.voice_sink)
            else:
                await ctx.send("You are not connected to a voice channel.")
                raise commands.CommandError("Author not connected to a voice channel.")

    #==============================================
    #Non-Command Functions
    #==============================================
    def execute_verbal_command(self, command):
        global loop
        print("Executing {}".format(command))

        if(command.startswith('play')):
            command = command[4:]
            print("Playing: {}".format(command))
            asyncio.run_coroutine_threadsafe(self.music.play(self.voice_ctx, command), loop)
        
        if(command.startswith('stop')):
            asyncio.run_coroutine_threadsafe(self._stop_voice_command(), loop)
        
        if(command.startswith('skip')):
            asyncio.run_coroutine_threadsafe(self.music.skip(self.voice_ctx), loop)
        
        if(command.startswith('help')):
            asyncio.run_coroutine_threadsafe(self._help_voice_command(), loop)

        if(command.startswith('clear')):
             asyncio.run_coroutine_threadsafe(self.music.clear(self.voice_ctx), loop)
             
        if(command.startswith('EE1')):
            print("suit")
            asyncio.run_coroutine_threadsafe(self.music.play(self.voice_ctx, "https://www.youtube.com/watch?v=x2qRDMHbXaM"), loop)
        
        
    #==============================================
    #Internal Use Functions
    #==============================================

    async def _stop_voice_command(self):
        await self.music.stop(self.voice_ctx)
        await self.voice_ctx.voice_client.disconnect()

        # try:
        #     self.voice_ctx.voice_client.stop_listening()
        #     self.voice_ctx = None
        # except:
        #     pass
    
    async def _help_voice_command(self):
        await self.voice_ctx.send(help_command)
        



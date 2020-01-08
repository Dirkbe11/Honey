import asyncio
import discord
from discord.ext import commands, tasks

from .sound.music import *
from .voice.voice_sink import *
print("Importing audiocontroller")

# loop = asyncio.get_event_loop()

class AudioController(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.music = Music(bot)
        self.voice_sink = VoiceSink(self.execute_verbal_command)
        self.voice_ctx = None
        self.voice_recognition_activated = False
        self.async_event_loop = asyncio.get_event_loop()

    #==============================================
    #text-Command Functions
    #==============================================
    @commands.command()
    async def voice_toggle(self, ctx, toggle_state):
        #changes if we're listening in the voice channel or not
         self.voice_recognition_activated = toggle_state
         
    @commands.command()
    async def join(self, ctx):
        if ctx.author.voice:
            await ctx.author.voice.channel.connect()
            self.voice_ctx = ctx
            if self.voice_recognition_activated:
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
        print("play")
        await self.music.play(ctx, url)
    
    @commands.command()
    async def volume(self, ctx, volume: int):
        await self.music.volume(ctx, volume)
    
    @commands.command()
    async def skip(self, ctx):
        await self.music.skip(ctx)
        # loop.create_task(self.music.check_queue())

    @commands.command()
    async def stop(self, ctx):
        await self.music.stop(ctx)
        await ctx.voice_client.disconnect()

        try:
            self.voice_ctx.voice_client.stop_listening()
            self.voice_ctx = None
        except:
            pass

    #ensure_voice: Decorator for the 'play' command
    #If the command author is in a voice channel, then we join it
    @play.before_invoke
    async def ensure_voice(self, ctx):
        print("decorater")
        if ctx.voice_client is None:
            print("voice context is none")
            if ctx.author.voice:
                await ctx.author.voice.channel.connect()
                self.voice_ctx = ctx
                if self.voice_recognition_activated:
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
            print("Stopping!")
            asyncio.run_coroutine_threadsafe(self.stop(self.voice_ctx))
        

    #==============================================
    #Internal Use Functions
    #==============================================

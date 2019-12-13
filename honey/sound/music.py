import asyncio
import discord
from discord.ext import commands, tasks

from .yt import *
print("Importing music")

#****************************
#Music
#****************************
class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot 
        self.song_list = {}

    ##################
    #Join: Joins the voice channel
    @commands.command()
    async def join(self, ctx, *, channel: discord.VoiceChannel):
        if ctx.voice_client is not None:
            return await ctx.voice_client.move_to(channel)
        
        await channel.connect()

    ##################
    #check_queue: Continously plays songs until the music queue is empty
    async def check_queue(self, ctx):
        if self.song_list[ctx.voice_client.session_id] is not None:
            if self.song_list[ctx.voice_client.session_id] != []:
                player = self.song_list[ctx.voice_client.session_id].pop(0)
                ctx.voice_client.play(player, after=lambda _: asyncio.run_coroutine_threadsafe(self.check_queue(ctx), self.bot.loop))
                await ctx.send('Playing from queue: {}'.format(player.title))

    ##################
    #Stop: non-command function to queue songs. Used by 'play' and 'queue' commands.
    async def queue_song(self, ctx, url):
        player = await YTDLSource.from_url(url, loop=self.bot.loop, stream=True)
        if ctx.voice_client.session_id in self.song_list:
            if self.song_list[ctx.voice_client.session_id] == []:
                self.song_list[ctx.voice_client.session_id] = [player]
            else:
                self.song_list[ctx.voice_client.session_id].append(player)
        else:
            self.song_list[ctx.voice_client.session_id] = [player]
        
        await ctx.send('Queued: {}'.format(player.title))

    ##################
    #queue: Adds a given song to the song queue    
    @commands.command()
    async def queue(self, ctx, *, url):
        await self.queue_song(ctx, url)

    ##################
    #play: If no song is currently playing, plays the given song. If a song
    #is already playing, then it will queue the given song
    @commands.command()
    async def play(self, ctx, *, url):
        if ctx.voice_client.is_playing():
            await self.queue_song(ctx, url)
        else:
            async with ctx.typing():
                #TODO: Don't await YTDLSource.from_url? this is causing fast song adds to mess up
                #alternatively, add lock of some sort to the channel?
                player = await YTDLSource.from_url(url, loop=self.bot.loop, stream=True)
                ctx.voice_client.play(player, after=lambda _: asyncio.run_coroutine_threadsafe(self.check_queue(ctx), self.bot.loop))

            await ctx.send('Now playing: {}'.format(player.title))

    ##################
    #volume: Adjust the volume via chat message
    @commands.command()
    async def volume(self, ctx, volume: int):
        if ctx.voice_client is None:
            return await ctx.send("Not connected to a voice channel.")

        ctx.voice_client.source.volume = volume / 100
        await ctx.send("Changed volume to {}%".format(volume))

    ##################
    #Stop: Clears the song queue and disconnects from the voice channel
    @commands.command()
    async def stop(self, ctx):
        self.song_list.clear()
        await ctx.voice_client.disconnect()

    ##################
    #ensure_voice: Decorator for the 'play' command
    #If the command author is in a voice channel, then we join it
    @play.before_invoke
    async def ensure_voice(self, ctx):
        if ctx.voice_client is None:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect()
            else:
                await ctx.send("You are not connected to a voice channel.")
                raise commands.CommandError("Author not connected to a voice channel.")
                



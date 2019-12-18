import asyncio
import discord
from discord.ext import commands, tasks

from .yt import *
from .song_queue import *

print("Importing music")

class Music():
    def __init__(self, bot):
        self.bot = bot 
        self.song_lock = asyncio.Lock()
        self.song_queue = Queue(bot)


    #Join: Joins the voice channel
    async def join(self, ctx, channel: discord.VoiceChannel):
        if ctx.voice_client is not None:
            return await ctx.voice_client.move_to(channel)
        
        await channel.connect()


    #check_queue: Continously plays songs until the music queue is empty
    async def check_queue(self, ctx):
        player = await self.song_queue.next_song(ctx)
        if player is not None:
            ctx.voice_client.play(player, after=lambda _: asyncio.run_coroutine_threadsafe(self.check_queue(ctx), self.bot.loop))
            await ctx.send('Now Playing: {}'.format(player.title))


    #queue_song: non-command function to queue songs. Used by 'play' and 'queue' commands.
    async def queue_song(self, ctx, url):
        song_name = await self.song_queue.queue_song(ctx, url)
        await ctx.send('Queued: {}'.format(song_name))


    #clear: clears the song queue
    async def clear(self, ctx):
        await self.song_queue.clear(ctx)
        embed = discord.Embed(title='Song Queue', description='Song queue cleared.')
        await ctx.send(embed=embed)


    #show: Shows all the songs in the queue
    async def show(self, ctx):
        message = await self.song_queue.show(ctx)
        await ctx.send(embed=message)


    #queue: Adds a given song to the song queue    
    async def queue(self, ctx, url):
        await self.queue_song(ctx, url)


    #play: If no song is currently playing, plays the given song. If a song
    #is already playing, then it will queue the given song
    async def play(self, ctx, url):
        '''Possibly better to just insert in queue then run loop,
        rather than use a lock?'''
        with await self.song_lock:
            if ctx.voice_client.is_playing():
                await self.queue_song(ctx, url)
            else:
                async with ctx.typing():
                    player = await YTDLSource.from_url(url, loop=self.bot.loop, stream=True)
                    ctx.voice_client.play(player, after=lambda _: asyncio.run_coroutine_threadsafe(self.check_queue(ctx), self.bot.loop))

                await ctx.send('Now playing: {}'.format(player.title))


    #volume: Adjust the volume via chat message
    async def volume(self, ctx, volume: int):
        if ctx.voice_client is None:
            return await ctx.send("Not connected to a voice channel.")

        ctx.voice_client.source.volume = volume / 100
        await ctx.send("Changed volume to {}%".format(volume))


    #Stop: Clears the song queue 
    async def stop(self, ctx):
        await self.song_queue.clear(ctx)


                



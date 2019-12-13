import asyncio
import discord
from discord.ext import commands, tasks

from .yt import *
print("Importing music")

# song_list = asyncio.Queue()
# play_next_song = asyncio.Event()

class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot 
        self.song_list = {}

    @commands.command()
    async def join(self, ctx, *, channel: discord.VoiceChannel):
    #joins voice channel
        print("join...")
        if ctx.voice_client is not None:
            return await ctx.voice_client.move_to(channel)
        
        await channel.connect()

    async def check_queue(self, ctx):
        print("checking queue")
        #Continously play next song in queue
        if self.song_list[ctx.voice_client.session_id] is not None:
            print("found new song to play for this VC!")
            player = song_list[ctx.voice_client.session_id].pop(0)
            ctx.voice_client.play(player, after=lambda: self.check_queue(ctx))
            await ctx.send('Playing from queue: {}'.format(player.title))
        else:
            print("DIDN'T FIND SONG TO PLAY!")

    async def queue_song(self, ctx, url):
        print("queueing song...")
        player = await YTDLSource.from_url(url, loop=self.bot.loop, stream=True)
        print(ctx.voice_client.session_id)
        if ctx.voice_client.session_id in self.song_list:
            if self.song_list[ctx.voice_client.session_id] == []:
                self.song_list[ctx.voice_client.session_id] = [player]
            else:
                self.song_list[ctx.voice_client.session_id].append(player)

        else:
            self.song_list[ctx.voice_client.session_id] = [player]
        
        await ctx.send('Queued: {}'.format(player.title))

            
    @commands.command()
    async def queue(self, ctx, *, url):
        await self.queue_song(ctx, url)

    @commands.command()
    async def play(self, ctx, *, url):
        print("PLAY")
        """Streams from a url (same as yt, but doesn't predownload)"""
        if ctx.voice_client.is_playing():
            print("NEED TO QUEUE")
            await self.queue_song(ctx, url)
        else:
            print("CAN PLAY NOW!")
            async with ctx.typing():
                player = await YTDLSource.from_url(url, loop=self.bot.loop, stream=True)
                ctx.voice_client.play(player, after=lambda: self.check_queue(ctx))

            await ctx.send('Now playing: {}'.format(player.title))


    @commands.command()
    async def volume(self, ctx, volume: int):
        """Changes the player's volume"""

        if ctx.voice_client is None:
            return await ctx.send("Not connected to a voice channel.")

        ctx.voice_client.source.volume = volume / 100
        await ctx.send("Changed volume to {}%".format(volume))

    @commands.command()
    async def stop(self, ctx):
        """Stops and disconnects the bot from voice"""
        # probably want to clear the queue out, too
        await ctx.voice_client.disconnect()

    @play.before_invoke
    async def ensure_voice(self, ctx):
        if ctx.voice_client is None:
            print("context voice client exist...")
            if ctx.author.voice:
                print("joining authors voice channel")
                await ctx.author.voice.channel.connect()
            else:
                print("author is not in voice channel")
                await ctx.send("You are not connected to a voice channel.")
                raise commands.CommandError("Author not connected to a voice channel.")



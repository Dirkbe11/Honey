import asyncio
import discord

from .yt import *

class Queue():
    def __init__(self, bot):
            self.song_list = {}
            self.bot = bot

    #next_song: returns the next song in the queue
    async def next_song(self, ctx):
        if self.song_list[ctx.voice_client.session_id] is not None:
            if self.song_list[ctx.voice_client.session_id] != []:
                player = self.song_list[ctx.voice_client.session_id].pop(0)
                return player
            else:
                return None

    #queue_song: adds song to the queue
    async def queue_song(self, ctx, url):
        player = await YTDLSource.from_url(url, loop=self.bot.loop, stream=True)
        if ctx.voice_client.session_id in self.song_list:
            if self.song_list[ctx.voice_client.session_id] == []:
                self.song_list[ctx.voice_client.session_id] = [player]
            else:
                self.song_list[ctx.voice_client.session_id].append(player)
        else:
            self.song_list[ctx.voice_client.session_id] = [player]

        return player.title

    #clears all songs from the queue
    async def clear(self, ctx):
            if ctx.voice_client is not None and ctx.voice_client.session_id in self.song_list:
                if self.song_list[ctx.voice_client.session_id] is not None:
                    self.song_list[ctx.voice_client.session_id].clear()
            
    #shows all songs in the queue
    async def show(self, ctx):
        embed_string = ""
        if ctx.voice_client is not None and ctx.voice_client.session_id in self.song_list:
            if self.song_list[ctx.voice_client.session_id] is not None:
                for song in self.song_list[ctx.voice_client.session_id]:
                    if(len(embed_string) + len('\n') + len(song.title)) >= 1024:
                        break;
                    embed_string = embed_string + '\n' + '-' + song.title

        if embed_string == "":
            embed_string = "empty"

        embed = discord.Embed(title='Song Queue', description=embed_string)
        return embed


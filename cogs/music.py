import discord
from discord.ext import commands
from discord import app_commands
import yt_dlp
import asyncio
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import os
import translations

YTDL_OPTIONS = {
    'format': 'bestaudio/best',
    'extractaudio': True,
    'audioformat': 'mp3',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': False,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0',
}

FFMPEG_OPTIONS = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
    'options': '-vn'
}

ytdl = yt_dlp.YoutubeDL(YTDL_OPTIONS)

class MusicQueue:
    def __init__(self):
        self.queue = []
        self.current = None
        self.loop = False
    
    def add(self, song):
        self.queue.append(song)
    
    def next(self):
        if self.loop and self.current:
            return self.current
        if self.queue:
            self.current = self.queue.pop(0)
            return self.current
        return None
    
    def clear(self):
        self.queue.clear()
        self.current = None
    
    def is_empty(self):
        return len(self.queue) == 0

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)
        self.data = data
        self.title = data.get('title')
        self.url = data.get('url')
        self.duration = data.get('duration')
        self.thumbnail = data.get('thumbnail')
        self.webpage_url = data.get('webpage_url')
    
    @classmethod
    async def from_url(cls, url, *, loop=None, stream=True):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))
        
        if 'entries' in data:
            data = data['entries'][0]
        
        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **FFMPEG_OPTIONS), data=data)

class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.queues = {}
        
        spotify_id = os.getenv('SPOTIFY_CLIENT_ID')
        spotify_secret = os.getenv('SPOTIFY_CLIENT_SECRET')
        
        if spotify_id and spotify_secret:
            try:
                self.spotify = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
                    client_id=spotify_id,
                    client_secret=spotify_secret
                ))
            except:
                self.spotify = None
        else:
            self.spotify = None
    
    def get_queue(self, guild_id):
        if guild_id not in self.queues:
            self.queues[guild_id] = MusicQueue()
        return self.queues[guild_id]
    
    async def play_next(self, ctx):
        queue = self.get_queue(ctx.guild.id)
        
        if queue.is_empty():
            await asyncio.sleep(180)
            if ctx.voice_client and not ctx.voice_client.is_playing():
                await ctx.voice_client.disconnect()
            return
        
        next_song = queue.next()
        if next_song:
            player = await YTDLSource.from_url(next_song['url'], loop=self.bot.loop, stream=True)
            ctx.voice_client.play(player, after=lambda e: asyncio.run_coroutine_threadsafe(
                self.play_next(ctx), self.bot.loop))
    
    async def search_spotify(self, query):
        if not self.spotify:
            return None
        
        try:
            if 'open.spotify.com/track/' in query:
                track_id = query.split('track/')[-1].split('?')[0]
                track = self.spotify.track(track_id)
            elif 'open.spotify.com/playlist/' in query:
                return None
            else:
                results = self.spotify.search(q=query, type='track', limit=1)
                if not results['tracks']['items']:
                    return None
                track = results['tracks']['items'][0]
            
            search_query = f"{track['name']} {track['artists'][0]['name']}"
            return search_query
        except:
            return None
    
    @commands.command(name='play', aliases=['p'])
    async def play(self, ctx, *, query: str):
        guild_id = ctx.guild.id
        
        if not ctx.author.voice:
            embed = discord.Embed(
                title="❌ Not in Voice Channel",
                description="You need to be in a voice channel to play music!",
                color=0xFF006E
            )
            await ctx.send(embed=embed)
            return
        
        voice_channel = ctx.author.voice.channel
        
        if not ctx.voice_client:
            await voice_channel.connect()
        
        async with ctx.typing():
            if 'spotify.com' in query:
                spotify_query = await self.search_spotify(query)
                if spotify_query:
                    query = spotify_query
                else:
                    embed = discord.Embed(
                        title="❌ Spotify Error",
                        description="Couldn't fetch Spotify track. Make sure SPOTIFY_CLIENT_ID and SPOTIFY_CLIENT_SECRET are set.",
                        color=0xFF006E
                    )
                    await ctx.send(embed=embed)
                    return
            
            try:
                player = await YTDLSource.from_url(query, loop=self.bot.loop, stream=True)
            except Exception as e:
                embed = discord.Embed(
                    title="❌ Playback Error",
                    description=f"Couldn't play: {str(e)}",
                    color=0xFF006E
                )
                await ctx.send(embed=embed)
                return
            
            queue = self.get_queue(guild_id)
            
            if ctx.voice_client.is_playing() or ctx.voice_client.is_paused():
                queue.add({
                    'url': query,
                    'title': player.title,
                    'requester': ctx.author
                })
                embed = discord.Embed(
                    title="📝 Added to Queue",
                    description=f"**{player.title}**",
                    color=0x8B00FF
                )
                embed.add_field(name="Position", value=str(len(queue.queue)), inline=True)
                embed.add_field(name="Requested by", value=ctx.author.mention, inline=True)
                if player.thumbnail:
                    embed.set_thumbnail(url=player.thumbnail)
                await ctx.send(embed=embed)
            else:
                queue.current = {
                    'url': query,
                    'title': player.title,
                    'requester': ctx.author
                }
                ctx.voice_client.play(player, after=lambda e: asyncio.run_coroutine_threadsafe(
                    self.play_next(ctx), self.bot.loop))
                
                embed = discord.Embed(
                    title="🎵 Now Playing",
                    description=f"**{player.title}**",
                    color=0x00F3FF
                )
                embed.add_field(name="Requested by", value=ctx.author.mention, inline=True)
                if player.duration:
                    mins, secs = divmod(player.duration, 60)
                    embed.add_field(name="Duration", value=f"{int(mins)}:{int(secs):02d}", inline=True)
                if player.thumbnail:
                    embed.set_thumbnail(url=player.thumbnail)
                await ctx.send(embed=embed)
    
    @commands.command(name='pause')
    async def pause(self, ctx):
        if ctx.voice_client and ctx.voice_client.is_playing():
            ctx.voice_client.pause()
            embed = discord.Embed(
                title="⏸️ Paused",
                description="Music paused",
                color=0x8B00FF
            )
            await ctx.send(embed=embed)
        else:
            await ctx.send("❌ Nothing is playing!")
    
    @commands.command(name='resume')
    async def resume(self, ctx):
        if ctx.voice_client and ctx.voice_client.is_paused():
            ctx.voice_client.resume()
            embed = discord.Embed(
                title="▶️ Resumed",
                description="Music resumed",
                color=0x00F3FF
            )
            await ctx.send(embed=embed)
        else:
            await ctx.send("❌ Music is not paused!")
    
    @commands.command(name='skip', aliases=['next'])
    async def skip(self, ctx):
        if ctx.voice_client and ctx.voice_client.is_playing():
            ctx.voice_client.stop()
            embed = discord.Embed(
                title="⏭️ Skipped",
                description="Skipped to next song",
                color=0x00F3FF
            )
            await ctx.send(embed=embed)
        else:
            await ctx.send("❌ Nothing is playing!")
    
    @commands.command(name='stop', aliases=['leave', 'disconnect'])
    async def stop(self, ctx):
        if ctx.voice_client:
            queue = self.get_queue(ctx.guild.id)
            queue.clear()
            await ctx.voice_client.disconnect()
            embed = discord.Embed(
                title="⏹️ Stopped",
                description="Music stopped and disconnected",
                color=0xFF006E
            )
            await ctx.send(embed=embed)
        else:
            await ctx.send("❌ Bot is not in a voice channel!")
    
    @commands.command(name='queue', aliases=['q'])
    async def queue_command(self, ctx):
        queue = self.get_queue(ctx.guild.id)
        
        if not queue.current and queue.is_empty():
            await ctx.send("❌ Queue is empty!")
            return
        
        embed = discord.Embed(
            title="📜 Music Queue",
            color=0x8B00FF
        )
        
        if queue.current:
            embed.add_field(
                name="🎵 Now Playing",
                value=f"**{queue.current['title']}**\nRequested by: {queue.current['requester'].mention}",
                inline=False
            )
        
        if not queue.is_empty():
            queue_text = ""
            for i, song in enumerate(queue.queue[:10], 1):
                queue_text += f"`{i}.` **{song['title']}**\nRequested by: {song['requester'].mention}\n\n"
            
            if len(queue.queue) > 10:
                queue_text += f"...and {len(queue.queue) - 10} more songs"
            
            embed.add_field(
                name="📝 Up Next",
                value=queue_text,
                inline=False
            )
        
        embed.set_footer(text=f"Total songs in queue: {len(queue.queue)}")
        await ctx.send(embed=embed)
    
    @commands.command(name='nowplaying', aliases=['np', 'current'])
    async def nowplaying(self, ctx):
        queue = self.get_queue(ctx.guild.id)
        
        if not queue.current:
            await ctx.send("❌ Nothing is playing!")
            return
        
        embed = discord.Embed(
            title="🎵 Now Playing",
            description=f"**{queue.current['title']}**",
            color=0x00F3FF
        )
        embed.add_field(name="Requested by", value=queue.current['requester'].mention, inline=True)
        
        if ctx.voice_client:
            status = "▶️ Playing" if ctx.voice_client.is_playing() else "⏸️ Paused"
            embed.add_field(name="Status", value=status, inline=True)
        
        await ctx.send(embed=embed)
    
    @commands.command(name='loop')
    async def loop(self, ctx):
        queue = self.get_queue(ctx.guild.id)
        queue.loop = not queue.loop
        
        status = "enabled" if queue.loop else "disabled"
        emoji = "🔁" if queue.loop else "➡️"
        
        embed = discord.Embed(
            title=f"{emoji} Loop {status.capitalize()}",
            description=f"Loop mode has been {status}",
            color=0x8B00FF
        )
        await ctx.send(embed=embed)
    
    @commands.command(name='volume', aliases=['vol'])
    async def volume(self, ctx, volume: int):
        if not ctx.voice_client:
            await ctx.send("❌ Not in a voice channel!")
            return
        
        if 0 <= volume <= 100:
            ctx.voice_client.source.volume = volume / 100
            embed = discord.Embed(
                title="🔊 Volume Changed",
                description=f"Volume set to {volume}%",
                color=0x00F3FF
            )
            await ctx.send(embed=embed)
        else:
            await ctx.send("❌ Volume must be between 0 and 100!")

async def setup(bot):
    await bot.add_cog(Music(bot))

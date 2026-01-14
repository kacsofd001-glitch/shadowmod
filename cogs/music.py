import discord
from discord.ext import commands
import wavelink
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import os
import re
import asyncio


class Music(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

        spotify_id = os.getenv('SPOTIFY_CLIENT_ID')
        spotify_secret = os.getenv('SPOTIFY_CLIENT_SECRET')

        if spotify_id and spotify_secret:
            try:
                self.spotify = spotipy.Spotify(
                    auth_manager=SpotifyClientCredentials(
                        client_id=spotify_id, client_secret=spotify_secret))
            except:
                self.spotify = None
        else:
            self.spotify = None

    async def cog_load(self):
        """Connect to Lavalink nodes when cog loads"""
        nodes = [
            wavelink.Node(uri='lavalinkv4.serenetia.com:443',
                          password='https://dsc.gg/ajidevserver'),
            wavelink.Node(uri='http://lava.link:80',
                          password='youshallnotpass'),
            wavelink.Node(uri='http://lavalink.divahost.net:60002',
                          password='divahostv4')
        ]

        try:
            await asyncio.wait_for(wavelink.Pool.connect(client=self.bot,
                                                         nodes=nodes),
                                   timeout=15.0)
            print(f"✅ Connected to Lavalink pool with {len(nodes)} nodes")
        except asyncio.TimeoutError:
            print("⚠️ Lavalink connection timed out")
            print("⚠️ Music features will be unavailable")
        except Exception as e:
            print(f"⚠️ Failed to connect to Lavalink nodes: {e}")
            print("⚠️ Music features will be unavailable")

    @commands.Cog.listener()
    async def on_wavelink_track_end(self,
                                    payload: wavelink.TrackEndEventPayload):
        """Auto-play next track when current track finishes naturally"""
        player = payload.player
        if not player:
            return

        if payload.reason is not wavelink.TrackEndReason.FINISHED:
            return

        if player.current:
            return

        if player.queue:
            next_track = await player.queue.get_wait()
            await player.play(next_track)

    def parse_spotify_url(self, url):
        """Extract Spotify track ID from URL"""
        spotify_regex = r'https?://open\.spotify\.com/track/([a-zA-Z0-9]+)'
        match = re.search(spotify_regex, url)
        return match.group(1) if match else None

    async def search_spotify_track(self, track_id):
        """Get track info from Spotify and search on YouTube"""
        if not self.spotify:
            return None

        try:
            track = self.spotify.track(track_id)
            artists = ', '.join(
                [artist['name'] for artist in track['artists']])
            query = f"{artists} - {track['name']}"
            return query
        except:
            return None

    @commands.command(name='play')
    async def play(self, ctx, *, query: str):
        """Play music from YouTube, Spotify, or search query"""
        if not ctx.author.voice:
            embed = discord.Embed(
                title="❌ Not in Voice Channel",
                description="You need to be in a voice channel to play music!",
                color=0xFF006E)
            await ctx.send(embed=embed)
            return

        voice_channel = ctx.author.voice.channel

        if not ctx.voice_client:
            try:
                vc: wavelink.Player = await voice_channel.connect(
                    cls=wavelink.Player)
            except Exception as e:
                embed = discord.Embed(
                    title="❌ Connection Error",
                    description=f"Failed to connect: {str(e)}",
                    color=0xFF006E)
                await ctx.send(embed=embed)
                return
        else:
            vc: wavelink.Player = ctx.voice_client

        spotify_id = self.parse_spotify_url(query)
        if spotify_id:
            spotify_query = await self.search_spotify_track(spotify_id)
            if spotify_query:
                query = spotify_query

        try:
            tracks: wavelink.Search = await wavelink.Playable.search(query)
            if not tracks:
                embed = discord.Embed(
                    title="❌ No Results",
                    description="No tracks found matching your query.",
                    color=0xFF006E)
                await ctx.send(embed=embed)
                return

            track = tracks[0] if isinstance(tracks, list) else tracks

            if vc.playing:
                await vc.queue.put_wait(track)
                embed = discord.Embed(
                    title="➕ Added to Queue",
                    description=
                    f"**{track.title}**\n`Position: {vc.queue.count}`",
                    color=0x8B00FF)
                if hasattr(track, 'artwork') and track.artwork:
                    embed.set_thumbnail(url=track.artwork)
            else:
                await vc.play(track)
                embed = discord.Embed(
                    title="🎵 Now Playing",
                    description=f"**{track.title}**\n`{track.author}`",
                    color=0x00F3FF)
                if hasattr(track, 'artwork') and track.artwork:
                    embed.set_thumbnail(url=track.artwork)

            await ctx.send(embed=embed)

        except Exception as e:
            embed = discord.Embed(title="❌ Playback Error",
                                  description=f"An error occurred: {str(e)}",
                                  color=0xFF006E)
            await ctx.send(embed=embed)

    @commands.command(name='pause')
    async def pause(self, ctx):
        """Pause the current playback"""
        vc: wavelink.Player = ctx.voice_client

        if not vc or not vc.playing:
            embed = discord.Embed(
                title="❌ Nothing Playing",
                description="There's nothing playing right now.",
                color=0xFF006E)
            await ctx.send(embed=embed)
            return

        await vc.pause(True)
        embed = discord.Embed(title="⏸️ Paused",
                              description="Playback has been paused.",
                              color=0x8B00FF)
        await ctx.send(embed=embed)

    @commands.command(name='resume')
    async def resume(self, ctx):
        """Resume paused playback"""
        vc: wavelink.Player = ctx.voice_client

        if not vc or not vc.paused:
            embed = discord.Embed(
                title="❌ Nothing Paused",
                description="There's nothing paused right now.",
                color=0xFF006E)
            await ctx.send(embed=embed)
            return

        await vc.pause(False)
        embed = discord.Embed(title="▶️ Resumed",
                              description="Playback has been resumed.",
                              color=0x00F3FF)
        await ctx.send(embed=embed)

    @commands.command(name='skip')
    async def skip(self, ctx):
        """Skip to the next song"""
        vc: wavelink.Player = ctx.voice_client

        if not vc or not vc.playing:
            embed = discord.Embed(
                title="❌ Nothing Playing",
                description="There's nothing playing right now.",
                color=0xFF006E)
            await ctx.send(embed=embed)
            return

        await vc.skip(force=True)
        embed = discord.Embed(title="⏭️ Skipped",
                              description="Skipped to the next track.",
                              color=0x8B00FF)
        await ctx.send(embed=embed)

    @commands.command(name='stop')
    async def stop(self, ctx):
        """Stop playback and disconnect"""
        vc: wavelink.Player = ctx.voice_client

        if not vc:
            embed = discord.Embed(
                title="❌ Not Connected",
                description="I'm not connected to a voice channel.",
                color=0xFF006E)
            await ctx.send(embed=embed)
            return

        await vc.disconnect()
        embed = discord.Embed(title="⏹️ Stopped",
                              description="Playback stopped and disconnected.",
                              color=0xFF006E)
        await ctx.send(embed=embed)

    @commands.command(name='queue')
    async def queue(self, ctx):
        """Display the music queue"""
        vc: wavelink.Player = ctx.voice_client

        if not vc:
            embed = discord.Embed(
                title="❌ Not Connected",
                description="I'm not connected to a voice channel.",
                color=0xFF006E)
            await ctx.send(embed=embed)
            return

        embed = discord.Embed(title="🎵 Music Queue", color=0x8B00FF)

        if vc.current:
            embed.add_field(
                name="Now Playing",
                value=f"🎶 **{vc.current.title}**\n`{vc.current.author}`",
                inline=False)

        if vc.queue:
            queue_list = []
            for i, track in enumerate(vc.queue[:10], 1):
                queue_list.append(f"{i}. **{track.title}** - `{track.author}`")

            embed.add_field(name=f"Up Next ({vc.queue.count} songs)",
                            value="\n".join(queue_list),
                            inline=False)
        else:
            if not vc.current:
                embed.description = "Queue is empty"

        if vc.queue.mode == wavelink.QueueMode.loop:
            embed.set_footer(text="🔁 Loop: ON")

        await ctx.send(embed=embed)

    @commands.command(name='nowplaying', aliases=['np'])
    async def nowplaying(self, ctx):
        """Show currently playing track"""
        vc: wavelink.Player = ctx.voice_client

        if not vc or not vc.current:
            embed = discord.Embed(
                title="❌ Nothing Playing",
                description="There's nothing playing right now.",
                color=0xFF006E)
            await ctx.send(embed=embed)
            return

        track = vc.current

        position = vc.position
        duration = track.length

        progress_bar_length = 20
        progress = int((position / duration) * progress_bar_length)
        bar = "█" * progress + "░" * (progress_bar_length - progress)

        position_str = f"{int(position // 60)}:{int(position % 60):02d}"
        duration_str = f"{int(duration // 60)}:{int(duration % 60):02d}"

        embed = discord.Embed(
            title="🎵 Now Playing",
            description=f"**{track.title}**\n`{track.author}`",
            color=0x00F3FF)

        embed.add_field(name="Progress",
                        value=f"`{position_str}` {bar} `{duration_str}`",
                        inline=False)

        if hasattr(track, 'artwork') and track.artwork:
            embed.set_thumbnail(url=track.artwork)

        if vc.queue.mode == wavelink.QueueMode.loop:
            embed.set_footer(text="🔁 Loop: ON")

        await ctx.send(embed=embed)

    @commands.command(name='loop')
    async def loop(self, ctx):
        """Toggle loop mode"""
        vc: wavelink.Player = ctx.voice_client

        if not vc:
            embed = discord.Embed(
                title="❌ Not Connected",
                description="I'm not connected to a voice channel.",
                color=0xFF006E)
            await ctx.send(embed=embed)
            return

        if vc.queue.mode == wavelink.QueueMode.loop:
            vc.queue.mode = wavelink.QueueMode.normal
            status = "disabled"
            emoji = "➡️"
        else:
            vc.queue.mode = wavelink.QueueMode.loop
            status = "enabled"
            emoji = "🔁"

        embed = discord.Embed(title=f"{emoji} Loop Mode",
                              description=f"Loop mode has been **{status}**.",
                              color=0x8B00FF)
        await ctx.send(embed=embed)

    @commands.command(name='volume')
    async def volume(self, ctx, volume: int):
        """Adjust playback volume (0-100)"""
        vc: wavelink.Player = ctx.voice_client

        if not vc:
            embed = discord.Embed(
                title="❌ Not Connected",
                description="I'm not connected to a voice channel.",
                color=0xFF006E)
            await ctx.send(embed=embed)
            return

        if volume < 0 or volume > 100:
            embed = discord.Embed(
                title="❌ Invalid Volume",
                description="Volume must be between 0 and 100.",
                color=0xFF006E)
            await ctx.send(embed=embed)
            return

        await vc.set_volume(volume)
        embed = discord.Embed(title="🔊 Volume Adjusted",
                              description=f"Volume set to **{volume}%**",
                              color=0x00F3FF)
        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Music(bot))

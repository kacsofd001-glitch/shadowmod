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
        # Connect to reliable public Lavalink nodes in the background to avoid blocking bot startup
        self.bot.loop.create_task(self.connect_nodes())

    async def connect_nodes(self):
        """Internal method to handle node connection"""
        # Using a set of known stable public Lavalink nodes for 2026
        # These are commonly available public nodes that often have high uptime
        nodes = [
            wavelink.Node(uri='https://lavalink.lexis.host:443',
                          password='lexis.host'),
            wavelink.Node(uri='https://lava-v3.ajieblogs.eu.org:443',
                          password='youshallnotpass'),
            wavelink.Node(uri='https://lavalink.panther-hosting.com:443',
                          password='youshallnotpass'),
            wavelink.Node(uri='https://lavalink.moe:443',
                          password='youshallnotpass'),
            wavelink.Node(uri='https://lava-v4.ajieblogs.eu.org:443',
                          password='youshallnotpass')
        ]

        try:
            # We use a smaller timeout and try to connect to the pool
            await wavelink.Pool.connect(client=self.bot, nodes=nodes)
            print(f"✅ Connected to Lavalink pool with {len(nodes)} nodes")
        except Exception as e:
            print(f"⚠️ Lavalink connection failed: {e}")
            print("⚠️ Music features will be unavailable until nodes are reachable")

    @commands.Cog.listener()
    async def on_wavelink_track_end(self,
                                    payload: wavelink.TrackEndEventPayload):
        """Auto-play next track when current track finishes naturally"""
        player = payload.player
        if not player:
            return

        # Handle queue progression if finished naturally
        if not player.current and player.queue:
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
            if not track:
                return None
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

        # Check if Lavalink is connected
        lavalink_available = False
        try:
            if hasattr(wavelink, 'Pool') and wavelink.Pool.nodes:
                for node in wavelink.Pool.nodes.values():
                    if node.status == wavelink.NodeStatus.CONNECTED:
                        lavalink_available = True
                        break
        except Exception:
            lavalink_available = False

        if lavalink_available:
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
                tracks = await wavelink.Playable.search(query)
                if not tracks:
                    embed = discord.Embed(
                        title="❌ No Results",
                        description="No tracks found matching your query.",
                        color=0xFF006E)
                    await ctx.send(embed=embed)
                    return

                # Handle if tracks is a playlist or list
                if isinstance(tracks, wavelink.Playlist):
                    track = tracks.tracks[0]
                elif isinstance(tracks, (list, tuple)):
                    track = tracks[0]
                else:
                    track = tracks

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
        else:
            # Fallback to discord.FFmpegPCMAudio if Lavalink is down
            await ctx.send("⚠️ Lavalink is currently unavailable. Using standard audio engine...")
            
            if not ctx.voice_client:
                vc = await voice_channel.connect()
            else:
                vc = ctx.voice_client

            try:
                # Use yt-dlp to get the direct stream URL
                cmd = ['yt-dlp', '--get-url', '--format', 'bestaudio', '--default-search', 'ytsearch', query]
                proc = await asyncio.create_subprocess_exec(
                    *cmd,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE
                )
                stdout, stderr = await proc.communicate()
                
                if proc.returncode != 0:
                    error_msg = stderr.decode().strip()
                    await ctx.send(f"❌ Failed to fetch audio: {error_msg[:100]}")
                    return

                url = stdout.decode().strip().split('\n')[0]
                
                FFMPEG_OPTIONS = {
                    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
                    'options': '-vn'
                }
                
                if vc.is_playing():
                    vc.stop()
                
                audio_source = discord.FFmpegPCMAudio(url, **FFMPEG_OPTIONS)
                vc.play(audio_source)
                
                embed = discord.Embed(
                    title="🎵 Now Playing (Standard Engine)",
                    description=f"**{query}**",
                    color=0x00F3FF)
                await ctx.send(embed=embed)

            except Exception as e:
                await ctx.send(f"❌ Standard playback error: {str(e)}")

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
        # Handle Lavalink skip
        if hasattr(ctx.voice_client, 'skip'):
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
        else:
            # Handle standard engine skip
            if ctx.voice_client and ctx.voice_client.is_playing():
                ctx.voice_client.stop()
                await ctx.send("⏭️ Skipped (Standard Engine)")
            else:
                await ctx.send("❌ Nothing playing to skip.")

    @commands.command(name='stop')
    async def stop(self, ctx):
        """Stop playback and disconnect"""
        if not ctx.voice_client:
            embed = discord.Embed(
                title="❌ Not Connected",
                description="I'm not connected to a voice channel.",
                color=0xFF006E)
            await ctx.send(embed=embed)
            return

        if hasattr(ctx.voice_client, 'disconnect'):
            await ctx.voice_client.disconnect()
        
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

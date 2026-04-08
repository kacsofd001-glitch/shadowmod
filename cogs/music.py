import discord
from discord.ext import commands
from discord import app_commands
import wavelink
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import os
import re
import asyncio


class MusicControlView(discord.ui.View):
    def __init__(self, bot, player: wavelink.Player):
        super().__init__(timeout=None)
        self.bot = bot
        self.player = player

    @discord.ui.button(label="⏯️", style=discord.ButtonStyle.primary)
    async def toggle_play(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not self.player: return
        if self.player.paused:
            await self.player.pause(False)
            await interaction.response.send_message("▶️ Resumed", ephemeral=True)
        else:
            await self.player.pause(True)
            await interaction.response.send_message("⏸️ Paused", ephemeral=True)

    @discord.ui.button(label="⏭️", style=discord.ButtonStyle.secondary)
    async def skip(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not self.player: return
        await self.player.skip(force=True)
        await interaction.response.send_message("⏭️ Skipped", ephemeral=True)

    @discord.ui.button(label="⏹️", style=discord.ButtonStyle.danger)
    async def stop_player(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not self.player: return
        await self.player.disconnect()
        await interaction.response.send_message("⏹️ Stopped", ephemeral=True)
        super().stop()

    @discord.ui.button(label="🔉", style=discord.ButtonStyle.secondary)
    async def vol_down(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not self.player: return
        vol = max(0, self.player.volume - 10)
        await self.player.set_volume(vol)
        await interaction.response.send_message(f"🔉 Volume: {vol}%", ephemeral=True)

    @discord.ui.button(label="🔊", style=discord.ButtonStyle.secondary)
    async def vol_up(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not self.player: return
        vol = min(100, self.player.volume + 10)
        await self.player.set_volume(vol)
        await interaction.response.send_message(f"🔊 Volume: {vol}%", ephemeral=True)

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
        print("🎵 Music cog loaded (Lavalink connection will be attempted in background)")
        # Don't block startup - connect in background with timeout
        self.bot.loop.create_task(self.connect_nodes_with_timeout())

    async def connect_nodes_with_timeout(self):
        """Internal method to handle node connection with timeout"""
        try:
            # Add a 5-second timeout to prevent hanging
            await asyncio.wait_for(self.connect_nodes(), timeout=5.0)
        except asyncio.TimeoutError:
            print("⚠️ Lavalink connection timeout (music features may be unavailable)")
        except Exception as e:
            print(f"⚠️ Lavalink connection failed: {e} (music features may be unavailable)")

    async def connect_nodes(self):
        """Internal method to handle node connection"""
        # We'll use a single reliable node or none to silence connection errors 
        # since we have a robust standard engine fallback.
        nodes = [
            wavelink.Node(uri='https://lava-v4.ajieblogs.eu.org:443',
                          password='youshallnotpass')
        ]

        try:
            # We try to connect silently in the background
            await wavelink.Pool.connect(client=self.bot, nodes=nodes)
        except Exception:
            # Silently fail as fallback is already implemented in the play command
            pass

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
        """Extract Spotify track or playlist ID from URL"""
        track_regex = r'https?://open\.spotify\.com/track/([a-zA-Z0-9]+)'
        playlist_regex = r'https?://open\.spotify\.com/playlist/([a-zA-Z0-9]+)'
        
        track_match = re.search(track_regex, url)
        if track_match:
            return {'type': 'track', 'id': track_match.group(1)}
            
        playlist_match = re.search(playlist_regex, url)
        if playlist_match:
            return {'type': 'playlist', 'id': playlist_match.group(1)}
            
        return None

    async def get_spotify_playlist(self, playlist_id):
        """Get all tracks from a Spotify playlist"""
        if not self.spotify:
            return []
            
        try:
            results = self.spotify.playlist_tracks(playlist_id)
            tracks = results['items']
            while results['next']:
                results = self.spotify.next(results)
                tracks.extend(results['items'])
            
            queries = []
            for item in tracks:
                track = item['track']
                if not track: continue
                artists = ', '.join([artist['name'] for artist in track['artists']])
                queries.append(f"{artists} - {track['name']}")
            return queries
        except:
            return []

    async def play(self, ctx, *, query: str):
        """Play music from YouTube, Spotify, or search query"""
        if not interaction.user.voice:
            embed = discord.Embed(
                title="❌ Not in Voice Channel",
                description="You need to be in a voice channel to play music!",
                color=0xFF006E)
            await interaction.response.send_message(embed=embed)
            return

        voice_channel = interaction.user.voice.channel

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
            if not self.bot.get_guild(interaction.guild.id).voice_client:
                try:
                    vc: wavelink.Player = await voice_channel.connect(cls=wavelink.Player)
                except Exception as e:
                    embed = discord.Embed(
                        title="❌ Connection Error",
                        description=f"Failed to connect: {str(e)}",
                        color=0xFF006E)
                    await interaction.response.send_message(embed=embed)
                    return
            else:
                vc: wavelink.Player = self.bot.get_guild(interaction.guild.id).voice_client

            spotify_info = self.parse_spotify_url(query)
            
            # Handle Spotify Playlists
            if spotify_info and spotify_info['type'] == 'playlist':
                await interaction.response.send_message("⌛ Processing Spotify playlist... This might take a moment.")
                queries = await self.get_spotify_playlist(spotify_info['id'])
                
                if not queries:
                    await interaction.response.send_message("❌ Failed to load Spotify playlist.")
                    return
                
                added_count = 0
                for q in queries:
                    try:
                        tracks = await wavelink.Playable.search(q)
                        if tracks:
                            track = tracks[0] if isinstance(tracks, list) else tracks
                            if vc.playing:
                                await vc.queue.put_wait(track)
                            else:
                                await vc.play(track)
                            added_count += 1
                    except:
                        continue
                
                embed = discord.Embed(
                    title="✅ Playlist Added",
                    description=f"Added **{added_count}** tracks from the Spotify playlist to the queue.",
                    color=0x1DB954)
                await interaction.response.send_message(embed=embed)
                return

            # Handle Spotify Tracks
            if spotify_info and spotify_info['type'] == 'track':
                spotify_query = await self.search_spotify_track(spotify_info['id'])
                if spotify_query:
                    query = spotify_query

            try:
                tracks = await wavelink.Playable.search(query)
                if not tracks:
                    embed = discord.Embed(
                        title="❌ No Results",
                        description="No tracks found matching your query.",
                        color=0xFF006E)
                    await interaction.response.send_message(embed=embed)
                    return

                # Handle YouTube Playlists
                if isinstance(tracks, wavelink.Playlist):
                    added_count = 0
                    for track in tracks.tracks:
                        if vc.playing:
                            await vc.queue.put_wait(track)
                        else:
                            await vc.play(track)
                        added_count += 1
                    
                    embed = discord.Embed(
                        title="✅ YouTube Playlist Added",
                        description=f"Added **{added_count}** tracks from **{tracks.name}** to the queue.",
                        color=0x8B00FF)
                    await interaction.response.send_message(embed=embed)
                    return

                track = tracks[0] if isinstance(tracks, list) else tracks

                if vc.playing:
                    await vc.queue.put_wait(track)
                    embed = discord.Embed(
                        title="➕ Added to Queue",
                        description=f"**{track.title}**\n`Position: {vc.queue.count}`",
                        color=0x8B00FF)
                else:
                    await vc.play(track)
                    embed = discord.Embed(
                        title="🎵 Now Playing",
                        description=f"**{track.title}**\n`{track.author}`",
                        color=0x00F3FF)

                if hasattr(track, 'artwork') and track.artwork:
                    embed.set_thumbnail(url=track.artwork)
                
                view = MusicControlView(self.bot, vc)
                await interaction.response.send_message(embed=embed, view=view)

            except Exception as e:
                embed = discord.Embed(title="❌ Playback Error",
                                      description=f"An error occurred: {str(e)}",
                                      color=0xFF006E)
                await interaction.response.send_message(embed=embed)
        else:
            # Fallback engine doesn't easily support playlists via yt-dlp search without more complexity
            await interaction.response.send_message("⚠️ Lavalink is unavailable. Playlist support is limited in fallback mode.")
            # Original single-track fallback logic follows...        else:
            # Fallback to discord.FFmpegPCMAudio if Lavalink is down
            await interaction.response.send_message("⚠️ Lavalink is currently unavailable. Using standard audio engine...")
            
            if not self.bot.get_guild(interaction.guild.id).voice_client:
                vc = await voice_channel.connect()
            else:
                vc = self.bot.get_guild(interaction.guild.id).voice_client

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
                    await interaction.response.send_message(f"❌ Failed to fetch audio: {error_msg[:100]}")
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
                await interaction.response.send_message(embed=embed)

            except Exception as e:
                await interaction.response.send_message(f"❌ Standard playback error: {str(e)}")

    async def pause(self, ctx):
        """Pause the current playback"""
        vc: wavelink.Player = self.bot.get_guild(interaction.guild.id).voice_client

        if not vc or not vc.playing:
            embed = discord.Embed(
                title="❌ Nothing Playing",
                description="There's nothing playing right now.",
                color=0xFF006E)
            await interaction.response.send_message(embed=embed)
            return

        await vc.pause(True)
        embed = discord.Embed(title="⏸️ Paused",
                              description="Playback has been paused.",
                              color=0x8B00FF)
        await interaction.response.send_message(embed=embed)

    async def resume(self, ctx):
        """Resume paused playback"""
        vc: wavelink.Player = self.bot.get_guild(interaction.guild.id).voice_client

        if not vc or not vc.paused:
            embed = discord.Embed(
                title="❌ Nothing Paused",
                description="There's nothing paused right now.",
                color=0xFF006E)
            await interaction.response.send_message(embed=embed)
            return

        await vc.pause(False)
        embed = discord.Embed(title="▶️ Resumed",
                              description="Playback has been resumed.",
                              color=0x00F3FF)
        await interaction.response.send_message(embed=embed)

    async def skip(self, ctx):
        """Skip to the next song"""
        # Handle Lavalink skip
        if hasattr(self.bot.get_guild(interaction.guild.id).voice_client, 'skip'):
            vc: wavelink.Player = self.bot.get_guild(interaction.guild.id).voice_client
            if not vc or not vc.playing:
                embed = discord.Embed(
                    title="❌ Nothing Playing",
                    description="There's nothing playing right now.",
                    color=0xFF006E)
                await interaction.response.send_message(embed=embed)
                return

            await vc.skip(force=True)
            embed = discord.Embed(title="⏭️ Skipped",
                                  description="Skipped to the next track.",
                                  color=0x8B00FF)
            await interaction.response.send_message(embed=embed)
        else:
            # Handle standard engine skip
            if self.bot.get_guild(interaction.guild.id).voice_client and self.bot.get_guild(interaction.guild.id).voice_client.is_playing():
                self.bot.get_guild(interaction.guild.id).voice_client.stop()
                await interaction.response.send_message("⏭️ Skipped (Standard Engine)")
            else:
                await interaction.response.send_message("❌ Nothing playing to skip.")

    async def stop(self, ctx):
        """Stop playback and disconnect"""
        if not self.bot.get_guild(interaction.guild.id).voice_client:
            embed = discord.Embed(
                title="❌ Not Connected",
                description="I'm not connected to a voice channel.",
                color=0xFF006E)
            await interaction.response.send_message(embed=embed)
            return

        if hasattr(self.bot.get_guild(interaction.guild.id).voice_client, 'disconnect'):
            await self.bot.get_guild(interaction.guild.id).voice_client.disconnect()
        
        embed = discord.Embed(title="⏹️ Stopped",
                              description="Playback stopped and disconnected.",
                              color=0xFF006E)
        await interaction.response.send_message(embed=embed)

    async def queue(self, ctx):
        """Display the music queue"""
        vc: wavelink.Player = self.bot.get_guild(interaction.guild.id).voice_client

        if not vc:
            embed = discord.Embed(
                title="❌ Not Connected",
                description="I'm not connected to a voice channel.",
                color=0xFF006E)
            await interaction.response.send_message(embed=embed)
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

        await interaction.response.send_message(embed=embed)

    async def nowplaying(self, ctx):
        """Show currently playing track"""
        vc: wavelink.Player = self.bot.get_guild(interaction.guild.id).voice_client

        if not vc or not vc.current:
            embed = discord.Embed(
                title="❌ Nothing Playing",
                description="There's nothing playing right now.",
                color=0xFF006E)
            await interaction.response.send_message(embed=embed)
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

        await interaction.response.send_message(embed=embed)

    async def loop(self, ctx):
        """Toggle loop mode"""
        vc: wavelink.Player = self.bot.get_guild(interaction.guild.id).voice_client

        if not vc:
            embed = discord.Embed(
                title="❌ Not Connected",
                description="I'm not connected to a voice channel.",
                color=0xFF006E)
            await interaction.response.send_message(embed=embed)
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
        await interaction.response.send_message(embed=embed)

    async def volume(self, ctx, volume: int):
        """Adjust playback volume (0-100)"""
        vc: wavelink.Player = self.bot.get_guild(interaction.guild.id).voice_client

        if not vc:
            embed = discord.Embed(
                title="❌ Not Connected",
                description="I'm not connected to a voice channel.",
                color=0xFF006E)
            await interaction.response.send_message(embed=embed)
            return

        if volume < 0 or volume > 100:
            embed = discord.Embed(
                title="❌ Invalid Volume",
                description="Volume must be between 0 and 100.",
                color=0xFF006E)
            await interaction.response.send_message(embed=embed)
            return

        await vc.set_volume(volume)
        embed = discord.Embed(title="🔊 Volume Adjusted",
                              description=f"Volume set to **{volume}%**",
                              color=0x00F3FF)
        await interaction.response.send_message(embed=embed)

    async def radio1(self, ctx):
        """Play Hungarian Rádió 1 (24/7) / Rádió 1 lejátszása (0-24)"""
        if not interaction.user.voice:
            await interaction.response.send_message("❌ You need to be in a voice channel! / Hangcsatornában kell lenned!")
            return

        voice_channel = interaction.user.voice.channel
        stream_url = "https://myradioonline.hu/radio1" # We'll use a direct stream search for wavelink
        
        # Lavalink connection check
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
            if not self.bot.get_guild(interaction.guild.id).voice_client:
                vc: wavelink.Player = await voice_channel.connect(cls=wavelink.Player)
            else:
                vc: wavelink.Player = self.bot.get_guild(interaction.guild.id).voice_client
            
            # Wavelink 3.x/4.x search for the stream
            try:
                # Use search query instead of direct URL for Lavalink nodes that might block direct stream decoding
                tracks = await wavelink.Playable.search("Rádió 1 Hungary Live")
                
                if not tracks:
                    # Fallback to direct stream URL as raw identifier
                    tracks = await wavelink.Playable.search("https://radio1.hu/stream/radio1.mp3")
                
                if not tracks:
                    raise Exception("No tracks found / Nem található adás")

                track = tracks[0] if isinstance(tracks, list) else tracks
                await vc.play(track)
                
                embed = discord.Embed(
                    title="📻 Rádió 1 - 0/24 Live",
                    description="Now broadcasting Hungarian Rádió 1! / Rádió 1 élő adás indítva!",
                    color=0xFFFF00
                )
                embed.set_thumbnail(url="https://radio1.hu/wp-content/themes/radio1/img/logo.png")
                await interaction.response.send_message(embed=embed, view=MusicControlView(self.bot, vc))
            except Exception as e:
                # If Lavalink fails, automatically trigger FFmpeg fallback
                await interaction.response.send_message(f"⚠️ Lavalink stream error. Switching to fallback engine... / Lavalink hiba. Átváltás tartalék motorra...")
                lavalink_available = False # Trigger the 'else' block
        
        if not lavalink_available:
            # Standard engine fallback (FFmpeg)
            if not self.bot.get_guild(interaction.guild.id).voice_client:
                try:
                    vc = await voice_channel.connect()
                except Exception as e:
                    await interaction.response.send_message(f"❌ Connection failed: {str(e)}")
                    return
            else:
                vc = self.bot.get_guild(interaction.guild.id).voice_client
            
            try:
                # Rádió 1 stream direct URL for FFmpeg
                url = "https://radio1.hu/stream/radio1.mp3"
                FFMPEG_OPTIONS = {
                    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
                    'options': '-vn'
                }
                
                if hasattr(vc, 'is_playing') and vc.is_playing():
                    vc.stop()
                
                audio_source = discord.FFmpegPCMAudio(url, **FFMPEG_OPTIONS)
                vc.play(audio_source)
                
                embed = discord.Embed(
                    title="📻 Rádió 1 - 0/24 Live (Standard Engine)",
                    description="Now broadcasting Hungarian Rádió 1! / Rádió 1 élő adás indítva!",
                    color=0xFFFF00)
                await interaction.response.send_message(embed=embed)
            except Exception as e:
                await interaction.response.send_message(f"❌ Standard radio error: {str(e)}")

async def setup(bot):
    await bot.add_cog(Music(bot))

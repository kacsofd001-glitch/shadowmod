import discord
from discord.ext import commands, tasks
from discord import app_commands
from datetime import datetime, timedelta, timezone
import config
import asyncio

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.check_temp_actions.start()
    
    def cog_unload(self):
        self.check_temp_actions.cancel()
    
    async def send_log(self, embed):
        cfg = config.load_config()
        log_channel_id = cfg.get('log_channel_id')
        
        if log_channel_id:
            log_channel = self.bot.get_channel(log_channel_id)
            if log_channel:
                await log_channel.send(embed=embed)
    
    @tasks.loop(minutes=1)
    async def check_temp_actions(self):
        cfg = config.load_config()
        current_time = datetime.now(timezone.utc).timestamp()
        
        temp_bans = cfg.get('temp_bans', {})
        for guild_id, bans in list(temp_bans.items()):
            guild = self.bot.get_guild(int(guild_id))
            if not guild:
                continue
            
            for user_id, unban_time in list(bans.items()):
                if current_time >= unban_time:
                    try:
                        user = await self.bot.fetch_user(int(user_id))
                        await guild.unban(user, reason="Temporary ban expired")
                        del temp_bans[guild_id][user_id]
                    except:
                        pass
        
        config.save_config(cfg)
    
    @check_temp_actions.before_loop
    async def before_check_temp_actions(self):
        await self.bot.wait_until_ready()
    
    @app_commands.command(name='ban', description='Ban a user from the server')
    @app_commands.checks.has_permissions(ban_members=True)
    async def ban_user(self, interaction: discord.Interaction, member: discord.Member, reason: str = "No reason provided"):
        from translations import get_text
        if member.top_role >= interaction.user.top_role:
            await interaction.response.send_message("❌ You cannot ban this user!")
            return
        
        embed = discord.Embed(
            title=get_text(interaction.guild.id, 'user_banned'),
            description=get_text(interaction.guild.id, 'user_banned_desc', member.mention),
            color=0xFF006E,
            timestamp=datetime.now(timezone.utc)
        )
        embed.add_field(name=get_text(interaction.guild.id, 'reason'), value=reason)
        embed.add_field(name=get_text(interaction.guild.id, 'moderator'), value=interaction.user.mention)
        
        await member.ban(reason=reason)
        await interaction.response.send_message(embed=embed)
        await self.send_log(embed)
    
    @app_commands.command(name='kick', description='Kick a user from the server')
    @app_commands.checks.has_permissions(kick_members=True)
    async def kick_user(self, interaction: discord.Interaction, member: discord.Member, reason: str = "No reason provided"):
        from translations import get_text
        if member.top_role >= interaction.user.top_role:
            await interaction.response.send_message("❌ You cannot kick this user!")
            return
        
        embed = discord.Embed(
            title=get_text(interaction.guild.id, 'user_kicked'),
            description=get_text(interaction.guild.id, 'user_kicked_desc', member.mention),
            color=0xFF006E,
            timestamp=datetime.now(timezone.utc)
        )
        embed.add_field(name=get_text(interaction.guild.id, 'reason'), value=reason)
        embed.add_field(name=get_text(interaction.guild.id, 'moderator'), value=interaction.user.mention)
        
        await member.kick(reason=reason)
        await interaction.response.send_message(embed=embed)
        await self.send_log(embed)
    
    @app_commands.command(name='mute', description='Mute a user')
    @app_commands.checks.has_permissions(moderate_members=True)
    async def mute_user(self, interaction: discord.Interaction, member: discord.Member):
        from translations import get_text
        cfg = config.load_config()
        muted_roles = cfg.get('muted_roles', {})
        muted_role_id = muted_roles.get(str(interaction.guild.id))
        
        if not muted_role_id:
            muted_role = await interaction.guild.create_role(name="Muted", color=discord.Color(0x0066FF))
            
            for channel in interaction.guild.channels:
                await channel.set_permissions(muted_role, send_messages=False, speak=False)
            
            if 'muted_roles' not in cfg:
                cfg['muted_roles'] = {}
            cfg['muted_roles'][str(interaction.guild.id)] = muted_role.id
            config.save_config(cfg)
        else:
            muted_role = interaction.guild.get_role(int(muted_role_id))
            if not muted_role:
                await interaction.response.send_message("❌ Muted role not found! Creating new one...")
                muted_role = await interaction.guild.create_role(name="Muted", color=discord.Color(0x0066FF))
                for channel in interaction.guild.channels:
                    await channel.set_permissions(muted_role, send_messages=False, speak=False)
                cfg['muted_roles'][str(interaction.guild.id)] = muted_role.id
                config.save_config(cfg)
        
        await member.add_roles(muted_role)
        
        embed = discord.Embed(
            title=get_text(interaction.guild.id, 'user_muted'),
            description=get_text(interaction.guild.id, 'user_muted_desc', member.mention),
            color=0x0066FF,
            timestamp=datetime.now(timezone.utc)
        )
        embed.add_field(name=get_text(interaction.guild.id, 'moderator'), value=interaction.user.mention)
        
        await interaction.response.send_message(embed=embed)
        await self.send_log(embed)
    
    @app_commands.command(name='unmute', description='Unmute a user')
    @app_commands.checks.has_permissions(moderate_members=True)
    async def unmute_user(self, interaction: discord.Interaction, member: discord.Member):
        from translations import get_text
        cfg = config.load_config()
        muted_roles = cfg.get('muted_roles', {})
        muted_role_id = muted_roles.get(str(interaction.guild.id))
        
        if not muted_role_id:
            await interaction.response.send_message(get_text(interaction.guild.id, 'no_muted_role'))
            return
        
        muted_role = interaction.guild.get_role(int(muted_role_id))
        if not muted_role:
            await interaction.response.send_message(get_text(interaction.guild.id, 'no_muted_role'))
            return
        
        if muted_role in member.roles:
            await member.remove_roles(muted_role)
            
            embed = discord.Embed(
                title=get_text(interaction.guild.id, 'user_unmuted'),
                description=get_text(interaction.guild.id, 'user_unmuted_desc', member.mention),
                color=0x00F3FF,
                timestamp=datetime.now(timezone.utc)
            )
            embed.add_field(name=get_text(interaction.guild.id, 'moderator'), value=interaction.user.mention)
            
            await interaction.response.send_message(embed=embed)
            await self.send_log(embed)
        else:
            await interaction.response.send_message(get_text(interaction.guild.id, 'user_not_muted'))
    
    @app_commands.command(name='tempmute', description='Temporarily mute a user')
    @app_commands.checks.has_permissions(moderate_members=True)
    async def temp_mute(self, interaction: discord.Interaction, member: discord.Member, duration: str):
        time_units = {'s': 1, 'm': 60, 'h': 3600, 'd': 86400}
        
        try:
            time_amount = int(duration[:-1])
            time_unit = duration[-1]
        except:
            await interaction.response.send_message("❌ Invalid time format! Use: 10s, 5m, 2h, 1d")
            return
        
        if time_unit not in time_units:
            await interaction.response.send_message("❌ Invalid time format! Use: 10s, 5m, 2h, 1d")
            return
        
        seconds = time_amount * time_units[time_unit]
        
        if seconds > 2419200:
            await interaction.response.send_message("❌ Maximum timeout duration is 28 days!")
            return
        
        if seconds < 1:
            await interaction.response.send_message("❌ Timeout duration must be at least 1 second!")
            return
        
        timeout_until = datetime.now(timezone.utc) + timedelta(seconds=seconds)
        
        try:
            await member.timeout(timeout_until, reason=f"Timed out by {interaction.user}")
            
            embed = discord.Embed(
                title="⏱️ User Timed Out",
                description=f"**User:** {member.mention}\n**Duration:** {duration}\n**Moderator:** {interaction.user.mention}",
                color=0x0066FF,
                timestamp=datetime.now(timezone.utc)
            )
            embed.add_field(name="Timeout Until", value=f"<t:{int(timeout_until.timestamp())}:F>", inline=False)
            
            await interaction.response.send_message(embed=embed)
            await self.send_log(embed)
        except discord.Forbidden:
            await interaction.response.send_message("❌ I don't have permission to timeout this user!")
        except discord.HTTPException as e:
            await interaction.response.send_message(f"❌ Failed to timeout user: {str(e)}")
    
    @app_commands.command(name='tempban', description='Temporarily ban a user')
    @app_commands.checks.has_permissions(ban_members=True)
    async def temp_ban(self, interaction: discord.Interaction, member: discord.Member, duration: str, reason: str = "No reason provided"):
        time_units = {'s': 1, 'm': 60, 'h': 3600, 'd': 86400}
        time_amount = int(duration[:-1])
        time_unit = duration[-1]
        
        if time_unit not in time_units:
            await interaction.response.send_message("❌ Invalid time format! Use: 10s, 5m, 2h, 1d")
            return
        
        seconds = time_amount * time_units[time_unit]
        unban_time = datetime.now(timezone.utc).timestamp() + seconds
        
        await member.ban(reason=reason)
        
        cfg = config.load_config()
        if 'temp_bans' not in cfg:
            cfg['temp_bans'] = {}
        if str(interaction.guild.id) not in cfg['temp_bans']:
            cfg['temp_bans'][str(interaction.guild.id)] = {}
        cfg['temp_bans'][str(interaction.guild.id)][str(member.id)] = unban_time
        config.save_config(cfg)
        
        embed = discord.Embed(
            title="🔨 User Temporarily Banned",
            description=f"**User:** {member.mention}\n**Duration:** {duration}\n**Reason:** {reason}\n**Moderator:** {interaction.user.mention}",
            color=0xFF006E,
            timestamp=datetime.now(timezone.utc)
        )
        
        await interaction.response.send_message(embed=embed)
        await self.send_log(embed)
    
    @app_commands.command(name='lock', description='Lock the current channel')
    @app_commands.checks.has_permissions(manage_channels=True)
    async def lock_channel(self, interaction: discord.Interaction):
        await interaction.channel.set_permissions(interaction.guild.default_role, send_messages=False)
        
        embed = discord.Embed(
            title="🔒 Channel Locked",
            description=f"This channel has been locked by {interaction.user.mention}",
            color=0xFF006E
        )
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name='unlock', description='Unlock the current channel')
    @app_commands.checks.has_permissions(manage_channels=True)
    async def unlock_channel(self, interaction: discord.Interaction):
        await interaction.channel.set_permissions(interaction.guild.default_role, send_messages=True)
        
        embed = discord.Embed(
            title="🔓 Channel Unlocked",
            description=f"This channel has been unlocked by {interaction.user.mention}",
            color=0x00F3FF
        )
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name='warn', description='Warn a user')
    @app_commands.checks.has_permissions(moderate_members=True)
    async def warn_user(self, interaction: discord.Interaction, member: discord.Member, reason: str = "No reason provided"):
        cfg = config.load_config()
        if 'warnings' not in cfg:
            cfg['warnings'] = {}
        
        user_id = str(member.id)
        if user_id not in cfg['warnings']:
            cfg['warnings'][user_id] = []
        
        warning = {
            'reason': reason,
            'moderator': str(interaction.user.id),
            'timestamp': datetime.now(timezone.utc).isoformat()
        }
        cfg['warnings'][user_id].append(warning)
        config.save_config(cfg)
        
        embed = discord.Embed(
            title="⚠️ User Warned",
            description=f"**User:** {member.mention}\n**Reason:** {reason}\n**Moderator:** {interaction.user.mention}\n**Total Warnings:** {len(cfg['warnings'][user_id])}",
            color=discord.Color.gold(),
            timestamp=datetime.now(timezone.utc)
        )
        
        await interaction.response.send_message(embed=embed)
        await self.send_log(embed)
    
    @app_commands.command(name='warnings', description='Check warnings for a user')
    @app_commands.checks.has_permissions(moderate_members=True)
    async def check_warnings(self, interaction: discord.Interaction, member: discord.Member):
        cfg = config.load_config()
        user_id = str(member.id)
        
        if 'warnings' not in cfg or user_id not in cfg['warnings']:
            await interaction.response.send_message(f"✅ {member.mention} has no warnings!")
            return
        
        warnings = cfg['warnings'][user_id]
        
        embed = discord.Embed(
            title=f"⚠️ Warnings for {member}",
            description=f"Total warnings: {len(warnings)}",
            color=discord.Color.gold()
        )
        
        for i, warn in enumerate(warnings[-5:], 1):
            moderator = interaction.guild.get_member(int(warn['moderator']))
            mod_name = moderator.mention if moderator else "Unknown"
            embed.add_field(
                name=f"Warning #{i}",
                value=f"**Reason:** {warn['reason']}\n**By:** {mod_name}\n**Date:** {warn['timestamp'][:10]}",
                inline=False
            )
        
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name='purge', description='Delete messages from the channel')
    @app_commands.checks.has_permissions(manage_messages=True)
    async def purge_messages(self, interaction: discord.Interaction, amount: int):
        from translations import get_text
        
        if amount < 1 or amount > 100:
            await interaction.response.send_message(get_text(interaction.guild.id, 'purge_invalid'))
            return
        
        try:
            deleted = await interaction.channel.purge(limit=amount + 1)
            
            embed = discord.Embed(
                title=get_text(interaction.guild.id, 'messages_purged'),
                description=get_text(interaction.guild.id, 'messages_purged_desc', len(deleted) - 1),
                color=0xFF006E,
                timestamp=datetime.now(timezone.utc)
            )
            embed.add_field(name=get_text(interaction.guild.id, 'moderator'), value=interaction.user.mention)
            
            msg = await interaction.response.send_message(embed=embed)
            await asyncio.sleep(5)
            await msg.delete()
            
            await self.send_log(embed)
            
        except discord.Forbidden:
            await interaction.response.send_message("❌ I don't have permission to delete messages!")
        except Exception as e:
            await interaction.response.send_message(f"❌ An error occurred: {str(e)}")

async def setup(bot):
    await bot.add_cog(Moderation(bot))

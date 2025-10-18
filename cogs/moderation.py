import discord
from discord.ext import commands, tasks
from datetime import datetime, timedelta
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
        current_time = datetime.utcnow().timestamp()
        
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
        
        temp_mutes = cfg.get('temp_mutes', {})
        for guild_id, mutes in list(temp_mutes.items()):
            guild = self.bot.get_guild(int(guild_id))
            if not guild:
                continue
            
            muted_role_id = cfg.get('muted_role_id')
            if not muted_role_id:
                continue
            
            muted_role = guild.get_role(muted_role_id)
            if not muted_role:
                continue
            
            for user_id, unmute_time in list(mutes.items()):
                if current_time >= unmute_time:
                    try:
                        member = guild.get_member(int(user_id))
                        if member:
                            await member.remove_roles(muted_role, reason="Temporary mute expired")
                        del temp_mutes[guild_id][user_id]
                    except:
                        pass
        
        config.save_config(cfg)
    
    @check_temp_actions.before_loop
    async def before_check_temp_actions(self):
        await self.bot.wait_until_ready()
    
    @commands.command(name='ban')
    @commands.has_permissions(ban_members=True)
    async def ban_user(self, ctx, member: discord.Member, *, reason="No reason provided"):
        if member.top_role >= ctx.author.top_role:
            await ctx.send("❌ You cannot ban this user!")
            return
        
        embed = discord.Embed(
            title="🔨 User Banned",
            description=f"**User:** {member.mention}\n**Reason:** {reason}\n**Moderator:** {ctx.author.mention}",
            color=discord.Color.red(),
            timestamp=datetime.utcnow()
        )
        
        await member.ban(reason=reason)
        await ctx.send(embed=embed)
        await self.send_log(embed)
    
    @commands.command(name='kick')
    @commands.has_permissions(kick_members=True)
    async def kick_user(self, ctx, member: discord.Member, *, reason="No reason provided"):
        if member.top_role >= ctx.author.top_role:
            await ctx.send("❌ You cannot kick this user!")
            return
        
        embed = discord.Embed(
            title="👢 User Kicked",
            description=f"**User:** {member.mention}\n**Reason:** {reason}\n**Moderator:** {ctx.author.mention}",
            color=discord.Color.orange(),
            timestamp=datetime.utcnow()
        )
        
        await member.kick(reason=reason)
        await ctx.send(embed=embed)
        await self.send_log(embed)
    
    @commands.command(name='mute')
    @commands.has_permissions(moderate_members=True)
    async def mute_user(self, ctx, member: discord.Member):
        cfg = config.load_config()
        muted_role_id = cfg.get('muted_role_id')
        
        if not muted_role_id:
            muted_role = await ctx.guild.create_role(name="Muted", color=discord.Color.dark_gray())
            
            for channel in ctx.guild.channels:
                await channel.set_permissions(muted_role, send_messages=False, speak=False)
            
            config.update_config('muted_role_id', muted_role.id)
        else:
            muted_role = ctx.guild.get_role(muted_role_id)
        
        await member.add_roles(muted_role)
        
        embed = discord.Embed(
            title="🔇 User Muted",
            description=f"**User:** {member.mention}\n**Moderator:** {ctx.author.mention}",
            color=discord.Color.dark_gray(),
            timestamp=datetime.utcnow()
        )
        
        await ctx.send(embed=embed)
        await self.send_log(embed)
    
    @commands.command(name='unmute')
    @commands.has_permissions(moderate_members=True)
    async def unmute_user(self, ctx, member: discord.Member):
        cfg = config.load_config()
        muted_role_id = cfg.get('muted_role_id')
        
        if not muted_role_id:
            await ctx.send("❌ No muted role found!")
            return
        
        muted_role = ctx.guild.get_role(muted_role_id)
        if muted_role in member.roles:
            await member.remove_roles(muted_role)
            
            embed = discord.Embed(
                title="🔊 User Unmuted",
                description=f"**User:** {member.mention}\n**Moderator:** {ctx.author.mention}",
                color=discord.Color.green(),
                timestamp=datetime.utcnow()
            )
            
            await ctx.send(embed=embed)
            await self.send_log(embed)
        else:
            await ctx.send("❌ User is not muted!")
    
    @commands.command(name='tempmute')
    @commands.has_permissions(moderate_members=True)
    async def temp_mute(self, ctx, member: discord.Member, duration: str):
        cfg = config.load_config()
        muted_role_id = cfg.get('muted_role_id')
        
        if not muted_role_id:
            muted_role = await ctx.guild.create_role(name="Muted", color=discord.Color.dark_gray())
            for channel in ctx.guild.channels:
                await channel.set_permissions(muted_role, send_messages=False, speak=False)
            config.update_config('muted_role_id', muted_role.id)
        else:
            muted_role = ctx.guild.get_role(muted_role_id)
        
        time_units = {'s': 1, 'm': 60, 'h': 3600, 'd': 86400}
        time_amount = int(duration[:-1])
        time_unit = duration[-1]
        
        if time_unit not in time_units:
            await ctx.send("❌ Invalid time format! Use: 10s, 5m, 2h, 1d")
            return
        
        seconds = time_amount * time_units[time_unit]
        unmute_time = datetime.utcnow().timestamp() + seconds
        
        await member.add_roles(muted_role)
        
        if 'temp_mutes' not in cfg:
            cfg['temp_mutes'] = {}
        if str(ctx.guild.id) not in cfg['temp_mutes']:
            cfg['temp_mutes'][str(ctx.guild.id)] = {}
        cfg['temp_mutes'][str(ctx.guild.id)][str(member.id)] = unmute_time
        config.save_config(cfg)
        
        embed = discord.Embed(
            title="🔇 User Temporarily Muted",
            description=f"**User:** {member.mention}\n**Duration:** {duration}\n**Moderator:** {ctx.author.mention}",
            color=discord.Color.dark_gray(),
            timestamp=datetime.utcnow()
        )
        
        await ctx.send(embed=embed)
        await self.send_log(embed)
    
    @commands.command(name='tempban')
    @commands.has_permissions(ban_members=True)
    async def temp_ban(self, ctx, member: discord.Member, duration: str, *, reason="No reason provided"):
        time_units = {'s': 1, 'm': 60, 'h': 3600, 'd': 86400}
        time_amount = int(duration[:-1])
        time_unit = duration[-1]
        
        if time_unit not in time_units:
            await ctx.send("❌ Invalid time format! Use: 10s, 5m, 2h, 1d")
            return
        
        seconds = time_amount * time_units[time_unit]
        unban_time = datetime.utcnow().timestamp() + seconds
        
        await member.ban(reason=reason)
        
        cfg = config.load_config()
        if 'temp_bans' not in cfg:
            cfg['temp_bans'] = {}
        if str(ctx.guild.id) not in cfg['temp_bans']:
            cfg['temp_bans'][str(ctx.guild.id)] = {}
        cfg['temp_bans'][str(ctx.guild.id)][str(member.id)] = unban_time
        config.save_config(cfg)
        
        embed = discord.Embed(
            title="🔨 User Temporarily Banned",
            description=f"**User:** {member.mention}\n**Duration:** {duration}\n**Reason:** {reason}\n**Moderator:** {ctx.author.mention}",
            color=discord.Color.red(),
            timestamp=datetime.utcnow()
        )
        
        await ctx.send(embed=embed)
        await self.send_log(embed)
    
    @commands.command(name='lock')
    @commands.has_permissions(manage_channels=True)
    async def lock_channel(self, ctx):
        await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=False)
        
        embed = discord.Embed(
            title="🔒 Channel Locked",
            description=f"This channel has been locked by {ctx.author.mention}",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)
    
    @commands.command(name='unlock')
    @commands.has_permissions(manage_channels=True)
    async def unlock_channel(self, ctx):
        await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=True)
        
        embed = discord.Embed(
            title="🔓 Channel Unlocked",
            description=f"This channel has been unlocked by {ctx.author.mention}",
            color=discord.Color.green()
        )
        await ctx.send(embed=embed)
    
    @commands.command(name='warn')
    @commands.has_permissions(moderate_members=True)
    async def warn_user(self, ctx, member: discord.Member, *, reason="No reason provided"):
        cfg = config.load_config()
        if 'warnings' not in cfg:
            cfg['warnings'] = {}
        
        user_id = str(member.id)
        if user_id not in cfg['warnings']:
            cfg['warnings'][user_id] = []
        
        warning = {
            'reason': reason,
            'moderator': str(ctx.author.id),
            'timestamp': datetime.utcnow().isoformat()
        }
        cfg['warnings'][user_id].append(warning)
        config.save_config(cfg)
        
        embed = discord.Embed(
            title="⚠️ User Warned",
            description=f"**User:** {member.mention}\n**Reason:** {reason}\n**Moderator:** {ctx.author.mention}\n**Total Warnings:** {len(cfg['warnings'][user_id])}",
            color=discord.Color.gold(),
            timestamp=datetime.utcnow()
        )
        
        await ctx.send(embed=embed)
        await self.send_log(embed)
    
    @commands.command(name='warnings')
    @commands.has_permissions(moderate_members=True)
    async def check_warnings(self, ctx, member: discord.Member):
        cfg = config.load_config()
        user_id = str(member.id)
        
        if 'warnings' not in cfg or user_id not in cfg['warnings']:
            await ctx.send(f"✅ {member.mention} has no warnings!")
            return
        
        warnings = cfg['warnings'][user_id]
        
        embed = discord.Embed(
            title=f"⚠️ Warnings for {member}",
            description=f"Total warnings: {len(warnings)}",
            color=discord.Color.gold()
        )
        
        for i, warn in enumerate(warnings[-5:], 1):
            moderator = ctx.guild.get_member(int(warn['moderator']))
            mod_name = moderator.mention if moderator else "Unknown"
            embed.add_field(
                name=f"Warning #{i}",
                value=f"**Reason:** {warn['reason']}\n**By:** {mod_name}\n**Date:** {warn['timestamp'][:10]}",
                inline=False
            )
        
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Moderation(bot))

import discord
from discord.ext import commands
from datetime import datetime
import config

class Logging(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    async def send_log(self, embed):
        cfg = config.load_config()
        log_channel_id = cfg.get('log_channel_id')
        
        if log_channel_id:
            log_channel = self.bot.get_channel(log_channel_id)
            if log_channel:
                await log_channel.send(embed=embed)
    
    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if message.author.bot:
            return
        
        embed = discord.Embed(
            title="🗑️ Message Deleted",
            description=f"**Author:** {message.author.mention}\n**Channel:** {message.channel.mention}",
            color=discord.Color.red(),
            timestamp=datetime.utcnow()
        )
        embed.add_field(
            name="Content",
            value=message.content[:1024] if message.content else "*No content*",
            inline=False
        )
        embed.set_footer(text=f"User ID: {message.author.id}")
        
        await self.send_log(embed)
    
    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if before.author.bot or before.content == after.content:
            return
        
        embed = discord.Embed(
            title="📝 Message Edited",
            description=f"**Author:** {before.author.mention}\n**Channel:** {before.channel.mention}",
            color=discord.Color.orange(),
            timestamp=datetime.utcnow()
        )
        embed.add_field(
            name="Before",
            value=before.content[:512] if before.content else "*No content*",
            inline=False
        )
        embed.add_field(
            name="After",
            value=after.content[:512] if after.content else "*No content*",
            inline=False
        )
        embed.set_footer(text=f"User ID: {before.author.id}")
        
        await self.send_log(embed)
    
    @commands.Cog.listener()
    async def on_member_join(self, member):
        embed = discord.Embed(
            title="📥 Member Joined",
            description=f"**User:** {member.mention} ({member})",
            color=discord.Color.green(),
            timestamp=datetime.utcnow()
        )
        embed.add_field(
            name="Account Created",
            value=f"{member.created_at.strftime('%Y-%m-%d')}",
            inline=True
        )
        embed.set_thumbnail(url=member.display_avatar.url)
        embed.set_footer(text=f"User ID: {member.id} | Total Members: {member.guild.member_count}")
        
        await self.send_log(embed)
    
    @commands.Cog.listener()
    async def on_member_remove(self, member):
        embed = discord.Embed(
            title="📤 Member Left",
            description=f"**User:** {member.mention} ({member})",
            color=discord.Color.red(),
            timestamp=datetime.utcnow()
        )
        embed.set_thumbnail(url=member.display_avatar.url)
        embed.set_footer(text=f"User ID: {member.id} | Total Members: {member.guild.member_count}")
        
        await self.send_log(embed)
    
    @commands.Cog.listener()
    async def on_member_ban(self, guild, user):
        embed = discord.Embed(
            title="🔨 Member Banned",
            description=f"**User:** {user.mention} ({user})",
            color=discord.Color.dark_red(),
            timestamp=datetime.utcnow()
        )
        embed.set_thumbnail(url=user.display_avatar.url)
        embed.set_footer(text=f"User ID: {user.id}")
        
        await self.send_log(embed)
    
    @commands.command(name='setlog')
    @commands.has_permissions(administrator=True)
    async def set_log_channel(self, ctx, channel: discord.TextChannel):
        config.update_config('log_channel_id', channel.id)
        
        embed = discord.Embed(
            title="✅ Log Channel Set",
            description=f"Log channel has been set to {channel.mention}",
            color=discord.Color.green()
        )
        await ctx.send(embed=embed)
        
        welcome_embed = discord.Embed(
            title="📋 Logging System Activated",
            description="This channel will now receive all bot logs including:\n• Message deletions and edits\n• Member joins and leaves\n• Bans and kicks\n• Anti-alt detections\n• Moderation actions",
            color=discord.Color.blue()
        )
        await channel.send(embed=welcome_embed)

async def setup(bot):
    await bot.add_cog(Logging(bot))

import discord
from discord.ext import commands
from datetime import datetime, timedelta
import config

class AntiAlt(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_member_join(self, member):
        cfg = config.load_config()
        min_age_days = cfg.get('min_account_age_days', 7)
        log_channel_id = cfg.get('log_channel_id')
        
        account_age = datetime.utcnow() - member.created_at
        age_in_days = account_age.days
        
        if age_in_days < min_age_days:
            embed = discord.Embed(
                title="🚨 Possible Alt Account Detected",
                description=f"**User:** {member.mention} ({member})\n**ID:** {member.id}",
                color=discord.Color.red(),
                timestamp=datetime.utcnow()
            )
            embed.add_field(
                name="Account Created",
                value=f"{member.created_at.strftime('%Y-%m-%d %H:%M:%S')} UTC",
                inline=False
            )
            embed.add_field(
                name="Account Age",
                value=f"{age_in_days} days old",
                inline=True
            )
            embed.add_field(
                name="Required Age",
                value=f"{min_age_days} days",
                inline=True
            )
            embed.set_thumbnail(url=member.display_avatar.url)
            embed.set_footer(text=f"User ID: {member.id}")
            
            if log_channel_id:
                log_channel = self.bot.get_channel(log_channel_id)
                if log_channel:
                    await log_channel.send(embed=embed)
            
            try:
                welcome_embed = discord.Embed(
                    title="⚠️ Account Age Warning",
                    description=f"Your account is only {age_in_days} days old. Please be aware that you may have limited permissions until your account ages.",
                    color=discord.Color.orange()
                )
                await member.send(embed=welcome_embed)
            except:
                pass
    
    @commands.command(name='setaltage')
    @commands.has_permissions(administrator=True)
    async def set_alt_age(self, ctx, days: int):
        if days < 0:
            await ctx.send("❌ Days must be a positive number!")
            return
        
        config.update_config('min_account_age_days', days)
        
        embed = discord.Embed(
            title="✅ Anti-Alt Configuration Updated",
            description=f"Minimum account age set to **{days} days**",
            color=discord.Color.green()
        )
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(AntiAlt(bot))

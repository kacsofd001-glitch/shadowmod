import discord
from discord.ext import commands
import asyncio
import os
from dotenv import load_dotenv
from datetime import datetime, timezone
import json

load_dotenv()

intents = discord.Intents.all()

# Shared stats file for web server
STATS_FILE = 'bot_stats.json'

class DiscordBot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix='!',
            intents=intents,
            help_command=None
        )
        self.start_time = datetime.now(timezone.utc)
        
    async def setup_hook(self):
        await self.load_extension('cogs.tickets')
        await self.load_extension('cogs.antialt')
        await self.load_extension('cogs.logging')
        await self.load_extension('cogs.moderation')
        await self.load_extension('cogs.games')
        await self.load_extension('cogs.fun')
        await self.load_extension('cogs.polls')
        await self.load_extension('cogs.roles')
        await self.load_extension('cogs.giveaways')
        await self.load_extension('cogs.nameauto')
        await self.load_extension('cogs.webhook_logging')
        await self.load_extension('cogs.language')
        await self.load_extension('cogs.aichat')
        await self.load_extension('cogs.verify')
        await self.load_extension('cogs.info')
        await self.load_extension('cogs.slash_commands')
        print("All cogs loaded successfully!")
        
    async def on_ready(self):
        print(f'Bot is ready! Logged in as {self.user}')
        print(f'Bot ID: {self.user.id}')
        print('------')
        
        try:
            synced = await self.tree.sync()
            print(f'Synced {len(synced)} slash commands')
        except Exception as e:
            print(f'Failed to sync commands: {e}')
        
        await self.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType.watching,
                name="🌐 /help | Futuristic Bot"
            )
        )
        
        # Update stats file for web server
        self.update_stats_file()
    
    def update_stats_file(self):
        """Update bot stats for web server"""
        total_members = sum(guild.member_count for guild in self.guilds)
        total_channels = sum(len(guild.channels) for guild in self.guilds)
        
        stats = {
            'start_time': self.start_time.isoformat(),
            'guilds': len(self.guilds),
            'users': total_members,
            'channels': total_channels,
            'status': 'online'
        }
        
        try:
            with open(STATS_FILE, 'w') as f:
                json.dump(stats, f)
        except:
            pass

bot = DiscordBot()

@bot.command(name='help')
async def help_command(ctx):
    embed = discord.Embed(
        title="⚡ SHADOW-MOD ✨ | COMMAND DATABASE",
        description="━━━━━━━━━━━━━━━━━━━━━━━━━\n`Next-Gen Discord Moderation System`\n━━━━━━━━━━━━━━━━━━━━━━━━━",
        color=0x00F3FF  # Neon cyan
    )
    
    embed.add_field(
        name="📊 INFORMATION SYSTEMS",
        value="`/serverinfo` - Server statistics & details\n`/botinfo` - Bot features & uptime\n`/userinfo [@user]` - User profile with badges\n`/support` - Support server link\n`/webpage` - Live web dashboard",
        inline=False
    )
    
    embed.add_field(
        name="🔐 SECURITY & VERIFICATION",
        value="`/setupverify` - Deploy verification system\n`/setlog #channel` - Set log channel for alerts",
        inline=False
    )
    
    embed.add_field(
        name="🛡️ ANTI-ALT SYSTEM",
        value="`Auto-detects new accounts on join`\n`/setaltage <days>` - Set min account age (default: 7d)\nAlerts sent to log channel automatically",
        inline=False
    )
    
    embed.add_field(
        name="⚔️ MODERATION MATRIX",
        value="`/ban` `/kick` `/mute` `/unmute` - User management\n`/tempmute <user> <time>` - Discord timeout (max 28d)\n`/purge <1-100>` - Bulk message deletion\n`/warn` `/lock` `/unlock` - Warnings & channel control",
        inline=False
    )
    
    embed.add_field(
        name="🧠 AI NEURAL LINK",
        value="**@mention me** to activate AI assistant\n`Responds in EN/HU based on server language`",
        inline=False
    )
    
    embed.add_field(
        name="🎮 ENTERTAINMENT SYSTEMS",
        value="`/rps` Rock-Paper-Scissors • `/tictactoe` Tic-Tac-Toe\n`/meme` Generate memes • `/8ball` Magic 8-ball\n`/coinflip` Flip coin • `/dice` Roll dice",
        inline=False
    )
    
    embed.add_field(
        name="🎁 ENGAGEMENT PROTOCOLS",
        value="`/poll` Interactive polls • `/giveaway` Prize systems\n`/ticket` Support tickets • `/createrole` Role management",
        inline=False
    )
    
    embed.add_field(
        name="🏷️ NAME AUTOMATION",
        value="`/setprefix <@role> <prefix>` - Set role prefix\n`/removeprefix <@role>` - Remove role prefix\n`/viewprefixes` - View all prefixes",
        inline=False
    )
    
    embed.add_field(
        name="🌐 SYSTEM CONFIGURATION",
        value="`/setlang <en/hu>` - Language switch\n`/setwebhook <url>` - Logging system\n`/ping` - Latency check",
        inline=False
    )
    
    embed.add_field(
        name="🌐 WEB RESOURCES",
        value="[📖 Full Command List](https://shadowmod.net/help)\n[📊 Live Dashboard](https://shadowmod.net/dashboard)",
        inline=False
    )
    
    embed.set_footer(text="⚡ 28 Slash Commands | Active Developer Ready | v2.0 FUTURISTIC ⚡")
    embed.set_thumbnail(url=ctx.bot.user.display_avatar.url)
    
    await ctx.send(embed=embed)

@bot.command(name='ping')
async def ping_command(ctx):
    latency = round(bot.latency * 1000)
    
    # Determine latency color
    if latency < 100:
        color = 0x00F3FF  # Neon cyan - excellent
        status = "⚡ OPTIMAL"
    elif latency < 200:
        color = 0x8B00FF  # Neon purple - good
        status = "✅ STABLE"
    else:
        color = 0xFF006E  # Neon pink - slow
        status = "⚠️ DEGRADED"
    
    embed = discord.Embed(
        title=f"📡 SYSTEM RESPONSE | {status}",
        description=f"```ansi\n\u001b[1;36mLatency: {latency}ms\u001b[0m\n```",
        color=color
    )
    embed.add_field(name="Status", value=status, inline=True)
    embed.add_field(name="Response Time", value=f"{latency}ms", inline=True)
    embed.set_footer(text="⚡ Neural Network Active")
    
    await ctx.send(embed=embed)

if __name__ == '__main__':
    TOKEN = os.getenv('DISCORD_TOKEN')
    if not TOKEN:
        print("ERROR: DISCORD_TOKEN not found in environment variables!")
        print("Please set up your Discord bot token.")
    else:
        bot.run(TOKEN)

import discord
from discord.ext import commands
import asyncio
import os
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.all()

class DiscordBot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix='!',
            intents=intents,
            help_command=None
        )
        
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
                name="your server | !help or /help"
            )
        )

bot = DiscordBot()

@bot.command(name='help')
async def help_command(ctx):
    embed = discord.Embed(
        title="🤖 Bot Commands Help",
        description="Here are all available commands:",
        color=discord.Color.blue()
    )
    
    embed.add_field(
        name="🎫 Ticket System",
        value="`!ticket` or `/ticket` - Create a ticket panel",
        inline=False
    )
    
    embed.add_field(
        name="🛡️ Moderation",
        value="`!ban <user>` or `/ban` - Ban a user\n`!kick <user>` or `/kick` - Kick a user\n`!mute <user>` or `/mute` - Mute a user\n`!purge <amount>` or `/purge` - Delete messages (1-100)\n`!warn <user>` or `/warn` - Warn a user",
        inline=False
    )
    
    embed.add_field(
        name="🎮 Games",
        value="`!rps` - Play Rock Paper Scissors\n`!tictactoe <@user>` - Play Tic Tac Toe",
        inline=False
    )
    
    embed.add_field(
        name="😄 Fun",
        value="`!meme` or `/meme` - Generate a meme 🌍\n`!8ball <question>` or `/8ball` - Magic 8-ball\n`!coinflip` or `/coinflip` - Flip a coin\n`!ping` or `/ping` - Check bot latency",
        inline=False
    )
    
    embed.add_field(
        name="📊 Polls & Roles",
        value="`!poll <question> <opt1> <opt2>` - Create poll\n`!addrole <@user> <@role>` - Add role to user",
        inline=False
    )
    
    embed.add_field(
        name="🎉 Giveaways",
        value="`!giveaway <time> <winners> <prize>` - Start giveaway\n`!reroll <message_id>` - Reroll giveaway",
        inline=False
    )
    
    embed.add_field(
        name="🤖 AI Chat (Admin)",
        value="`/aichat <#channel> <en/hu> <on/off>` - Configure AI chat in a channel",
        inline=False
    )
    
    embed.add_field(
        name="⚙️ Configuration (Admin)",
        value="`!setlang <en/hu>` or `/setlang` - Change language\n`!setwebhook <url>` - Set webhook logging\n`!setprefix <@role> <prefix>` - Role name prefix",
        inline=False
    )
    
    embed.set_footer(text="Use / for slash commands to keep Active Developer Badge! 🌟")
    
    await ctx.send(embed=embed)

@bot.command(name='ping')
async def ping_command(ctx):
    latency = round(bot.latency * 1000)
    
    embed = discord.Embed(
        title="🏓 Pong!",
        description=f"Bot latency: **{latency}ms**",
        color=discord.Color.green()
    )
    
    await ctx.send(embed=embed)

if __name__ == '__main__':
    TOKEN = os.getenv('DISCORD_TOKEN')
    if not TOKEN:
        print("ERROR: DISCORD_TOKEN not found in environment variables!")
        print("Please set up your Discord bot token.")
    else:
        bot.run(TOKEN)

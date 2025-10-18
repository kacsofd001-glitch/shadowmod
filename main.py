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
        print("All cogs loaded successfully!")
        
    async def on_ready(self):
        print(f'Bot is ready! Logged in as {self.user}')
        print(f'Bot ID: {self.user.id}')
        print('------')
        await self.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType.watching,
                name="your server | !help"
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
        value="`!ticket` - Create a ticket panel\n`!closeticket` - Close a ticket",
        inline=False
    )
    
    embed.add_field(
        name="🛡️ Moderation",
        value="`!ban <user> [reason]` - Ban a user\n`!kick <user> [reason]` - Kick a user\n`!mute <user>` - Mute a user\n`!unmute <user>` - Unmute a user\n`!tempmute <user> <time>` - Temporarily mute\n`!tempban <user> <time>` - Temporarily ban\n`!lock` - Lock channel\n`!unlock` - Unlock channel\n`!warn <user> [reason]` - Warn a user\n`!warnings <user>` - Check warnings",
        inline=False
    )
    
    embed.add_field(
        name="🎮 Games",
        value="`!rps` - Play Rock Paper Scissors\n`!tictactoe <@user>` - Play Tic Tac Toe",
        inline=False
    )
    
    embed.add_field(
        name="😄 Fun",
        value="`!meme` - Generate a random meme\n`!sound` - Random sound response\n`!8ball <question>` - Magic 8-ball\n`!coinflip` - Flip a coin\n`!roll 2d6` - Roll dice",
        inline=False
    )
    
    embed.add_field(
        name="📊 Polls",
        value="`!poll <question> <option1> <option2>...` - Create poll\n`!quickpoll <question>` - Yes/No/Maybe poll",
        inline=False
    )
    
    embed.add_field(
        name="👥 Roles",
        value="`!addrole <@user> <@role>` - Add role to user\n`!removerole <@user> <@role>` - Remove role\n`!createrole <name> [color]` - Create role\n`!deleterole <@role>` - Delete role\n`!roles` - List all roles",
        inline=False
    )
    
    embed.add_field(
        name="🎉 Giveaways",
        value="`!giveaway <time> <winners> <prize>` - Start giveaway\n`!reroll <message_id>` - Reroll giveaway",
        inline=False
    )
    
    embed.add_field(
        name="📝 Name Automation",
        value="`!setprefix <@role> <prefix>` - Set role prefix\n`!removeprefix <@role>` - Remove prefix\n`!viewprefixes` - View all prefixes\n`!updateallnicks` - Update all nicknames",
        inline=False
    )
    
    embed.add_field(
        name="⚙️ Configuration",
        value="`!setlog <#channel>` - Set log channel\n`!setaltage <days>` - Set minimum account age",
        inline=False
    )
    
    embed.set_footer(text="Use buttons for interactive features!")
    
    await ctx.send(embed=embed)

if __name__ == '__main__':
    TOKEN = os.getenv('DISCORD_TOKEN')
    if not TOKEN:
        print("ERROR: DISCORD_TOKEN not found in environment variables!")
        print("Please set up your Discord bot token.")
    else:
        bot.run(TOKEN)

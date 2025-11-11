import discord
from discord.ext import commands

class InteractiveHelp(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    async def show_help(self, interaction):
        """Show interactive help menu"""
        embed = discord.Embed(
            title="⚡ SHADOW-MOD Help Menu ✨",
            description="The ultimate all-in-one Discord bot with 60+ features!",
            color=0x00F3FF
        )
        
        embed.set_thumbnail(url=self.bot.user.display_avatar.url)
        
        embed.add_field(
            name="📋 Categories",
            value=(
                "Click a button below to explore commands by category!\n\n"
                "🛡️ **Moderation** - Manage your server\n"
                "💰 **Economy** - Currency & shop system\n"
                "🎮 **Games** - Fun mini-games\n"
                "🎭 **Fun** - Entertainment commands\n"
                "⚙️ **Utility** - Helpful tools\n"
                "📊 **Stats** - Analytics & tracking"
            ),
            inline=False
        )
        
        embed.set_footer(text="SHADOW-MOD v4.0 | Use /setup for configuration wizard")
        
        view = HelpView(self.bot)
        await interaction.response.send_message(embed=embed, view=view)

class HelpView(discord.ui.View):
    def __init__(self, bot):
        super().__init__(timeout=180)
        self.bot = bot
    
    @discord.ui.button(label="🛡️ Moderation", style=discord.ButtonStyle.primary, emoji="🛡️")
    async def moderation_help(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(
            title="🛡️ Moderation Commands",
            description="Powerful moderation tools",
            color=0xFF0000
        )
        
        commands_list = (
            "`/ban <user> [reason]` - Ban a user\n"
            "`/kick <user> [reason]` - Kick a user\n"
            "`/mute <user> [duration]` - Mute a user\n"
            "`/tempban <user> <duration>` - Temporarily ban\n"
            "`/warn <user> <reason>` - Warn a user\n"
            "`/lock [channel]` - Lock a channel\n"
            "`/unlock [channel]` - Unlock a channel\n"
            "`/purge <amount>` - Delete messages\n"
            "`/slowmode <seconds>` - Set slowmode\n"
            "`/antiraid enable` - Enable anti-raid"
        )
        
        embed.add_field(name="Commands", value=commands_list, inline=False)
        await interaction.response.edit_message(embed=embed)
    
    @discord.ui.button(label="💰 Economy", style=discord.ButtonStyle.success, emoji="💰")
    async def economy_help(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(
            title="💰 Economy Commands",
            description="Virtual currency system",
            color=0xFFD700
        )
        
        commands_list = (
            "`/balance [user]` - Check balance\n"
            "`/daily` - Claim daily reward ($500)\n"
            "`/work` - Work for money ($50-200)\n"
            "`/give <user> <amount>` - Give money\n"
            "`/rob <user>` - Attempt to rob\n"
            "`/blackjack <bet>` - Play blackjack\n"
            "`/slots <bet>` - Spin the slots\n"
            "`/coinflip <bet> <choice>` - Flip a coin\n"
            "`/shop` - View the item shop\n"
            "`/buy <item>` - Purchase an item"
        )
        
        embed.add_field(name="Commands", value=commands_list, inline=False)
        await interaction.response.edit_message(embed=embed)
    
    @discord.ui.button(label="🎮 Games", style=discord.ButtonStyle.primary, emoji="🎮")
    async def games_help(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(
            title="🎮 Mini-Games",
            description="Fun games to play!",
            color=0xFF00FF
        )
        
        commands_list = (
            "`/trivia [category]` - Answer trivia\n"
            "`/scramble` - Unscramble words\n"
            "`/connectfour @user` - Play Connect Four\n"
            "`/rps <choice>` - Rock Paper Scissors\n"
            "`/8ball <question>` - Ask the magic 8-ball\n"
            "`/tictactoe @user` - Tic-Tac-Toe\n"
            "`/blackjack <bet>` - Card game\n"
            "`/slots <bet>` - Slot machine"
        )
        
        embed.add_field(name="Commands", value=commands_list, inline=False)
        await interaction.response.edit_message(embed=embed)
    
    @discord.ui.button(label="⚙️ Utility", style=discord.ButtonStyle.secondary, emoji="⚙️")
    async def utility_help(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(
            title="⚙️ Utility Commands",
            description="Helpful tools and features",
            color=0x00F3FF
        )
        
        commands_list = (
            "`/serverinfo` - Server information\n"
            "`/userinfo [user]` - User information\n"
            "`/avatar [user]` - Get user's avatar\n"
            "`/poll <question>` - Create a poll\n"
            "`/remind <time> <message>` - Set a reminder\n"
            "`/afk [reason]` - Set AFK status\n"
            "`/birthday <MM-DD>` - Set your birthday\n"
            "`/suggest <idea>` - Submit a suggestion\n"
            "`/translate <text>` - Translate text"
        )
        
        embed.add_field(name="Commands", value=commands_list, inline=False)
        await interaction.response.edit_message(embed=embed)
    
    @discord.ui.button(label="🏠 Back", style=discord.ButtonStyle.secondary, row=1)
    async def back_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(
            title="⚡ SHADOW-MOD Help Menu ✨",
            description="The ultimate all-in-one Discord bot with 60+ features!",
            color=0x00F3FF
        )
        
        embed.set_thumbnail(url=self.bot.user.display_avatar.url)
        
        embed.add_field(
            name="📋 Categories",
            value=(
                "Click a button below to explore commands by category!\n\n"
                "🛡️ **Moderation** - Manage your server\n"
                "💰 **Economy** - Currency & shop system\n"
                "🎮 **Games** - Fun mini-games\n"
                "🎭 **Fun** - Entertainment commands\n"
                "⚙️ **Utility** - Helpful tools\n"
                "📊 **Stats** - Analytics & tracking"
            ),
            inline=False
        )
        
        await interaction.response.edit_message(embed=embed)

async def setup(bot):
    await bot.add_cog(InteractiveHelp(bot))

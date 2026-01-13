import discord
from discord.ext import commands

class InteractiveHelp(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    async def show_help(self, interaction):
        """Show interactive help menu"""
        from translations import get_text
        guild_id = interaction.guild.id
        embed = discord.Embed(
            title=get_text(guild_id, 'help_title'),
            description=get_text(guild_id, 'help_description'),
            color=0x00F3FF
        )
        
        embed.set_thumbnail(url=self.bot.user.display_avatar.url)
        
        embed.add_field(
            name=get_text(guild_id, 'help_engagement'),
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
        
        embed.set_footer(text=get_text(guild_id, 'help_footer'))
        
        view = HelpView(self.bot, guild_id)
        await interaction.response.send_message(embed=embed, view=view)

class HelpView(discord.ui.View):
    def __init__(self, bot, guild_id):
        super().__init__(timeout=180)
        self.bot = bot
        self.guild_id = guild_id
    
    @discord.ui.button(label="🛡️ Moderation", style=discord.ButtonStyle.primary, emoji="🛡️")
    async def moderation_help(self, interaction: discord.Interaction, button: discord.ui.Button):
        from translations import get_text
        embed = discord.Embed(
            title=get_text(self.guild_id, 'help_moderation'),
            description=get_text(self.guild_id, 'help_moderation_desc'),
            color=0xFF0000
        )
        
        await interaction.response.edit_message(embed=embed)
    
    @discord.ui.button(label="💰 Economy", style=discord.ButtonStyle.success, emoji="💰")
    async def economy_help(self, interaction: discord.Interaction, button: discord.ui.Button):
        from translations import get_text
        embed = discord.Embed(
            title="💰 Economy Commands",
            description="Virtual currency system",
            color=0xFFD700
        )
        
        await interaction.response.edit_message(embed=embed)
    
    @discord.ui.button(label="🎮 Games", style=discord.ButtonStyle.primary, emoji="🎮")
    async def games_help(self, interaction: discord.Interaction, button: discord.ui.Button):
        from translations import get_text
        embed = discord.Embed(
            title=get_text(self.guild_id, 'help_games'),
            description=get_text(self.guild_id, 'help_games_desc'),
            color=0xFF00FF
        )
        
        await interaction.response.edit_message(embed=embed)
    
    @discord.ui.button(label="⚙️ Utility", style=discord.ButtonStyle.secondary, emoji="⚙️")
    async def utility_help(self, interaction: discord.Interaction, button: discord.ui.Button):
        from translations import get_text
        embed = discord.Embed(
            title=get_text(self.guild_id, 'help_config'),
            description=get_text(self.guild_id, 'help_config_desc'),
            color=0x00F3FF
        )
        
        await interaction.response.edit_message(embed=embed)
    
    @discord.ui.button(label="🏠 Back", style=discord.ButtonStyle.secondary, row=1)
    async def back_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        from translations import get_text
        embed = discord.Embed(
            title=get_text(self.guild_id, 'help_title'),
            description=get_text(self.guild_id, 'help_description'),
            color=0x00F3FF
        )
        
        embed.set_thumbnail(url=self.bot.user.display_avatar.url)
        
        await interaction.response.edit_message(embed=embed)

async def setup(bot):
    await bot.add_cog(InteractiveHelp(bot))

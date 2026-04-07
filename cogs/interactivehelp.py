import discord
from discord.ext import commands

class InteractiveHelp(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    async def show_help(self, interaction):
        """Show interactive help menu"""
        import translations
        from translations import get_text
        guild_id = interaction.guild.id
        lang = translations.get_guild_language(guild_id)
        
        embed = discord.Embed(
            title=get_text(guild_id, 'help_title', lang=lang),
            description=get_text(guild_id, 'help_description', lang=lang),
            color=0x00F3FF
        )
        
        embed.set_thumbnail(url=self.bot.user.display_avatar.url)
        
        embed.add_field(
            name=get_text(guild_id, 'help_engagement', lang=lang),
            value=(
                "Click a button below to explore commands by category!\n\n"
                "🛡️ **Moderation** - Manage your server\n"
                "💰 **Economy** - Currency & shop system\n"
                "🎮 **Games** - Fun mini-games\n"
                "🎭 **Fun** - Entertainment commands\n"
                "⚙️ **Utility** - Helpful tools\n"
                "📊 **Stats** - Analytics & tracking\n"
                "📬 **ModMail** - Support system"
            ) if lang == 'en' else (
                "Kattints az alábbi gombra a parancsok megtekintéséhez kategóriák szerint!\n\n"
                "🛡️ **Moderáció** - Szerver kezelése\n"
                "💰 **Gazdaság** - Pénzrendszer & bolt\n"
                "🎮 **Játékok** - Szórakoztató minijátékok\n"
                "🎭 **Szórakozás** - Szórakoztató parancsok\n"
                "⚙️ **Eszközök** - Hasznos eszközök\n"
                "📊 **Statisztika** - Analytics & nyomkövetés\n"
                "📬 **ModMail** - Támogatási rendszer"
            ),
            inline=False
        )
        
        embed.set_footer(text=get_text(guild_id, 'help_footer', lang=lang))
        
        view = HelpView(self.bot, guild_id)
        
        # Send everything in a single immediate response to avoid webhook timeouts
        await interaction.response.send_message(embed=embed, view=view)

class HelpView(discord.ui.View):
    def __init__(self, bot, guild_id):
        super().__init__(timeout=180)
        self.bot = bot
        self.guild_id = guild_id
    
    @discord.ui.button(label="🛡️ Moderation", style=discord.ButtonStyle.primary, emoji="🛡️")
    async def moderation_help(self, interaction: discord.Interaction, button: discord.ui.Button):
        import translations
        from translations import get_text
        lang = translations.get_guild_language(self.guild_id)
        
        mod_title_en = get_text(self.guild_id, 'help_moderation', lang='en')
        mod_title = get_text(self.guild_id, 'help_moderation', lang=lang)
        
        embed = discord.Embed(
            title=mod_title,
            description=(
                "`/ban` - Ban user\n"
                "`/kick` - Kick user\n"
                "`/mute` / `/unmute` - Mute/unmute user\n"
                "`/warn` - Warn user\n"
                "`/purge` - Delete messages\n"
                "`/tempmute` - Timeout user\n"
                "`/lock` / `/unlock` - Channel lock\n"
                "`/say` - Make bot send a message\n"
                "`/embedsay` - Make bot send an embed"
            ) if lang == 'en' else (
                "`/ban` - Felhasználó kitiltása\n"
                "`/kick` - Felhasználó kirúgása\n"
                "`/mute` / `/unmute` - Felhasználó némítása/visszahangosítása\n"
                "`/warn` - Felhasználó figyelmeztetése\n"
                "`/purge` - Üzenetek törlése\n"
                "`/tempmute` - Felhasználó időtúltöltése\n"
                "`/lock` / `/unlock` - Csatorna zárolása\n"
                "`/say` - Bot szöveg küldése\n"
                "`/embedsay` - Bot embed küldése"
            ),
            color=0xFF0000
        )
        await interaction.response.edit_message(embed=embed)
    
    @discord.ui.button(label="💰 Economy", style=discord.ButtonStyle.success, emoji="💰")
    async def economy_help(self, interaction: discord.Interaction, button: discord.ui.Button):
        import translations
        from translations import get_text
        lang = translations.get_guild_language(self.guild_id)
        embed = discord.Embed(
            title=get_text(self.guild_id, 'cat_economy', lang=lang),
            description=(
                "`/balance` - Check coins\n"
                "`/work` - Earn coins\n"
                "`/daily` - Daily reward\n"
                "`/shop` - View items\n"
                "`/buy` - Purchase item\n"
                "`/rob` - Attempt robbery\n"
                "`/pay` - Send money\n"
                "`/top` - Economy leaderboard\n"
                "`/inventory` - Show items"
            ) if lang == 'en' else (
                "`/balance` - Egyenleg ellenőrzése\n"
                "`/work` - Pénz keresése\n"
                "`/daily` - Napi jutalom\n"
                "`/shop` - Elérrhető tárgyak\n"
                "`/buy` - Tárgy vásárlása\n"
                "`/rob` - Rablási kísérlet\n"
                "`/pay` - Pénz küldése\n"
                "`/top` - Gazdasági rangsor\n"
                "`/inventory` - Tárolóedény"
            ),
            color=0xFFD700
        )
        await interaction.response.edit_message(embed=embed)
    
    @discord.ui.button(label="🎮 Games", style=discord.ButtonStyle.primary, emoji="🎮")
    async def games_help(self, interaction: discord.Interaction, button: discord.ui.Button):
        import translations
        from translations import get_text
        lang = translations.get_guild_language(self.guild_id)
        embed = discord.Embed(
            title=get_text(self.guild_id, 'help_games', lang=lang),
            description=(
                "`/rps` - Rock-Paper-Scissors\n"
                "`/tictactoe` - Tic-Tac-Toe\n"
                "`/dice` - Roll dice\n"
                "`/coinflip` - Flip coin\n"
                "`/trivia` - Fun trivia\n"
                "`/blackjack` - Casino game\n"
                "`/slots` - Slot machine\n"
                "`/connectfour` - Connect Four"
            ) if lang == 'en' else (
                "`/rps` - Kő-papír-olló\n"
                "`/tictactoe` - Amőba\n"
                "`/dice` - Kocka dobása\n"
                "`/coinflip` - Érmefeldobás\n"
                "`/trivia` - Érdekes trivia\n"
                "`/blackjack` - Kaszinó játék\n"
                "`/slots` - Nyerőgép\n"
                "`/connectfour` - Négy összeköt"
            ),
            color=0xFF00FF
        )
        await interaction.response.edit_message(embed=embed)
    
    @discord.ui.button(label="⚙️ Utility", style=discord.ButtonStyle.secondary, emoji="⚙️")
    async def utility_help(self, interaction: discord.Interaction, button: discord.ui.Button):
        import translations
        from translations import get_text
        lang = translations.get_guild_language(self.guild_id)
        embed = discord.Embed(
            title=get_text(self.guild_id, 'help_config', lang=lang),
            description=(
                "`/ping` - Latency check\n"
                "`/serverinfo` - Server stats\n"
                "`/botinfo` - Bot details\n"
                "`/userinfo` - User profile\n"
                "`/setlang` - Change language\n"
                "`/setprefix` - Role nickname prefix\n"
                "`/setlog` - Set log channel\n"
                "`/setwebhook` - Set logging webhook\n"
                "`/setupvoice` - Setup temp voice system\n"
                "`/voicename` - Rename your temp voice channel"
            ) if lang == 'en' else (
                "`/ping` - Késleltetés ellenőrzés\n"
                "`/serverinfo` - Szerver statisztikák\n"
                "`/botinfo` - Bot részletei\n"
                "`/userinfo` - Felhasználó profil\n"
                "`/setlang` - Nyelv módosítása\n"
                "`/setprefix` - Szerep becenév prefix\n"
                "`/setlog` - Naplócsatorna beállítása\n"
                "`/setwebhook` - Webhook beállítása\n"
                "`/setupvoice` - Temp hang rendszer\n"
                "`/voicename` - Temp hang csatorna átnevezése"
            ),
            color=0x00F3FF
        )
        await interaction.response.edit_message(embed=embed)

    @discord.ui.button(label="🎭 Fun", style=discord.ButtonStyle.secondary, emoji="🎭", row=1)
    async def fun_help(self, interaction: discord.Interaction, button: discord.ui.Button):
        import translations
        from translations import get_text
        lang = translations.get_guild_language(self.guild_id)
        embed = discord.Embed(
            title=get_text(self.guild_id, 'help_fun', lang=lang),
            description=get_text(self.guild_id, 'help_fun_desc', lang=lang),
            color=0xFF00FF
        )
        await interaction.response.edit_message(embed=embed)

    @discord.ui.button(label="📊 Stats", style=discord.ButtonStyle.secondary, emoji="📊", row=1)
    async def stats_help(self, interaction: discord.Interaction, button: discord.ui.Button):
        import translations
        from translations import get_text
        lang = translations.get_guild_language(self.guild_id)
        embed = discord.Embed(
            title=get_text(self.guild_id, 'help_stats', lang=lang),
            description=get_text(self.guild_id, 'help_stats_desc', lang=lang),
            color=0x00FF00
        )
        await interaction.response.edit_message(embed=embed)
    
    @discord.ui.button(label="📬 ModMail", style=discord.ButtonStyle.secondary, emoji="📬", row=2)
    async def modmail_help(self, interaction: discord.Interaction, button: discord.ui.Button):
        import translations
        from translations import get_text
        lang = translations.get_guild_language(self.guild_id)
        embed = discord.Embed(
            title=get_text(self.guild_id, 'help_modmail', lang=lang),
            description=get_text(self.guild_id, 'help_modmail_desc', lang=lang),
            color=0x00F3FF
        )
        await interaction.response.edit_message(embed=embed)
    
    @discord.ui.button(label="🏠 Back", style=discord.ButtonStyle.secondary, row=2)
    async def back_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        import translations
        from translations import get_text
        lang = translations.get_guild_language(self.guild_id)
        embed = discord.Embed(
            title=get_text(self.guild_id, 'help_title', lang=lang),
            description=get_text(self.guild_id, 'help_description', lang=lang),
            color=0x00F3FF
        )
        
        embed.set_thumbnail(url=self.bot.user.display_avatar.url)
        
        await interaction.response.edit_message(embed=embed)

async def setup(bot):
    await bot.add_cog(InteractiveHelp(bot))

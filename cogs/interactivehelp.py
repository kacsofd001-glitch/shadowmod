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
                "� **Music** - Music playback system\n"
                "🎭 **Fun** - Entertainment commands\n"
                "⚙️ **Utility** - Helpful tools\n"
                "📊 **Stats** - Analytics & tracking\n"
                "📬 **ModMail** - Support system"
            ) if lang == 'en' else (
                "Kattints az alábbi gombra a parancsok megtekintéséhez kategóriák szerint!\n\n"
                "🛡️ **Moderáció** - Szerver kezelése\n"
                "💰 **Gazdaság** - Pénzrendszer & bolt\n"
                "🎮 **Játékok** - Szórakoztató minijátékok\n"
                "🎵 **Zene** - Zenelejátszás rendszer\n"
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
                "`/warn` / `/warnings` - Warn user / Check warnings\n"
                "`/purge` - Delete messages\n"
                "`/tempmute` - Timeout user\n"
                "`/tempban` - Temporarily ban user\n"
                "`/lock` / `/unlock` - Channel lock\n"
                "`/ticket` / `/closeticket` - Create/close support ticket\n"
                "`/poll` / `/quickpoll` - Create a poll"
            ) if lang == 'en' else (
                "`/ban` - Felhasználó kitiltása\n"
                "`/kick` - Felhasználó kirúgása\n"
                "`/mute` / `/unmute` - Felhasználó némítása/visszahangosítása\n"
                "`/warn` / `/warnings` - Felhasználó figyelmeztetése / Figyelmeztetések megtekintése\n"
                "`/purge` - Üzenetek törlése\n"
                "`/tempmute` - Felhasználó időtúltöltése\n"
                "`/tempban` - Felhasználó ideiglenes kitiltása\n"
                "`/lock` / `/unlock` - Csatorna zárolása\n"
                "`/ticket` / `/closeticket` - Támogatási jegy létrehozása/lezárása\n"
                "`/poll` / `/quickpoll` - Szavazás létrehozása"
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
                "`/coinflip` - Flip coin\n"
                "`/roll` - Roll dice\n"
                "`/8ball` - Magic 8-ball\n"
                "`/connectfour` - Connect Four\n"
                "`/giveaway` - Start giveaway\n"
                "`/reroll` - Reroll giveaway"
            ) if lang == 'en' else (
                "`/rps` - Kő-papír-olló\n"
                "`/tictactoe` - Amőba\n"
                "`/coinflip` - Érmefeldobás\n"
                "`/roll` - Kocka dobása\n"
                "`/8ball` - Mágikus 8-as\n"
                "`/connectfour` - Négy összeköt\n"
                "`/giveaway` - Nyeremény rajzolás\n"
                "`/reroll` - Nyeremény újrahúzása"
            ),
            color=0xFF00FF
        )
        await interaction.response.edit_message(embed=embed)
    
    @discord.ui.button(label="🎵 Music", style=discord.ButtonStyle.primary, emoji="🎵", row=1)
    async def music_help(self, interaction: discord.Interaction, button: discord.ui.Button):
        import translations
        from translations import get_text
        lang = translations.get_guild_language(self.guild_id)
        embed = discord.Embed(
            title=get_text(self.guild_id, 'help_music', lang=lang) if 'help_music' in translations.get_text.__dict__ else ('🎵 Music' if lang == 'en' else '🎵 Zene'),
            description=(
                "`/play` - Play music\n"
                "`/pause` - Pause playback\n"
                "`/resume` - Resume playback\n"
                "`/skip` - Skip track\n"
                "`/stop` - Stop and disconnect\n"
                "`/queue` - View music queue\n"
                "`/nowplaying` - Current track info\n"
                "`/loop` - Toggle loop mode\n"
                "`/volume` - Adjust volume\n"
                "`/radio1` - Play live radio"
            ) if lang == 'en' else (
                "`/play` - Zene lejátszása\n"
                "`/pause` - Lejátszás szüneteltetése\n"
                "`/resume` - Lejátszás folytatása\n"
                "`/skip` - Dal kihagyása\n"
                "`/stop` - Leállítás és bontás\n"
                "`/queue` - Sorlista megtekintése\n"
                "`/nowplaying` - Jelenlegi dal info\n"
                "`/loop` - Hurok mód váltása\n"
                "`/volume` - Hangerő beállítása\n"
                "`/radio1` - Élő rádió lejátszása"
            ),
            color=0x8B00FF
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
                "`/serverinfo` - Server stats\n"
                "`/botinfo` - Bot details\n"
                "`/userinfo` - User profile\n"
                "`/support` - Support info\n"
                "`/webpage` - Bot dashboard\n"
                "`/setlang` - Change language\n"
                "`/setlog` - Set log channel\n"
                "`/setwebhook` - Set logging webhook\n"
                "`/testwebhook` - Test webhook\n"
                "`/loginfo` - Logging info\n"
                "`/createrole` - Create role\n"
                "`/deleterole` - Delete role\n"
                "`/addrole` - Add role to user\n"
                "`/removerole` - Remove role from user\n"
                "`/roleinfo` - Role information\n"
                "`/roles` - List server roles\n"
                "`/servers` - Bot server list\n"
                "`/createinvite` - Create invite\n"
                "`/setaltage` - Set alt account age\n"
                "`/setupverify` - Setup verify system\n"
                "`/setprefix` - Configure role prefix\n"
                "`/removeprefix` - Remove role prefix\n"
                "`/updateallnicks` - Update all nicknames\n"
                "`/viewprefixes` - View role prefixes"
            ) if lang == 'en' else (
                "`/serverinfo` - Szerver statisztikák\n"
                "`/botinfo` - Bot részletei\n"
                "`/userinfo` - Felhasználó profil\n"
                "`/support` - Támogatás info\n"
                "`/webpage` - Bot irányítópult\n"
                "`/setlang` - Nyelv módosítása\n"
                "`/setlog` - Naplócsatorna beállítása\n"
                "`/setwebhook` - Webhook beállítása\n"
                "`/testwebhook` - Webhook tesztelése\n"
                "`/loginfo` - Naplózás info\n"
                "`/createrole` - Szerep létrehozása\n"
                "`/deleterole` - Szerep törlése\n"
                "`/addrole` - Szerep hozzáadása\n"
                "`/removerole` - Szerep eltávolítása\n"
                "`/roleinfo` - Szerep információ\n"
                "`/roles` - Szerver szerepek\n"
                "`/servers` - Bot szerver lista\n"
                "`/createinvite` - Meghívó létrehozása\n"
                "`/setaltage` - Alt fiók kor beállítása\n"
                "`/setupverify` - Ellenőrzés rendszer\n"
                "`/setprefix` - Szerep prefix beállítása\n"
                "`/removeprefix` - Szerep prefix eltávolítása\n"
                "`/updateallnicks` - Összes becenév frissítése\n"
                "`/viewprefixes` - Szerep prefixek megtekintése"
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
            description=(
                "`/meme` - Send a random meme\n"
                "`/8ball` - Magic 8-ball\n"
                "`/coinflip` - Flip a coin\n"
                "`/roll` - Roll the dice\n"
                "`/sound` - Play a funny sound"
            ) if lang == 'en' else (
                "`/meme` - Véletlenszerű mém\n"
                "`/8ball` - Mágikus 8-as\n"
                "`/coinflip` - Érmefeldobás\n"
                "`/roll` - Kocka dobása\n"
                "`/sound` - Szórakoztató hang"
            ),
            color=0xFF00FF
        )
        await interaction.response.edit_message(embed=embed)

    @discord.ui.button(label="📊 Stats", style=discord.ButtonStyle.secondary, emoji="📊", row=2)
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

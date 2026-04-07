import discord
from discord.ext import commands
from discord import app_commands
import config
import translations
from datetime import datetime, timezone
import json

class Community(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    # ==================== ACHIEVEMENTS SYSTEM ====================
    
    @app_commands.command(name="achievements", description="View your achievements / Tekintsd meg az eléréseidet")
    async def achievements(self, interaction: discord.Interaction, user: discord.User = None):
        """View achievements for you or another user"""
        target_user = user or interaction.user
        guild_id = interaction.guild.id
        lang = translations.get_guild_language(guild_id)
        
        cfg = config.load_config()
        achievements = cfg.get('achievements', {}).get(str(guild_id), {}).get(str(target_user.id), [])
        
        if not achievements:
            await interaction.response.send_message(
                f"❌ {target_user.mention} hasn't earned any achievements yet!" if lang == 'en'
                else f"❌ {target_user.mention} még nem szerzett eléréseket!",
                ephemeral=True
            )
            return
        
        embed = discord.Embed(
            title=f"🏆 {target_user.name}'s Achievements" if lang == 'en' else f"🏆 {target_user.name} Elérései",
            color=0x00F3FF
        )
        
        achievements_list = {
            'first_message': '💬 First Message',
            'first_message_hu': '💬 Első Üzenet',
            'level_10': '⭐ Level 10',
            'level_50': '⭐⭐ Level 50',
            'trusted': '✅ Trusted Member',
            'trusted_hu': '✅ Megbízható Tag',
            'moderator': '♠️ Moderator',
            'helper': '🤝 Helper',
        }
        
        for achievement in achievements:
            emoji = "✅"
            embed.add_field(name=f"{emoji} {achievement}", value="Unlocked", inline=False)
        
        await interaction.response.send_message(embed=embed)
    
    # ==================== AFK STATUS SYSTEM ====================
    
    @app_commands.command(name="afk", description="Set your AFK status / Állítsd be az AFK státuszod")
    @app_commands.describe(reason="Why are you AFK? / Miért vagy AFK?")
    async def afk(self, interaction: discord.Interaction, reason: str = "No reason provided"):
        """Set AFK status"""
        guild_id = interaction.guild.id
        lang = translations.get_guild_language(guild_id)
        
        cfg = config.load_config()
        if 'afk_users' not in cfg:
            cfg['afk_users'] = {}
        if str(guild_id) not in cfg['afk_users']:
            cfg['afk_users'][str(guild_id)] = {}
        
        cfg['afk_users'][str(guild_id)][str(interaction.user.id)] = {
            'reason': reason,
            'timestamp': datetime.now(timezone.utc).isoformat()
        }
        config.save_config(cfg)
        
        embed = discord.Embed(
            title="✅ AFK Set" if lang == 'en' else "✅ AFK Beállítva",
            description=f"Reason: {reason}",
            color=0x00F3FF
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)
    
    @app_commands.command(name="back", description="Remove your AFK status / Távolítsd el az AFK státuszod")
    async def back(self, interaction: discord.Interaction):
        """Remove AFK status"""
        guild_id = interaction.guild.id
        lang = translations.get_guild_language(guild_id)
        
        cfg = config.load_config()
        if 'afk_users' in cfg and str(guild_id) in cfg['afk_users']:
            if str(interaction.user.id) in cfg['afk_users'][str(guild_id)]:
                del cfg['afk_users'][str(guild_id)][str(interaction.user.id)]
                config.save_config(cfg)
                
                embed = discord.Embed(
                    title="✅ Welcome Back!" if lang == 'en' else "✅ Üdvözlünk Vissza!",
                    color=0x00F3FF
                )
                await interaction.response.send_message(embed=embed, ephemeral=True)
                return
        
        await interaction.response.send_message(
            "❌ You are not AFK!" if lang == 'en' else "❌ Nem vagy AFK!",
            ephemeral=True
        )
    
    # ==================== REPORT SYSTEM ====================
    
    @app_commands.command(name="report-user", description="Report a user / Jelents be egy felhasználót")
    @app_commands.describe(
        user="User to report / Jelzendő felhasználó",
        reason="Report reason / Bejelentés oka"
    )
    async def report_user(self, interaction: discord.Interaction, user: discord.User, reason: str):
        """Report a user to moderators"""
        guild_id = interaction.guild.id
        lang = translations.get_guild_language(guild_id)
        
        if user.id == interaction.user.id:
            await interaction.response.send_message(
                "❌ You cannot report yourself!" if lang == 'en' else "❌ Nem jellentheted be magadat!",
                ephemeral=True
            )
            return
        
        cfg = config.load_config()
        log_channel_id = cfg.get('guild_log_channels', {}).get(str(guild_id))
        
        if not log_channel_id:
            await interaction.response.send_message(
                "❌ No log channel configured!" if lang == 'en' else "❌ Nincs napló csatorna beállítva!",
                ephemeral=True
            )
            return
        
        # Store report
        if 'reports' not in cfg:
            cfg['reports'] = {}
        if str(guild_id) not in cfg['reports']:
            cfg['reports'][str(guild_id)] = []
        
        report_data = {
            'reporter': str(interaction.user.id),
            'reported': str(user.id),
            'reason': reason,
            'timestamp': datetime.now(timezone.utc).isoformat()
        }
        cfg['reports'][str(guild_id)].append(report_data)
        config.save_config(cfg)
        
        # Send to log channel
        log_channel = interaction.guild.get_channel(int(log_channel_id))
        if log_channel:
            embed = discord.Embed(
                title="📋 User Report",
                description=f"**Reporter:** {interaction.user.mention}\n**Reported User:** {user.mention}\n**Reason:** {reason}",
                color=0xFF0000
            )
            await log_channel.send(embed=embed)
        
        await interaction.response.send_message(
            "✅ Report submitted!" if lang == 'en' else "✅ Bejelentés elküldve!",
            ephemeral=True
        )
    
    @app_commands.command(name="report-server", description="Report a server issue / Jelents be egy szerver problémát")
    @app_commands.describe(issue="What's wrong / Mi a gond")
    async def report_server(self, interaction: discord.Interaction, issue: str):
        """Report a server issue"""
        guild_id = interaction.guild.id
        lang = translations.get_guild_language(guild_id)
        
        cfg = config.load_config()
        log_channel_id = cfg.get('guild_log_channels', {}).get(str(guild_id))
        
        if not log_channel_id:
            await interaction.response.send_message(
                "❌ No log channel configured!" if lang == 'en' else "❌ Nincs napló csatorna beállítva!",
                ephemeral=True
            )
            return
        
        # Send to log channel
        log_channel = interaction.guild.get_channel(int(log_channel_id))
        if log_channel:
            embed = discord.Embed(
                title="🆘 Server Issue Report",
                description=f"**Reporter:** {interaction.user.mention}\n**Issue:** {issue}",
                color=0xFF6600
            )
            await log_channel.send(embed=embed)
        
        await interaction.response.send_message(
            "✅ Issue reported!" if lang == 'en' else "✅ Probléma bejelentve!",
            ephemeral=True
        )
    
    # ==================== APPEAL SYSTEM ====================
    
    @app_commands.command(name="appeal", description="Appeal a ban or mute / Fellebbezz egy tiltás vagy némítás ellen")
    @app_commands.describe(reason="Why should we unban you? / Miért kellene feloldanod?")
    async def appeal(self, interaction: discord.Interaction, reason: str):
        """Appeal a ban/mute"""
        guild_id = interaction.guild.id
        lang = translations.get_guild_language(guild_id)
        
        cfg = config.load_config()
        
        # Store appeal
        if 'appeals' not in cfg:
            cfg['appeals'] = {}
        if str(guild_id) not in cfg['appeals']:
            cfg['appeals'][str(guild_id)] = []
        
        appeal_data = {
            'user': str(interaction.user.id),
            'reason': reason,
            'status': 'pending',
            'timestamp': datetime.now(timezone.utc).isoformat()
        }
        cfg['appeals'][str(guild_id)].append(appeal_data)
        config.save_config(cfg)
        
        # Send DM to user confirmation
        try:
            embed = discord.Embed(
                title="📝 Appeal Submitted",
                description=f"Your appeal for **{interaction.guild.name}** has been received and will be reviewed by staff.",
                color=0x00F3FF
            )
            await interaction.user.send(embed=embed)
        except:
            pass
        
        await interaction.response.send_message(
            "✅ Appeal submitted! Staff will review it soon." if lang == 'en'
            else "✅ Fellebbezés beküldve! A személyzet hamarosan felülvizsgálja.",
            ephemeral=True
        )
    
    # ==================== MODLOG SEARCH ====================
    
    @app_commands.command(name="modlog-search", description="Search moderation logs / Keress a moderációs naplóban")
    @app_commands.describe(
        user="User to search for / Keresendő felhasználó",
        action="Action type (ban/kick/mute/warn) / Művelet típusa"
    )
    @app_commands.checks.has_permissions(moderate_members=True)
    async def modlog_search(self, interaction: discord.Interaction, user: discord.User = None, action: str = None):
        """Search moderation logs"""
        guild_id = interaction.guild.id
        lang = translations.get_guild_language(guild_id)
        
        cfg = config.load_config()
        
        # Get all moderation data
        warnings = cfg.get('warnings', {}).get(str(guild_id), {})
        
        results = []
        if user:
            user_warnings = warnings.get(str(user.id), [])
            results = user_warnings
        
        if not results:
            await interaction.response.send_message(
                "❌ No records found!" if lang == 'en' else "❌ Nincs találat!",
                ephemeral=True
            )
            return
        
        embed = discord.Embed(
            title=f"📋 Mod Log - {user.name if user else 'All'}" if lang == 'en'
            else f"📋 Moderációs napló - {user.name if user else 'Összes'}",
            color=0xFF0000
        )
        
        for i, record in enumerate(results[:10], 1):
            embed.add_field(
                name=f"Record {i}" if lang == 'en' else f"Rekord {i}",
                value=f"Reason: {record.get('reason', 'N/A')}\nDate: {record.get('date', 'N/A')}",
                inline=False
            )
        
        await interaction.response.send_message(embed=embed, ephemeral=True)
    
    # ==================== BIRTHDAY SYSTEM ====================
    
    @app_commands.command(name="birthday", description="Set your birthday / Állítsd be a születésnapod")
    @app_commands.describe(date="Your birthday (DD/MM format) / Születésnapod (NN/HH formátum)")
    async def birthday(self, interaction: discord.Interaction, date: str):
        """Set your birthday"""
        guild_id = interaction.guild.id
        lang = translations.get_guild_language(guild_id)
        
        # Validate date format
        try:
            day, month = map(int, date.split('/'))
            if not (1 <= day <= 31 and 1 <= month <= 12):
                raise ValueError
        except:
            await interaction.response.send_message(
                "❌ Invalid date format! Use DD/MM" if lang == 'en' else "❌ Érvénytelen dátumformátum! Használd a NN/HH formátumot",
                ephemeral=True
            )
            return
        
        cfg = config.load_config()
        if 'birthdays' not in cfg:
            cfg['birthdays'] = {}
        if str(guild_id) not in cfg['birthdays']:
            cfg['birthdays'][str(guild_id)] = {}
        
        cfg['birthdays'][str(guild_id)][str(interaction.user.id)] = {
            'date': date,
            'timestamp': datetime.now(timezone.utc).isoformat()
        }
        config.save_config(cfg)
        
        await interaction.response.send_message(
            f"✅ Birthday set to {date}!" if lang == 'en' else f"✅ Születésnap beállítva: {date}!",
            ephemeral=True
        )
    
    # ==================== AUTOMOD SETTINGS ====================
    
    @app_commands.command(name="automod-settings", description="Configure AutoMod / AutoMod beállítása")
    @app_commands.describe(
        feature="Feature to configure (spam/links/badwords) / Konfigurálható funkció"
    )
    @app_commands.checks.has_permissions(administrator=True)
    async def automod_settings(self, interaction: discord.Interaction, feature: str):
        """Configure AutoMod settings"""
        guild_id = interaction.guild.id
        lang = translations.get_guild_language(guild_id)
        
        cfg = config.load_config()
        if 'automod' not in cfg:
            cfg['automod'] = {}
        if str(guild_id) not in cfg['automod']:
            cfg['automod'][str(guild_id)] = {
                'enabled': False,
                'spam_detection': True,
                'link_filter': False,
                'bad_words': [],
                'caps_filter': False,
                'punishment': 'warn'
            }
        
        settings = cfg['automod'][str(guild_id)]
        
        if feature.lower() == 'spam':
            settings['spam_detection'] = not settings['spam_detection']
            status = "enabled" if settings['spam_detection'] else "disabled"
        elif feature.lower() == 'links':
            settings['link_filter'] = not settings['link_filter']
            status = "enabled" if settings['link_filter'] else "disabled"
        elif feature.lower() == 'badwords':
            settings['enabled'] = not settings['enabled']
            status = "enabled" if settings['enabled'] else "disabled"
        else:
            await interaction.response.send_message(
                "❌ Unknown feature! Use: spam, links, badwords" if lang == 'en'
                else "❌ Ismeretlen funkció! Használd: spam, links, badwords",
                ephemeral=True
            )
            return
        
        config.save_config(cfg)
        
        embed = discord.Embed(
            title=f"⚙️ AutoMod Updated" if lang == 'en' else f"⚙️ AutoMod Frissítve",
            description=f"**Feature:** {feature}\n**Status:** {status}",
            color=0x00F3FF
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)
    
    @app_commands.command(name="automod-badwords", description="Add/remove bad words from AutoMod / Bad words hozzáadása/eltávolítása")
    @app_commands.describe(
        action="Add or remove / Hozzáadás vagy eltávolítás",
        word="The word to manage / Kezelendő szó"
    )
    @app_commands.checks.has_permissions(administrator=True)
    async def automod_badwords(self, interaction: discord.Interaction, action: str, word: str):
        """Manage bad words in AutoMod"""
        guild_id = interaction.guild.id
        lang = translations.get_guild_language(guild_id)
        
        cfg = config.load_config()
        if 'automod' not in cfg:
            cfg['automod'] = {}
        if str(guild_id) not in cfg['automod']:
            cfg['automod'][str(guild_id)] = {'bad_words': []}
        
        bad_words = cfg['automod'][str(guild_id)].get('bad_words', [])
        
        if action.lower() == 'add':
            if word.lower() not in bad_words:
                bad_words.append(word.lower())
                cfg['automod'][str(guild_id)]['bad_words'] = bad_words
                config.save_config(cfg)
                
                embed = discord.Embed(
                    title="✅ Word Added" if lang == 'en' else "✅ Szó Hozzáadva",
                    description=f"'{word}' added to bad words filter",
                    color=0x00F3FF
                )
            else:
                embed = discord.Embed(
                    title="⚠️ Already Exists" if lang == 'en' else "⚠️ Már Létezik",
                    color=0xFF6600
                )
        
        elif action.lower() == 'remove':
            if word.lower() in bad_words:
                bad_words.remove(word.lower())
                cfg['automod'][str(guild_id)]['bad_words'] = bad_words
                config.save_config(cfg)
                
                embed = discord.Embed(
                    title="✅ Word Removed" if lang == 'en' else "✅ Szó Eltávolítva",
                    description=f"'{word}' removed from bad words filter",
                    color=0x00F3FF
                )
            else:
                embed = discord.Embed(
                    title="❌ Word Not Found" if lang == 'en' else "❌ Szó Nem Található",
                    color=0xFF0000
                )
        else:
            embed = discord.Embed(
                title="❌ Invalid Action" if lang == 'en' else "❌ Érvénytelen Művelet",
                description="Use 'add' or 'remove'",
                color=0xFF0000
            )
        
        await interaction.response.send_message(embed=embed, ephemeral=True)

async def setup(bot):
    await bot.add_cog(Community(bot))

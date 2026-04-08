"""
Hungarian Server Defense System
Commands for managing Hungarian-specific automod features
"""
import discord
from discord.ext import commands
from discord import app_commands
from hungarian_automod import (
    HUNGARIAN_BAD_WORDS, ENGLISH_BAD_WORDS, 
    get_bad_words_for_language, merge_bad_words
)
from database import get_guild_settings, update_guild_settings
import translations

class HungarianDefense(commands.Cog):
    """Hungarian language-specific server defense features"""
    
    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.command(name='hudefense_enable', description='Enable Hungarian defense automod')
    @app_commands.checks.has_permissions(manage_guild=True)
    async def enable_hu_defense(self, interaction: discord.Interaction):
        """Enable Hungarian automod"""
        settings = get_guild_settings(str(interaction.guild.id))
        
        settings['automod'] = settings.get('automod', {})
        settings['automod']['enabled'] = True
        settings['automod']['spam_detection'] = True
        
        # Enable Hungarian bad words by default
        if not settings['bad_words']:
            settings['bad_words'] = HUNGARIAN_BAD_WORDS.copy()
        
        settings['language'] = 'hu'
        update_guild_settings(str(interaction.guild.id), settings)
        
        embed = discord.Embed(
            title="✅ Hungarian Defense Enabled",
            description="Your server is now protected with Hungarian automod!\n\n"
                       f"🔒 Bad Words: {len(HUNGARIAN_BAD_WORDS)} words blocked\n"
                       "🛡️ Language: Hungarian\n"
                       "📊 Spam Detection: Enabled",
            color=discord.Color.green()
        )
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name='hudefense_disable', description='Disable Hungarian defense automod')
    @app_commands.checks.has_permissions(manage_guild=True)
    async def disable_hu_defense(self, interaction: discord.Interaction):
        """Disable Hungarian automod"""
        settings = get_guild_settings(str(interaction.guild.id))
        settings['automod'] = settings.get('automod', {})
        settings['automod']['enabled'] = False
        update_guild_settings(str(interaction.guild.id), settings)
        
        embed = discord.Embed(
            title="❌ Hungarian Defense Disabled",
            description="Hungarian automod has been disabled.",
            color=discord.Color.red()
        )
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name='hudefense_status', description='Check Hungarian defense status')
    async def defense_status(self, interaction: discord.Interaction):
        """Check Hungarian defense status"""
        settings = get_guild_settings(str(interaction.guild.id))
        automod = settings.get('automod', {})
        is_enabled = automod.get('enabled', False)
        
        bad_words_count = len(settings.get('bad_words', []))
        
        embed = discord.Embed(
            title="🛡️ Hungarian Defense Status",
            color=discord.Color.green() if is_enabled else discord.Color.red()
        )
        embed.add_field(name="Status", value="✅ Enabled" if is_enabled else "❌ Disabled", inline=True)
        embed.add_field(name="Bad Words Blocked", value=str(bad_words_count), inline=True)
        embed.add_field(name="Spam Detection", value="✅ On" if automod.get('spam_detection') else "❌ Off", inline=True)
        embed.add_field(
            name="Language",
            value=settings.get('language', 'en').upper(),
            inline=True
        )
        
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name='hudefense_addbadword', description='Add a custom bad word to filter')
    @app_commands.checks.has_permissions(manage_guild=True)
    async def add_bad_word(self, interaction: discord.Interaction, word: str):
        """Add a custom bad word to the filter"""
        if len(word) < 2:
            await interaction.response.send_message("❌ Word must be at least 2 characters long")
            return
        
        settings = get_guild_settings(str(interaction.guild.id))
        bad_words = settings.get('bad_words', [])
        
        word_lower = word.lower()
        if word_lower in bad_words:
            await interaction.response.send_message(f"⚠️ '{word}' is already in the bad words list")
            return
        
        bad_words.append(word_lower)
        settings['bad_words'] = bad_words
        update_guild_settings(str(interaction.guild.id), settings)
        
        embed = discord.Embed(
            title="✅ Word Added",
            description=f"'{word}' has been added to the bad words filter",
            color=discord.Color.green()
        )
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name='hudefense_removebadword', description='Remove a word from filter')
    @app_commands.checks.has_permissions(manage_guild=True)
    async def remove_bad_word(self, interaction: discord.Interaction, word: str):
        """Remove a word from the bad words filter"""
        settings = get_guild_settings(str(interaction.guild.id))
        bad_words = settings.get('bad_words', [])
        
        word_lower = word.lower()
        if word_lower not in bad_words:
            await interaction.response.send_message(f"⚠️ '{word}' is not in the bad words list")
            return
        
        bad_words.remove(word_lower)
        settings['bad_words'] = bad_words
        update_guild_settings(str(interaction.guild.id), settings)
        
        embed = discord.Embed(
            title="✅ Word Removed",
            description=f"'{word}' has been removed from the bad words filter",
            color=discord.Color.green()
        )
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name='hudefense_preview', description='Preview the bad words list')
    async def preview_bad_words(self, interaction: discord.Interaction):
        """Preview the bad words list"""
        settings = get_guild_settings(str(interaction.guild.id))
        bad_words = settings.get('bad_words', [])
        language = settings.get('language', 'en')
        
        if not bad_words:
            await interaction.response.send_message("❌ No bad words configured")
            return
        
        # Send in chunks to avoid message length limit
        chunks = [bad_words[i:i+50] for i in range(0, len(bad_words), 50)]
        
        for i, chunk in enumerate(chunks, 1):
            embed = discord.Embed(
                title=f"🛡️ Bad Words List ({language.upper()}) - Part {i}/{len(chunks)}",
                description=", ".join(chunk),
                color=discord.Color.orange()
            )
            embed.set_footer(text=f"Total: {len(bad_words)} words")
            if i == 1:
                await interaction.response.send_message(embed=embed)
            else:
                await interaction.followup.send(embed=embed)
    
    @app_commands.command(name='hudefense_resetbadwords', description='Reset bad words to defaults')
    @app_commands.checks.has_permissions(manage_guild=True)
    async def reset_bad_words(self, interaction: discord.Interaction):
        """Reset bad words to default for server language"""
        settings = get_guild_settings(str(interaction.guild.id))
        language = settings.get('language', 'en')
        
        default_words = get_bad_words_for_language(language)
        settings['bad_words'] = default_words.copy()
        update_guild_settings(str(interaction.guild.id), settings)
        
        embed = discord.Embed(
            title="✅ Reset to Defaults",
            description=f"Bad words list has been reset to {language.upper()} defaults\n"
                       f"📊 {len(default_words)} words now blocked",
            color=discord.Color.green()
        )
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name='hudefense_stats', description='Show defense statistics')
    async def defense_stats(self, interaction: discord.Interaction):
        """Show defense statistics"""
        settings = get_guild_settings(str(interaction.guild.id))
        
        bad_words = settings.get('bad_words', [])
        language = settings.get('language', 'en')
        automod_enabled = settings.get('automod', {}).get('enabled', False)
        
        embed = discord.Embed(
            title="📊 Hungarian Defense Statistics",
            color=discord.Color.blue()
        )
        embed.add_field(name="Status", value="✅ Active" if automod_enabled else "❌ Inactive")
        embed.add_field(name="Language", value=language.upper())
        embed.add_field(name="Bad Words Protected", value=str(len(bad_words)))
        embed.add_field(
            name="Default Bad Words",
            value=len(get_bad_words_for_language(language))
        )
        embed.add_field(
            name="Custom Bad Words",
            value=max(0, len(bad_words) - len(get_bad_words_for_language(language)))
        )
        
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(HungarianDefense(bot))

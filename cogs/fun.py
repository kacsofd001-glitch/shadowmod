import discord
from discord.ext import commands
from discord import app_commands
import aiohttp
import random
import config
from translations import get_text, get_guild_language
from urllib.parse import quote

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.sounds = [
            "🎵 *Ding dong!*",
            "🔔 *Ring ring!*",
            "📯 *Toot toot!*",
            "🎺 *Doot doot!*",
            "🥁 *Ba dum tss!*",
            "🎸 *Strum strum!*",
            "🎹 *Piano notes!*",
            "🎷 *Smooth jazz!*",
            "📢 *Honk honk!*",
            "🔊 *Beep boop!*"
        ]
        
        self.meme_templates_en = [
            ("drake", "Old boring way", "Cool new way"),
            ("buzz", "Memes", "Memes everywhere"),
            ("doge", "Such wow", "Very meme"),
            ("yoda", "Do or do not", "There is no try"),
            ("both", "Why not both?", "Both is good"),
            ("aliens", "I'm not saying it was", "But it was"),
            ("interesting", "That's very", "Interesting"),
            ("disaster", "I see this as", "An absolute win"),
            ("fine", "This is fine", "Everything is fine"),
            ("think", "Modern problems", "Modern solutions"),
        ]
        
        self.meme_templates_hu = [
            ("drake", "Régi unalmas módszer", "Menő új módszer"),
            ("buzz", "Mémek", "Mémek mindenhol"),
            ("doge", "Ilyen hűha", "Nagyon mém"),
            ("yoda", "Tedd vagy ne tedd", "Nincs próba"),
            ("both", "Miért ne mindkettő?", "Mindkettő jó"),
            ("aliens", "Nem azt mondom hogy az volt", "De az volt"),
            ("interesting", "Ez nagyon", "Érdekes"),
            ("disaster", "Ezt úgy látom", "Abszolút győzelem"),
            ("fine", "Ez rendben van", "Minden rendben"),
            ("think", "Modern problémák", "Modern megoldások"),
        ]
    
    @app_commands.command(name='sound', description='Execute sound command')
    async def random_sound(self, interaction: discord.Interaction):
        sound = random.choice(self.sounds)
        
        embed = discord.Embed(
            title="🔊 Random Sound",
            description=sound,
            color=discord.Color.random()
        )
        
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name='coinflip', description='Execute coinflip command')
    async def coin_flip(self, interaction: discord.Interaction):
        from translations import get_text
        result = random.choice([get_text(interaction.guild.id, 'heads'), get_text(interaction.guild.id, 'tails')])
        emoji = '🪙'
        
        embed = discord.Embed(
            title=get_text(interaction.guild.id, 'coin_flip'),
            description=get_text(interaction.guild.id, 'coin_result', result),
            color=discord.Color.gold()
        )
        
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name='roll', description='Execute roll command')
    async def dice_roll(self, interaction: discord.Interaction, dice: str = "1d6"):
        try:
            rolls, sides = map(int, dice.split('d'))
            
            if rolls > 100 or sides > 1000:
                await interaction.response.send_message("❌ That's too many dice or sides!")
                return
            
            results = [random.randint(1, sides) for _ in range(rolls)]
            total = sum(results)
            
            embed = discord.Embed(
                title="🎲 Dice Roll",
                description=f"Rolling {rolls}d{sides}",
                color=discord.Color.random()
            )
            
            embed.add_field(name="Results", value=", ".join(map(str, results)), inline=False)
            
            embed.add_field(name="Total", value=str(total), inline=False)
            
            await interaction.response.send_message(embed=embed)
        except:
            await interaction.response.send_message("❌ Invalid format! Use: `!roll 2d6` (rolls, d, sides)")

async def setup(bot):
    await bot.add_cog(Fun(bot))

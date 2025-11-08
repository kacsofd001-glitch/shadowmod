import discord
from discord.ext import commands
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
    
    @commands.command(name='meme')
    async def random_meme(self, ctx):
        lang = get_guild_language(ctx.guild.id)
        
        templates = self.meme_templates_hu if lang == 'hu' else self.meme_templates_en
        template_name, top_text, bottom_text = random.choice(templates)
        
        top_text_encoded = quote(top_text, safe='')
        bottom_text_encoded = quote(bottom_text, safe='')
        
        meme_url = f"https://api.memegen.link/images/{template_name}/{top_text_encoded}/{bottom_text_encoded}.png"
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.head(meme_url, timeout=aiohttp.ClientTimeout(total=5)) as response:
                    if response.status != 200:
                        raise Exception("Meme API unavailable")
            
            embed = discord.Embed(
                title=get_text(ctx.guild.id, 'meme_title'),
                color=discord.Color.random()
            )
            embed.set_image(url=meme_url)
            embed.set_footer(text=get_text(ctx.guild.id, 'generated_meme'))
            
            await ctx.send(embed=embed)
        except Exception:
            embed = discord.Embed(
                title=get_text(ctx.guild.id, 'meme_title'),
                description=f"**{top_text}**\n\n*{bottom_text}*",
                color=discord.Color.random()
            )
            embed.set_footer(text=get_text(ctx.guild.id, 'generated_meme'))
            await ctx.send(embed=embed)
    
    
    @commands.command(name='sound')
    async def random_sound(self, ctx):
        sound = random.choice(self.sounds)
        
        embed = discord.Embed(
            title="🔊 Random Sound",
            description=sound,
            color=discord.Color.random()
        )
        
        await ctx.send(embed=embed)
    
    @commands.command(name='8ball')
    async def eight_ball(self, ctx, *, question: str = ""):
        if not question:
            await ctx.send("❌ Please ask a question!")
            return
        
        responses = [
            "Yes, definitely! ✅",
            "It is certain! ✅",
            "Without a doubt! ✅",
            "Yes! ✅",
            "Most likely! ✅",
            "Outlook good! ✅",
            "Signs point to yes! ✅",
            "Reply hazy, try again! 🤔",
            "Ask again later! 🤔",
            "Better not tell you now! 🤔",
            "Cannot predict now! 🤔",
            "Concentrate and ask again! 🤔",
            "Don't count on it! ❌",
            "My reply is no! ❌",
            "My sources say no! ❌",
            "Outlook not so good! ❌",
            "Very doubtful! ❌"
        ]
        
        answer = random.choice(responses)
        
        embed = discord.Embed(
            title="🎱 Magic 8 Ball",
            color=discord.Color.purple()
        )
        embed.add_field(name="Question", value=question, inline=False)
        embed.add_field(name="Answer", value=answer, inline=False)
        
        await ctx.send(embed=embed)
    
    @commands.command(name='coinflip')
    async def coin_flip(self, ctx):
        result = random.choice(['Heads', 'Tails'])
        emoji = '🪙'
        
        embed = discord.Embed(
            title=f"{emoji} Coin Flip",
            description=f"**Result:** {result}!",
            color=discord.Color.gold()
        )
        
        await ctx.send(embed=embed)
    
    @commands.command(name='roll')
    async def dice_roll(self, ctx, dice: str = "1d6"):
        try:
            rolls, sides = map(int, dice.split('d'))
            
            if rolls > 100 or sides > 1000:
                await ctx.send("❌ That's too many dice or sides!")
                return
            
            results = [random.randint(1, sides) for _ in range(rolls)]
            total = sum(results)
            
            embed = discord.Embed(
                title="🎲 Dice Roll",
                description=f"Rolling {rolls}d{sides}",
                color=discord.Color.blue()
            )
            
            if len(results) <= 20:
                embed.add_field(name="Results", value=", ".join(map(str, results)), inline=False)
            
            embed.add_field(name="Total", value=str(total), inline=False)
            
            await ctx.send(embed=embed)
        except:
            await ctx.send("❌ Invalid format! Use: `!roll 2d6` (rolls, d, sides)")

async def setup(bot):
    await bot.add_cog(Fun(bot))

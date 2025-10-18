import discord
from discord.ext import commands
import aiohttp
import random

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
    
    @commands.command(name='meme')
    async def random_meme(self, ctx):
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get('https://meme-api.com/gimme') as response:
                    if response.status == 200:
                        data = await response.json()
                        
                        embed = discord.Embed(
                            title=data['title'],
                            url=data['postLink'],
                            color=discord.Color.random()
                        )
                        embed.set_image(url=data['url'])
                        embed.set_footer(text=f"👍 {data['ups']} upvotes | r/{data['subreddit']}")
                        
                        await ctx.send(embed=embed)
                    else:
                        await self.fallback_meme(ctx)
            except Exception as e:
                await self.fallback_meme(ctx)
    
    async def fallback_meme(self, ctx):
        meme_texts = [
            ("When you're debugging at 3 AM", "And you find the bug was a typo"),
            ("Nobody:", "Discord bots: I'm gonna crash for no reason"),
            ("Me: writes 1000 lines of code", "Also me: forgets semicolon"),
            ("Code on my machine:", "Code on production:"),
            ("Client: Can you make a small change?", "The codebase:")
        ]
        
        meme = random.choice(meme_texts)
        
        embed = discord.Embed(
            title="😂 Random Meme",
            description=f"**{meme[0]}**\n\n*{meme[1]}*",
            color=discord.Color.random()
        )
        embed.set_footer(text="Generated meme")
        
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
    async def eight_ball(self, ctx, *, question: str = None):
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

import discord
from discord.ext import commands
from discord import app_commands
import aiohttp
import config
from translations import get_text, get_guild_language
import os

class AIChat(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.openai_api_key = os.getenv('OPENAI_API_KEY')
    
    @app_commands.command(name="aichat", description="Configure AI chat for a channel / AI csevegés beállítása")
    @app_commands.describe(
        channel="Channel for AI chat / Csatorna az AI csevegéshez",
        language="AI response language (en/hu) / AI válasz nyelve",
        enabled="Enable or disable / Bekapcsolás vagy kikapcsolás"
    )
    @app_commands.checks.has_permissions(administrator=True)
    async def aichat_config(
        self, 
        interaction: discord.Interaction,
        channel: discord.TextChannel,
        language: str,
        enabled: bool
    ):
        if language not in ['en', 'hu']:
            await interaction.response.send_message("❌ Language must be 'en' or 'hu'", ephemeral=True)
            return
        
        cfg = config.load_config()
        if 'ai_chat_channels' not in cfg:
            cfg['ai_chat_channels'] = {}
        
        channel_id = str(channel.id)
        
        if enabled:
            cfg['ai_chat_channels'][channel_id] = {
                'guild_id': str(interaction.guild.id),
                'language': language,
                'enabled': True
            }
            config.save_config(cfg)
            
            embed = discord.Embed(
                title="✅ AI Chat Enabled",
                description=f"AI chat enabled in {channel.mention}",
                color=discord.Color.green()
            )
            embed.add_field(name="Language", value=language.upper(), inline=True)
            embed.add_field(name="Status", value="✅ Enabled", inline=True)
            
            await interaction.response.send_message(embed=embed)
        else:
            if channel_id in cfg.get('ai_chat_channels', {}):
                del cfg['ai_chat_channels'][channel_id]
                config.save_config(cfg)
            
            embed = discord.Embed(
                title="🔇 AI Chat Disabled",
                description=f"AI chat disabled in {channel.mention}",
                color=discord.Color.red()
            )
            
            await interaction.response.send_message(embed=embed)
    
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        
        if not self.openai_api_key:
            return
        
        cfg = config.load_config()
        ai_channels = cfg.get('ai_chat_channels', {})
        channel_id = str(message.channel.id)
        
        if channel_id not in ai_channels:
            return
        
        channel_config = ai_channels[channel_id]
        if not channel_config.get('enabled', False):
            return
        
        async with message.channel.typing():
            try:
                response_text = await self.get_ai_response(
                    message.content,
                    channel_config.get('language', 'en')
                )
                
                if len(response_text) > 2000:
                    chunks = [response_text[i:i+2000] for i in range(0, len(response_text), 2000)]
                    for chunk in chunks:
                        await message.reply(chunk, mention_author=False)
                else:
                    await message.reply(response_text, mention_author=False)
                    
            except Exception as e:
                await message.reply("❌ Sorry, I couldn't process that message.", mention_author=False)
    
    async def get_ai_response(self, user_message: str, language: str) -> str:
        """Get AI response from OpenAI API"""
        
        system_prompt = {
            'en': "You are a helpful and friendly Discord bot assistant. Keep responses concise and helpful.",
            'hu': "Egy segítőkész és barátságos Discord bot asszisztens vagy. Tömör és hasznos válaszokat adj."
        }
        
        headers = {
            "Authorization": f"Bearer {self.openai_api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": "gpt-3.5-turbo",
            "messages": [
                {"role": "system", "content": system_prompt.get(language, system_prompt['en'])},
                {"role": "user", "content": user_message}
            ],
            "max_tokens": 500,
            "temperature": 0.7
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.post(
                "https://api.openai.com/v1/chat/completions",
                headers=headers,
                json=data,
                timeout=aiohttp.ClientTimeout(total=30)
            ) as response:
                if response.status == 200:
                    result = await response.json()
                    return result['choices'][0]['message']['content']
                else:
                    raise Exception(f"OpenAI API error: {response.status}")

async def setup(bot):
    await bot.add_cog(AIChat(bot))

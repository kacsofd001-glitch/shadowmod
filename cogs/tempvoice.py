import discord
from discord.ext import commands
import config

class TempVoice(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    def get_tempvoice_config(self, guild_id):
        """Get temp voice settings"""
        cfg = config.load_config()
        tempvoice = cfg.get('tempvoice', {})
        return tempvoice.get(str(guild_id), {
            'enabled': False,
            'create_channel_id': None,
            'category_id': None,
            'channel_name': '{user}\'s Channel',
            'temp_channels': []
        })
    
    def save_tempvoice_config(self, guild_id, settings):
        """Save temp voice settings"""
        cfg = config.load_config()
        if 'tempvoice' not in cfg:
            cfg['tempvoice'] = {}
        cfg['tempvoice'][str(guild_id)] = settings
        config.save_config(cfg)
    
    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        settings = self.get_tempvoice_config(member.guild.id)
        
        if not settings['enabled']:
            return
        
        # User joined the "create channel" voice channel
        if after.channel and after.channel.id == settings['create_channel_id']:
            category = member.guild.get_channel(settings['category_id'])
            
            channel_name = settings['channel_name'].format(user=member.name)
            
            # Create temp channel
            temp_channel = await member.guild.create_voice_channel(
                name=channel_name,
                category=category,
                reason="Temporary voice channel"
            )
            
            # Move user to temp channel
            try:
                await member.move_to(temp_channel)
            except:
                pass
            
            # Track temp channel
            settings['temp_channels'].append(temp_channel.id)
            self.save_tempvoice_config(member.guild.id, settings)
        
        # Check if temp channel is now empty
        if before.channel and before.channel.id in settings['temp_channels']:
            if len(before.channel.members) == 0:
                try:
                    await before.channel.delete(reason="Temporary voice channel empty")
                    settings['temp_channels'].remove(before.channel.id)
                    self.save_tempvoice_config(member.guild.id, settings)
                except:
                    pass

async def setup(bot):
    await bot.add_cog(TempVoice(bot))

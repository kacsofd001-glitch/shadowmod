import discord
from discord.ext import commands, tasks
import config
import aiohttp

class Webhooks(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.check_feeds.start()
    
    def cog_unload(self):
        self.check_feeds.cancel()
    
    def get_webhook_config(self, guild_id):
        """Get webhook integration settings"""
        cfg = config.load_config()
        webhooks = cfg.get('webhooks', {})
        return webhooks.get(str(guild_id), {
            'github': {
                'enabled': False,
                'channel_id': None,
                'repos': []
            },
            'youtube': {
                'enabled': False,
                'channel_id': None,
                'channels': []
            },
            'twitch': {
                'enabled': False,
                'channel_id': None,
                'streamers': []
            },
            'rss': {
                'enabled': False,
                'channel_id': None,
                'feeds': []
            }
        })
    
    def save_webhook_config(self, guild_id, settings):
        """Save webhook settings"""
        cfg = config.load_config()
        if 'webhooks' not in cfg:
            cfg['webhooks'] = {}
        cfg['webhooks'][str(guild_id)] = settings
        config.save_config(cfg)
    
    @tasks.loop(minutes=15)
    async def check_feeds(self):
        """Check for updates from various sources"""
        pass
    
    @check_feeds.before_loop
    async def before_check_feeds(self):
        await self.bot.wait_until_ready()
    
    async def add_github_repo(self, guild_id, channel_id, repo_url):
        """Add GitHub repository for updates"""
        settings = self.get_webhook_config(guild_id)
        settings['github']['enabled'] = True
        settings['github']['channel_id'] = channel_id
        
        if repo_url not in settings['github']['repos']:
            settings['github']['repos'].append(repo_url)
        
        self.save_webhook_config(guild_id, settings)
        return True
    
    async def add_youtube_channel(self, guild_id, channel_id, youtube_channel):
        """Add YouTube channel for upload notifications"""
        settings = self.get_webhook_config(guild_id)
        settings['youtube']['enabled'] = True
        settings['youtube']['channel_id'] = channel_id
        
        if youtube_channel not in settings['youtube']['channels']:
            settings['youtube']['channels'].append(youtube_channel)
        
        self.save_webhook_config(guild_id, settings)
        return True
    
    async def add_twitch_streamer(self, guild_id, channel_id, twitch_username):
        """Add Twitch streamer for live notifications"""
        settings = self.get_webhook_config(guild_id)
        settings['twitch']['enabled'] = True
        settings['twitch']['channel_id'] = channel_id
        
        if twitch_username not in settings['twitch']['streamers']:
            settings['twitch']['streamers'].append(twitch_username)
        
        self.save_webhook_config(guild_id, settings)
        return True

async def setup(bot):
    await bot.add_cog(Webhooks(bot))

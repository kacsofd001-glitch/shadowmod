import discord
from discord.ext import commands
import config

class ModMail(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    def get_modmail_config(self, guild_id):
        """Get modmail settings"""
        cfg = config.load_config()
        modmail = cfg.get('modmail', {})
        return modmail.get(str(guild_id), {
            'enabled': False,
            'category_id': None,
            'active_tickets': {}
        })
    
    def save_modmail_config(self, guild_id, settings):
        """Save modmail settings"""
        cfg = config.load_config()
        if 'modmail' not in cfg:
            cfg['modmail'] = {}
        cfg['modmail'][str(guild_id)] = settings
        config.save_config(cfg)
    
    @commands.Cog.listener()
    async def on_message(self, message):
        # Ignore bots
        if message.author.bot:
            return
        
        # ============ CASE 1: User sends DM to bot ============
        if not message.guild and message.author != self.bot.user:
            # User sent DM to bot - check all guilds for modmail
            for guild in self.bot.guilds:
                member = guild.get_member(message.author.id)
                if not member:
                    continue
                
                settings = self.get_modmail_config(guild.id)
                if not settings['enabled']:
                    continue
                
                user_key = str(message.author.id)
                
                # Check if user has active ticket
                if user_key in settings['active_tickets']:
                    channel_id = settings['active_tickets'][user_key]
                    channel = guild.get_channel(channel_id)
                    
                    if channel:
                        embed = discord.Embed(
                            description=message.content,
                            color=0x00F3FF,
                            timestamp=discord.utils.utcnow()
                        )
                        embed.set_author(name=f"{message.author.name} (User)", icon_url=message.author.display_avatar.url)
                        embed.set_footer(text=f"ID: {message.author.id}")
                        
                        if message.attachments:
                            embed.set_image(url=message.attachments[0].url)
                        
                        await channel.send(embed=embed)
                        await message.add_reaction('✅')
                        return
                
                # Create new ticket
                category = guild.get_channel(settings['category_id'])
                if not category:
                    continue
                
                channel = await guild.create_text_channel(
                    name=f"modmail-{message.author.name}",
                    category=category,
                    topic=f"ModMail ticket for {message.author.name} ({message.author.id})"
                )
                
                settings['active_tickets'][user_key] = channel.id
                self.save_modmail_config(guild.id, settings)
                
                # Send opening message
                embed = discord.Embed(
                    title="📬 New ModMail Ticket",
                    description=f"**User:** {message.author.mention} ({message.author.name})\n**ID:** {message.author.id}",
                    color=0x00F3FF
                )
                embed.add_field(name="How to Reply", value="Just message in this channel - your reply will be sent to the user's DMs!")
                await channel.send(embed=embed)
                
                # Send first message
                msg_embed = discord.Embed(
                    description=message.content,
                    color=0x00F3FF,
                    timestamp=discord.utils.utcnow()
                )
                msg_embed.set_author(name=f"{message.author.name} (User)", icon_url=message.author.display_avatar.url)
                await channel.send(embed=msg_embed)
                
                # Confirm to user
                await message.add_reaction('✅')
                await message.author.send("✅ Your message has been sent to the server staff! They will respond soon.")
                return
        
        # ============ CASE 2: Staff replies in modmail channel ============
        if message.guild:
            # Check if this is a modmail channel
            for guild in self.bot.guilds:
                if guild.id != message.guild.id:
                    continue
                
                settings = self.get_modmail_config(guild.id)
                if not settings['enabled']:
                    return
                
                # Find if this message is in a modmail channel
                user_id = None
                for uid_str, ch_id in settings['active_tickets'].items():
                    if ch_id == message.channel.id:
                        user_id = int(uid_str)
                        break
                
                if not user_id:
                    return
                
                # This is a modmail channel - relay message to user
                try:
                    user = await self.bot.fetch_user(user_id)
                    
                    # Create embed for user DM
                    embed = discord.Embed(
                        description=message.content,
                        color=0x00F3FF,
                        timestamp=discord.utils.utcnow()
                    )
                    embed.set_author(name=f"{message.author.name} (Staff)", icon_url=message.author.display_avatar.url)
                    embed.set_footer(text=f"Server: {message.guild.name}")
                    
                    if message.attachments:
                        embed.set_image(url=message.attachments[0].url)
                    
                    await user.send(embed=embed)
                    await message.add_reaction('✉️')
                    
                except discord.Forbidden:
                    embed = discord.Embed(
                        title="❌ Could not send DM",
                        description=f"User {user_id} has DMs disabled or blocked the bot.",
                        color=0xFF0000
                    )
                    await message.channel.send(embed=embed)
                except Exception as e:
                    print(f"❌ Error sending modmail reply: {e}")

async def setup(bot):
    await bot.add_cog(ModMail(bot))

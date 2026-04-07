import discord
from discord.ext import commands
from discord import app_commands
import config

class ModMail(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.command(name="modmail_setup", description="Set up modmail for this server")
    @app_commands.checks.has_permissions(administrator=True)
    async def modmail_setup(self, interaction: discord.Interaction, category: discord.CategoryChannel):
        """Set up modmail category for this server only"""
        # Only works in guilds, not DMs
        if not interaction.guild:
            await interaction.response.send_message("❌ This command can only be used in servers!", ephemeral=True)
            return
        
        settings = self.get_modmail_config(interaction.guild.id)
        settings['enabled'] = True
        settings['category_id'] = category.id
        self.save_modmail_config(interaction.guild.id, settings)
        
        embed = discord.Embed(
            title="✅ ModMail Enabled",
            description=f"ModMail has been set up for **{interaction.guild.name}** only!\n\nCategory: {category.mention}",
            color=0x00F3FF
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)
    
    @app_commands.command(name="modmail_disable", description="Disable modmail for this server")
    @app_commands.checks.has_permissions(administrator=True)
    async def modmail_disable(self, interaction: discord.Interaction):
        """Disable modmail for this server only"""
        if not interaction.guild:
            await interaction.response.send_message("❌ This command can only be used in servers!", ephemeral=True)
            return
        
        settings = self.get_modmail_config(interaction.guild.id)
        settings['enabled'] = False
        self.save_modmail_config(interaction.guild.id, settings)
        
        embed = discord.Embed(
            title="✅ ModMail Disabled",
            description=f"ModMail has been disabled for **{interaction.guild.name}**.",
            color=0xFF0000
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)
    
    @app_commands.command(name="modmail_status", description="Check modmail status for this server")
    @app_commands.checks.has_permissions(administrator=True)
    async def modmail_status(self, interaction: discord.Interaction):
        """Check modmail status for this server only"""
        if not interaction.guild:
            await interaction.response.send_message("❌ This command can only be used in servers!", ephemeral=True)
            return
        
        settings = self.get_modmail_config(interaction.guild.id)
        status = "✅ Enabled" if settings['enabled'] else "❌ Disabled"
        category_info = f"<#{settings['category_id']}>" if settings['category_id'] else "Not set"
        ticket_count = len(settings.get('active_tickets', {}))
        
        embed = discord.Embed(
            title="ModMail Status for this Server",
            color=0x00F3FF
        )
        embed.add_field(name="Status", value=status, inline=False)
        embed.add_field(name="Category", value=category_info, inline=False)
        embed.add_field(name="Active Tickets", value=str(ticket_count), inline=False)
        
        await interaction.response.send_message(embed=embed, ephemeral=True)
    
    @app_commands.command(name="close-modmail", description="Close a completed modmail ticket")
    @app_commands.checks.has_permissions(administrator=True)
    async def close_modmail(self, interaction: discord.Interaction):
        """Close the current modmail ticket"""
        if not interaction.guild:
            await interaction.response.send_message("❌ This command can only be used in servers!", ephemeral=True)
            return
        
        settings = self.get_modmail_config(interaction.guild.id)
        
        # Find if this channel is a modmail ticket
        user_id = None
        user_key = None
        for uid_str, ch_id in settings['active_tickets'].items():
            if ch_id == interaction.channel_id:
                user_id = int(uid_str)
                user_key = uid_str
                break
        
        if not user_id:
            await interaction.response.send_message(
                "❌ This is not a modmail channel!",
                ephemeral=True
            )
            return
        
        try:
            # Get the user to notify them
            user = await self.bot.fetch_user(user_id)
            
            # Notify user
            close_embed = discord.Embed(
                title="📬 ModMail Ticket Closed",
                description=f"Your support ticket with **{interaction.guild.name}** has been closed.",
                color=0xFF0000
            )
            try:
                await user.send(embed=close_embed)
            except:
                pass
            
            # Remove from active tickets
            del settings['active_tickets'][user_key]
            self.save_modmail_config(interaction.guild.id, settings)
            
            # Respond to staff
            embed = discord.Embed(
                title="✅ Ticket Closed",
                description=f"ModMail ticket for {user.mention} has been closed and removed from tracking.",
                color=0x00F3FF
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            print(f"✅ ModMail: Closed ticket for {user_id}")
            
        except Exception as e:
            embed = discord.Embed(
                title="❌ Error",
                description=f"Failed to close ticket: {str(e)}",
                color=0xFF0000
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            print(f"❌ ModMail Close Error: {e}")
    
    
    async def cog_app_command_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        """Handle command errors"""
        if isinstance(error, app_commands.MissingPermissions):
            await interaction.response.send_message(
                "❌ You need administrator permissions to use this command!",
                ephemeral=True
            )
        else:
            await interaction.response.send_message(
                f"❌ Error: {str(error)}",
                ephemeral=True
            )
    
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
            # User sent DM to bot - check only the FIRST guild with modmail enabled
            for guild in self.bot.guilds:
                member = guild.get_member(message.author.id)
                if not member:
                    continue
                
                settings = self.get_modmail_config(guild.id)
                if not settings['enabled']:
                    continue
                
                # Found a guild with modmail - handle ticket for ONLY this guild, then stop
                user_key = str(message.author.id)
                
                # Check if user has active ticket in THIS guild
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
                
                # Create NEW ticket ONLY in this guild
                category = guild.get_channel(settings['category_id'])
                if category:
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
                    
                    # Send first user message
                    msg_embed = discord.Embed(
                        description=message.content,
                        color=0x00F3FF,
                        timestamp=discord.utils.utcnow()
                    )
                    msg_embed.set_author(name=f"{message.author.name} (User)", icon_url=message.author.display_avatar.url)
                    await channel.send(embed=msg_embed)
                    
                    # Confirm to user
                    await message.add_reaction('✅')
                    try:
                        await message.author.send("✅ Your message has been sent to the server staff! They will respond soon.")
                    except:
                        pass
                
                # STOP after handling this guild - don't process other guilds
                return
        
        # ============ CASE 2: Staff replies in modmail channel ============
        if message.guild:
            # Check if this message is in a modmail channel
            settings = self.get_modmail_config(message.guild.id)
            
            if not settings['enabled']:
                return
            
            # Find if this message is in a modmail channel
            user_id = None
            for uid_str, ch_id in settings['active_tickets'].items():
                if ch_id == message.channel.id:
                    user_id = int(uid_str)
                    break
            
            # Not a modmail channel, ignore
            if not user_id:
                return
            
            # This IS a modmail channel - relay staff message to the user
            try:
                user = await self.bot.fetch_user(user_id)
                
                # Create embed for user DM
                embed = discord.Embed(
                    description=message.content if message.content else "(no text)",
                    color=0x00F3FF,
                    timestamp=discord.utils.utcnow()
                )
                embed.set_author(name=f"{message.author.name} (Staff Reply)", icon_url=message.author.display_avatar.url)
                embed.set_footer(text=f"Server: {message.guild.name}")
                
                if message.attachments:
                    embed.set_image(url=message.attachments[0].url)
                
                await user.send(embed=embed)
                await message.add_reaction('✉️')
                print(f"✅ ModMail: Sent reply from {message.author.name} to {user_id}")
                
            except discord.Forbidden:
                # User has DMs closed
                embed = discord.Embed(
                    title="❌ DMs Closed",
                    description=f"Could not send DM to user {user_id} - they may have DMs disabled.",
                    color=0xFF0000
                )
                try:
                    await message.channel.send(embed=embed, delete_after=10)
                except:
                    pass
                    
            except Exception as e:
                print(f"❌ ModMail Error: {e}")

async def setup(bot):
    await bot.add_cog(ModMail(bot))

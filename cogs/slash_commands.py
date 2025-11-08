import discord
from discord import app_commands
from discord.ext import commands
import config
import translations
from datetime import datetime, timezone, timedelta

class SlashCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.command(name="help", description="Show all bot commands / Összes parancs megjelenítése")
    async def slash_help(self, interaction: discord.Interaction):
        guild_id = interaction.guild.id
        
        embed = discord.Embed(
            title=translations.get_text(guild_id, 'help_title'),
            description=translations.get_text(guild_id, 'help_description'),
            color=discord.Color.blue()
        )
        
        embed.add_field(
            name=translations.get_text(guild_id, 'help_tickets'),
            value=translations.get_text(guild_id, 'help_tickets_desc'),
            inline=False
        )
        
        embed.add_field(
            name=translations.get_text(guild_id, 'help_moderation'),
            value=translations.get_text(guild_id, 'help_moderation_desc'),
            inline=False
        )
        
        embed.add_field(
            name=translations.get_text(guild_id, 'help_games'),
            value=translations.get_text(guild_id, 'help_games_desc'),
            inline=False
        )
        
        embed.add_field(
            name=translations.get_text(guild_id, 'help_fun'),
            value=translations.get_text(guild_id, 'help_fun_desc'),
            inline=False
        )
        
        embed.add_field(
            name=translations.get_text(guild_id, 'help_polls_roles'),
            value=translations.get_text(guild_id, 'help_polls_roles_desc'),
            inline=False
        )
        
        embed.add_field(
            name=translations.get_text(guild_id, 'help_giveaways'),
            value=translations.get_text(guild_id, 'help_giveaways_desc'),
            inline=False
        )
        
        embed.add_field(
            name=translations.get_text(guild_id, 'help_config'),
            value=translations.get_text(guild_id, 'help_config_desc'),
            inline=False
        )
        
        embed.set_footer(text=translations.get_text(guild_id, 'help_footer'))
        
        await interaction.response.send_message(embed=embed, ephemeral=True)
    
    @app_commands.command(name="ticket", description="Create a ticket panel / Jegy panel létrehozása")
    @app_commands.checks.has_permissions(administrator=True)
    async def slash_ticket(self, interaction: discord.Interaction):
        ticket_cog = self.bot.get_cog('Tickets')
        if ticket_cog:
            view = ticket_cog.TicketView()
            self.bot.add_view(view)
            
            guild_id = interaction.guild.id
            
            embed = discord.Embed(
                title=translations.get_text(guild_id, 'ticket_title'),
                description=translations.get_text(guild_id, 'ticket_description'),
                color=discord.Color.blue()
            )
            embed.add_field(
                name=translations.get_text(guild_id, 'ticket_how_it_works'),
                value=translations.get_text(guild_id, 'ticket_steps'),
                inline=False
            )
            
            await interaction.response.send_message(embed=embed, view=view)
    
    @app_commands.command(name="meme", description="Get a random meme / Véletlen meme lekérése")
    async def slash_meme(self, interaction: discord.Interaction):
        import random
        from urllib.parse import quote
        import aiohttp
        
        guild_id = interaction.guild.id
        lang = translations.get_guild_language(guild_id)
        
        fun_cog = self.bot.get_cog('Fun')
        if not fun_cog:
            await interaction.response.send_message("❌ Meme feature unavailable", ephemeral=True)
            return
        
        templates = fun_cog.meme_templates_hu if lang == 'hu' else fun_cog.meme_templates_en
        template_name, top_text, bottom_text = random.choice(templates)
        
        top_text_encoded = quote(top_text, safe='')
        bottom_text_encoded = quote(bottom_text, safe='')
        
        meme_url = f"https://api.memegen.link/images/{template_name}/{top_text_encoded}/{bottom_text_encoded}.png"
        
        await interaction.response.defer()
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.head(meme_url, timeout=aiohttp.ClientTimeout(total=5)) as response:
                    if response.status != 200:
                        raise Exception("Meme API unavailable")
            
            embed = discord.Embed(
                title=translations.get_text(guild_id, 'meme_title'),
                color=discord.Color.random()
            )
            embed.set_image(url=meme_url)
            embed.set_footer(text=translations.get_text(guild_id, 'generated_meme'))
            
            await interaction.followup.send(embed=embed)
        except Exception:
            embed = discord.Embed(
                title=translations.get_text(guild_id, 'meme_title'),
                description=f"**{top_text}**\n\n*{bottom_text}*",
                color=discord.Color.random()
            )
            embed.set_footer(text=translations.get_text(guild_id, 'generated_meme'))
            await interaction.followup.send(embed=embed)
    
    @app_commands.command(name="8ball", description="Ask the magic 8-ball / Kérdezd a varázs labdát")
    @app_commands.describe(question="Your question / A kérdésed")
    async def slash_8ball(self, interaction: discord.Interaction, question: str):
        import random
        
        guild_id = interaction.guild.id
        responses = translations.get_text(guild_id, '8ball_responses')
        
        embed = discord.Embed(
            title=translations.get_text(guild_id, 'magic_8ball'),
            color=discord.Color.purple()
        )
        embed.add_field(name=translations.get_text(guild_id, 'question'), value=question, inline=False)
        embed.add_field(name=translations.get_text(guild_id, 'answer'), value=random.choice(responses), inline=False)
        
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name="coinflip", description="Flip a coin / Pénzfeldobás")
    async def slash_coinflip(self, interaction: discord.Interaction):
        import random
        
        guild_id = interaction.guild.id
        lang = translations.get_guild_language(guild_id)
        
        result_key = 'heads' if random.choice([True, False]) else 'tails'
        result = translations.get_text(guild_id, result_key)
        
        embed = discord.Embed(
            title=translations.get_text(guild_id, 'coin_flip'),
            description=translations.get_text(guild_id, 'coin_result', result),
            color=discord.Color.gold()
        )
        
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name="ban", description="Ban a user / Felhasználó kitiltása")
    @app_commands.describe(user="User mention or ID / Felhasználó mention vagy ID", reason="Reason / Indok")
    @app_commands.checks.has_permissions(ban_members=True)
    async def slash_ban(self, interaction: discord.Interaction, user: str, reason: str = None):
        guild_id = interaction.guild.id
        
        try:
            # Try to convert string to user ID or extract from mention
            user_id = None
            if user.startswith('<@') and user.endswith('>'):
                user_id = int(user.strip('<@!>'))
            else:
                try:
                    user_id = int(user)
                except ValueError:
                    await interaction.response.send_message(translations.get_text(guild_id, 'invalid_user'), ephemeral=True)
                    return
            
            # Fetch the user
            try:
                target_user = await interaction.guild.fetch_member(user_id)
            except:
                target_user = await self.bot.fetch_user(user_id)
            
            await interaction.guild.ban(target_user, reason=reason)
            
            embed = discord.Embed(
                title=translations.get_text(guild_id, 'user_banned'),
                description=translations.get_text(guild_id, 'user_banned_desc', target_user.mention),
                color=discord.Color.red()
            )
            if reason:
                embed.add_field(name=translations.get_text(guild_id, 'reason'), value=reason, inline=False)
            embed.add_field(name=translations.get_text(guild_id, 'moderator'), value=interaction.user.mention, inline=True)
            
            await interaction.response.send_message(embed=embed)
        except Exception as e:
            await interaction.response.send_message(translations.get_text(guild_id, 'ban_failed', str(e)), ephemeral=True)
    
    @app_commands.command(name="kick", description="Kick a user / Felhasználó kirúgása")
    @app_commands.describe(user="User mention or ID / Felhasználó mention vagy ID", reason="Reason / Indok")
    @app_commands.checks.has_permissions(kick_members=True)
    async def slash_kick(self, interaction: discord.Interaction, user: str, reason: str = None):
        guild_id = interaction.guild.id
        
        try:
            # Try to convert string to user ID or extract from mention
            user_id = None
            if user.startswith('<@') and user.endswith('>'):
                user_id = int(user.strip('<@!>'))
            else:
                try:
                    user_id = int(user)
                except ValueError:
                    await interaction.response.send_message(translations.get_text(guild_id, 'invalid_user'), ephemeral=True)
                    return
            
            # Fetch the member
            target_user = await interaction.guild.fetch_member(user_id)
            
            await target_user.kick(reason=reason)
            
            embed = discord.Embed(
                title=translations.get_text(guild_id, 'user_kicked'),
                description=translations.get_text(guild_id, 'user_kicked_desc', target_user.mention),
                color=discord.Color.orange()
            )
            if reason:
                embed.add_field(name=translations.get_text(guild_id, 'reason'), value=reason, inline=False)
            embed.add_field(name=translations.get_text(guild_id, 'moderator'), value=interaction.user.mention, inline=True)
            
            await interaction.response.send_message(embed=embed)
        except Exception as e:
            await interaction.response.send_message(translations.get_text(guild_id, 'kick_failed', str(e)), ephemeral=True)
    
    @app_commands.command(name="mute", description="Mute a user / Felhasználó némítása")
    @app_commands.describe(user="User mention or ID / Felhasználó mention vagy ID")
    @app_commands.checks.has_permissions(manage_roles=True)
    async def slash_mute(self, interaction: discord.Interaction, user: str):
        guild_id_int = interaction.guild.id
        guild_id = str(guild_id_int)
        
        try:
            # Try to convert string to user ID or extract from mention
            user_id = None
            if user.startswith('<@') and user.endswith('>'):
                user_id = int(user.strip('<@!>'))
            else:
                try:
                    user_id = int(user)
                except ValueError:
                    await interaction.response.send_message(translations.get_text(guild_id_int, 'invalid_user'), ephemeral=True)
                    return
            
            # Fetch the member
            target_user = await interaction.guild.fetch_member(user_id)
            
            cfg = config.load_config()
            muted_role_id = cfg.get('muted_roles', {}).get(guild_id)
            
            if not muted_role_id:
                muted_role = await interaction.guild.create_role(name="Muted", color=discord.Color.dark_gray())
                cfg.setdefault('muted_roles', {})[guild_id] = muted_role.id
                config.save_config(cfg)
                
                for channel in interaction.guild.channels:
                    await channel.set_permissions(muted_role, send_messages=False, speak=False)
            else:
                muted_role = interaction.guild.get_role(muted_role_id)
            
            await target_user.add_roles(muted_role)
            
            embed = discord.Embed(
                title=translations.get_text(guild_id_int, 'user_muted'),
                description=translations.get_text(guild_id_int, 'user_muted_desc', target_user.mention),
                color=discord.Color.dark_gray()
            )
            
            await interaction.response.send_message(embed=embed)
        except Exception as e:
            await interaction.response.send_message(f"❌ Error: {str(e)}", ephemeral=True)
    
    @app_commands.command(name="unmute", description="Unmute a user / Felhasználó visszahangosítása")
    @app_commands.describe(user="User mention or ID / Felhasználó mention vagy ID")
    @app_commands.checks.has_permissions(manage_roles=True)
    async def slash_unmute(self, interaction: discord.Interaction, user: str):
        guild_id_int = interaction.guild.id
        guild_id = str(guild_id_int)
        
        try:
            # Try to convert string to user ID or extract from mention
            user_id = None
            if user.startswith('<@') and user.endswith('>'):
                user_id = int(user.strip('<@!>'))
            else:
                try:
                    user_id = int(user)
                except ValueError:
                    await interaction.response.send_message(translations.get_text(guild_id_int, 'invalid_user'), ephemeral=True)
                    return
            
            # Fetch the member
            target_user = await interaction.guild.fetch_member(user_id)
            
            cfg = config.load_config()
            muted_role_id = cfg.get('muted_roles', {}).get(guild_id)
            
            if not muted_role_id:
                await interaction.response.send_message(translations.get_text(guild_id_int, 'no_muted_role'), ephemeral=True)
                return
            
            muted_role = interaction.guild.get_role(muted_role_id)
            if muted_role in target_user.roles:
                await target_user.remove_roles(muted_role)
                
                embed = discord.Embed(
                    title=translations.get_text(guild_id_int, 'user_unmuted'),
                    description=translations.get_text(guild_id_int, 'user_unmuted_desc', target_user.mention),
                    color=discord.Color.green()
                )
                
                await interaction.response.send_message(embed=embed)
            else:
                await interaction.response.send_message(translations.get_text(guild_id_int, 'user_not_muted'), ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"❌ Error: {str(e)}", ephemeral=True)
    
    @app_commands.command(name="lock", description="Lock the channel / Csatorna lezárása")
    @app_commands.checks.has_permissions(manage_channels=True)
    async def slash_lock(self, interaction: discord.Interaction):
        guild_id = interaction.guild.id
        
        await interaction.channel.set_permissions(
            interaction.guild.default_role,
            send_messages=False
        )
        
        embed = discord.Embed(
            title=translations.get_text(guild_id, 'channel_locked'),
            description=translations.get_text(guild_id, 'channel_locked_desc'),
            color=discord.Color.red()
        )
        
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name="unlock", description="Unlock the channel / Csatorna feloldása")
    @app_commands.checks.has_permissions(manage_channels=True)
    async def slash_unlock(self, interaction: discord.Interaction):
        guild_id = interaction.guild.id
        
        await interaction.channel.set_permissions(
            interaction.guild.default_role,
            send_messages=True
        )
        
        embed = discord.Embed(
            title=translations.get_text(guild_id, 'channel_unlocked'),
            description=translations.get_text(guild_id, 'channel_unlocked_desc'),
            color=discord.Color.green()
        )
        
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name="warn", description="Warn a user / Felhasználó figyelmeztetése")
    @app_commands.describe(user="User mention or ID / Felhasználó mention vagy ID", reason="Reason / Indok")
    @app_commands.checks.has_permissions(manage_messages=True)
    async def slash_warn(self, interaction: discord.Interaction, user: str, reason: str = None):
        guild_id = interaction.guild.id
        
        try:
            # Try to convert string to user ID or extract from mention
            user_id_int = None
            if user.startswith('<@') and user.endswith('>'):
                user_id_int = int(user.strip('<@!>'))
            else:
                try:
                    user_id_int = int(user)
                except ValueError:
                    await interaction.response.send_message(translations.get_text(guild_id, 'invalid_user'), ephemeral=True)
                    return
            
            # Fetch the member
            target_user = await interaction.guild.fetch_member(user_id_int)
            
            cfg = config.load_config()
            warnings = cfg.get('warnings', {})
            user_id = str(target_user.id)
            
            if user_id not in warnings:
                warnings[user_id] = []
            
            warnings[user_id].append({
                'reason': reason or translations.get_text(guild_id, 'no_reason_provided'),
                'moderator': str(interaction.user),
                'timestamp': datetime.now(timezone.utc).isoformat()
            })
            
            cfg['warnings'] = warnings
            config.save_config(cfg)
            
            embed = discord.Embed(
                title=translations.get_text(guild_id, 'user_warned'),
                description=translations.get_text(guild_id, 'user_warned_desc', target_user.mention),
                color=discord.Color.yellow()
            )
            embed.add_field(name=translations.get_text(guild_id, 'reason'), value=reason or translations.get_text(guild_id, 'no_reason_provided'), inline=False)
            embed.add_field(name=translations.get_text(guild_id, 'total_warnings'), value=str(len(warnings[user_id])), inline=True)
            
            await interaction.response.send_message(embed=embed)
        except Exception as e:
            await interaction.response.send_message(f"❌ Error: {str(e)}", ephemeral=True)
    
    @app_commands.command(name="setlog", description="Set log channel / Napló csatorna beállítása")
    @app_commands.describe(channel="The channel / A csatorna")
    @app_commands.checks.has_permissions(administrator=True)
    async def slash_setlog(self, interaction: discord.Interaction, channel: discord.TextChannel):
        guild_id = interaction.guild.id
        config.update_config('log_channel_id', channel.id)
        
        embed = discord.Embed(
            title=translations.get_text(guild_id, 'log_channel_set'),
            description=translations.get_text(guild_id, 'log_channel_desc', channel.mention),
            color=discord.Color.green()
        )
        
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name="setwebhook", description="Set webhook for logging / Webhook beállítása")
    @app_commands.describe(webhook_url="Discord webhook URL / Discord webhook URL")
    @app_commands.checks.has_permissions(administrator=True)
    async def slash_setwebhook(self, interaction: discord.Interaction, webhook_url: str):
        guild_id = interaction.guild.id
        webhook_cog = self.bot.get_cog('WebhookLogging')
        if webhook_cog:
            webhook_cog.webhook_url = webhook_url
            config.update_config('webhook_url', webhook_url)
            
            test_embed = discord.Embed(
                title=translations.get_text(guild_id, 'webhook_set'),
                description=translations.get_text(guild_id, 'webhook_set_desc'),
                color=discord.Color.green(),
                timestamp=datetime.now(timezone.utc)
            )
            test_embed.add_field(
                name=translations.get_text(guild_id, 'test_message'),
                value=translations.get_text(guild_id, 'webhook_working'),
                inline=False
            )
            
            await webhook_cog.send_to_webhook(test_embed)
            await interaction.response.send_message(translations.get_text(guild_id, 'webhook_configured'))
    
    @app_commands.command(name="testwebhook", description="Test webhook / Webhook tesztelése")
    @app_commands.checks.has_permissions(administrator=True)
    async def slash_testwebhook(self, interaction: discord.Interaction):
        guild_id = interaction.guild.id
        webhook_cog = self.bot.get_cog('WebhookLogging')
        if webhook_cog:
            test_embed = discord.Embed(
                title=translations.get_text(guild_id, 'webhook_test'),
                description=translations.get_text(guild_id, 'webhook_test_desc'),
                color=discord.Color.blue(),
                timestamp=datetime.now(timezone.utc)
            )
            test_embed.add_field(name=translations.get_text(guild_id, 'tested_by'), value=str(interaction.user), inline=True)
            test_embed.add_field(name=translations.get_text(guild_id, 'channel'), value=interaction.channel.mention, inline=True)
            
            await webhook_cog.send_to_webhook(test_embed)
            await interaction.response.send_message(translations.get_text(guild_id, 'test_webhook_sent'))

async def setup(bot):
    await bot.add_cog(SlashCommands(bot))

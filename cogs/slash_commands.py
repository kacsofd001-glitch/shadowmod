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
            color=0x00F3FF
        )
        
        embed.add_field(
            name=translations.get_text(guild_id, 'help_info'),
            value=translations.get_text(guild_id, 'help_info_desc'),
            inline=False
        )
        
        embed.add_field(
            name=translations.get_text(guild_id, 'help_security'),
            value=translations.get_text(guild_id, 'help_security_desc'),
            inline=False
        )
        
        embed.add_field(
            name=translations.get_text(guild_id, 'help_antialt'),
            value=translations.get_text(guild_id, 'help_antialt_desc'),
            inline=False
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
            name=translations.get_text(guild_id, 'help_music'),
            value=translations.get_text(guild_id, 'help_music_desc'),
            inline=False
        )
        
        embed.add_field(
            name=translations.get_text(guild_id, 'help_games'),
            value=translations.get_text(guild_id, 'help_games_desc'),
            inline=False
        )
        
        embed.add_field(
            name=translations.get_text(guild_id, 'help_engagement'),
            value=translations.get_text(guild_id, 'help_engagement_desc'),
            inline=False
        )
        
        embed.add_field(
            name=translations.get_text(guild_id, 'help_nameauto'),
            value=translations.get_text(guild_id, 'help_nameauto_desc'),
            inline=False
        )
        
        embed.add_field(
            name=translations.get_text(guild_id, 'help_config'),
            value=translations.get_text(guild_id, 'help_config_desc'),
            inline=False
        )
        
        embed.set_footer(text="⚡ Made by MoonlightVFX | 46 Slash Commands Ready ⚡")
        
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
                color=0x8B00FF
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
                color=0xFF006E
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
                color=0xFF006E
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
                    color=0x00F3FF
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
            color=0xFF006E
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
            color=0x00F3FF
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
            color=0x00F3FF
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
                color=0x00F3FF,
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
                color=0x8B00FF,
                timestamp=datetime.now(timezone.utc)
            )
            test_embed.add_field(name=translations.get_text(guild_id, 'tested_by'), value=str(interaction.user), inline=True)
            test_embed.add_field(name=translations.get_text(guild_id, 'channel'), value=interaction.channel.mention, inline=True)
            
            await webhook_cog.send_to_webhook(test_embed)
            await interaction.response.send_message(translations.get_text(guild_id, 'test_webhook_sent'))
    
    @app_commands.command(name="ping", description="Check bot latency / Bot késleltetés ellenőrzése")
    async def slash_ping(self, interaction: discord.Interaction):
        latency = round(self.bot.latency * 1000)
        
        embed = discord.Embed(
            title="🏓 Pong!",
            description=f"Bot latency: **{latency}ms**",
            color=0x00F3FF
        )
        
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name="purge", description="Delete multiple messages / Több üzenet törlése")
    @app_commands.describe(amount="Number of messages to delete (1-100) / Törölni kívánt üzenetek száma")
    @app_commands.checks.has_permissions(manage_messages=True)
    async def slash_purge(self, interaction: discord.Interaction, amount: int):
        import asyncio
        
        guild_id = interaction.guild.id
        
        if amount < 1 or amount > 100:
            await interaction.response.send_message(
                translations.get_text(guild_id, 'purge_invalid'),
                ephemeral=True
            )
            return
        
        await interaction.response.defer(ephemeral=True)
        
        try:
            deleted = await interaction.channel.purge(limit=amount)
            
            embed = discord.Embed(
                title=translations.get_text(guild_id, 'messages_purged'),
                description=translations.get_text(guild_id, 'messages_purged_desc', len(deleted)),
                color=0xFF006E,
                timestamp=datetime.now(timezone.utc)
            )
            embed.add_field(
                name=translations.get_text(guild_id, 'moderator'),
                value=interaction.user.mention
            )
            
            await interaction.followup.send(embed=embed, ephemeral=True)
            
            mod_cog = self.bot.get_cog('Moderation')
            if mod_cog:
                await mod_cog.send_log(embed)
                
        except discord.Forbidden:
            await interaction.followup.send(
                "❌ I don't have permission to delete messages!",
                ephemeral=True
            )
        except Exception as e:
            await interaction.followup.send(
                f"❌ An error occurred: {str(e)}",
                ephemeral=True
            )

    @app_commands.command(name="serverinfo", description="Show server information / Szerver információk megjelenítése")
    async def slash_serverinfo(self, interaction: discord.Interaction):
        info_cog = self.bot.get_cog('Info')
        if info_cog:
            ctx = await self.bot.get_context(interaction)
            ctx.author = interaction.user
            ctx.guild = interaction.guild
            ctx.send = interaction.response.send_message
            await info_cog.serverinfo(ctx)
        else:
            await interaction.response.send_message("❌ Feature unavailable", ephemeral=True)
    
    @app_commands.command(name="botinfo", description="Show bot information / Bot információk megjelenítése")
    async def slash_botinfo(self, interaction: discord.Interaction):
        info_cog = self.bot.get_cog('Info')
        if info_cog:
            ctx = await self.bot.get_context(interaction)
            ctx.author = interaction.user
            ctx.guild = interaction.guild
            ctx.send = interaction.response.send_message
            await info_cog.botinfo(ctx)
        else:
            await interaction.response.send_message("❌ Feature unavailable", ephemeral=True)
    
    @app_commands.command(name="userinfo", description="Show user information / Felhasználó információk megjelenítése")
    async def slash_userinfo(self, interaction: discord.Interaction, member: discord.Member = None):
        info_cog = self.bot.get_cog('Info')
        if info_cog:
            ctx = await self.bot.get_context(interaction)
            ctx.author = interaction.user
            ctx.guild = interaction.guild
            ctx.send = interaction.response.send_message
            await info_cog.userinfo(ctx, member)
        else:
            await interaction.response.send_message("❌ Feature unavailable", ephemeral=True)
    
    @app_commands.command(name="support", description="Get support server invite / Support szerver meghívó")
    async def slash_support(self, interaction: discord.Interaction):
        info_cog = self.bot.get_cog('Info')
        if info_cog:
            ctx = await self.bot.get_context(interaction)
            ctx.author = interaction.user
            ctx.send = interaction.response.send_message
            await info_cog.support(ctx)
        else:
            await interaction.response.send_message("❌ Feature unavailable", ephemeral=True)
    
    @app_commands.command(name="webpage", description="Get web dashboard link / Web irányítópult link")
    async def slash_webpage(self, interaction: discord.Interaction):
        info_cog = self.bot.get_cog('Info')
        if info_cog:
            ctx = await self.bot.get_context(interaction)
            ctx.author = interaction.user
            ctx.send = interaction.response.send_message
            await info_cog.webpage(ctx)
        else:
            await interaction.response.send_message("❌ Feature unavailable", ephemeral=True)
    
    @app_commands.command(name="setprefix", description="Set role prefix for nicknames / Szerep prefix beállítása")
    @app_commands.describe(role="The role to set prefix for / Szerep", prefix="Prefix text (max 10 chars) / Prefix szöveg")
    @app_commands.checks.has_permissions(administrator=True)
    async def slash_setprefix(self, interaction: discord.Interaction, role: discord.Role, prefix: str):
        nameauto_cog = self.bot.get_cog('NameAutomation')
        if nameauto_cog:
            if len(prefix) > 10:
                await interaction.response.send_message("❌ Prefix must be 10 characters or less!", ephemeral=True)
                return
            
            import config as cfg_module
            cfg = cfg_module.load_config()
            if 'role_prefixes' not in cfg:
                cfg['role_prefixes'] = {}
            
            cfg['role_prefixes'][str(role.id)] = prefix
            cfg_module.save_config(cfg)
            
            embed = discord.Embed(
                title="✅ Prefix Set",
                description=f"Members with {role.mention} will have `{prefix}` prefix in their nickname!",
                color=0x00F3FF
            )
            embed.add_field(name="Example", value=f"{prefix} Username", inline=False)
            
            await interaction.response.send_message(embed=embed)
            
            await interaction.followup.send("🔄 Updating member nicknames...", ephemeral=True)
            count = 0
            for member in interaction.guild.members:
                if role in member.roles:
                    await nameauto_cog.update_member_nickname(member)
                    count += 1
            
            embed.add_field(name="Updated", value=f"{count} members updated!", inline=False)
            await interaction.edit_original_response(embed=embed)
        else:
            await interaction.response.send_message("❌ Feature unavailable", ephemeral=True)
    
    @app_commands.command(name="removeprefix", description="Remove role prefix / Szerep prefix eltávolítása")
    @app_commands.describe(role="The role to remove prefix from / Szerep")
    @app_commands.checks.has_permissions(administrator=True)
    async def slash_removeprefix(self, interaction: discord.Interaction, role: discord.Role):
        nameauto_cog = self.bot.get_cog('NameAutomation')
        if nameauto_cog:
            import config as cfg_module
            cfg = cfg_module.load_config()
            role_prefixes = cfg.get('role_prefixes', {})
            
            if str(role.id) not in role_prefixes:
                await interaction.response.send_message(f"❌ {role.mention} doesn't have a prefix set!", ephemeral=True)
                return
            
            del cfg['role_prefixes'][str(role.id)]
            cfg_module.save_config(cfg)
            
            embed = discord.Embed(
                title="✅ Prefix Removed",
                description=f"Prefix removed from {role.mention}",
                color=0x00F3FF
            )
            
            await interaction.response.send_message(embed=embed)
            
            await interaction.followup.send("🔄 Updating member nicknames...", ephemeral=True)
            count = 0
            for member in interaction.guild.members:
                if role in member.roles:
                    await nameauto_cog.update_member_nickname(member)
                    count += 1
            
            embed.add_field(name="Updated", value=f"{count} members updated!", inline=False)
            await interaction.edit_original_response(embed=embed)
        else:
            await interaction.response.send_message("❌ Feature unavailable", ephemeral=True)
    
    @app_commands.command(name="viewprefixes", description="View all role prefixes / Összes szerep prefix megtekintése")
    async def slash_viewprefixes(self, interaction: discord.Interaction):
        import config as cfg_module
        cfg = cfg_module.load_config()
        role_prefixes = cfg.get('role_prefixes', {})
        
        if not role_prefixes:
            await interaction.response.send_message("❌ No role prefixes configured!", ephemeral=True)
            return
        
        embed = discord.Embed(
            title="📋 Role Prefixes",
            description="Current role prefix configuration:",
            color=0x8B00FF
        )
        
        for role_id, prefix in role_prefixes.items():
            role = interaction.guild.get_role(int(role_id))
            if role:
                embed.add_field(
                    name=role.name,
                    value=f"Prefix: `{prefix}`",
                    inline=False
                )
        
        await interaction.response.send_message(embed=embed, ephemeral=True)
    
    @app_commands.command(name="setaltage", description="Set minimum account age / Minimális fiók kor beállítása")
    @app_commands.describe(days="Minimum account age in days / Minimális fiók kor napokban")
    @app_commands.checks.has_permissions(administrator=True)
    async def slash_setaltage(self, interaction: discord.Interaction, days: int):
        if days < 0:
            await interaction.response.send_message("❌ Days must be a positive number!", ephemeral=True)
            return
        
        import config as cfg_module
        cfg_module.update_config('min_account_age_days', days)
        
        embed = discord.Embed(
            title="✅ Anti-Alt Configuration Updated",
            description=f"Minimum account age set to **{days} days**",
            color=0x00F3FF
        )
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name="tempmute", description="Temporarily mute a user / Felhasználó ideiglenes némítása")
    @app_commands.describe(
        user="User to mute / Némítandó felhasználó",
        duration="Duration (e.g., 1h, 30m, 1d) / Időtartam"
    )
    @app_commands.checks.has_permissions(moderate_members=True)
    async def slash_tempmute(self, interaction: discord.Interaction, user: discord.Member, duration: str):
        moderation_cog = self.bot.get_cog('Moderation')
        if moderation_cog:
            try:
                time_dict = moderation_cog.parse_time(duration)
                delta = timedelta(**time_dict)
                
                if delta.total_seconds() > 2419200:
                    await interaction.response.send_message("❌ Maximum timeout duration is 28 days!", ephemeral=True)
                    return
                
                await user.timeout(delta, reason=f"Timed out by {interaction.user}")
                
                embed = discord.Embed(
                    title="🔇 User Timed Out",
                    description=f"{user.mention} has been timed out",
                    color=0xFF006E
                )
                embed.add_field(name="Duration", value=duration, inline=True)
                embed.add_field(name="Moderator", value=interaction.user.mention, inline=True)
                
                await interaction.response.send_message(embed=embed)
            except ValueError as e:
                await interaction.response.send_message(f"❌ Invalid time format! Use: 1h, 30m, 1d, etc.", ephemeral=True)
        else:
            await interaction.response.send_message("❌ Feature unavailable", ephemeral=True)
    
    @app_commands.command(name="dice", description="Roll a dice / Kockadobás")
    @app_commands.describe(sides="Number of sides (default: 6) / Oldalak száma")
    async def slash_dice(self, interaction: discord.Interaction, sides: int = 6):
        fun_cog = self.bot.get_cog('Fun')
        if fun_cog:
            await interaction.response.defer()
            
            import random
            result = random.randint(1, sides)
            
            embed = discord.Embed(
                title="🎲 Dice Roll",
                description=f"You rolled a **{result}** on a {sides}-sided dice!",
                color=0x8B00FF
            )
            embed.set_footer(text=f"Rolled by {interaction.user.display_name}")
            
            await interaction.followup.send(embed=embed)
        else:
            await interaction.response.send_message("❌ Feature unavailable", ephemeral=True)
    
    @app_commands.command(name="rps", description="Play Rock-Paper-Scissors / Kő-Papír-Olló játék")
    @app_commands.describe(choice="Your choice / Választásod")
    @app_commands.choices(choice=[
        app_commands.Choice(name="🪨 Rock / Kő", value="rock"),
        app_commands.Choice(name="📄 Paper / Papír", value="paper"),
        app_commands.Choice(name="✂️ Scissors / Olló", value="scissors")
    ])
    async def slash_rps(self, interaction: discord.Interaction, choice: str):
        games_cog = self.bot.get_cog('Games')
        if games_cog:
            import random
            
            choices = ['rock', 'paper', 'scissors']
            bot_choice = random.choice(choices)
            
            emoji_map = {'rock': '🪨', 'paper': '📄', 'scissors': '✂️'}
            
            if choice == bot_choice:
                result = "It's a tie!"
                color = 0x8B00FF
            elif (choice == 'rock' and bot_choice == 'scissors') or \
                 (choice == 'paper' and bot_choice == 'rock') or \
                 (choice == 'scissors' and bot_choice == 'paper'):
                result = "You win!"
                color = 0x00F3FF
            else:
                result = "I win!"
                color = 0xFF006E
            
            embed = discord.Embed(
                title="🎮 Rock-Paper-Scissors",
                description=f"**You:** {emoji_map[choice]}\n**Bot:** {emoji_map[bot_choice]}\n\n**{result}**",
                color=color
            )
            
            await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message("❌ Feature unavailable", ephemeral=True)
    
    @app_commands.command(name="tictactoe", description="Play Tic-Tac-Toe / Amőba játék")
    @app_commands.describe(opponent="Player to challenge / Kihívandó játékos")
    async def slash_tictactoe(self, interaction: discord.Interaction, opponent: discord.Member):
        games_cog = self.bot.get_cog('Games')
        if games_cog:
            if opponent == interaction.user:
                await interaction.response.send_message("❌ You can't play against yourself!", ephemeral=True)
                return
            
            if opponent.bot:
                await interaction.response.send_message("❌ You can't play against a bot!", ephemeral=True)
                return
            
            view = games_cog.TicTacToeView(interaction.user, opponent)
            
            embed = discord.Embed(
                title="⭕ Tic-Tac-Toe",
                description=f"{interaction.user.mention} vs {opponent.mention}\n\n{interaction.user.mention}'s turn (⭕)",
                color=0x8B00FF
            )
            
            await interaction.response.send_message(embed=embed, view=view)
        else:
            await interaction.response.send_message("❌ Feature unavailable", ephemeral=True)
    
    @app_commands.command(name="poll", description="Create a poll / Szavazás létrehozása")
    @app_commands.describe(
        question="Poll question / Kérdés",
        option1="First option / Első lehetőség",
        option2="Second option / Második lehetőség",
        option3="Third option (optional) / Harmadik lehetőség",
        option4="Fourth option (optional) / Negyedik lehetőség"
    )
    async def slash_poll(self, interaction: discord.Interaction, question: str, option1: str, option2: str, 
                        option3: str = None, option4: str = None):
        polls_cog = self.bot.get_cog('Polls')
        if polls_cog:
            options = [option1, option2]
            if option3:
                options.append(option3)
            if option4:
                options.append(option4)
            
            view = polls_cog.PollView(options)
            
            embed = discord.Embed(
                title="📊 " + question,
                description="Click the buttons below to vote!",
                color=0x8B00FF
            )
            
            for i, option in enumerate(options, 1):
                embed.add_field(name=f"Option {i}", value=option, inline=False)
            
            embed.set_footer(text=f"Poll by {interaction.user.display_name}")
            
            await interaction.response.send_message(embed=embed, view=view)
        else:
            await interaction.response.send_message("❌ Feature unavailable", ephemeral=True)
    
    @app_commands.command(name="giveaway", description="Create a giveaway / Nyereményjáték létrehozása")
    @app_commands.describe(
        prize="Prize to give away / Nyeremény",
        duration="Duration (e.g., 1h, 1d) / Időtartam",
        winners="Number of winners / Nyertesek száma"
    )
    @app_commands.checks.has_permissions(manage_guild=True)
    async def slash_giveaway(self, interaction: discord.Interaction, prize: str, duration: str, winners: int = 1):
        giveaway_cog = self.bot.get_cog('Giveaways')
        if giveaway_cog:
            try:
                time_dict = giveaway_cog.parse_time(duration)
                end_time = datetime.now(timezone.utc) + timedelta(**time_dict)
                
                embed = discord.Embed(
                    title="🎁 GIVEAWAY",
                    description=f"**Prize:** {prize}\n**Winners:** {winners}\n**Ends:** <t:{int(end_time.timestamp())}:R>",
                    color=0xFF006E
                )
                embed.set_footer(text=f"Hosted by {interaction.user.display_name}")
                
                from datetime import datetime, timezone
                giveaway_id = f"giveaway_{interaction.channel.id}_{int(datetime.now(timezone.utc).timestamp())}"
                view = giveaway_cog.GiveawayView(end_time, winners, prize, giveaway_id)
                
                await interaction.response.send_message(embed=embed, view=view)
                
                message = await interaction.original_response()
                self.bot.loop.create_task(giveaway_cog.end_giveaway(message, end_time, winners, prize))
            except ValueError:
                await interaction.response.send_message("❌ Invalid time format! Use: 1h, 30m, 1d, etc.", ephemeral=True)
        else:
            await interaction.response.send_message("❌ Feature unavailable", ephemeral=True)
    
    @app_commands.command(name="createrole", description="Create a new role / Új szerep létrehozása")
    @app_commands.describe(
        name="Role name / Szerep neve",
        color="Hex color (e.g., #FF0000) / Szín"
    )
    @app_commands.checks.has_permissions(manage_roles=True)
    async def slash_createrole(self, interaction: discord.Interaction, name: str, color: str = None):
        try:
            role_color = discord.Color.default()
            if color:
                color = color.lstrip('#')
                role_color = discord.Color(int(color, 16))
            
            role = await interaction.guild.create_role(name=name, color=role_color)
            
            embed = discord.Embed(
                title="✅ Role Created",
                description=f"Role {role.mention} has been created!",
                color=0x00F3FF
            )
            
            await interaction.response.send_message(embed=embed)
        except ValueError:
            await interaction.response.send_message("❌ Invalid color format! Use hex format like #FF0000", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"❌ Error creating role: {str(e)}", ephemeral=True)
    
    @app_commands.command(name="closeticket", description="Close a ticket / Jegy lezárása")
    @app_commands.checks.has_permissions(manage_channels=True)
    async def slash_closeticket(self, interaction: discord.Interaction):
        ticket_cog = self.bot.get_cog('Tickets')
        if ticket_cog:
            if not interaction.channel.name.startswith('ticket-'):
                await interaction.response.send_message("❌ This command can only be used in ticket channels!", ephemeral=True)
                return
            
            embed = discord.Embed(
                title="🎫 Ticket Closed",
                description="This ticket has been closed.",
                color=0xFF006E
            )
            
            await interaction.response.send_message(embed=embed)
            await interaction.channel.delete(reason="Ticket closed")
        else:
            await interaction.response.send_message("❌ Feature unavailable", ephemeral=True)
    
    @app_commands.command(name="play", description="Play music from YouTube, Spotify, or SoundCloud / Zene lejátszása")
    @app_commands.describe(query="Song name or URL / Dal neve vagy URL")
    async def slash_play(self, interaction: discord.Interaction, query: str):
        music_cog = self.bot.get_cog('Music')
        if music_cog:
            await interaction.response.defer()
            
            class FakeContext:
                def __init__(self, interaction):
                    self.author = interaction.user
                    self.guild = interaction.guild
                    self.channel = interaction.channel
                    self.bot = interaction.client
                    self.voice_client = interaction.guild.voice_client
                    self._interaction = interaction
                
                async def send(self, *args, **kwargs):
                    try:
                        await self._interaction.followup.send(*args, **kwargs)
                    except:
                        await self._interaction.channel.send(*args, **kwargs)
            
            ctx = FakeContext(interaction)
            await music_cog.play(ctx, query=query)
        else:
            await interaction.response.send_message("❌ Music feature unavailable", ephemeral=True)
    
    @app_commands.command(name="pause", description="Pause the current playback / Lejátszás szüneteltetése")
    async def slash_pause(self, interaction: discord.Interaction):
        import wavelink
        vc: wavelink.Player = interaction.guild.voice_client
        
        if not vc or not vc.playing:
            await interaction.response.send_message("❌ Nothing is playing", ephemeral=True)
            return
        
        await vc.pause(True)
        await interaction.response.send_message("⏸️ Paused playback", ephemeral=True)
    
    @app_commands.command(name="resume", description="Resume paused playback / Lejátszás folytatása")
    async def slash_resume(self, interaction: discord.Interaction):
        import wavelink
        vc: wavelink.Player = interaction.guild.voice_client
        
        if not vc or not vc.paused:
            await interaction.response.send_message("❌ Nothing is paused", ephemeral=True)
            return
        
        await vc.pause(False)
        await interaction.response.send_message("▶️ Resumed playback", ephemeral=True)
    
    @app_commands.command(name="skip", description="Skip to the next song / Következő dal")
    async def slash_skip(self, interaction: discord.Interaction):
        import wavelink
        vc: wavelink.Player = interaction.guild.voice_client
        
        if not vc or not vc.playing:
            await interaction.response.send_message("❌ Nothing is playing", ephemeral=True)
            return
        
        await vc.skip(force=True)
        await interaction.response.send_message("⏭️ Skipped to next song", ephemeral=True)
    
    @app_commands.command(name="stop", description="Stop playback and disconnect / Lejátszás leállítása")
    async def slash_stop(self, interaction: discord.Interaction):
        import wavelink
        vc: wavelink.Player = interaction.guild.voice_client
        
        if not vc:
            await interaction.response.send_message("❌ Not connected to voice", ephemeral=True)
            return
        
        await vc.disconnect()
        await interaction.response.send_message("⏹️ Stopped playback and disconnected", ephemeral=True)
    
    @app_commands.command(name="queue", description="Display the music queue / Zene sor megjelenítése")
    async def slash_queue(self, interaction: discord.Interaction):
        import wavelink
        vc: wavelink.Player = interaction.guild.voice_client
        
        if not vc:
            await interaction.response.send_message("❌ Not connected to voice", ephemeral=True)
            return
        
        embed = discord.Embed(
            title="🎵 Music Queue",
            color=0x8B00FF
        )
        
        if vc.current:
            embed.add_field(
                name="Now Playing",
                value=f"🎶 **{vc.current.title}**\n`{vc.current.author}`",
                inline=False
            )
        
        if vc.queue:
            queue_list = []
            for i, track in enumerate(vc.queue[:10], 1):
                queue_list.append(f"{i}. **{track.title}** - `{track.author}`")
            
            embed.add_field(
                name=f"Up Next ({vc.queue.count} songs)",
                value="\n".join(queue_list),
                inline=False
            )
        else:
            if not vc.current:
                embed.description = "Queue is empty"
        
        if vc.queue.mode == wavelink.QueueMode.loop:
            embed.set_footer(text="🔁 Loop: ON")
        
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name="nowplaying", description="Show currently playing track / Jelenlegi dal megjelenítése")
    async def slash_nowplaying(self, interaction: discord.Interaction):
        import wavelink
        vc: wavelink.Player = interaction.guild.voice_client
        
        if not vc or not vc.current:
            await interaction.response.send_message("❌ Nothing is playing", ephemeral=True)
            return
        
        track = vc.current
        
        position = vc.position
        duration = track.length
        
        progress_bar_length = 20
        progress = int((position / duration) * progress_bar_length) if duration > 0 else 0
        bar = "█" * progress + "░" * (progress_bar_length - progress)
        
        position_str = f"{int(position // 60)}:{int(position % 60):02d}"
        duration_str = f"{int(duration // 60)}:{int(duration % 60):02d}"
        
        embed = discord.Embed(
            title="🎵 Now Playing",
            description=f"**{track.title}**\n`{track.author}`",
            color=0x00F3FF
        )
        
        embed.add_field(
            name="Progress",
            value=f"`{position_str}` {bar} `{duration_str}`",
            inline=False
        )
        
        if hasattr(track, 'artwork') and track.artwork:
            embed.set_thumbnail(url=track.artwork)
        
        if vc.queue.mode == wavelink.QueueMode.loop:
            embed.set_footer(text="🔁 Loop: ON")
        
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name="loop", description="Toggle loop mode / Ismétlés be/ki")
    async def slash_loop(self, interaction: discord.Interaction):
        import wavelink
        vc: wavelink.Player = interaction.guild.voice_client
        
        if not vc:
            await interaction.response.send_message("❌ Not connected to voice", ephemeral=True)
            return
        
        if vc.queue.mode == wavelink.QueueMode.loop:
            vc.queue.mode = wavelink.QueueMode.normal
            status = "disabled"
            emoji = "➡️"
        else:
            vc.queue.mode = wavelink.QueueMode.loop
            status = "enabled"
            emoji = "🔁"
        
        await interaction.response.send_message(f"{emoji} Loop mode {status}", ephemeral=True)
    
    @app_commands.command(name="volume", description="Adjust playback volume / Hangerő beállítása")
    @app_commands.describe(volume="Volume level (0-100) / Hangerő szint (0-100)")
    async def slash_volume(self, interaction: discord.Interaction, volume: int):
        import wavelink
        
        if volume < 0 or volume > 100:
            await interaction.response.send_message("❌ Volume must be between 0 and 100", ephemeral=True)
            return
        
        vc: wavelink.Player = interaction.guild.voice_client
        
        if not vc:
            await interaction.response.send_message("❌ Not connected to voice", ephemeral=True)
            return
        
        await vc.set_volume(volume)
        await interaction.response.send_message(f"🔊 Volume set to {volume}%", ephemeral=True)
    
    @app_commands.command(name="servers", description="List all servers the bot is in (Owner Only) / Bot által használt szerverek listája")
    async def slash_servers(self, interaction: discord.Interaction):
        if not await self.bot.is_owner(interaction.user):
            await interaction.response.send_message(translations.get_text(interaction.guild.id, 'owner_only'), ephemeral=True)
            return
        
        guild_id = interaction.guild.id if interaction.guild else None
        
        embed = discord.Embed(
            title=translations.get_text(guild_id, 'servers_title'),
            description=translations.get_text(guild_id, 'servers_description', len(self.bot.guilds)),
            color=0x00ffff
        )
        
        server_list = []
        for guild in self.bot.guilds:
            server_list.append(f"**{guild.name}**\n`ID: {guild.id}`")
        
        if server_list:
            chunks = [server_list[i:i+10] for i in range(0, len(server_list), 10)]
            for i, chunk in enumerate(chunks):
                embed.add_field(
                    name=f"Servers {i*10 + 1}-{min((i+1)*10, len(server_list))}",
                    value="\n\n".join(chunk),
                    inline=False
                )
        
        embed.set_footer(text=translations.get_text(guild_id, 'servers_footer', len(self.bot.guilds)))
        if self.bot.user.avatar:
            embed.set_thumbnail(url=self.bot.user.avatar.url)
        
        await interaction.response.send_message(embed=embed, ephemeral=True)
    
    @app_commands.command(name="createinvite", description="Create an invite for a server (Owner Only) / Meghívó létrehozása szerverhez")
    @app_commands.describe(server_id="Server ID to create invite for / Szerver ID meghívó létrehozásához")
    async def slash_createinvite(self, interaction: discord.Interaction, server_id: str):
        if not await self.bot.is_owner(interaction.user):
            await interaction.response.send_message(translations.get_text(interaction.guild.id, 'owner_only'), ephemeral=True)
            return
        
        guild_id = interaction.guild.id if interaction.guild else None
        
        try:
            target_server_id = int(server_id)
        except ValueError:
            await interaction.response.send_message(translations.get_text(guild_id, 'server_not_found'), ephemeral=True)
            return
        
        guild = self.bot.get_guild(target_server_id)
        
        if guild is None:
            await interaction.response.send_message(translations.get_text(guild_id, 'server_not_found'), ephemeral=True)
            return
        
        text_channels = [ch for ch in guild.text_channels if ch.permissions_for(guild.me).create_instant_invite]
        
        if not text_channels:
            await interaction.response.send_message(translations.get_text(guild_id, 'no_permission_invite', guild.name), ephemeral=True)
            return
        
        channel = text_channels[0]
        
        try:
            invite = await channel.create_invite(max_age=0, max_uses=0, reason=f"Created by bot owner {interaction.user}")
            
            embed = discord.Embed(
                title=translations.get_text(guild_id, 'invite_created'),
                description=translations.get_text(guild_id, 'invite_created_desc', guild.name),
                color=0x00ffff
            )
            embed.add_field(name=translations.get_text(guild_id, 'invite_link'), value=invite.url, inline=False)
            embed.add_field(name=translations.get_text(guild_id, 'invite_expires'), value=translations.get_text(guild_id, 'invite_never'), inline=True)
            if guild.icon:
                embed.set_thumbnail(url=guild.icon.url)
            
            await interaction.response.send_message(embed=embed, ephemeral=True)
        
        except discord.Forbidden:
            await interaction.response.send_message(translations.get_text(guild_id, 'no_permission_invite', guild.name), ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"❌ Error creating invite: {e}", ephemeral=True)

async def setup(bot):
    await bot.add_cog(SlashCommands(bot))

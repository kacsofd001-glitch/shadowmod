import discord
from discord import app_commands
from discord.ext import commands
import config
from datetime import datetime, timezone, timedelta

class SlashCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.command(name="help", description="Show all bot commands")
    async def slash_help(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="🤖 Bot Commands Help",
            description="Here are all available commands:",
            color=discord.Color.blue()
        )
        
        embed.add_field(
            name="🎫 Ticket System",
            value="`/ticket` or `!ticket` - Create a ticket panel\n`!closeticket` - Close a ticket",
            inline=False
        )
        
        embed.add_field(
            name="🛡️ Moderation",
            value="`/ban` `/kick` `/mute` `/unmute` - Basic moderation\n`!tempmute <user> <time>` - Temporarily mute\n`!tempban <user> <time>` - Temporarily ban\n`/lock` `/unlock` - Lock/unlock channel\n`/warn` - Warn a user",
            inline=False
        )
        
        embed.add_field(
            name="🎮 Games",
            value="`!rps` - Play Rock Paper Scissors\n`!tictactoe <@user>` - Play Tic Tac Toe",
            inline=False
        )
        
        embed.add_field(
            name="😄 Fun",
            value="`/meme` - Random meme\n`/8ball` - Magic 8-ball\n`/coinflip` - Flip a coin\n`!sound` - Random sound",
            inline=False
        )
        
        embed.add_field(
            name="📊 Polls & Roles",
            value="`!poll` - Create poll\n`!quickpoll` - Yes/No poll\n`!createrole` - Create role\n`!addrole` - Add role to user",
            inline=False
        )
        
        embed.add_field(
            name="🎉 Giveaways",
            value="`!giveaway <time> <winners> <prize>` - Start giveaway\n`!reroll <message_id>` - Reroll winner",
            inline=False
        )
        
        embed.add_field(
            name="⚙️ Configuration",
            value="`/setlog` - Set log channel\n`/setwebhook` - Set webhook for logging\n`/testwebhook` - Test webhook",
            inline=False
        )
        
        embed.set_footer(text="Commands work with ! or / prefix! Use buttons for interactive features")
        
        await interaction.response.send_message(embed=embed, ephemeral=True)
    
    @app_commands.command(name="ticket", description="Create a ticket panel")
    @app_commands.checks.has_permissions(administrator=True)
    async def slash_ticket(self, interaction: discord.Interaction):
        ticket_cog = self.bot.get_cog('Tickets')
        if ticket_cog:
            view = ticket_cog.TicketView()
            self.bot.add_view(view)
            
            embed = discord.Embed(
                title="🎫 Support Tickets",
                description="Need help? Click the button below to create a ticket!",
                color=discord.Color.blue()
            )
            embed.add_field(
                name="How it works:",
                value="• Click 'Create Ticket'\n• A private channel will be created\n• Our staff will assist you\n• Close ticket when done",
                inline=False
            )
            
            await interaction.response.send_message(embed=embed, view=view)
    
    @app_commands.command(name="meme", description="Get a random meme")
    async def slash_meme(self, interaction: discord.Interaction):
        import aiohttp
        import random
        
        await interaction.response.defer()
        
        async with aiohttp.ClientSession() as session:
            async with session.get('https://meme-api.com/gimme') as response:
                if response.status == 200:
                    data = await response.json()
                    
                    embed = discord.Embed(
                        title=data['title'],
                        color=discord.Color.random()
                    )
                    embed.set_image(url=data['url'])
                    embed.set_footer(text=f"From r/{data['subreddit']} | 👍 {data['ups']}")
                    
                    await interaction.followup.send(embed=embed)
                else:
                    await interaction.followup.send("❌ Couldn't fetch a meme right now!")
    
    @app_commands.command(name="8ball", description="Ask the magic 8-ball a question")
    @app_commands.describe(question="Your question for the 8-ball")
    async def slash_8ball(self, interaction: discord.Interaction, question: str):
        import random
        
        responses = [
            "It is certain.", "It is decidedly so.", "Without a doubt.",
            "Yes definitely.", "You may rely on it.", "As I see it, yes.",
            "Most likely.", "Outlook good.", "Yes.", "Signs point to yes.",
            "Reply hazy, try again.", "Ask again later.", "Better not tell you now.",
            "Cannot predict now.", "Concentrate and ask again.",
            "Don't count on it.", "My reply is no.", "My sources say no.",
            "Outlook not so good.", "Very doubtful."
        ]
        
        embed = discord.Embed(
            title="🎱 Magic 8-Ball",
            color=discord.Color.purple()
        )
        embed.add_field(name="Question", value=question, inline=False)
        embed.add_field(name="Answer", value=random.choice(responses), inline=False)
        
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name="coinflip", description="Flip a coin")
    async def slash_coinflip(self, interaction: discord.Interaction):
        import random
        
        result = random.choice(['Heads', 'Tails'])
        emoji = '🪙'
        
        embed = discord.Embed(
            title=f"{emoji} Coin Flip",
            description=f"**The coin landed on: {result}!**",
            color=discord.Color.gold()
        )
        
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name="ban", description="Ban a user from the server")
    @app_commands.describe(user="The user to ban", reason="Reason for the ban")
    @app_commands.checks.has_permissions(ban_members=True)
    async def slash_ban(self, interaction: discord.Interaction, user: discord.Member, reason: str = None):
        try:
            await user.ban(reason=reason)
            
            embed = discord.Embed(
                title="🔨 User Banned",
                description=f"{user.mention} has been banned from the server.",
                color=discord.Color.red()
            )
            if reason:
                embed.add_field(name="Reason", value=reason, inline=False)
            embed.add_field(name="Moderator", value=interaction.user.mention, inline=True)
            
            await interaction.response.send_message(embed=embed)
        except Exception as e:
            await interaction.response.send_message(f"❌ Failed to ban user: {str(e)}", ephemeral=True)
    
    @app_commands.command(name="kick", description="Kick a user from the server")
    @app_commands.describe(user="The user to kick", reason="Reason for the kick")
    @app_commands.checks.has_permissions(kick_members=True)
    async def slash_kick(self, interaction: discord.Interaction, user: discord.Member, reason: str = None):
        try:
            await user.kick(reason=reason)
            
            embed = discord.Embed(
                title="👢 User Kicked",
                description=f"{user.mention} has been kicked from the server.",
                color=discord.Color.orange()
            )
            if reason:
                embed.add_field(name="Reason", value=reason, inline=False)
            embed.add_field(name="Moderator", value=interaction.user.mention, inline=True)
            
            await interaction.response.send_message(embed=embed)
        except Exception as e:
            await interaction.response.send_message(f"❌ Failed to kick user: {str(e)}", ephemeral=True)
    
    @app_commands.command(name="mute", description="Mute a user")
    @app_commands.describe(user="The user to mute")
    @app_commands.checks.has_permissions(manage_roles=True)
    async def slash_mute(self, interaction: discord.Interaction, user: discord.Member):
        cfg = config.load_config()
        guild_id = str(interaction.guild.id)
        muted_role_id = cfg.get('muted_roles', {}).get(guild_id)
        
        if not muted_role_id:
            muted_role = await interaction.guild.create_role(name="Muted", color=discord.Color.dark_gray())
            cfg.setdefault('muted_roles', {})[guild_id] = muted_role.id
            config.save_config(cfg)
            
            for channel in interaction.guild.channels:
                await channel.set_permissions(muted_role, send_messages=False, speak=False)
        else:
            muted_role = interaction.guild.get_role(muted_role_id)
        
        await user.add_roles(muted_role)
        
        embed = discord.Embed(
            title="🔇 User Muted",
            description=f"{user.mention} has been muted.",
            color=discord.Color.dark_gray()
        )
        
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name="unmute", description="Unmute a user")
    @app_commands.describe(user="The user to unmute")
    @app_commands.checks.has_permissions(manage_roles=True)
    async def slash_unmute(self, interaction: discord.Interaction, user: discord.Member):
        cfg = config.load_config()
        guild_id = str(interaction.guild.id)
        muted_role_id = cfg.get('muted_roles', {}).get(guild_id)
        
        if not muted_role_id:
            await interaction.response.send_message("❌ No muted role found!", ephemeral=True)
            return
        
        muted_role = interaction.guild.get_role(muted_role_id)
        if muted_role in user.roles:
            await user.remove_roles(muted_role)
            
            embed = discord.Embed(
                title="🔊 User Unmuted",
                description=f"{user.mention} has been unmuted.",
                color=discord.Color.green()
            )
            
            await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message("❌ User is not muted!", ephemeral=True)
    
    @app_commands.command(name="lock", description="Lock the current channel")
    @app_commands.checks.has_permissions(manage_channels=True)
    async def slash_lock(self, interaction: discord.Interaction):
        await interaction.channel.set_permissions(
            interaction.guild.default_role,
            send_messages=False
        )
        
        embed = discord.Embed(
            title="🔒 Channel Locked",
            description="This channel has been locked.",
            color=discord.Color.red()
        )
        
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name="unlock", description="Unlock the current channel")
    @app_commands.checks.has_permissions(manage_channels=True)
    async def slash_unlock(self, interaction: discord.Interaction):
        await interaction.channel.set_permissions(
            interaction.guild.default_role,
            send_messages=True
        )
        
        embed = discord.Embed(
            title="🔓 Channel Unlocked",
            description="This channel has been unlocked.",
            color=discord.Color.green()
        )
        
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name="warn", description="Warn a user")
    @app_commands.describe(user="The user to warn", reason="Reason for the warning")
    @app_commands.checks.has_permissions(manage_messages=True)
    async def slash_warn(self, interaction: discord.Interaction, user: discord.Member, reason: str = None):
        cfg = config.load_config()
        warnings = cfg.get('warnings', {})
        user_id = str(user.id)
        
        if user_id not in warnings:
            warnings[user_id] = []
        
        warnings[user_id].append({
            'reason': reason or 'No reason provided',
            'moderator': str(interaction.user),
            'timestamp': datetime.now(timezone.utc).isoformat()
        })
        
        cfg['warnings'] = warnings
        config.save_config(cfg)
        
        embed = discord.Embed(
            title="⚠️ User Warned",
            description=f"{user.mention} has been warned.",
            color=discord.Color.yellow()
        )
        embed.add_field(name="Reason", value=reason or "No reason provided", inline=False)
        embed.add_field(name="Total Warnings", value=str(len(warnings[user_id])), inline=True)
        
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name="setlog", description="Set the log channel for bot events")
    @app_commands.describe(channel="The channel to send logs to")
    @app_commands.checks.has_permissions(administrator=True)
    async def slash_setlog(self, interaction: discord.Interaction, channel: discord.TextChannel):
        config.update_config('log_channel_id', channel.id)
        
        embed = discord.Embed(
            title="✅ Log Channel Set",
            description=f"Log channel has been set to {channel.mention}",
            color=discord.Color.green()
        )
        
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name="setwebhook", description="Set webhook URL for bot error logging")
    @app_commands.describe(webhook_url="The Discord webhook URL")
    @app_commands.checks.has_permissions(administrator=True)
    async def slash_setwebhook(self, interaction: discord.Interaction, webhook_url: str):
        webhook_cog = self.bot.get_cog('WebhookLogging')
        if webhook_cog:
            webhook_cog.webhook_url = webhook_url
            config.update_config('webhook_url', webhook_url)
            
            test_embed = discord.Embed(
                title="✅ Webhook Set",
                description="Bot logging webhook has been configured!",
                color=discord.Color.green(),
                timestamp=datetime.now(timezone.utc)
            )
            test_embed.add_field(
                name="Test Message",
                value="If you see this, webhook logging is working!",
                inline=False
            )
            
            await webhook_cog.send_to_webhook(test_embed)
            await interaction.response.send_message("✅ Webhook logging configured! Check your webhook channel.")
    
    @app_commands.command(name="testwebhook", description="Test the webhook logging system")
    @app_commands.checks.has_permissions(administrator=True)
    async def slash_testwebhook(self, interaction: discord.Interaction):
        webhook_cog = self.bot.get_cog('WebhookLogging')
        if webhook_cog:
            test_embed = discord.Embed(
                title="🧪 Test Webhook",
                description="This is a test message from the bot!",
                color=discord.Color.blue(),
                timestamp=datetime.now(timezone.utc)
            )
            test_embed.add_field(name="Tested by", value=str(interaction.user), inline=True)
            test_embed.add_field(name="Channel", value=interaction.channel.mention, inline=True)
            
            await webhook_cog.send_to_webhook(test_embed)
            await interaction.response.send_message("✅ Test webhook sent! Check your webhook channel.")

async def setup(bot):
    await bot.add_cog(SlashCommands(bot))

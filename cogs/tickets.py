import discord
from discord.ext import commands
from discord.ui import Button, View
from discord import app_commands
import config

class TicketView(View):
    def __init__(self):
        super().__init__(timeout=None)
    
    @discord.ui.button(label='📩 Create Ticket', style=discord.ButtonStyle.green, custom_id='create_ticket')
    async def create_ticket(self, interaction: discord.Interaction, button: Button):
        from translations import get_text
        guild = interaction.guild
        user = interaction.user
        
        cfg = config.load_config()
        ticket_num = cfg.get('ticket_counter', 0) + 1
        config.update_config('ticket_counter', ticket_num)
        
        category = None
        if cfg.get('ticket_category_id'):
            category = guild.get_channel(cfg['ticket_category_id'])
        
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            user: discord.PermissionOverwrite(read_messages=True, send_messages=True),
            guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True)
        }
        
        channel = await guild.create_text_channel(
            name=f'ticket-{ticket_num}',
            category=category,
            overwrites=overwrites
        )
        
        embed = discord.Embed(
            title=get_text(guild.id, 'ticket_title') + f" #{ticket_num}",
            description=get_text(guild.id, 'ticket_description') + f"\n\n{user.mention}, please describe your issue.",
            color=0x00F3FF
        )
        embed.set_footer(text=get_text(guild.id, 'ticket_closed'))
        
        close_view = CloseTicketView()
        await channel.send(embed=embed, view=close_view)
        
        await interaction.response.send_message(
            get_text(guild.id, 'ticket_created_desc', channel.mention),
            ephemeral=True
        )

class CloseTicketView(View):
    def __init__(self):
        super().__init__(timeout=None)
    
    @discord.ui.button(label='🔒 Close Ticket', style=discord.ButtonStyle.red, custom_id='close_ticket')
    async def close_ticket(self, interaction: discord.Interaction, button: Button):
        embed = discord.Embed(
            title="🔒 Ticket Closed",
            description=f"Ticket closed by {interaction.user.mention}",
            color=0xFF006E
        )
        
        await interaction.response.send_message(embed=embed)
        await interaction.channel.delete(reason=f"Ticket closed by {interaction.user}")

class Tickets(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @app_commands.command(name='ticket', description='Execute ticket command')
    @app_commands.checks.has_permissions(administrator=True)
    async def create_ticket_panel(self, interaction: discord.Interaction):
        from translations import get_text
        embed = discord.Embed(
            title=get_text(interaction.guild.id, 'ticket_title'),
            description=get_text(interaction.guild.id, 'ticket_description') + "\n\n" + get_text(interaction.guild.id, 'ticket_steps'),
            color=0x8B00FF
        )
        embed.set_footer(text=get_text(interaction.guild.id, 'help_footer'))
        
        view = TicketView()
        await interaction.response.send_message(embed=embed, view=view)
        # Message deletion not supported in slash commands
    
    @app_commands.command(name='closeticket', description='Execute closeticket command')
    @app_commands.checks.has_permissions(manage_channels=True)
    async def close_ticket_cmd(self, interaction: discord.Interaction):
        if 'ticket-' in interaction.channel.name:
            embed = discord.Embed(
                title="🔒 Ticket Closed",
                description=f"Ticket closed by {interaction.user.mention}",
                color=0xFF006E
            )
            await interaction.response.send_message(embed=embed)
            await interaction.channel.delete(reason=f"Ticket closed by {interaction.user}")
        else:
            await interaction.response.send_message("❌ This command can only be used in ticket channels!")

async def setup(bot):
    await bot.add_cog(Tickets(bot))
    bot.add_view(TicketView())
    bot.add_view(CloseTicketView())

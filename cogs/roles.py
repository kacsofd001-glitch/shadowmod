import discord
from discord.ext import commands
from discord import app_commands
from datetime import datetime, timezone

class Roles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.command(name='createrole', description='Execute createrole command')
    @app_commands.checks.has_permissions(manage_roles=True)
    async def create_role(self, interaction: discord.Interaction, name: str, color: str = None):
        try:
            role_color = discord.Color.default()
            if color:
                color = color.replace('#', '')
                role_color = discord.Color(int(color, 16))
            
            role = await interaction.guild.create_role(name=name, color=role_color)
            
            embed = discord.Embed(
                title="✅ Role Created",
                description=f"Role **{role.mention}** has been created!",
                color=discord.Color.green(),
                timestamp=datetime.now(timezone.utc)
            )
            await interaction.response.send_message(embed=embed)
        except ValueError:
            await interaction.response.send_message("❌ Invalid color format! Use hex color (e.g., #FF5733)")
        except Exception as e:
            await interaction.response.send_message(f"❌ Error creating role: {str(e)}")
    
    @app_commands.command(name='deleterole', description='Execute deleterole command')
    @app_commands.checks.has_permissions(manage_roles=True)
    async def delete_role(self, interaction: discord.Interaction, role: discord.Role):
        if role >= interaction.user.top_role and interaction.user.id != interaction.guild.owner_id:
            await interaction.response.send_message("❌ You cannot delete a role higher than or equal to your highest role!")
            return
        
        role_name = role.name
        await role.delete()
        
        embed = discord.Embed(
            title="✅ Role Deleted",
            description=f"Role **{role_name}** has been deleted!",
            color=discord.Color.green(),
            timestamp=datetime.now(timezone.utc)
        )
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name='addrole', description='Execute addrole command')
    @app_commands.checks.has_permissions(manage_roles=True)
    async def add_role(self, interaction: discord.Interaction, member: discord.Member, role: discord.Role):
        if role >= interaction.user.top_role and interaction.user.id != interaction.guild.owner_id:
            await interaction.response.send_message("❌ You cannot assign a role higher than or equal to your highest role!")
            return
        
        if role in member.roles:
            await interaction.response.send_message(f"❌ {member.mention} already has the {role.mention} role!")
            return
        
        await member.add_roles(role)
        
        embed = discord.Embed(
            title="✅ Role Added",
            description=f"Added {role.mention} to {member.mention}",
            color=discord.Color.green(),
            timestamp=datetime.now(timezone.utc)
        )
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name='removerole', description='Execute removerole command')
    @app_commands.checks.has_permissions(manage_roles=True)
    async def remove_role(self, interaction: discord.Interaction, member: discord.Member, role: discord.Role):
        if role not in member.roles:
            await interaction.response.send_message(f"❌ {member.mention} doesn't have the {role.mention} role!")
            return
        
        await member.remove_roles(role)
        
        embed = discord.Embed(
            title="✅ Role Removed",
            description=f"Removed {role.mention} from {member.mention}",
            color=discord.Color.green(),
            timestamp=datetime.now(timezone.utc)
        )
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name='roleinfo', description='Execute roleinfo command')
    async def role_info(self, interaction: discord.Interaction, role: discord.Role):
        embed = discord.Embed(
            title=f"📋 Role Info: {role.name}",
            color=role.color,
            timestamp=datetime.now(timezone.utc)
        )
        
        embed.add_field(name="ID", value=role.id, inline=True)
        embed.add_field(name="Color", value=str(role.color), inline=True)
        embed.add_field(name="Position", value=role.position, inline=True)
        embed.add_field(name="Members", value=len(role.members), inline=True)
        embed.add_field(name="Mentionable", value="Yes" if role.mentionable else "No", inline=True)
        embed.add_field(name="Hoisted", value="Yes" if role.hoist else "No", inline=True)
        embed.add_field(name="Created", value=role.created_at.strftime('%Y-%m-%d'), inline=True)
        
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name='roles', description='Execute roles command')
    async def list_roles(self, interaction: discord.Interaction):
        roles = sorted(interaction.guild.roles[1:], key=lambda r: r.position, reverse=True)
        
        embed = discord.Embed(
            title=f"📋 Server Roles ({len(roles)})",
            color=discord.Color.blue(),
            timestamp=datetime.now(timezone.utc)
        )
        
        role_list = "\n".join([f"{role.mention} - {len(role.members)} members" for role in roles[:25]])
        embed.description = role_list
        
        if len(roles) > 25:
            embed.set_footer(text=f"Showing 25 of {len(roles)} roles")
        
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(Roles(bot))

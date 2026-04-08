import discord
from discord.ext import commands
from discord import app_commands
import config

class NameAutomation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    def get_prefix_for_member(self, member):
        cfg = config.load_config()
        role_prefixes = cfg.get('role_prefixes', {})
        
        for role in sorted(member.roles, key=lambda r: r.position, reverse=True):
            role_id = str(role.id)
            if role_id in role_prefixes:
                return role_prefixes[role_id]
        
        return None
    
    async def update_member_nickname(self, member):
        if member.bot:
            return
        
        try:
            cfg = config.load_config()
            role_prefixes = cfg.get('role_prefixes', {})
            all_prefixes = list(set(role_prefixes.values()))
            
            prefix = self.get_prefix_for_member(member)
            
            current_nick = member.display_name
            
            # Remove all existing prefixes from the nickname
            changed = True
            while changed:
                changed = False
                for p in all_prefixes:
                    prefix_with_space = f"{p} "
                    if current_nick.startswith(prefix_with_space):
                        current_nick = current_nick[len(prefix_with_space):]
                        changed = True
                        break
            
            # Remove any leading/trailing whitespace
            current_nick = current_nick.strip()
            
            if prefix:
                new_nick = f"{prefix} {current_nick}"
            else:
                new_nick = current_nick
            
            # Limit to 32 characters (Discord's nickname limit)
            new_nick = new_nick[:32]
            
            # Only update if the nickname actually changed
            if member.nick != new_nick:
                await member.edit(nick=new_nick)
        except discord.Forbidden:
            pass
        except Exception:
            pass
    
    @commands.Cog.listener()
    async def on_member_join(self, member):
        await self.update_member_nickname(member)
    
    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        if before.roles != after.roles:
            await self.update_member_nickname(after)
    
    @app_commands.command(name='setprefix', description='Execute setprefix command')
    @app_commands.checks.has_permissions(administrator=True)
    async def set_role_prefix(self, interaction: discord.Interaction, role: discord.Role, prefix: str):
        if len(prefix) > 10:
            await interaction.response.send_message("❌ Prefix must be 10 characters or less!")
            return
        
        cfg = config.load_config()
        if 'role_prefixes' not in cfg:
            cfg['role_prefixes'] = {}
        
        old_prefix = cfg['role_prefixes'].get(str(role.id))
        cfg['role_prefixes'][str(role.id)] = prefix
        config.save_config(cfg)
        
        embed = discord.Embed(
            title="✅ Prefix Set",
            description=f"Members with {role.mention} will have `{prefix}` prefix in their nickname!",
            color=0x00F3FF
        )
        embed.add_field(name="Example", value=f"{prefix} Username", inline=False)
        
        msg = await interaction.response.send_message(embed=embed)
        
        await msg.edit(content="🔄 Updating member nicknames...", embed=embed)
        count = 0
        for member in interaction.guild.members:
            if role in member.roles:
                await self.update_member_nickname(member)
                count += 1
        
        embed.add_field(name="Updated", value=f"{count} members updated!", inline=False)
        await msg.edit(content=None, embed=embed)
    
    @app_commands.command(name='removeprefix', description='Execute removeprefix command')
    @app_commands.checks.has_permissions(administrator=True)
    async def remove_role_prefix(self, interaction: discord.Interaction, role: discord.Role):
        cfg = config.load_config()
        role_prefixes = cfg.get('role_prefixes', {})
        
        if str(role.id) not in role_prefixes:
            await interaction.response.send_message(f"❌ {role.mention} doesn't have a prefix set!")
            return
        
        del cfg['role_prefixes'][str(role.id)]
        config.save_config(cfg)
        
        embed = discord.Embed(
            title="✅ Prefix Removed",
            description=f"Prefix removed from {role.mention}",
            color=0x00F3FF
        )
        
        msg = await interaction.response.send_message(embed=embed)
        
        await msg.edit(content="🔄 Updating member nicknames...", embed=embed)
        count = 0
        for member in interaction.guild.members:
            if role in member.roles:
                await self.update_member_nickname(member)
                count += 1
        
        embed.add_field(name="Updated", value=f"{count} members updated!", inline=False)
        await msg.edit(content=None, embed=embed)
    
    @app_commands.command(name='updateallnicks', description='Execute updateallnicks command')
    @app_commands.checks.has_permissions(administrator=True)
    async def update_all_nicknames(self, interaction: discord.Interaction):
        await interaction.response.send_message("🔄 Updating all member nicknames... This may take a while.")
        
        count = 0
        for member in interaction.guild.members:
            await self.update_member_nickname(member)
            count += 1
        
        embed = discord.Embed(
            title="✅ Nicknames Updated",
            description=f"Updated nicknames for {count} members!",
            color=0x00F3FF
        )
        
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name='viewprefixes', description='Execute viewprefixes command')
    async def view_prefixes(self, interaction: discord.Interaction):
        cfg = config.load_config()
        role_prefixes = cfg.get('role_prefixes', {})
        
        if not role_prefixes:
            await interaction.response.send_message("❌ No role prefixes configured!")
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
        
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(NameAutomation(bot))

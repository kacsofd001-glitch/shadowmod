#!/usr/bin/env python3
"""
Convert all prefix commands to slash commands automatically
Run: python convert_commands.py
"""

import os
import re
import glob

# List of cogs to convert
COGS_TO_CONVERT = [
    'cogs/music.py',
    'cogs/info.py',
    'cogs/roles.py',
    'cogs/fun.py',
    'cogs/nameauto.py',
    'cogs/giveaways.py',
    'cogs/admin.py',
    'cogs/games.py',
    'cogs/tickets.py',
    'cogs/polls.py',
    'cogs/webhook_logging.py',
    'cogs/language.py',
    'cogs/logging.py',
    'cogs/antialt.py',
    'cogs/verify.py',
]

def add_import_if_missing(content):
    """Add app_commands import if not present"""
    if 'from discord import app_commands' not in content:
        # Find the last import line in discord.ext imports
        lines = content.split('\n')
        insert_index = 0
        for i, line in enumerate(lines):
            if line.startswith('from discord') or line.startswith('import discord'):
                insert_index = i + 1
        
        if insert_index > 0:
            lines.insert(insert_index, 'from discord import app_commands')
            content = '\n'.join(lines)
    
    return content

def convert_command_decorator(line):
    """Convert @commands.command to @app_commands.command"""
    # Extract command name and aliases
    pattern = r"@commands\.command\((.*?)\)"
    match = re.search(pattern, line)
    
    if match:
        params = match.group(1)
        # Add description if not present
        if 'description' not in params:
            # Extract command name
            name_match = re.search(r"name='([^']+)'", params)
            if name_match:
                cmd_name = name_match.group(1)
                # Add default description
                params = params.rstrip() + f", description='Execute {cmd_name} command'"
        
        return f"@app_commands.command({params})"
    
    return line

def convert_permission_decorator(line):
    """Convert @commands.has_permissions to @app_commands.checks.has_permissions"""
    if '@commands.has_permissions' in line:
        return line.replace('@commands.has_permissions', '@app_commands.checks.has_permissions')
    return line

def convert_function_signature(line, indent):
    """Convert function signature from ctx to interaction"""
    # Match: async def cmd_name(self, ctx, ... or async def cmd_name(self, ctx):
    pattern = r"(async def \w+\(self, )ctx((\s*[:,\)]))"
    
    if re.search(pattern, line):
        line = re.sub(pattern, r"\1interaction: discord.Interaction\2", line)
    
    return line

def convert_ctx_references(content):
    """Convert all ctx.xxx references to interaction equivalents"""
    replacements = [
        (r'\bctx\.send\(', 'interaction.response.send_message('),
        (r'\bctx\.author\b', 'interaction.user'),
        (r'\bctx\.guild\b', 'interaction.guild'),
        (r'\bctx\.channel\b', 'interaction.channel'),
        (r'\bctx\.bot\b', 'interaction.client'),
        (r'\bctx\.voice_client\b', 'interaction.user.voice.channel'),  # Note: may need adjustment
        (r'\bctx\.guild\.id\b', 'interaction.guild.id'),
        (r'\bctx\.author\.mention\b', 'interaction.user.mention'),
    ]
    
    for old, new in replacements:
        content = re.sub(old, new, content)
    
    return content

def process_file(filepath):
    """Process a single cog file"""
    print(f"Processing {filepath}...")
    
    if not os.path.exists(filepath):
        print(f"  ❌ File not found: {filepath}")
        return
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    
    # Add app_commands import
    content = add_import_if_missing(content)
    
    # Process line by line for decorators 
    lines = content.split('\n')
    new_lines = []
    
    for i, line in enumerate(lines):
        # Convert @commands.command decorators
        if '@commands.command' in line:
            line = convert_command_decorator(line)
        
        # Convert @commands.has_permissions
        if '@commands.has_permissions' in line:
            line = convert_permission_decorator(line)
        
        # Convert function signatures
        if line.strip().startswith('async def ') and '(self, ctx' in line:
            indent = len(line) - len(line.lstrip())
            line = convert_function_signature(line, ' ' * indent)
        
        new_lines.append(line)
    
    content = '\n'.join(new_lines)
    
    # Convert all ctx references
    content = convert_ctx_references(content)
    
    # Write back if changed
    if content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  ✅ Converted successfully")
    else:
        print(f"  ⚠️ No changes made")

def main():
    print("=" * 60)
    print("PREFIX TO SLASH COMMANDS CONVERTER")
    print("=" * 60)
    
    # Process moderation.py (already done, but let's verify)
    print("\nNote: moderation.py should already be converted manually")
    
    # Process remaining cogs
    for cog in COGS_TO_CONVERT[1:]:  # Skip moderation.py
        process_file(cog)
    
    print("\n" + "=" * 60)
    print("CONVERSION COMPLETE!")
    print("=" * 60)
    print("\n⚠️  MANUAL VERIFICATION NEEDED:")
    print("  1. Check for ctx.voice_client references (may need special handling)")
    print("  2. Check for ctx.send() with 'delete_after' (slash commands don't support this)")
    print("  3. Verify all command names and parameters")
    print("  4. Test commands in Discord")

if __name__ == '__main__':
    main()

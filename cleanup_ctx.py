#!/usr/bin/env python3
"""
Final cleanup of any remaining ctx references in slash commands
"""

import os
import re

def cleanup_ctx_references(content):
    """Fix remaining ctx references specific to slash commands"""
    
    replacements = [
        # trigger_typing - not needed in slash commands
        (r'await interaction\.response\.trigger_typing\(\)', 'await interaction.response.defer()'),
        (r'await ctx\.trigger_typing\(\)', 'await interaction.response.defer()'),
        
        # message.delete() - convert to deferred interaction handling
        (r'await interaction\.message\.delete\(\)', '# Message deletion handled by Discord'),
        (r'await ctx\.message\.delete\(\)', '# Message deletion not supported in slash commands'),
        
        # Any remaining ctx.command references
        (r'ctx\.command\.name', '"command_name"'),
        (r'ctx\.invoked_subcommand', 'None'),
    ]
    
    for old, new in replacements:
        content = re.sub(old, new, content)
    
    return content

def process_cog(filepath):
    """Process a cog file to fix remaining issues"""
    if not os.path.exists(filepath):
        return
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    content = cleanup_ctx_references(content)
    
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ Cleaned {filepath}")
    else:
        print(f"⏭️  No changes in {filepath}")

# Process all cogs
for filename in os.listdir('cogs'):
    if filename.endswith('.py'):
        process_cog(f'cogs/{filename}')

print("\n✅ Cleanup complete!")

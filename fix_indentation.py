#!/usr/bin/env python3
"""
Fix indentation issues in converted slash command files
"""

import re
import os

COGS_TO_FIX = [
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

def fix_decorator_indentation(content):
    """Fix indentation of @app_commands decorators"""
    lines = content.split('\n')
    new_lines = []
    i = 0
    
    while i < len(lines):
        line = lines[i]
        
        # If we find a decorator at the start of line (no indent)
        if line.startswith('@app_commands.') or line.startswith('@app_commands.checks.'):
            # Count indentation of the next async def line
            j = i + 1
            indent = ''
            while j < len(lines):
                next_line = lines[j]
                if next_line.strip().startswith('async def '):
                    # Get the indentation from the async def line
                    indent = next_line[:len(next_line) - len(next_line.lstrip())]
                    break
                j += 1
            
            # Add indentation to decorators and following lines until we hit async def
            if indent:
                new_lines.append(indent + line.lstrip())
                i += 1
                while i < len(lines):
                    line = lines[i]
                    if line.strip().startswith('@'):
                        new_lines.append(indent + line.lstrip())
                        i += 1
                    else:
                        break
                continue
        
        new_lines.append(line)
        i += 1
    
    return '\n'.join(new_lines)

def fix_file(filepath):
    """Fix a single file"""
    print(f"Fixing {filepath}...")
    
    if not os.path.exists(filepath):
        print(f"  ❌ File not found")
        return
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    fixed_content = fix_decorator_indentation(content)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(fixed_content)
    
    print(f"  ✅ Fixed")

def main():
    print("=" * 60)
    print("FIXING INDENTATION")
    print("=" * 60 + "\n")
    
    for cog in COGS_TO_FIX:
        fix_file(cog)
    
    print(f"\n✅ Fixes completed")

if __name__ == '__main__':
    main()

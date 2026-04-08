#!/usr/bin/env python3
"""
Audit: Check if all converted commands are documented in help
"""

import re
import os

# Define the 58 converted commands
converted_commands = {
    'moderation.py': ['ban', 'kick', 'mute', 'unmute', 'tempmute', 'tempban', 'lock', 'unlock', 'warn', 'warnings', 'purge'],
    'music.py': ['play', 'pause', 'resume', 'skip', 'stop', 'queue', 'nowplaying', 'loop', 'volume', 'radio1'],
    'info.py': ['serverinfo', 'botinfo', 'userinfo', 'support', 'webpage'],
    'roles.py': ['createrole', 'deleterole', 'addrole', 'removerole', 'roleinfo', 'roles'],
    'fun.py': ['meme', 'sound', '8ball', 'coinflip', 'roll'],
    'nameauto.py': ['setprefix', 'removeprefix', 'updateallnicks', 'viewprefixes'],
    'giveaways.py': ['giveaway', 'reroll'],
    'admin.py': ['servers', 'createinvite'],
    'games.py': ['rps', 'tictactoe'],
    'tickets.py': ['ticket', 'closeticket'],
    'polls.py': ['poll', 'quickpoll'],
    'webhook_logging.py': ['setwebhook', 'testwebhook', 'loginfo'],
    'language.py': ['setlang'],
    'logging.py': ['setlog'],
    'antialt.py': ['setaltage'],
    'verify.py': ['setupverify']
}

# Read the help file
with open('cogs/interactivehelp.py', 'r', encoding='utf-8') as f:
    help_content = f.read()

# Extract documented commands (looking for backtick format)
documented = set(re.findall(r'`/([a-z_0-9]+)`', help_content))

# Flatten converted commands
all_converted = set()
for cog, cmds in converted_commands.items():
    all_converted.update(cmds)

# Find missing commands
missing = all_converted - documented

# Find documented commands not in converted list
extra_documented = documented - all_converted

print('📊 COMMAND DOCUMENTATION AUDIT')
print('=' * 60)
print(f'\nTotal Converted Commands: {len(all_converted)}')
print(f'Documented Commands: {len(documented)}')
print(f'Missing from Help: {len(missing)}')

if missing:
    print(f'\n❌ MISSING FROM HELP ({len(missing)} commands):')
    for cmd in sorted(missing):
        print(f'   - /{cmd}')

if extra_documented:
    print(f'\n⚠️  DOCUMENTED BUT NOT CONVERTED ({len(extra_documented)} commands):')
    for cmd in sorted(extra_documented):
        print(f'   - /{cmd}')

if not missing and not extra_documented:
    print('\n✅ All commands documented!')

print('\n' + '=' * 60)
print('COMMAND COVERAGE:')
print(f'{len(documented)}/{len(all_converted)} ({round(len(documented)/len(all_converted)*100)}%)')

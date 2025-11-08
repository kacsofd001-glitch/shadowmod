# Discord Bot Project

## Overview
A comprehensive Discord bot built with Python featuring:
- Automated ticket system with buttons
- Anti-alt account detection
- Advanced logging to Discord channels
- **Webhook logging system for bot errors and events**
- Full moderation suite (ban, kick, mute, tempmute, tempban, lock, unlock, warnings)
- Interactive games (Rock-Paper-Scissors, Tic-Tac-Toe)
- Fun commands (memes, sounds, 8ball, coinflip, dice)
- Poll system with button voting and live results
- Role management (create, delete, assign, remove)
- Giveaway system with automatic winner selection
- Name automation with role-based prefixes
- **Dual prefix support (! and /) for active developer badge**

All features use Discord embeds and button components for a modern user experience.

## Project Structure
```
.
├── main.py              # Main bot entry point (dual prefix support)
├── config.py            # Configuration management
├── cogs/                # Bot feature modules
│   ├── tickets.py       # Ticket system
│   ├── antialt.py       # Anti-alt detection
│   ├── logging.py       # Event logging
│   ├── moderation.py    # Moderation commands
│   ├── games.py         # Interactive games
│   ├── fun.py           # Fun commands
│   ├── polls.py         # Poll system
│   ├── roles.py         # Role management
│   ├── giveaways.py     # Giveaway system
│   ├── nameauto.py      # Name automation
│   └── webhook_logging.py  # Webhook logging for bot errors
├── .env                 # Environment variables (DISCORD_TOKEN)
├── bot_config.json      # Runtime configuration (auto-generated)
└── README.md            # User documentation
```

## Setup Requirements
1. Discord bot token must be set in environment as `DISCORD_TOKEN`
2. Bot requires these Discord intents: members, messages, message_content, guilds
3. Recommended permissions: Administrator (or manage_channels, ban_members, kick_members, manage_roles, manage_messages)

## Recent Changes (November 2025)
- **Added webhook logging system** - Real-time bot error and event monitoring via Discord webhooks
- **Added dual prefix support** (! and /) - Helps users maintain Discord active developer badge
- Added poll system with interactive button voting
- Added role management commands (create, delete, assign, remove)
- Added giveaway system with automatic winner selection and reroll
- Added name automation with role-based prefix system
- Fixed giveaway unique custom_ids for concurrent giveaways
- Fixed giveaway reroll to work with ended giveaways
- Fixed timezone-aware datetime handling for anti-alt and moderation
- Fixed per-guild muted role support
- Initial bot implementation with all core features
- Modular cog-based architecture for maintainability
- Persistent button views for ticket system
- Automatic temporary ban/mute expiration system
- Integration with meme API for fun commands

## User Preferences
None specified yet.

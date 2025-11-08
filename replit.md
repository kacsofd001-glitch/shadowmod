# ⚡ SHADOW-MOD ✨ | Futuristic Discord Bot

## Overview
**Next-Gen Discord Moderation System v2.0 FUTURISTIC**

A comprehensive Discord bot built with Python featuring a cyberpunk neon theme and:
- **Multilanguage support (English & Hungarian)**
- **AI Chat Assistant** - OpenAI-powered responses in designated channels
- **Verification system** - Button-based member verification with anti-alt protection
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
- **28 slash commands for Active Developer Badge maintenance**
- **Verification system** - Button-based verification with anti-alt checks
- **Information Commands** - Server info, bot info, user info with badges
- **Support & Web Links** - Quick access to support server and live dashboard

All features use Discord embeds and button components for a modern user experience.

## Project Structure
```
.
├── bot_launcher.py      # Combined launcher for bot + web server
├── main.py              # Main bot entry point (dual prefix support)
├── web_server.py        # Flask web server for stats dashboard
├── bot_stats.json       # Shared stats file between bot and web server
├── config.py            # Configuration management
├── translations.py      # Multilanguage translation system
├── templates/           # HTML templates for web dashboard
│   ├── index.html       # Futuristic stats page
│   └── help.html        # Command documentation page
├── static/              # Static assets for web server
│   ├── css/style.css    # Cyberpunk neon theme styles
│   └── js/script.js     # Interactive dashboard animations
├── cogs/                # Bot feature modules
│   ├── tickets.py       # Ticket system
│   ├── antialt.py       # Anti-alt detection
│   ├── logging.py       # Event logging
│   ├── moderation.py    # Moderation commands
│   ├── games.py         # Interactive games
│   ├── fun.py           # Fun commands (including multilingual memes)
│   ├── polls.py         # Poll system
│   ├── roles.py         # Role management
│   ├── giveaways.py     # Giveaway system
│   ├── nameauto.py      # Name automation
│   ├── webhook_logging.py  # Webhook logging for bot errors
│   ├── language.py      # Language switching commands
│   ├── aichat.py        # AI chat assistant with OpenAI
│   ├── verify.py        # Member verification with anti-alt checks
│   ├── info.py          # Information commands (serverinfo, botinfo, userinfo, etc)
│   └── slash_commands.py  # Slash command implementations (25 commands)
├── .env                 # Environment variables (DISCORD_TOKEN)
├── bot_config.json      # Runtime configuration (auto-generated)
└── README.md            # User documentation
```

## Setup Requirements
1. Discord bot token must be set in environment as `DISCORD_TOKEN`
2. **Optional:** OpenAI API key as `OPENAI_API_KEY` for AI chat feature
3. Bot requires these Discord intents: members, messages, message_content, guilds
4. Recommended permissions: Administrator (or manage_channels, ban_members, kick_members, manage_roles, manage_messages)

## Recent Changes (November 2025)
- **📋 NAVIGATION MENU** - Added sticky navigation bar to both pages with links to Dashboard, Commands, Support Server, and Add Bot
- **🔗 QUICK LINKS & OWNER PROFILE** - Added support server, bot invite links, and developer profile section to both dashboard and help page
- **📖 HELP PAGE** - Created shadowmod.net/help with full command documentation in futuristic theme, linked in !help, /help, /botinfo, and dashboard
- **🌐 CUSTOM DOMAIN** - Bot now uses shadowmod.net as custom domain for web dashboard
- **🌐 DASHBOARD PATH UPDATE** - Web dashboard moved to `/dashboard` path with automatic redirect from root for backward compatibility
- **🔧 HELP COMMAND UPDATE** - Added anti-alt system section, standardized all commands with slash notation, reorganized categories for clarity
- **🏷️ ROLE PREFIX SLASH COMMANDS** - Added /setprefix, /removeprefix, /viewprefixes for name automation (now 28 slash commands!)
- **📊 INFORMATION COMMANDS** - Added serverinfo, botinfo, userinfo (with badges), support, and webpage commands
- **🔄 UPDATED HELP COMMAND** - Both !help and /help now show all commands organized by futuristic categories with neon cyan theme
- **🎨 FUTURISTIC THEME** - Complete UI overhaul with cyberpunk neon colors (cyan, pink, purple, blue)
- **🌐 Live Web Stats Page** - Public dashboard showing real-time bot statistics at port 5000
- **Updated tempmute** - Now uses Discord's native timeout feature (max 28 days) instead of role-based muting
- **Enhanced AI Chat** - Bot now responds when mentioned anywhere (mention-only mode)
- **Added verification system** - Button-based member verification with anti-alt protection
- **Added /purge command** - Bulk message deletion (1-100 messages) with multilingual support
- **Added AI Chat Assistant** - OpenAI-powered responses in designated channels with language support (en/hu)
- **Added /ping command** - For Active Developer Badge maintenance
- **Added multilingual meme generator** - Memes automatically generate in English or Hungarian based on server language
- **Fixed role prefix duplication bug** - Role prefixes no longer duplicate when updated; auto-updates all members on prefix change
- **Updated moderation commands** - All slash commands (/ban, /kick, /mute, /unmute, /warn) now accept both user mentions and user IDs
- **Added multilanguage support** - English and Hungarian translations for all commands and messages
- **Added language switcher** - !setlang and /setlang commands to change server language
- **Added webhook logging system** - Real-time bot error and event monitoring via Discord webhooks
- **Added dual prefix support** (! and /) - Helps users maintain Discord active developer badge
- Added 16 slash commands with bilingual descriptions
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

# ⚡ SHADOW-MOD ✨ | Futuristic Discord Bot

## Overview
**Next-Gen Discord Moderation System v2.0 FUTURISTIC**

A comprehensive Discord bot built with Python featuring a cyberpunk neon theme and:
- **Multilanguage support (English & Hungarian)**
- **AI Chat Assistant** - OpenAI-powered responses in designated channels
- **Music System** - Play music from YouTube, Spotify, and SoundCloud with queue management
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
- **48 slash commands for Active Developer Badge maintenance**
- **Music slash commands** - All music features now support both ! and / prefixes
- **Admin Commands** - Owner-only server management (list servers, create invites)
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
│   ├── music.py         # Music player (YouTube, Spotify, SoundCloud)
│   ├── admin.py         # Owner-only admin commands (servers, createinvite)
│   └── slash_commands.py  # Slash command implementations (48 commands total)
├── .env                 # Environment variables (DISCORD_TOKEN)
├── bot_config.json      # Runtime configuration (auto-generated)
└── README.md            # User documentation
```

## Setup Requirements
1. Discord bot token must be set in environment as `DISCORD_TOKEN`
2. **Optional:** OpenAI API key as `OPENAI_API_KEY` for AI chat feature
3. **Optional:** Spotify API credentials (`SPOTIFY_CLIENT_ID`, `SPOTIFY_CLIENT_SECRET`) for Spotify track metadata
4. Bot requires these Discord intents: members, messages, message_content, guilds
5. Recommended permissions: Administrator (or manage_channels, ban_members, kick_members, manage_roles, manage_messages, connect, speak)
6. **Music System:** Uses public Lavalink nodes (automatically connects to available nodes). No additional setup required for basic music functionality.

## Recent Changes (November 2025)
- **🎨 CYAN BOX FIX (RESOLVED)** - Fixed persistent cyan bordered rectangle around hero section. Root cause: `.logo-glow` element with radial-gradient cyan background (300px x 300px) was rendering as visible frame effect around the SHADOW-MOD title area. Solution: disabled `.logo-glow` element entirely. (User discovered the root cause!)
- **📱 MOBILE NAVIGATION FIX** - Significantly enlarged mobile navigation buttons for better tap targets. Tablet (768px): 48px height with larger padding (14x20px). Small mobile (480px): 44px height meeting WCAG standards with 1.2em emoji icons. Buttons now 22-50% larger and much easier to click on all mobile devices.
- **🎨 UI/UX IMPROVEMENTS** - Reduced excessive glow effects on text, slowed down and dimmed animated starfield background for better eye comfort, added dark text outlines/shadows for improved readability against all backgrounds. Fixed navigation button hitboxes with 50% larger clickable areas, proper cursor pointers, and 44px minimum height (WCAG compliant). Website is now easier on the eyes while maintaining cyberpunk aesthetic.
- **📬 SERVER JOIN NOTIFICATIONS** - Bot now sends DM notification to owner when invited to new servers. Includes server info (name, ID, member count, owner details, creation date) and updated total server count.
- **📋 LOGGING OPTIMIZATION** - Fixed duplicate logging when members join. Consolidated logging.py and antialt.py into single comprehensive message that shows join info + alt detection warning (if applicable) in one embed. Cleaner log channel with no duplication.
- **🔧 ADMIN COMMANDS** - Added owner-only server management commands: /servers (list all servers with name/ID) and /createinvite <server_id> (create permanent invite). Total slash commands: 48
- **🎵 LAVALINK INTEGRATION** - Migrated music system to Lavalink for cloud environment compatibility. Uses public Lavalink nodes with automatic fallback. Supports YouTube, Spotify (metadata), and SoundCloud playback via wavelink library.
- **🎵 MUSIC SLASH COMMANDS** - Added 9 music slash commands (/play, /pause, /resume, /skip, /stop, /queue, /nowplaying, /loop, /volume)
- **📖 UPDATED HELP SYSTEM** - Refreshed !help, /help, and help.html to prominently display music platform support (YouTube, Spotify, SoundCloud) with dual prefix info
- **🎵 MUSIC SYSTEM** - Complete music player with YouTube, Spotify, and SoundCloud support via Lavalink. Features: play, pause, resume, skip, stop, queue, nowplaying, loop, and volume commands
- **👤 CREATOR BRANDING** - Updated all "v2.0 FUTURISTIC" references to "Made by MoonlightVFX" across website, bot commands, and documentation
- **📱 MOBILE-RESPONSIVE NAV** - Navigation bar now fully responsive with tablet (768px) and mobile (480px) breakpoints, smaller buttons and text on mobile, emoji-only mode for tiny screens
- **🎨 CSS CLASSES** - Converted inline navigation styles to proper CSS classes for better maintainability and responsive design
- **🌐 LANGUAGE TOGGLE** - Added EN/HU language switcher slider on website with localStorage persistence and full Hungarian translations
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

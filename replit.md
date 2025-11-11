# ⚡ SHADOW-MOD ✨ | Futuristic Discord Bot

## Overview
**Next-Gen Discord Moderation System v2.0 FUTURISTIC**

SHADOW-MOD is a comprehensive, cyberpunk-themed Discord bot built with Python, designed to provide advanced moderation, utility, and entertainment features. It aims to be an all-in-one solution for Discord servers, offering a modern user experience through Discord embeds and button components. The bot features multilanguage support (English & Hungarian), an AI Chat Assistant, a robust music system, and a sophisticated verification process with anti-alt protection. It also includes a full suite of moderation tools, interactive games, fun commands, a polling system, advanced role and giveaway management, and a unique name automation system. With extensive slash command support for the Active Developer Badge, custom command creation, and integrated auto-moderation, SHADOW-MOD is built to enhance server management and user engagement. Key capabilities also include customizable welcome/goodbye systems, reaction roles, a leveling/XP system, reminders, AFK status tracking, server statistics, and a community suggestion system.

## User Preferences
None specified yet.

## System Architecture
The bot is built with a modular, cog-based architecture in Python, ensuring maintainability and scalability. It features dual prefix support (`!` and `/`) and extensive slash command implementations (75+ commands across 27 cogs). A Flask web server (`web_server.py`) provides a live statistics dashboard, sharing data via `bot_stats.json`. Configuration is managed through `config.py` and `bot_config.json`, with multilingual translations handled by `translations.py`.

**UI/UX Decisions:**
- **Cyberpunk Neon Theme:** The bot and its accompanying web dashboard feature a futuristic, cyberpunk neon aesthetic with cyan, pink, purple, and blue color schemes.
- **Interactive Components:** All features heavily utilize Discord embeds, buttons, and other interactive components for a modern and engaging user experience.
- **Responsive Design:** The web dashboard is fully mobile-responsive, ensuring usability across various devices.
- **Readability:** UI elements are designed for eye comfort, with reduced excessive glow effects, dimmed backgrounds, and improved text readability with outlines/shadows.

**Technical Implementations:**
- **AI Chat Assistant:** Powered by OpenAI, responding to mentions in designated channels.
- **Music System:** Utilizes Lavalink for robust music playback from YouTube, Spotify (with metadata), and SoundCloud, managed via the `wavelink` library.
- **Verification System:** Button-based verification with integrated anti-alt account detection.
- **Custom Commands:** An owner-only system to create, remove, and modify custom text commands, stored dynamically.
- **Auto-Moderation:** Automated detection and punishment for spam, bad words, suspicious links, excessive caps, and emoji spam.
- **Logging:** Advanced logging to Discord channels for events, and a separate webhook logging system for bot errors and critical events.
- **Persistent Data:** Uses `bot_config.json` for runtime configuration and `bot_stats.json` for shared statistics.
- **Database:** Not explicitly stated, but implies local file-based storage for configurations and stats.

**Feature Specifications:**
- **Multi-language Support:** English and Hungarian, with a language switching command.
- **Server Management:** Comprehensive moderation suite (ban, kick, mute, tempmute, tempban, lock, unlock, warnings), role management, custom prefixes.
- **User Engagement:** Interactive games (RPS, Tic-Tac-Toe), fun commands (memes, sounds, 8ball), polls with live voting, giveaways, leveling/XP system with role rewards, reminders, AFK status.
- **Server Customization:** Customizable welcome/goodbye messages with auto-roles, reaction roles, name automation with role-based prefixes, suggestion system.
- **Information & Analytics:** Server info, bot info, user info (with badges), server statistics tracking.

## External Dependencies
- **Discord API:** Core integration for bot functionality.
- **OpenAI API:** For the AI Chat Assistant feature (`OPENAI_API_KEY`).
- **Lavalink:** Used by the `wavelink` library for the music system; connects to public Lavalink nodes.
- **Spotify API:** For Spotify track metadata integration within the music system (`SPOTIFY_CLIENT_ID`, `SPOTIFY_CLIENT_SECRET`).
- **Flask:** Python web framework for the web statistics dashboard.
- **Meme API:** For the multilingual meme generator (specific API not named).
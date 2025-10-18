# 🤖 Discord Bot with Buttons & Embeds

A feature-rich Discord bot built with Python and discord.py featuring an automated ticket system, anti-alt detection, comprehensive logging, moderation tools, interactive games, and fun commands!

## ✨ Features

### 🎫 Ticket System
- Button-based ticket creation
- Automatic ticket channels with proper permissions
- Easy ticket closing with confirmation embeds

### 🛡️ Anti-Alt Detection
- Automatically detects new/alt accounts based on account age
- Configurable minimum account age threshold
- Logs suspicious joins to your designated log channel

### 📋 Logging System
- Logs all important events to a Discord channel
- Message deletions and edits
- Member joins and leaves
- Bans, kicks, and moderation actions
- No need to check bot code!

### 🔨 Moderation Commands
- `!ban` - Ban users
- `!kick` - Kick users
- `!mute` / `!unmute` - Mute/unmute users
- `!tempmute` - Temporary mute with automatic unmute
- `!tempban` - Temporary ban with automatic unban
- `!lock` / `!unlock` - Lock/unlock channels
- `!warn` - Warn users
- `!warnings` - Check user warnings

### 🎮 Interactive Games
- **Rock Paper Scissors** - Play against the bot with button controls
- **Tic Tac Toe** - Challenge another user to a game with interactive board

### 😄 Fun Commands
- `!meme` - Generate random memes
- `!sound` - Random sound effects
- `!8ball` - Ask the magic 8-ball
- `!coinflip` - Flip a coin
- `!roll` - Roll dice (e.g., `!roll 2d6`)

### 📊 Poll System
- **Interactive Polls** - Create polls with button voting
- **Quick Polls** - Fast yes/no/maybe polls with reactions
- **Live Results** - Real-time vote counting with progress bars

### 👥 Role Management
- Create and delete roles with custom colors
- Assign/remove roles from members
- View role information and member counts
- List all server roles

### 🎉 Giveaway System
- Create timed giveaways with automatic winner selection
- Button-based entry system
- Multiple winner support
- Automatic ending and winner announcement
- Reroll functionality

### 📝 Name Automation
- Automatically add role prefixes to member nicknames
- Configure custom prefixes for different roles (e.g., "M |" for members, "A |" for admins)
- Automatic nickname updates on join and role changes
- Bulk nickname update commands

## 🚀 Setup Instructions

### 1. Get Your Discord Bot Token

1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Click "New Application" and give it a name
3. Go to the "Bot" section
4. Click "Add Bot"
5. Under the bot's username, click "Reset Token" and copy it
6. Enable these Privileged Gateway Intents:
   - Presence Intent
   - Server Members Intent
   - Message Content Intent

### 2. Set Up Your Bot Token

Create a `.env` file in the project root and add:
```
DISCORD_TOKEN=your_bot_token_here
```

### 3. Invite the Bot to Your Server

1. Go to OAuth2 > URL Generator in the Discord Developer Portal
2. Select scopes: `bot` and `applications.commands`
3. Select bot permissions:
   - Administrator (or specific permissions you want)
4. Copy the generated URL and open it in your browser
5. Select your server and authorize

### 4. Run the Bot

The bot will start automatically on Replit. If you need to run it manually:
```bash
python main.py
```

## 📖 Command Guide

### Setup Commands (Admin Only)
- `!setlog #channel` - Set the channel for bot logs
- `!setaltage <days>` - Set minimum account age (default: 7 days)
- `!ticket` - Create a ticket panel with button

### Moderation Commands
```
!ban @user [reason]       - Ban a user
!kick @user [reason]      - Kick a user
!mute @user               - Mute a user
!unmute @user             - Unmute a user
!tempmute @user 10m       - Temporarily mute (10s, 5m, 2h, 1d)
!tempban @user 1d reason  - Temporarily ban
!lock                     - Lock current channel
!unlock                   - Unlock current channel
!warn @user [reason]      - Warn a user
!warnings @user           - Check user's warnings
```

### Game Commands
```
!rps                - Play Rock Paper Scissors
!tictactoe @user    - Play Tic Tac Toe with another user
```

### Fun Commands
```
!meme              - Get a random meme
!sound             - Random sound effect
!8ball <question>  - Ask the magic 8-ball
!coinflip          - Flip a coin
!roll 2d6          - Roll dice
```

### Poll Commands
```
!poll <question> <opt1> <opt2> ...  - Create interactive poll with buttons
!quickpoll <question>               - Create yes/no/maybe poll with reactions
```

### Role Commands
```
!addrole @user @role       - Add a role to a user
!removerole @user @role    - Remove a role from a user
!createrole <name> [color] - Create a new role (color in hex: #FF5733)
!deleterole @role          - Delete a role
!roleinfo @role            - View detailed role information
!roles                     - List all server roles
```

### Giveaway Commands
```
!giveaway <time> <winners> <prize>  - Start a giveaway (e.g., !giveaway 1d 2 Nitro)
!reroll <message_id>                - Reroll a giveaway winner
```

### Name Automation Commands
```
!setprefix @role <prefix>  - Set automatic name prefix for role (e.g., M |)
!removeprefix @role        - Remove prefix from a role
!viewprefixes              - View all configured role prefixes
!updateallnicks            - Manually update all member nicknames
```

### General
```
!help              - Show all commands
```

## 🎨 All Features Use Embeds & Buttons!

Every interaction with this bot uses Discord's modern UI features:
- ✅ Beautiful embed messages with colors and formatting
- ✅ Interactive buttons for games and actions
- ✅ Persistent button views for ticket creation
- ✅ User-friendly and visually appealing

## 📝 Configuration

The bot stores configuration in `bot_config.json` including:
- Log channel ID
- Ticket counter
- Muted role IDs (per guild)
- Minimum account age for alt detection
- User warnings
- Temporary bans and mutes
- Active giveaways
- Role name prefixes

## 🔧 Troubleshooting

**Bot doesn't respond:**
- Make sure the bot has proper permissions
- Check if Message Content Intent is enabled
- Verify the bot token is correct in `.env`

**Temp mute/ban not working:**
- The bot needs to stay online for temporary actions to expire
- Check the bot's role is higher than the muted role

**Tickets not creating:**
- Ensure the bot has "Manage Channels" permission
- The bot's role must be higher than @everyone

## 📦 Dependencies

- discord.py - Discord API wrapper
- python-dotenv - Environment variable management
- aiohttp - Async HTTP requests for meme API
- Pillow - Image processing

## 🎉 Enjoy!

Your Discord bot is now ready with all features working through beautiful embeds and interactive buttons!

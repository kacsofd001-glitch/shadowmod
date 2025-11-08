"""
Multilanguage support for the Discord bot
Supports English (en) and Hungarian (hu)
"""

TRANSLATIONS = {
    'en': {
        # General
        'bot_ready': 'Bot is ready! Logged in as {}',
        'help_title': '🤖 Bot Commands Help',
        'help_description': 'Here are all available commands:',
        'help_footer': 'Commands work with ! or / prefix! Use buttons for interactive features',
        
        # Tickets
        'ticket_title': '🎫 Support Tickets',
        'ticket_description': 'Need help? Click the button below to create a ticket!',
        'ticket_how_it_works': 'How it works:',
        'ticket_steps': '• Click \'Create Ticket\'\n• A private channel will be created\n• Our staff will assist you\n• Close ticket when done',
        'ticket_button': '🎫 Create Ticket',
        'ticket_created': 'Ticket Created',
        'ticket_created_desc': 'Your ticket has been created: {}',
        'ticket_closed': 'Ticket Closed',
        'ticket_closed_desc': 'This ticket has been closed.',
        
        # Moderation
        'user_banned': '🔨 User Banned',
        'user_banned_desc': '{} has been banned from the server.',
        'user_kicked': '👢 User Kicked',
        'user_kicked_desc': '{} has been kicked from the server.',
        'user_muted': '🔇 User Muted',
        'user_muted_desc': '{} has been muted.',
        'user_unmuted': '🔊 User Unmuted',
        'user_unmuted_desc': '{} has been unmuted.',
        'channel_locked': '🔒 Channel Locked',
        'channel_locked_desc': 'This channel has been locked.',
        'channel_unlocked': '🔓 Channel Unlocked',
        'channel_unlocked_desc': 'This channel has been unlocked.',
        'user_warned': '⚠️ User Warned',
        'user_warned_desc': '{} has been warned.',
        'reason': 'Reason',
        'moderator': 'Moderator',
        'total_warnings': 'Total Warnings',
        'no_muted_role': 'No muted role found!',
        'user_not_muted': 'User is not muted!',
        'ban_failed': 'Failed to ban user: {}',
        'kick_failed': 'Failed to kick user: {}',
        'messages_purged': '🗑️ Messages Purged',
        'messages_purged_desc': 'Deleted {} messages from this channel.',
        'purge_limit': 'You can only delete up to 100 messages at once!',
        'purge_invalid': 'Please provide a valid number of messages to delete (1-100).',
        
        # Fun commands
        'magic_8ball': '🎱 Magic 8-Ball',
        'question': 'Question',
        'answer': 'Answer',
        'coin_flip': '🪙 Coin Flip',
        'coin_result': '**The coin landed on: {}!**',
        'heads': 'Heads',
        'tails': 'Tails',
        'meme_error': "❌ Couldn't fetch a meme right now!",
        'meme_footer': 'From r/{} | 👍 {}',
        'meme_title': '😂 Generated Meme',
        'generated_meme': 'Generated meme',
        
        # Configuration
        'webhook_set': '✅ Webhook Set',
        'webhook_set_desc': 'Bot logging webhook has been configured!',
        'webhook_test': '🧪 Test Webhook',
        'webhook_test_desc': 'This is a test message from the bot!',
        'tested_by': 'Tested by',
        'channel': 'Channel',
        'test_message': 'Test Message',
        'webhook_working': 'If this appears in your webhook channel, logging is working!',
        'webhook_configured': '✅ Webhook logging configured! Check your webhook channel.',
        'test_webhook_sent': '✅ Test webhook sent! Check your webhook channel.',
        'log_channel_set': '✅ Log Channel Set',
        'log_channel_desc': 'Log channel has been set to {}',
        
        # Language
        'language_set': '✅ Language Set',
        'language_set_desc': 'Server language has been set to **{}**',
        'language_en': 'English',
        'language_hu': 'Hungarian',
        'language_english': 'English',
        'language_hungarian': 'Hungarian',
        'current_language': 'Current language',
        
        # 8ball responses
        '8ball_responses': [
            "It is certain.", "It is decidedly so.", "Without a doubt.",
            "Yes definitely.", "You may rely on it.", "As I see it, yes.",
            "Most likely.", "Outlook good.", "Yes.", "Signs point to yes.",
            "Reply hazy, try again.", "Ask again later.", "Better not tell you now.",
            "Cannot predict now.", "Concentrate and ask again.",
            "Don't count on it.", "My reply is no.", "My sources say no.",
            "Outlook not so good.", "Very doubtful."
        ],
        
        # Help command
        'help_info': '📊 Information',
        'help_info_desc': '`/serverinfo` - Server statistics\n`/botinfo` - Bot features & uptime\n`/userinfo [@user]` - User profile with badges\n`/support` - Support server link\n`/webpage` - Live web dashboard',
        'help_security': '🔐 Security & Verification',
        'help_security_desc': '`/setupverify` - Deploy verification system\n`/setlog #channel` - Set log channel for alerts',
        'help_antialt': '🛡️ Anti-Alt System',
        'help_antialt_desc': '`Auto-detects new accounts on join`\n`/setaltage <days>` - Set min account age (default: 7d)\nAlerts sent to log channel automatically',
        'help_tickets': '🎫 Ticket System',
        'help_tickets_desc': '`/ticket` - Create a ticket panel\n`/closeticket` - Close a ticket',
        'help_moderation': '⚔️ Moderation',
        'help_moderation_desc': '`/ban` - Ban user\n`/kick` - Kick user\n`/mute` `/unmute` - Mute/unmute user\n`/tempmute <user> <time>` - Discord timeout (max 28d)\n`/purge <1-100>` - Bulk delete messages\n`/warn` - Warn user\n`/lock` `/unlock` - Lock/unlock channel',
        'help_music': '🎵 Music System',
        'help_music_desc': '`!play <song>` - Play music (YouTube/Spotify/SoundCloud)\n`!pause` - Pause playback\n`!resume` - Resume playback\n`!skip` - Skip song\n`!stop` - Stop & disconnect\n`!queue` - Show queue\n`!nowplaying` - Current song\n`!loop` - Toggle loop\n`!volume <0-100>` - Adjust volume',
        'help_games': '🎮 Entertainment',
        'help_games_desc': '`/rps` - Rock Paper Scissors\n`/tictactoe` - Tic Tac Toe\n`/meme` - Random meme\n`/8ball` - Magic 8-ball\n`/coinflip` - Flip coin\n`/dice` - Roll dice',
        'help_engagement': '🎁 Engagement',
        'help_engagement_desc': '`/poll` - Interactive polls\n`/giveaway` - Prize systems\n`/ticket` - Support tickets\n`/createrole` - Role management',
        'help_nameauto': '🏷️ Name Automation',
        'help_nameauto_desc': '`/setprefix <@role> <prefix>` - Set role prefix\n`/removeprefix <@role>` - Remove role prefix\n`/viewprefixes` - View all prefixes',
        'help_config': '🌐 System Configuration',
        'help_config_desc': '`/setlang <en/hu>` - Language switch\n`/setwebhook <url>` - Logging system\n`/ping` - Latency check',
        'no_reason_provided': 'No reason provided',
        
        # Errors
        'error_occurred': '❌ An error occurred: {}',
        'no_permission': '❌ You don\'t have permission to use this command!',
        'missing_argument': '❌ Missing required argument: {}',
        'invalid_language': '❌ Invalid language! Use: `en` (English) or `hu` (Hungarian)',
        'error_setting_language': '❌ Error setting language!',
        'invalid_user': '❌ Invalid user! Please provide a valid user mention or user ID.',
    },
    
    'hu': {
        # General
        'bot_ready': 'Bot készen áll! Bejelentkezve mint {}',
        'help_title': '🤖 Bot Parancsok Súgó',
        'help_description': 'Itt vannak az összes elérhető parancs:',
        'help_footer': 'A parancsok ! vagy / előtaggal működnek! Használj gombokat az interaktív funkciókhoz',
        
        # Tickets
        'ticket_title': '🎫 Támogatási Jegyek',
        'ticket_description': 'Segítségre van szükséged? Kattints az alábbi gombra jegy létrehozásához!',
        'ticket_how_it_works': 'Hogyan működik:',
        'ticket_steps': '• Kattints a \'Jegy Létrehozása\' gombra\n• Egy privát csatorna jön létre\n• A személyzetünk segíteni fog\n• Zárd le a jegyet, amikor készen vagy',
        'ticket_button': '🎫 Jegy Létrehozása',
        'ticket_created': 'Jegy Létrehozva',
        'ticket_created_desc': 'A jegyed létrehozva: {}',
        'ticket_closed': 'Jegy Lezárva',
        'ticket_closed_desc': 'Ez a jegy le lett zárva.',
        
        # Moderation
        'user_banned': '🔨 Felhasználó Kitiltva',
        'user_banned_desc': '{} kitiltva a szerverről.',
        'user_kicked': '👢 Felhasználó Kirúgva',
        'user_kicked_desc': '{} kirúgva a szerverről.',
        'user_muted': '🔇 Felhasználó Némítva',
        'user_muted_desc': '{} némítva.',
        'user_unmuted': '🔊 Felhasználó Visszahangosítva',
        'user_unmuted_desc': '{} visszahangosítva.',
        'channel_locked': '🔒 Csatorna Lezárva',
        'channel_locked_desc': 'Ez a csatorna le lett zárva.',
        'channel_unlocked': '🔓 Csatorna Feloldva',
        'channel_unlocked_desc': 'Ez a csatorna fel lett oldva.',
        'user_warned': '⚠️ Felhasználó Figyelmeztetve',
        'user_warned_desc': '{} figyelmeztetést kapott.',
        'reason': 'Indok',
        'moderator': 'Moderátor',
        'total_warnings': 'Összes Figyelmeztetés',
        'no_muted_role': 'Nincs némítási szerep!',
        'user_not_muted': 'A felhasználó nincs némítva!',
        'ban_failed': 'Nem sikerült kitiltani a felhasználót: {}',
        'kick_failed': 'Nem sikerült kirúgni a felhasználót: {}',
        'messages_purged': '🗑️ Üzenetek Törölve',
        'messages_purged_desc': '{} üzenet törölve ebből a csatornából.',
        'purge_limit': 'Egyszerre maximum 100 üzenetet törölhetsz!',
        'purge_invalid': 'Kérlek adj meg egy érvényes számot (1-100).',
        
        # Fun commands
        'magic_8ball': '🎱 Varázs 8-as Labda',
        'question': 'Kérdés',
        'answer': 'Válasz',
        'coin_flip': '🪙 Pénzfeldobás',
        'coin_result': '**A pénz így esett: {}!**',
        'heads': 'Fej',
        'tails': 'Írás',
        'meme_error': '❌ Nem sikerült meme-et lekérni!',
        'meme_footer': 'r/{} -ból/-ből | 👍 {}',
        'meme_title': '😂 Generált Meme',
        'generated_meme': 'Generált meme',
        
        # Configuration
        'webhook_set': '✅ Webhook Beállítva',
        'webhook_set_desc': 'A bot webhook naplózás be lett állítva!',
        'webhook_test': '🧪 Webhook Teszt',
        'webhook_test_desc': 'Ez egy teszt üzenet a bottól!',
        'tested_by': 'Tesztelte',
        'channel': 'Csatorna',
        'test_message': 'Teszt Üzenet',
        'webhook_working': 'Ha ez megjelenik a webhook csatornádban, a naplózás működik!',
        'webhook_configured': '✅ Webhook naplózás beállítva! Ellenőrizd a webhook csatornát.',
        'test_webhook_sent': '✅ Teszt webhook elküldve! Ellenőrizd a webhook csatornát.',
        'log_channel_set': '✅ Napló Csatorna Beállítva',
        'log_channel_desc': 'A napló csatorna beállítva: {}',
        
        # Language
        'language_set': '✅ Nyelv Beállítva',
        'language_set_desc': 'A szerver nyelve beállítva: **{}**',
        'language_en': 'Angol',
        'language_hu': 'Magyar',
        'language_english': 'Angol',
        'language_hungarian': 'Magyar',
        'current_language': 'Jelenlegi nyelv',
        
        # 8ball responses
        '8ball_responses': [
            "Biztos.", "Határozottan igen.", "Kétségtelenül.",
            "Igen, határozottan.", "Számíthatsz rá.", "Úgy látom, igen.",
            "Valószínűleg.", "Jó a kilátás.", "Igen.", "A jelek igenre mutatnak.",
            "Homályos, próbáld újra.", "Kérdezd később.", "Jobb, ha most nem mondom meg.",
            "Most nem lehet megjósolni.", "Összpontosíts és kérdezd újra.",
            "Ne számíts rá.", "A válaszom nem.", "A forrásaim szerint nem.",
            "Nem jó a kilátás.", "Nagyon kétséges."
        ],
        
        # Help command
        'help_info': '📊 Információk',
        'help_info_desc': '`/serverinfo` - Szerver statisztikák\n`/botinfo` - Bot funkciók & működési idő\n`/userinfo [@user]` - Felhasználó profil jelvényekkel\n`/support` - Support szerver link\n`/webpage` - Élő webes vezérlőpult',
        'help_security': '🔐 Biztonság & Hitelesítés',
        'help_security_desc': '`/setupverify` - Hitelesítési rendszer telepítése\n`/setlog #csatorna` - Napló csatorna beállítása',
        'help_antialt': '🛡️ Anti-Alt Rendszer',
        'help_antialt_desc': '`Automatikusan észleli az új fiókokat`\n`/setaltage <napok>` - Min. fiók kor (alapértelmezett: 7 nap)\nRiasztások automatikusan a napló csatornába',
        'help_tickets': '🎫 Jegy Rendszer',
        'help_tickets_desc': '`/ticket` - Jegy panel létrehozása\n`/closeticket` - Jegy lezárása',
        'help_moderation': '⚔️ Moderáció',
        'help_moderation_desc': '`/ban` - Felhasználó kitiltása\n`/kick` - Felhasználó kirúgása\n`/mute` `/unmute` - Némítás/visszahangosítás\n`/tempmute <user> <idő>` - Discord timeout (max 28 nap)\n`/purge <1-100>` - Tömeges üzenet törlés\n`/warn` - Figyelmeztetés\n`/lock` `/unlock` - Csatorna zárolás/feloldás',
        'help_music': '🎵 Zene Rendszer',
        'help_music_desc': '`!play <dal>` - Zene lejátszás (YouTube/Spotify/SoundCloud)\n`!pause` - Szüneteltetés\n`!resume` - Folytatás\n`!skip` - Dal átl épése\n`!stop` - Leállítás\n`!queue` - Várólista\n`!nowplaying` - Jelenlegi dal\n`!loop` - Ismétlés be/ki\n`!volume <0-100>` - Hangerő',
        'help_games': '🎮 Szórakoztatás',
        'help_games_desc': '`/rps` - Kő Papír Olló\n`/tictactoe` - Amőba\n`/meme` - Véletlen meme\n`/8ball` - Varázs labda\n`/coinflip` - Pénzfeldobás\n`/dice` - Kockadobás',
        'help_engagement': '🎁 Közösségi',
        'help_engagement_desc': '`/poll` - Interaktív szavazások\n`/giveaway` - Nyereményjátékok\n`/ticket` - Support jegyek\n`/createrole` - Szerep kezelés',
        'help_nameauto': '🏷️ Név Automatizálás',
        'help_nameauto_desc': '`/setprefix <@role> <prefix>` - Szerep prefix beállítása\n`/removeprefix <@role>` - Szerep prefix eltávolítása\n`/viewprefixes` - Összes prefix megtekintése',
        'help_config': '🌐 Rendszer Konfiguráció',
        'help_config_desc': '`/setlang <en/hu>` - Nyelv váltás\n`/setwebhook <url>` - Naplózó rendszer\n`/ping` - Késleltetés ellenőrzés',
        'no_reason_provided': 'Nincs megadva indok',
        
        # Errors
        'error_occurred': '❌ Hiba történt: {}',
        'no_permission': '❌ Nincs jogosultságod ehhez a parancshoz!',
        'missing_argument': '❌ Hiányzó kötelező paraméter: {}',
        'invalid_language': '❌ Érvénytelen nyelv! Használd: `en` (English) vagy `hu` (Hungarian)',
        'error_setting_language': '❌ Hiba a nyelv beállításakor!',
        'invalid_user': '❌ Érvénytelen felhasználó! Adj meg egy érvényes mention-t vagy felhasználó ID-t.',
    }
}

def get_text(guild_id, key, *args, **kwargs):
    """
    Get translated text for a guild
    
    Args:
        guild_id: Discord guild ID
        key: Translation key
        *args: Format arguments
        **kwargs: Additional options (lang override)
    
    Returns:
        Translated and formatted string
    """
    import config
    
    cfg = config.load_config()
    guild_langs = cfg.get('guild_languages', {})
    lang = kwargs.get('lang') or guild_langs.get(str(guild_id), 'en')
    
    # Fallback to English if language not found
    if lang not in TRANSLATIONS:
        lang = 'en'
    
    # Get translation, fallback to English if key not found
    text = TRANSLATIONS[lang].get(key)
    if text is None:
        text = TRANSLATIONS['en'].get(key, key)
    
    # Format with arguments if provided
    if args:
        try:
            return text.format(*args)
        except:
            return text
    
    return text

def get_guild_language(guild_id):
    """Get the current language for a guild"""
    import config
    
    cfg = config.load_config()
    guild_langs = cfg.get('guild_languages', {})
    return guild_langs.get(str(guild_id), 'en')

def set_guild_language(guild_id, lang):
    """Set the language for a guild"""
    import config
    
    if lang not in TRANSLATIONS:
        return False
    
    cfg = config.load_config()
    if 'guild_languages' not in cfg:
        cfg['guild_languages'] = {}
    
    cfg['guild_languages'][str(guild_id)] = lang
    config.save_config(cfg)
    return True

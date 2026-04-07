# -*- coding: utf-8 -*-
"""
Multilanguage support for the Discord bot
Supports English (en) and Hungarian (hu)
"""

TRANSLATIONS = {
    'en': {
        # General
        'bot_ready': 'Bot is ready! Logged in as {}',
        'pong': '🏓 Pong! {}ms',
        
        # Help
        'help_title': '🤖 Help Menu',
        'help_description': 'Choose a category to view commands:',
        'help_footer': '⚡ Made by MoonlightVFX | Futuristic Bot ⚡',
        'help_engagement': 'Click buttons to explore!',
        'help_unavailable': '❌ Help system is currently unavailable.',
        'error_loading_help': '❌ Error loading help: {}',
        
        # Categories
        'cat_moderation': '🛡️ Moderation',
        'cat_economy': '💰 Economy',
        'cat_games': '🎮 Mini-Games',
        'cat_fun': '🎭 Fun',
        'cat_utility': '⚙️ Utility',
        'cat_stats': '📊 Stats',
        'cat_setup': '🧙 Setup',
        'cat_back': '🏠 Back',
        
        # Help Descriptions
        'help_moderation': '⚔️ Moderation',
        'help_economy': '💰 Economy',
        'help_games': '🎮 Games',
        'help_fun': '🎭 Fun',
        'help_config': '🌐 Configuration',
        'help_stats': '📊 Stats',
        'help_modmail': '📬 ModMail',
        
        # Tickets
        'ticket_title': '🎫 Support Tickets',
        'ticket_description': 'Need help? Click the button below to create a ticket!',
        'ticket_how_it_works': 'How it works:',
        'ticket_steps': "• Click 'Create Ticket'\n• A private channel will be created\n• Our staff will assist you\n• Close ticket when done",
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
        
        # Language
        'language_set': '✅ Language Set',
        'language_set_desc': 'Server language has been set to **{}**',
        'language_en': 'English',
        'language_hu': 'Hungarian',
        'language_english': 'English',
        'language_hungarian': 'Hungarian',
        'current_language': 'Current language',
        'invalid_language': '❌ Invalid language! Use: `en` (English) or `hu` (Hungarian)',
        'error_setting_language': '❌ Error setting language!',
        
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
        
        # Errors
        'error_occurred': '❌ An error occurred: {}',
        'no_permission': "❌ You don't have permission to use this command!",
        'missing_argument': '❌ Missing required argument: {}',
        'permission_denied': "❌ You don't have permission to use this!",
        'message_sent': '✅ Message sent',
        'embed_sent': '✅ Embed sent',
        'generic_error': '❌ Error: {}',
        'invalid_user': '❌ Invalid user! Please provide a valid user mention or user ID.',
        'no_reason_provided': 'No reason provided',
    },
    
    'hu': {
        # General
        'bot_ready': 'Bot készen áll! Bejelentkezve mint {}',
        'pong': '🏓 Pong! {}ms',
        
        # Help
        'help_title': '🤖 Súgó Menü',
        'help_description': 'Válassz kategóriát a parancsok megtekintéséhez:',
        'help_footer': '⚡ MoonlightVFX által készítve | Futurisztikus Bot ⚡',
        'help_engagement': 'Kattints a gombokra a felfedezéshez!',
        'help_unavailable': '❌ A súgó rendszer jelenleg nem elérhető.',
        'error_loading_help': '❌ Hiba a súgó betöltésekor: {}',
        
        # Categories
        'cat_moderation': '🛡️ Moderáció',
        'cat_economy': '💰 Gazdaság',
        'cat_games': '🎮 Mini-Játékok',
        'cat_fun': '🎭 Szórakozás',
        'cat_utility': '⚙️ Eszközök',
        'cat_stats': '📊 Statisztika',
        'cat_setup': '🧙 Telepítés',
        'cat_back': '🏠 Vissza',
        
        # Help Descriptions
        'help_moderation': '⚔️ Moderáció',
        'help_economy': '💰 Gazdaság',
        'help_games': '🎮 Játékok',
        'help_fun': '🎭 Szórakozás',
        'help_config': '🌐 Konfiguráció',
        'help_stats': '📊 Statisztika',
        'help_modmail': '📬 ModMail',
        
        # Tickets
        'ticket_title': '🎫 Támogatási Jegyek',
        'ticket_description': 'Segítségre van szükséged? Kattints az alábbi gombra jegy létrehozásához!',
        'ticket_how_it_works': 'Hogyan működik:',
        'ticket_steps': "• Kattints a 'Jegy Létrehozása' gombra\n• Egy privát csatorna jön létre\n• A személyzetünk segíteni fog\n• Zárd le a jegyet, amikor készen vagy",
        'ticket_button': '🎫 Jegy Létrehozása',
        'ticket_created': 'Jegy Létrehozva',
        'ticket_created_desc': 'A jegyed létrehozva: {}',
        'ticket_closed': 'Jegy Lezárva',
        'ticket_closed_desc': 'Ez a jegy le lett zárva.',
        
        # Moderation
        'user_banned': '🔨 Felhasználó Kitiltva',
        'user_banned_desc': '{} ki lett bannolva a szerverről.',
        'user_kicked': '👢 Felhasználó Kirúgva',
        'user_kicked_desc': '{} ki lett rúgva a szerverről.',
        'user_muted': '🔇 Felhasználó Némítva',
        'user_muted_desc': '{} némítva lett.',
        'user_unmuted': '🔊 Felhasználó Visszahangosítva',
        'user_unmuted_desc': '{} vissza lett hangosítva.',
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
        
        # Language
        'language_set': '✅ Nyelv Beállítva',
        'language_set_desc': 'A szerver nyelve beállítva: **{}**',
        'language_en': 'Angol',
        'language_hu': 'Magyar',
        'language_english': 'Angol',
        'language_hungarian': 'Magyar',
        'current_language': 'Jelenlegi nyelv',
        'invalid_language': '❌ Érvénytelen nyelv! Használd: `en` (English) vagy `hu` (Hungarian)',
        'error_setting_language': '❌ Hiba a nyelv beállításakor!',
        
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
        
        # Errors
        'error_occurred': '❌ Hiba történt: {}',
        'no_permission': '❌ Nincs jogosultságod ehhez a parancshoz!',
        'missing_argument': '❌ Hiányzó kötelező paraméter: {}',
        'permission_denied': '❌ Nincs jogosultságod ehhez!',
        'message_sent': '✅ Üzenet elküldve',
        'embed_sent': '✅ Embed elküldve',
        'generic_error': '❌ Hiba: {}',
        'invalid_user': '❌ Érvénytelen felhasználó! Adj meg egy érvényes mention-t vagy felhasználó ID-t.',
        'no_reason_provided': 'Nincs megadva indok',
    }
}

def get_text(guild_id, key, *args, **kwargs):
    """Get translated text for a guild"""
    import config
    
    guild_id_str = str(guild_id)
    cfg = config.load_config()
    guild_langs = cfg.get('guild_languages', {})
    lang = kwargs.get('lang') or guild_langs.get(guild_id_str, 'en')
    
    if lang not in TRANSLATIONS:
        lang = 'en'
    
    text = TRANSLATIONS[lang].get(key)
    if text is None:
        text = TRANSLATIONS['en'].get(key, key)
    
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

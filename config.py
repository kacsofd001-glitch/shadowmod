import json
import os

CONFIG_FILE = 'bot_config.json'

DEFAULT_CONFIG = {
    'log_channel_id': None,
    'ticket_category_id': None,
    'ticket_counter': 0,
    'muted_roles': {},
    'min_account_age_days': 7,
    'warnings': {},
    'temp_bans': {},
    'temp_mutes': {},
    'giveaways': {},
    'completed_giveaways': {},
    'role_prefixes': {},
    'webhook_url': None,
    'guild_languages': {},
    'guild_prefixes': {}
}

def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    return DEFAULT_CONFIG.copy()

def save_config(config):
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=4)

def get_config():
    return load_config()

def update_config(key, value):
    config = load_config()
    config[key] = value
    save_config(config)
    return config

def get_guild_prefix(guild_id):
    """Get the prefix for a specific guild"""
    config = load_config()
    guild_prefixes = config.get('guild_prefixes', {})
    return guild_prefixes.get(str(guild_id), '!')

def set_guild_prefix(guild_id, prefix):
    """Set the prefix for a specific guild"""
    config = load_config()
    if 'guild_prefixes' not in config:
        config['guild_prefixes'] = {}
    config['guild_prefixes'][str(guild_id)] = prefix
    save_config(config)
    return prefix

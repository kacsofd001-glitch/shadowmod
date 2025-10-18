import json
import os

CONFIG_FILE = 'bot_config.json'

DEFAULT_CONFIG = {
    'log_channel_id': None,
    'ticket_category_id': None,
    'ticket_counter': 0,
    'muted_role_id': None,
    'min_account_age_days': 7,
    'warnings': {},
    'temp_bans': {},
    'temp_mutes': {}
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

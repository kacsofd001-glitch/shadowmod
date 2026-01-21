from flask import Flask, render_template, jsonify, redirect, request, session
from flask_cors import CORS
from datetime import datetime, timezone
import json
import os
import threading
import time
import sys
import requests
import secrets
from functools import wraps
from urllib.parse import quote

# Ensure unbuffered output
os.environ['PYTHONUNBUFFERED'] = '1'

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY', secrets.token_hex(32))
CORS(app)

# Import database module
from database import (
    init_db, get_guild_settings, update_guild_settings,
    save_user_session, get_user_session, delete_user_session,
    cache_user_guilds, get_user_admin_guilds, guild_exists_in_cache
)

# Discord OAuth2 configuration
DISCORD_CLIENT_ID = os.getenv('DISCORD_CLIENT_ID')
DISCORD_CLIENT_SECRET = os.getenv('DISCORD_CLIENT_SECRET')
DISCORD_REDIRECT_URI = os.getenv('DISCORD_REDIRECT_URI', 'https://shadowmod.onrender.com/auth/discord/callback')
DISCORD_API_BASE = 'https://discord.com/api'

# Check if OAuth2 is configured
OAUTH_CONFIGURED = bool(DISCORD_CLIENT_ID and DISCORD_CLIENT_SECRET)

# Initialize database on startup
init_db()

# Log OAuth configuration status
if not OAUTH_CONFIGURED:
    print("\n⚠️ WARNING: Discord OAuth2 is not configured!")
    print("❌ DISCORD_CLIENT_ID:", "NOT SET" if not DISCORD_CLIENT_ID else "✅ SET")
    print("❌ DISCORD_CLIENT_SECRET:", "NOT SET" if not DISCORD_CLIENT_SECRET else "✅ SET")
    print("\nTo fix this, set environment variables on Render:")
    print("  1. Go to Render Dashboard → Your Service")
    print("  2. Environment → Add Variable")
    print("  3. Add: DISCORD_CLIENT_ID=<your_client_id>")
    print("  4. Add: DISCORD_CLIENT_SECRET=<your_client_secret>")
    print("="*70)
else:
    print("\n✅ Discord OAuth2 is configured!")
    print(f"   Client ID: {DISCORD_CLIENT_ID[:10]}...")
    print("="*70)

STATS_FILE = 'bot_stats.json'

def login_required(f):
    """Decorator to require Discord login"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user_id = session.get('user_id')
        if not user_id:
            return redirect('/auth/discord')
        return f(*args, **kwargs)
    return decorated_function

def get_discord_user_info(access_token):
    """Get current user info from Discord"""
    headers = {'Authorization': f'Bearer {access_token}'}
    response = requests.get(f'{DISCORD_API_BASE}/v10/users/@me', headers=headers)
    return response.json() if response.status_code == 200 else None

def get_discord_user_guilds(access_token):
    """Get user's guilds from Discord"""
    headers = {'Authorization': f'Bearer {access_token}'}
    response = requests.get(f'{DISCORD_API_BASE}/v10/users/@me/guilds', headers=headers)
    return response.json() if response.status_code == 200 else []

def get_bot_stats():
    """Load stats from file"""
    try:
        if os.path.exists(STATS_FILE):
            with open(STATS_FILE, 'r') as f:
                stats = json.load(f)
                stats['start_time'] = datetime.fromisoformat(stats['start_time'])
                return stats
    except:
        pass
    
    # Default stats if file doesn't exist
    return {
        'start_time': datetime.now(timezone.utc),
        'guilds': 0,
        'users': 0,
        'channels': 0,
        'status': 'initializing'
    }

@app.route('/')
def index():
    """Public homepage"""
    user_id = session.get('user_id')
    
    response = app.make_response(render_template('index_public.html',
                         user_id=user_id,
                         username=session.get('username'),
                         avatar_url=session.get('avatar_url')))
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    return response

@app.route('/auth/discord')
def auth_discord():
    """Redirect to Discord OAuth2"""
    if not OAUTH_CONFIGURED:
        return render_template('oauth_error.html', error_type='not_configured'), 503
    
    state = secrets.token_urlsafe(32)
    session['oauth_state'] = state
    
    auth_url = (
    f'https://discord.com/api/oauth2/authorize?'
    f'client_id={DISCORD_CLIENT_ID}&'
    f'redirect_uri={quote(DISCORD_REDIRECT_URI)}&'
    f'response_type=code&'
    f'scope=identify%20guilds&'
    f'state={state}'
)
    return redirect(auth_url)

@app.route('/auth/discord/callback')
def auth_callback():
    """Handle Discord OAuth2 callback"""
    code = request.args.get('code')
    state = request.args.get('state')
    
    # Verify state
    if state != session.get('oauth_state'):
        return 'Invalid state', 403
    
    if not code:
        return 'No authorization code', 400
    
    # Exchange code for token
    data = {
        'client_id': DISCORD_CLIENT_ID,
        'client_secret': DISCORD_CLIENT_SECRET,
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': DISCORD_REDIRECT_URI,
        'scope': 'identify guilds'
    }
    
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    response = requests.post(
    'https://discord.com/api/oauth2/token',
    data=data,
    headers=headers
)

    
    if response.status_code != 200:
        return 'Failed to authenticate with Discord', 401
    
    token_data = response.json()
    access_token = token_data.get('access_token')
    refresh_token = token_data.get('refresh_token')
    expires_in = token_data.get('expires_in', 604800)  # 7 days default
    
    # Get user info
    user_info = get_discord_user_info(access_token)
    if not user_info:
        return 'Failed to get user info', 401
    
    user_id = user_info['id']
    username = user_info['username']
    avatar_hash = user_info.get('avatar')
    avatar_url = f'https://cdn.discordapp.com/avatars/{user_id}/{avatar_hash}.png' if avatar_hash else ''
    
    # Get guilds and cache
    guilds = get_discord_user_guilds(access_token)
    cache_user_guilds(user_id, guilds)
    
    # Save session
    save_user_session(user_id, access_token, refresh_token, username, avatar_url, expires_in)
    
    # Set session
    session['user_id'] = user_id
    session['username'] = username
    session['avatar_url'] = avatar_url
    
    return redirect('/dashboard')

@app.route('/auth/logout')
def logout():
    """Logout user"""
    user_id = session.get('user_id')
    if user_id:
        delete_user_session(user_id)
    session.clear()
    return redirect('/')


@app.route('/dashboard')
@login_required
def dashboard():
    """Main dashboard with guild list"""
    user_id = session.get('user_id')
    admin_guilds = get_user_admin_guilds(user_id)
    
    response = app.make_response(render_template('dashboard.html', 
                         username=session.get('username'),
                         avatar_url=session.get('avatar_url'),
                         admin_guilds=admin_guilds))
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    return response

@app.route('/dashboard/server/<guild_id>')
@login_required
def server_settings(guild_id):
    """Server settings page"""
    user_id = session.get('user_id')
    
    # Verify user is admin
    if not guild_exists_in_cache(user_id, guild_id):
        return 'Unauthorized', 403
    
    settings = get_guild_settings(guild_id)
    
    response = app.make_response(render_template('server_settings.html',
                         guild_id=guild_id,
                         username=session.get('username'),
                         avatar_url=session.get('avatar_url'),
                         settings=json.dumps(settings)))
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    return response

@app.route('/api/settings/<guild_id>', methods=['GET'])
@login_required
def api_get_settings(guild_id):
    """Get guild settings API"""
    user_id = session.get('user_id')
    
    if not guild_exists_in_cache(user_id, guild_id):
        return jsonify({'error': 'Unauthorized'}), 403
    
    settings = get_guild_settings(guild_id)
    return jsonify(settings)

@app.route('/api/settings/<guild_id>', methods=['POST'])
@login_required
def api_update_settings(guild_id):
    """Update guild settings API"""
    user_id = session.get('user_id')
    
    if not guild_exists_in_cache(user_id, guild_id):
        return jsonify({'error': 'Unauthorized'}), 403
    
    try:
        data = request.get_json()
        update_guild_settings(guild_id, data)
        return jsonify({'success': True, 'message': 'Settings updated'})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/servers')
@login_required
def api_servers():
    """Get user's admin servers"""
    user_id = session.get('user_id')
    admin_guilds = get_user_admin_guilds(user_id)
    return jsonify({'servers': admin_guilds})


@app.route('/help')
def help_page():
    """Display bot commands and help information"""
    response = app.make_response(render_template('help.html'))
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

@app.route('/api/stats')
def api_stats():
    try:
        stats = get_bot_stats()
        uptime = datetime.now(timezone.utc) - stats['start_time']
        
        return jsonify({
            'guilds': stats.get('guilds', 0),
            'users': stats.get('users', 0),
            'channels': stats.get('channels', 0),
            'uptime_seconds': int(uptime.total_seconds()),
            'status': stats.get('status', 'online')
        })
    except Exception as e:
        return jsonify({
            'guilds': 0,
            'users': 0,
            'channels': 0,
            'uptime_seconds': 0,
            'status': 'initializing',
            'error': str(e)
        }), 500

def start_bot():
    """Start the Discord bot in background thread"""
    print("\n🤖 Starting Discord bot in background...", flush=True)
    try:
        # Import bot module
        import main
        TOKEN = os.getenv('DISCORD_TOKEN')
        if not TOKEN:
            print("❌ DISCORD_TOKEN not found!", flush=True)
            return
        print("✅ TOKEN found, connecting to Discord...", flush=True)
        main.bot.run(TOKEN)
    except KeyboardInterrupt:
        print("\n⏹️ Bot stopped", flush=True)
    except Exception as e:
        print(f"❌ Bot error: {e}", flush=True)
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    print("=" * 70, flush=True)
    print("🚀 DiscordSage Application Startup", flush=True)
    print("=" * 70, flush=True)
    print(f"🔑 DISCORD_TOKEN: {'✅ SET' if os.getenv('DISCORD_TOKEN') else '❌ NOT SET'}", flush=True)
    print("=" * 70, flush=True)
    
    # Start bot in background thread
    print("\n📋 Initializing services...", flush=True)
    bot_thread = threading.Thread(target=start_bot, daemon=False, name="DiscordBot")
    bot_thread.start()
    
    # Give bot a moment to initialize
    time.sleep(2)
    
    # Start Flask web server (blocking)
    print("\n🌐 Starting Flask web server on 0.0.0.0:5000...", flush=True)
    try:
        app.run(host='0.0.0.0', port=5000, debug=False)
    except Exception as e:
        print(f"❌ Web server crashed: {e}", flush=True)
        import traceback
        traceback.print_exc()
    
    print("\n⏳ Waiting for bot thread...", flush=True)
    bot_thread.join(timeout=5)
    print("🛑 Application shutdown complete", flush=True)

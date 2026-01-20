from flask import Flask, render_template, jsonify, redirect
from flask_cors import CORS
from datetime import datetime, timezone
import json
import os
import threading
import time
import sys

# Ensure unbuffered output
os.environ['PYTHONUNBUFFERED'] = '1'

app = Flask(__name__)
CORS(app)

STATS_FILE = 'bot_stats.json'

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
    """Redirect root path to dashboard"""
    return redirect('/dashboard', code=302)

@app.route('/dashboard')
def dashboard():
    stats = get_bot_stats()
    uptime = datetime.now(timezone.utc) - stats['start_time']
    hours, remainder = divmod(int(uptime.total_seconds()), 3600)
    minutes, seconds = divmod(remainder, 60)
    days, hours = divmod(hours, 24)
    
    uptime_str = f"{days}d {hours}h {minutes}m {seconds}s"
    
    response = app.make_response(render_template('index.html', 
                         guilds=stats['guilds'],
                         users=stats['users'],
                         channels=stats['channels'],
                         uptime=uptime_str,
                         status=stats['status']))
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

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

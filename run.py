import os
import sys
import threading
import time

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("=" * 60)
print("🚀 DiscordSage Application Startup")
print("=" * 60)

def run_bot():
    """Run the Discord bot directly"""
    print("\n🤖 [BOT THREAD] Starting Discord bot...")
    try:
        # Import and run the bot
        import main
        TOKEN = os.getenv('DISCORD_TOKEN')
        if not TOKEN:
            print("❌ [BOT] DISCORD_TOKEN not found in environment!")
            return
        print("[BOT] Connecting to Discord...")
        main.bot.run(TOKEN)
    except KeyboardInterrupt:
        print("[BOT] Bot stopped by keyboard interrupt")
    except Exception as e:
        print(f"❌ [BOT] Bot crashed: {e}")
        import traceback
        traceback.print_exc()

def run_web():
    """Run the Flask web server directly"""
    print("\n🌐 [WEB THREAD] Starting Flask web server...")
    try:
        import web_server
        print("[WEB] Starting Flask on 0.0.0.0:5000...")
        web_server.app.run(host='0.0.0.0', port=5000, debug=False)
    except Exception as e:
        print(f"❌ [WEB] Web server crashed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print(f"\n📁 Working directory: {os.getcwd()}")
    print(f"🐍 Python version: {sys.version}")
    print(f"🔑 DISCORD_TOKEN set: {'Yes' if os.getenv('DISCORD_TOKEN') else 'No'}\n")
    
    # Start bot in background thread (daemon=False so it keeps process alive)
    bot_thread = threading.Thread(target=run_bot, daemon=False, name="BotThread")
    bot_thread.start()
    
    # Give bot a moment to start
    time.sleep(1)
    
    # Start web server in main thread (blocking)
    run_web()

#!/usr/bin/env python3
import os
import sys
import threading
import time
import signal
from dotenv import load_dotenv

# Build version for tracking deployments
BUILD_VERSION = "1.0.6-direct-import-bot"

# Load environment variables
load_dotenv()

# Ensure output is not buffered
os.environ['PYTHONUNBUFFERED'] = '1'

print("=" * 70, flush=True)
print("🚀 ShadowMod Application Startup", flush=True)
print(f"📦 Build: {BUILD_VERSION}", flush=True)
print("=" * 70, flush=True)
print(f"📁 Working directory: {os.getcwd()}", flush=True)
print(f"🐍 Python: {sys.executable}", flush=True)
print(f"🔑 DISCORD_TOKEN: {'✅ SET' if os.getenv('DISCORD_TOKEN') else '❌ NOT SET'}", flush=True)
print("=" * 70, flush=True)

bot_instance = None
web_process = None
stop_event = threading.Event()

def run_bot_direct():
    """Run the Discord bot directly in this thread"""
    global bot_instance
    
    restart_count = 0
    max_restarts = 5
    restart_delay = 5
    
    while restart_count < max_restarts and not stop_event.is_set():
        print(f"\n🤖 [BOT] Starting bot (attempt {restart_count + 1}/{max_restarts})...", flush=True)
        try:
            # Import bot here to get fresh instance each restart
            print("🤖 [BOT] Loading Discord bot from main.py...", flush=True)
            from main import bot
            bot_instance = bot
            
            TOKEN = os.getenv('DISCORD_TOKEN')
            if not TOKEN:
                print("❌ [BOT] FATAL: DISCORD_TOKEN is missing!", flush=True)
                sys.exit(1)
            
            print("🤖 [BOT] ✅ Bot loaded, connecting to Discord...", flush=True)
            # This runs forever until interrupted
            bot.run(TOKEN)
            
            # If we get here, bot.run() exited normally (clean shutdown)
            print("✅ [BOT] Bot shutdown cleanly", flush=True)
            break
            
        except KeyboardInterrupt:
            print("\n⏹️  [BOT] Bot interrupted", flush=True)
            break
        except Exception as e:
            print(f"❌ [BOT] Bot error: {e}", flush=True)
            import traceback
            traceback.print_exc()
            
            restart_count += 1
            if restart_count < max_restarts and not stop_event.is_set():
                print(f"⏳ [BOT] Restarting in {restart_delay}s (attempt {restart_count + 1}/{max_restarts})...", flush=True)
                time.sleep(restart_delay)
            else:
                print(f"❌ [BOT] Max restart attempts ({max_restarts}) reached", flush=True)
                break

def run_web_direct():
    """Run the Flask web server directly in this thread"""
    try:
        print("\n🌐 [WEB] Loading Flask web server...", flush=True)
        from web_server import app
        
        port = int(os.environ.get("PORT", 10000))
        print(f"🌐 [WEB] ✅ Flask loaded, starting on port {port}...", flush=True)
        app.run(host='0.0.0.0', port=port, debug=False, use_reloader=False)
        
    except Exception as e:
        print(f"❌ [WEB] Web server error: {e}", flush=True)
        import traceback
        traceback.print_exc()

def signal_handler(sig, frame):
    """Handle shutdown signals"""
    print("\n⏹️  [MAIN] Received shutdown signal, cleaning up...", flush=True)
    stop_event.set()
    sys.exit(0)

if __name__ == "__main__":
    print("\n📋 Starting ShadowMod services...\n", flush=True)
    
    # Register signal handlers for graceful shutdown
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    try:
        # Start bot thread
        print("🤖 [MAIN] Creating bot thread...", flush=True)
        bot_thread = threading.Thread(target=run_bot_direct, daemon=False, name="BotThread")
        bot_thread.start()
        print("✅ [MAIN] Bot thread started", flush=True)
        
        # Start web server thread
        print("🌐 [MAIN] Creating web server thread...", flush=True)
        web_thread = threading.Thread(target=run_web_direct, daemon=False, name="WebThread")
        web_thread.start()
        print("✅ [MAIN] Web server thread started", flush=True)
        
        print("\n✅ [MAIN] All services started - application running\n", flush=True)
        
        # Keep main thread alive
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\n⏹️  [MAIN] Interrupted by user", flush=True)
        signal_handler(None, None)
    except Exception as e:
        print(f"❌ [MAIN] Fatal error: {e}", flush=True)
        import traceback
        traceback.print_exc()
        sys.exit(1)
    
    print("\n🌐 [WEB] Starting web server...", flush=True)
    try:
        env = os.environ.copy()
        env['PYTHONUNBUFFERED'] = '1'
        
        web_process = subprocess.Popen(
            [sys.executable, '-u', 'web_server.py'],
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1
        )
        
        print("🌐 [WEB] Web server started, streaming logs...", flush=True)
        
        # Stream output from web server
        for line in web_process.stdout:
            if line.strip():
                print(f"🌐 [WEB] {line.rstrip()}", flush=True)
        
        # Wait for process
        return_code = web_process.wait()
        print(f"❌ [WEB] Web server process exited with code {return_code}", flush=True)
        
    except Exception as e:
        print(f"❌ [WEB] Failed to start web server: {e}", flush=True)
        import traceback
        traceback.print_exc()

def signal_handler(sig, frame):
    """Handle shutdown signals"""
    print("\n⏹️  Received shutdown signal, cleaning up...", flush=True)
    
    if bot_process:
        print("🛑 Stopping bot process...", flush=True)
        bot_process.terminate()
        try:
            bot_process.wait(timeout=5)
        except:
            bot_process.kill()
    
    if web_process:
        print("🛑 Stopping web server...", flush=True)
        web_process.terminate()
        try:
            web_process.wait(timeout=5)
        except:
            web_process.kill()
    
    print("✅ Cleanup complete", flush=True)
    sys.exit(0)

if __name__ == "__main__":
    print("\n📋 Starting ShadowMod services...\n", flush=True)
    
    # Register signal handlers for graceful shutdown
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Start bot in background thread with restart logic
    print("🤖 [MAIN] Starting bot thread...", flush=True)
    bot_thread = threading.Thread(target=run_bot_with_restart, daemon=False, name="BotThread")
    bot_thread.start()
    
    # Start web server in separate thread (non-blocking)
    print("🌐 [MAIN] Starting web server thread...", flush=True)
    web_thread = threading.Thread(target=run_web, daemon=False, name="WebThread")
    web_thread.start()
    
    print("✅ [MAIN] Both services started\n", flush=True)
    
    # Keep main thread alive - wait for both threads
    try:
        print("⏳ [MAIN] Keeping application alive...", flush=True)
        while True:
            time.sleep(1)
            # Check if threads are still alive periodically
            if not bot_thread.is_alive():
                print("⚠️  [MAIN] Bot thread died, restarting...", flush=True)
                bot_thread = threading.Thread(target=run_bot_with_restart, daemon=False, name="BotThread")
                bot_thread.start()
            
            if not web_thread.is_alive():
                print("❌ [MAIN] Web thread died!", flush=True)
                break
    except KeyboardInterrupt:
        print("\n⏹️  [MAIN] Interrupted", flush=True)
        signal_handler(None, None)

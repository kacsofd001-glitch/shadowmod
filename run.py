#!/usr/bin/env python3
"""
ShadowMod Main Application Runner
Runs Discord bot and Flask web server together in separate threads
"""

import os
import sys
import threading
import time
import signal
from dotenv import load_dotenv
from monitor import log_event, print_diagnostics

# Build version for tracking deployments
BUILD_VERSION = "1.0.8-enhanced-monitoring"

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

log_event("STARTUP", "Application starting", {"build": BUILD_VERSION})

bot_instance = None
stop_event = threading.Event()
shutdown_lock = threading.Lock()

def graceful_exit(reason="User request"):
    """Ensure clean shutdown"""
    with shutdown_lock:
        if not stop_event.is_set():
            print(f"\n⏹️  [MAIN] Initiating graceful shutdown ({reason})...", flush=True)
            log_event("SHUTDOWN", f"Graceful shutdown: {reason}")
            print_diagnostics()
            stop_event.set()
            time.sleep(0.5)
            sys.exit(0)

def run_bot_direct():
    """Run the Discord bot directly in this thread with crash handling"""
    global bot_instance
    
    restart_count = 0
    max_restarts = 5
    restart_delay = 3
    
    while restart_count < max_restarts and not stop_event.is_set():
        try:
            print(f"\n🤖 [BOT] Starting bot (attempt {restart_count + 1}/{max_restarts})...", flush=True)
            
            # Import bot here to get fresh instance each restart
            print("🤖 [BOT] Loading Discord bot from main.py...", flush=True)
            from main import bot
            bot_instance = bot
            
            TOKEN = os.getenv('DISCORD_TOKEN')
            if not TOKEN:
                print("❌ [BOT] FATAL: DISCORD_TOKEN is missing!", flush=True)
                log_event("ERROR", "DISCORD_TOKEN not set", {"error": "Missing environment variable"})
                graceful_exit("Missing DISCORD_TOKEN")
                return
            
            print("🤖 [BOT] ✅ Bot loaded, connecting to Discord...", flush=True)
            log_event("BOT_START", f"Starting bot (attempt {restart_count + 1})")
            
            # This runs forever until interrupted or crashes
            bot.run(TOKEN)
            
            # If we get here, bot.run() exited
            if stop_event.is_set():
                print("✅ [BOT] Bot shutdown on stop signal", flush=True)
                log_event("BOT_STOP", "Bot exited cleanly")
                return
            else:
                print("⚠️  [BOT] Bot exited unexpectedly (no error logged)", flush=True)
                log_event("BOT_EXIT", "Bot exited without error", {"attempt": restart_count + 1})
                restart_count += 1
                
        except KeyboardInterrupt:
            print("\n⏹️  [BOT] Bot interrupted by user", flush=True)
            log_event("BOT_INTERRUPT", "Interrupted by keyboard")
            graceful_exit("Bot interrupted by user")
            return
        except Exception as e:
            print(f"❌ [BOT] Bot crashed: {type(e).__name__}: {e}", flush=True)
            log_event("BOT_CRASH", f"{type(e).__name__}: {e}", {"attempt": restart_count + 1})
            import traceback
            traceback.print_exc()
            
            restart_count += 1
            if restart_count < max_restarts and not stop_event.is_set():
                print(f"⏳ [BOT] Restarting in {restart_delay}s (attempt {restart_count + 1}/{max_restarts})...", flush=True)
                time.sleep(restart_delay)
            else:
                print(f"❌ [BOT] Max restart attempts ({max_restarts}) reached or shutdown triggered", flush=True)
                log_event("BOT_MAX_RESTARTS", f"Max restart attempts reached", {"restarts": max_restarts})
                graceful_exit(f"Max restarts ({max_restarts}) exceeded")
                return
    
    print("❌ [BOT] Bot thread exiting", flush=True)
    log_event("BOT_THREAD_EXIT", "Bot thread exited")

def run_web_direct():
    """Run the Flask web server directly in this thread"""
    try:
        print("\n🌐 [WEB] Loading Flask web server...", flush=True)
        from web_server import app
        
        port = int(os.environ.get("PORT", 10000))
        print(f"🌐 [WEB] ✅ Flask loaded, starting on port {port}...", flush=True)
        log_event("WEB_START", f"Web server starting on port {port}")
        
        app.run(host='0.0.0.0', port=port, debug=False, use_reloader=False, threaded=True)
        
    except KeyboardInterrupt:
        print("\n⏹️  [WEB] Web server interrupted", flush=True)
        log_event("WEB_INTERRUPT", "Web server interrupted")
        graceful_exit("Web server interrupted")
    except Exception as e:
        print(f"❌ [WEB] Web server crashed: {type(e).__name__}: {e}", flush=True)
        log_event("WEB_CRASH", f"{type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        graceful_exit(f"Web server crashed: {e}")

def signal_handler(sig, frame):
    """Handle shutdown signals"""
    sig_name = signal.Signals(sig).name if sig else "UNKNOWN"
    print(f"\n⏹️  [MAIN] Received {sig_name} signal, cleaning up...", flush=True)
    log_event("SIGNAL", f"Received {sig_name}")
    graceful_exit(f"{sig_name} signal")

if __name__ == "__main__":
    print("\n📋 Starting ShadowMod services...\n", flush=True)
    log_event("SERVICES_START", "Starting bot and web services")
    
    # Register signal handlers for graceful shutdown
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    try:
        # Start bot thread
        print("🤖 [MAIN] Creating bot thread...", flush=True)
        bot_thread = threading.Thread(target=run_bot_direct, daemon=False, name="BotThread")
        bot_thread.start()
        print("✅ [MAIN] Bot thread started", flush=True)
        log_event("BOT_THREAD_START", "Bot thread created and started")
        
        # Start web server thread
        print("🌐 [MAIN] Creating web server thread...", flush=True)
        web_thread = threading.Thread(target=run_web_direct, daemon=False, name="WebThread")
        web_thread.start()
        print("✅ [MAIN] Web server thread started", flush=True)
        log_event("WEB_THREAD_START", "Web thread created and started")
        
        print("\n✅ [MAIN] All services started - application running\n", flush=True)
        
        # Keep main thread alive and monitor for issues
        last_check = time.time()
        check_interval = 10  # Check every 10 seconds
        
        while True:
            time.sleep(1)
            
            # Periodic check for dead threads
            current_time = time.time()
            if current_time - last_check >= check_interval:
                last_check = current_time
                
                bot_alive = bot_thread.is_alive()
                web_alive = web_thread.is_alive()
                
                if not bot_alive and not stop_event.is_set():
                    print("⚠️  [MAIN] ⚠️ BOT THREAD DIED UNEXPECTEDLY! ⚠️", flush=True)
                    log_event("CRITICAL", "Bot thread died unexpectedly")
                    graceful_exit("Bot thread died")
                
                if not web_alive and not stop_event.is_set():
                    print("⚠️  [MAIN] ⚠️ WEB THREAD DIED UNEXPECTEDLY! ⚠️", flush=True)
                    log_event("CRITICAL", "Web thread died unexpectedly")
                    graceful_exit("Web thread died")
            
    except KeyboardInterrupt:
        print("\n⏹️  [MAIN] Interrupted by user", flush=True)
        log_event("USER_INTERRUPT", "Interrupted by Ctrl+C")
        graceful_exit("User interrupt")
    except Exception as e:
        print(f"❌ [MAIN] Fatal error: {e}", flush=True)
        log_event("FATAL_ERROR", str(e))
        import traceback
        traceback.print_exc()
        print_diagnostics()
        sys.exit(1)
        signal_handler(None, None)

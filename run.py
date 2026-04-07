#!/usr/bin/env python3
import os
import sys
import subprocess
import threading
import time
import signal

# Build version for tracking deployments  - tracks which version is running on Render
BUILD_VERSION = "1.0.5-c64d991-process-fix"

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

bot_process = None
web_process = None

def run_bot_with_restart():
    """Run the Discord bot in subprocess with auto-restart on crash"""
    global bot_process
    
    restart_count = 0
    max_restarts = 5
    restart_delay = 5
    
    while restart_count < max_restarts:
        print(f"\n🤖 [BOT] Starting bot (attempt {restart_count + 1}/{max_restarts})...", flush=True)
        try:
            # Run bot with unbuffered output
            env = os.environ.copy()
            env['PYTHONUNBUFFERED'] = '1'
            
            bot_process = subprocess.Popen(
                [sys.executable, '-u', 'run_bot.py'],
                env=env,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1
            )
            
            print("🤖 [BOT] Bot started, streaming logs...", flush=True)
            
            # Stream output from bot
            for line in bot_process.stdout:
                if line.strip():
                    print(f"🤖 [BOT] {line.rstrip()}", flush=True)
            
            # Wait for process
            return_code = bot_process.wait()
            print(f"⚠️  [BOT] Bot process exited with code {return_code}", flush=True)
            
            if return_code == 0:
                print("✅ [BOT] Bot shutdown cleanly", flush=True)
                break
            else:
                restart_count += 1
                if restart_count < max_restarts:
                    print(f"⏳ [BOT] Restarting in {restart_delay}s...", flush=True)
                    time.sleep(restart_delay)
                else:
                    print(f"❌ [BOT] Max restart attempts ({max_restarts}) reached", flush=True)
        
        except Exception as e:
            print(f"❌ [BOT] Failed to start bot: {e}", flush=True)
            import traceback
            traceback.print_exc()

def run_web():
    """Run the Flask web server"""
    global web_process
    
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

import os
import threading
import subprocess
import sys

def run_bot():
    """Run the Discord bot"""
    print("🤖 Starting Discord bot...")
    subprocess.run([sys.executable, "main.py"])

def run_web():
    """Run the Flask web server"""
    print("🌐 Starting web server...")
    subprocess.run([sys.executable, "web_server.py"])

if __name__ == "__main__":
    # Start bot in background thread
    bot_thread = threading.Thread(target=run_bot, daemon=False)
    bot_thread.start()
    
    # Start web server in main thread
    run_web()

"""
Separate bot runner - runs only the Discord bot
Use this as a separate worker process on Render
"""

import os
import sys
import time
from dotenv import load_dotenv

# Load environment early
load_dotenv()
print("🔄 Loading Discord bot...", flush=True)

try:
    from main import bot
    
    TOKEN = os.getenv('DISCORD_TOKEN')
    if not TOKEN:
        print("❌ FATAL: DISCORD_TOKEN is missing!", flush=True)
        sys.exit(1)
    
    print("🤖 Starting Discord bot...", flush=True)
    bot.run(TOKEN)
    
except KeyboardInterrupt:
    print("\n⏹️  Bot interrupted by user", flush=True)
    sys.exit(0)
    
except Exception as e:
    print(f"❌ Bot crashed with error: {e}", flush=True)
    import traceback
    traceback.print_exc()
    sys.exit(1)

"""
Separate web server runner - runs only the Flask web server without bot
Use this for Render: add to Procfile as: web: python run_web.py
"""

import os
import sys
from web_server import app

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    print(f"🚀 Web Server Starting on port {port}", flush=True)
    print(f"📍 Routes available:", flush=True)
    print(f"   - GET  / (Homepage)", flush=True)
    print(f"   - GET  /why-us (Why Us page)", flush=True)
    print(f"   - GET  /help (Commands)", flush=True)
    print(f"   - GET  /auth/discord (OAuth)", flush=True)
    print(f"   - GET  /dashboard (Dashboard)", flush=True)
    app.run(host='0.0.0.0', port=port, debug=False)

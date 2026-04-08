"""
Process monitoring and health checking for ShadowMod
Provides diagnostics when bot stops unexpectedly
"""

import os
import json
import time
from datetime import datetime

MONITOR_FILE = 'bot_monitor.json'

def log_event(event_type, message, details=None):
    """Log an event to monitoring file"""
    try:
        # Load existing events
        events = []
        if os.path.exists(MONITOR_FILE):
            try:
                with open(MONITOR_FILE, 'r') as f:
                    events = json.load(f)
            except:
                events = []
        
        # Add new event
        event = {
            'timestamp': datetime.now().isoformat(),
            'type': event_type,
            'message': message,
            'details': details or {}
        }
        events.append(event)
        
        # Keep last 100 events
        events = events[-100:]
        
        # Save
        with open(MONITOR_FILE, 'w') as f:
            json.dump(events, f, indent=2)
    except Exception as e:
        print(f"⚠️ Failed to log event: {e}")

def get_recent_events(count=10):
    """Get recent events from monitor log"""
    try:
        if os.path.exists(MONITOR_FILE):
            with open(MONITOR_FILE, 'r') as f:
                events = json.load(f)
                return events[-count:]
    except:
        pass
    return []

def print_diagnostics():
    """Print diagnostic information"""
    print("\n" + "=" * 70)
    print("📊 BOT DIAGNOSTICS")
    print("=" * 70)
    
    # Check monitor log
    events = get_recent_events(10)
    if events:
        print("\n📋 Recent Events:")
        for i, event in enumerate(events, 1):
            print(f"  {i}. [{event['type']}] {event['timestamp']}")
            print(f"     {event['message']}")
    
    # Check bot stats
    if os.path.exists('bot_stats.json'):
        try:
            with open('bot_stats.json', 'r') as f:
                stats = json.load(f)
                print(f"\n📈 Bot Stats:")
                print(f"  Start Time: {stats.get('start_time', 'N/A')}")
                print(f"  Guilds: {stats.get('guilds', 0)}")
                print(f"  Users: {stats.get('users', 0)}")
                print(f"  Channels: {stats.get('channels', 0)}")
        except:
            pass
    
    # Check error log
    if os.path.exists('bot_errors.log'):
        try:
            with open('bot_errors.log', 'r') as f:
                lines = f.readlines()
                if lines:
                    print(f"\n❌ Recent Errors ({len(lines)} total):")
                    for line in lines[-5:]:
                        print(f"  {line.strip()}")
        except:
            pass
    
    print("=" * 70 + "\n")

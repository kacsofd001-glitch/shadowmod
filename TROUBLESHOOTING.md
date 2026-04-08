# Bot Shutdown Troubleshooting Guide

## Problem: Bot Stops Without Errors

When your bot suddenly stops with the message "Received shutdown signal, cleaning up..." but no error is logged, it's likely one of these:

### Recent Fixes Applied (v1.0.8)

1. **Enhanced Process Monitoring** - Now logs all major events:
   - Bot start/stop/crash events
   - Web server status changes
   - Thread lifecycle events
   - All exceptions with stack traces

2. **Thread Health Checking** - Main thread now monitors:
   - Bot thread heartbeat every 10 seconds
   - Web server thread status
   - Immediate shutdown if a thread dies unexpectedly

3. **Better Diagnostics** - New `monitor.py` module:
   - Tracks all events in `bot_monitor.json`
   - Provides `print_diagnostics()` on shutdown
   - Automatically displays last 10 events + errors

## How to Investigate Shutdowns

### 1. Check the Monitor Log
After bot stops, look at `bot_monitor.json`:
```json
{
  "timestamp": "2026-04-08T02:16:43.123456",
  "type": "BOT_CRASH",
  "message": "Exception details here",
  "details": {"attempt": 1}
}
```

Common event types:
- `BOT_CRASH` - Bot threw an exception
- `BOT_EXIT` - Bot exited without error
- `WEB_CRASH` - Flask crashed
- `CRITICAL` - Thread died unexpectedly

### 2. Check Error Logs
- `bot_errors.log` - Event handler errors
- `bot_monitor.json` - All shutdown events

### 3. Common Causes

| Symptom | Cause | Fix |
|---------|-------|-----|
| Clean shutdown, no errors | Cog import fails silently | Check `main.py` cog loading |
| Web thread dies | Flask port conflict | Change PORT env var |
| Bot thread dies | Discord connection issue | Check internet/token |
| Restart loop | Cog bug on startup | Check recent cog changes |

## Running Diagnostics

### Manually Check Bot Status
```python
from monitor import print_diagnostics
print_diagnostics()
```

### View Recent Events
```python
from monitor import get_recent_events
events = get_recent_events(20)
for e in events:
    print(f"{e['timestamp']} - {e['type']}: {e['message']}")
```

### Start Bot with Debug Output
```bash
python run.py
```
All thread activity is now logged with timestamps.

## Prevention

1. **Test Cogs Locally** - Before deploying, ensure no cogs fail on import
2. **Monitor bot_monitor.json** - Check for patterns before crashes
3. **Check Discord Status** - Sometimes Discord API has issues
4. **Verify Environment** - Ensure TOKEN, PORT, and other env vars are set

## Build Versions and Features

| Version | Features |
|---------|----------|
| 1.0.6 | Basic bot/web separation |
| 1.0.7 | Stable threading |
| 1.0.8 | **Enhanced monitoring ← Current** |

### New in 1.0.8
- ✅ Event logging to `bot_monitor.json`
- ✅ Diagnostic printing on shutdown
- ✅ Thread health checks every 10 seconds
- ✅ Better error context in logs
- ✅ Failed shutdown reasons tracked

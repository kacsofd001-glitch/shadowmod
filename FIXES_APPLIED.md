# ShadowMod - Fixes for "Why Us" Page and Random Shutdowns

## Problems Fixed

### 1. "Why Us" URL Not Working
**Root Cause:** The route was defined but couldn't be accessed reliably when the bot was running in a background thread in Flask.

**Solution:** 
- Removed the Discord bot thread from `web_server.py`
- Added error handling and logging to the `/why-us` route
- Bot now runs as a completely separate process managed by `run.py`
- Added health check endpoint at `/api/health`

### 2. Bot Randomly Shutting Down on Render
**Root Cause:** 
- Bot was running in a daemon thread within Flask, causing it to be killed when Flask crashed
- No restart mechanism if the bot crashed
- Complex threading/process mixing made debugging difficult

**Solution:**
- Separated bot and web server into independent processes
- Added auto-restart logic to `run_bot.py` (max 5 restart attempts)
- Improved process management in `run.py` with signal handling
- Better error logging for both services
- Each service can now run independently

## File Changes

### New Files Created
1. **`run_bot.py`** - Standalone Discord bot runner
   - Handles all bot startup logic
   - Clean error reporting
   - Can be run independently if needed

2. **`run_web.py`** - Standalone web server runner
   - Only runs Flask (no bot interference)
   - Useful for testing web routes locally

### Modified Files
1. **`web_server.py`**
   - Removed bot threading code
   - Added error handling to `/why-us` route
   - Added `/api/health` endpoint for monitoring
   - Cleaned up unused imports

2. **`run.py`**
   - Improved process management
   - Added auto-restart logic for bot (5 attempts)
   - Added signal handlers for graceful shutdown
   - Better process logging

## Testing Locally

### Test the Web Server
```bash
python run_web.py
# Visit: http://localhost:10000/why-us
# Check health: http://localhost:10000/api/health
```

### Test the Bot
```bash
python run_bot.py
# Watch for successful login and command sync
```

### Test Everything Together
```bash
python run.py
# Both services start with proper logging
# Bot auto-restarts if it crashes (up to 5 times)
```

## Deployment Instructions for Render

### Option 1: Single Dyno (Current Setup)
Update your `Procfile`:
```
web: python run.py
```

This will start both the web server and bot in the same process with proper isolation and restart logic.

### Option 2: Separate Dynos (Recommended for Production)
Update your `Procfile`:
```
web: python run_web.py
worker: python run_bot.py
```

Then in Render dashboard:
1. Add a new "Worker" service with the same repo
2. Set the command to `python run_bot.py`
3. Make sure both services share the same environment variables

## Key Improvements

✅ **Better Stability:** Web server no longer depends on bot thread  
✅ **Auto-Restart:** Bot restarts automatically if it crashes (up to 5 times)  
✅ **Error Logging:** Both services log independently for easier debugging  
✅ **Health Monitoring:** New `/api/health` endpoint for monitoring  
✅ **Graceful Shutdown:** Proper signal handling for clean shutdowns  
✅ **Why Us URL:** Now accessible and properly error-handled  

## Testing the Fix

1. **Test Why Us Page:**
   ```
   Visit: https://your-render-url/why-us
   Check logs for: "✅ /why-us route accessed successfully"
   ```

2. **Test Health Check:**
   ```
   Visit: https://your-render-url/api/health
   Should return: {"status": "ok", "service": "web-server", "bot": "runs separately"}
   ```

3. **Monitor Logs:**
   - Web server logs start with `🌐 [WEB]`
   - Bot logs start with `🤖 [BOT]`
   - Easy to distinguish which service has issues

## Troubleshooting

If the bot still shuts down randomly:

1. **Check Render logs** for error messages in bot output
2. **Check if a cog is crashing** - look for `❌ Error in event` in logs
3. **Increase restart attempts** - edit `max_restarts = 5` in `run.py`
4. **Use separate dynos** - Option 2 in Procfile for more stability

## Questions or Issues?

Check the logs in Render dashboard:
- Filter by `🌐 [WEB]` for web server issues
- Filter by `🤖 [BOT]` for bot issues
- Look at `/api/health` endpoint to verify web server is running

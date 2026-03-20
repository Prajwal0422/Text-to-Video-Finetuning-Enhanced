# Troubleshooting Guide

## Common Issues

### Video Generation Fails
**Symptom:** "Generation failed" error message

**Solutions:**
1. Check Pexels API key in `.env` file
2. Verify internet connection
3. Check server logs for specific errors
4. Try a different prompt
5. Restart the server

### Server Won't Start
**Symptom:** Server fails to start or crashes

**Solutions:**
1. Check if port 8000 is already in use
2. Verify Python version (3.11+ required)
3. Install missing dependencies: `pip install -r requirements.txt`
4. Check FFmpeg installation
5. Review error logs

### WebSocket Connection Failed
**Symptom:** Dashboard shows "offline" status

**Solutions:**
1. Refresh the browser page
2. Check if server is running
3. Clear browser cache
4. Try a different browser
5. Check firewall settings

### Slow Generation
**Symptom:** Video takes too long to generate

**Solutions:**
1. Use "Fast Mode" instead of "Quality Mode"
2. Reduce video duration
3. Check internet speed
4. Clear clip cache: delete `outputs/cache/`
5. Restart server

### No Clips Found
**Symptom:** "No clips found" error

**Solutions:**
1. Try more generic prompts
2. Check Pexels API quota
3. Use different keywords
4. Wait and retry (API rate limit)
5. Check API key validity

## Error Messages

### "Model experiencing high traffic"
- **Cause:** API rate limiting
- **Solution:** Wait 5-10 seconds, system will retry automatically

### "Timeout error"
- **Cause:** Request took too long
- **Solution:** System will switch to fallback mode automatically

### "Local generation mode"
- **Cause:** All API methods failed
- **Solution:** Uses cached clips, may have limited variety

## Performance Tips

1. **Use specific prompts** - "sunset over ocean" vs "nature"
2. **Keep prompts under 100 characters**
3. **Avoid complex scenes** - simpler prompts work better
4. **Use recommended categories** - nature, city, travel, etc.
5. **Clear cache periodically** - prevents disk space issues

## Getting Help

1. Check server logs: Process output in terminal
2. Review API stats: `http://localhost:8000/api/stats`
3. Test API health: `http://localhost:8000/api/health`
4. Check GitHub issues
5. Review documentation files

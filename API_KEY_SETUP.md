# 🔑 API Key Setup Guide

## Do You Need an API Key?

**Short Answer: Optional but HIGHLY RECOMMENDED**

The system works in two modes:

### ✅ WITH API Key (Recommended)
- Access to 1000+ HD stock videos
- Better quality clips
- More variety
- Faster matching
- 200 requests/hour (free tier)

### ⚠️ WITHOUT API Key (Fallback Mode)
- Uses sample/placeholder videos
- Limited variety
- Generic results
- Still works, but lower quality

---

## 🎯 Getting Your FREE Pexels API Key

### Step 1: Sign Up
1. Go to: **https://www.pexels.com/api/**
2. Click "Get Started" or "Sign Up"
3. Create a free account (email + password)

### Step 2: Get API Key
1. After login, go to: **https://www.pexels.com/api/new/**
2. Fill in the form:
   - **App Name**: NEXUS VISION
   - **App Description**: Text-to-video generation platform
   - **App URL**: http://localhost:8000 (or your domain)
3. Click "Generate API Key"
4. **Copy your API key** (looks like: `abc123xyz456...`)

### Step 3: Add to Your System

#### Option A: Environment Variable (Recommended)

**Windows (PowerShell):**
```powershell
$env:PEXELS_API_KEY="your_api_key_here"
```

**Windows (Command Prompt):**
```cmd
set PEXELS_API_KEY=your_api_key_here
```

**Linux/Mac:**
```bash
export PEXELS_API_KEY="your_api_key_here"
```

#### Option B: Create .env File
1. Copy the example file:
```bash
cd backend
copy .env.example .env
```

2. Edit `.env` file and add your key:
```
PEXELS_API_KEY=your_actual_api_key_here
```

3. Install python-dotenv:
```bash
pip install python-dotenv
```

4. Update `backend/main.py` to load .env:
```python
from dotenv import load_dotenv
load_dotenv()
```

#### Option C: Hardcode (Not Recommended for Production)
Edit `backend/main.py`:
```python
video_gen = VideoGenerator(pexels_api_key="your_api_key_here")
```

---

## 🔍 Verify API Key is Working

### Method 1: Check Server Logs
When you start the server, you should see:
```
✅ Pexels API key found
```

Instead of:
```
⚠️  No Pexels API key found. Using fallback method.
```

### Method 2: Test API Call
Run this test:
```python
import os
import requests

api_key = os.getenv('PEXELS_API_KEY')
headers = {'Authorization': api_key}
response = requests.get(
    'https://api.pexels.com/videos/search?query=sunset&per_page=1',
    headers=headers
)

if response.status_code == 200:
    print("✅ API key is working!")
else:
    print(f"❌ Error: {response.status_code}")
```

### Method 3: Generate a Video
1. Go to http://localhost:8000
2. Enter prompt: "Beautiful sunset"
3. Check server logs for:
```
🔍 Searching for: sunset
📥 Downloading: scene_1_sunset.mp4
✅ Downloaded: scene_1_sunset.mp4
```

---

## 📊 API Limits

### Free Tier (No Credit Card Required)
- **200 requests per hour**
- **Unlimited total requests**
- **No daily limit**
- **HD video access**
- **Commercial use allowed**

### What Counts as a Request?
- Each keyword search = 1 request
- Downloading video = 0 requests (free)
- Typical video generation = 3-5 requests

### Example Usage
- 1 video with 5 scenes = 5 requests
- You can generate ~40 videos per hour
- Resets every hour

---

## 🚨 Troubleshooting

### "Invalid API Key" Error
**Causes:**
- Typo in API key
- Extra spaces in key
- Key not activated yet

**Solutions:**
1. Copy key again from Pexels
2. Remove any spaces: `"abc123"` not `" abc123 "`
3. Wait 5 minutes after generating key
4. Regenerate key if needed

### "Rate Limit Exceeded"
**Cause:** Used 200 requests in last hour

**Solutions:**
1. Wait for hour to reset
2. Use cached clips (automatic)
3. Get multiple API keys (different accounts)
4. Reduce scenes per video

### "No Results Found"
**Cause:** Keyword too specific or unusual

**Solutions:**
1. System automatically uses fallback
2. Try more common keywords
3. Check spelling

---

## 🎯 Best Practices

### 1. Set Environment Variable Permanently

**Windows:**
```powershell
[System.Environment]::SetEnvironmentVariable(
    'PEXELS_API_KEY', 
    'your_key_here', 
    'User'
)
```

**Linux/Mac (add to ~/.bashrc or ~/.zshrc):**
```bash
echo 'export PEXELS_API_KEY="your_key_here"' >> ~/.bashrc
source ~/.bashrc
```

### 2. Keep Key Secret
- ❌ Don't commit to Git
- ❌ Don't share publicly
- ❌ Don't hardcode in code
- ✅ Use environment variables
- ✅ Use .env file (add to .gitignore)

### 3. Monitor Usage
Check your usage at: https://www.pexels.com/api/

---

## 🔄 Alternative APIs (Future)

If you want to use other stock footage sources:

### Pixabay (Alternative)
- Free API: https://pixabay.com/api/docs/
- Similar to Pexels
- 5,000 requests/hour

### Unsplash (Images Only)
- Free API: https://unsplash.com/developers
- 50 requests/hour

To add support, modify `backend/clip_fetcher.py`

---

## ✅ Quick Setup Checklist

- [ ] Sign up at Pexels.com
- [ ] Generate API key
- [ ] Copy API key
- [ ] Set environment variable OR create .env file
- [ ] Restart server
- [ ] Test with a video generation
- [ ] Verify in server logs

---

## 📞 Need Help?

### Pexels Support
- Email: api@pexels.com
- Docs: https://www.pexels.com/api/documentation/

### NEXUS VISION Issues
- Check SETUP_GUIDE.md
- Check server logs
- Verify API key is set correctly

---

## 🎉 Summary

**Recommended Setup:**
1. Get free Pexels API key (5 minutes)
2. Set as environment variable
3. Restart server
4. Enjoy high-quality video generation!

**Without API Key:**
- System still works
- Uses fallback clips
- Lower quality results

**The choice is yours, but the API key is FREE and makes a huge difference!** 🚀

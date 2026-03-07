# 🚀 NEXUS VISION - Complete Setup & Run Instructions

## 📋 Table of Contents
1. [Prerequisites](#prerequisites)
2. [Quick Start (5 Minutes)](#quick-start)
3. [API Key Setup](#api-key-setup)
4. [Running the Application](#running-the-application)
5. [Troubleshooting](#troubleshooting)
6. [Advanced Configuration](#advanced-configuration)

---

## Prerequisites

### Required Software
- **Python 3.8+** - [Download](https://www.python.org/downloads/)
- **pip** - Comes with Python
- **Git** - [Download](https://git-scm.com/downloads)
- **Internet Connection** - For downloading clips

### System Requirements
- **OS**: Windows 10/11, Linux, macOS
- **RAM**: 4GB minimum, 8GB recommended
- **Storage**: 2GB free space
- **GPU**: Optional (CPU works fine)

---

## Quick Start

### Step 1: Clone the Repository
```bash
git clone https://github.com/Prajwal0422/Text-to-Video-Finetuning-Enhanced.git
cd Text-to-Video-Finetuning-Enhanced
```

### Step 2: Install Python Dependencies
```bash
pip install -r requirements.txt
```

**What gets installed:**
- `fastapi` - Web framework
- `uvicorn` - ASGI server
- `moviepy` - Video editing
- `requests` - HTTP library
- `python-multipart` - File uploads
- `websockets` - Real-time communication

### Step 3: Run the Application
```bash
python start_project.py
```

**Or manually:**
```bash
cd backend
python main.py
```

### Step 4: Open Your Browser
Navigate to: **http://localhost:8000**

You should see the NEXUS VISION homepage!

---

## API Key Setup

### Do You Need an API Key?

**Optional but HIGHLY RECOMMENDED**

- ✅ **WITH API Key**: Access to 1000+ HD stock videos, better quality
- ⚠️ **WITHOUT API Key**: Uses fallback clips, limited variety

### Getting Your FREE Pexels API Key

#### 1. Sign Up at Pexels
Visit: **https://www.pexels.com/api/**
- Click "Get Started"
- Create free account (email + password)

#### 2. Generate API Key
Visit: **https://www.pexels.com/api/new/**
- **App Name**: NEXUS VISION
- **App Description**: Text-to-video generation
- **App URL**: http://localhost:8000
- Click "Generate API Key"
- **Copy your key** (looks like: `abc123xyz456...`)

#### 3. Set Environment Variable

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

#### 4. Make it Permanent (Optional)

**Windows (Permanent):**
```powershell
[System.Environment]::SetEnvironmentVariable('PEXELS_API_KEY', 'your_key_here', 'User')
```

**Linux/Mac (Add to ~/.bashrc or ~/.zshrc):**
```bash
echo 'export PEXELS_API_KEY="your_key_here"' >> ~/.bashrc
source ~/.bashrc
```

#### 5. Verify API Key
Restart the server and check logs:
```
✅ Pexels API key found
```

---

## Running the Application

### Method 1: Using Start Script (Recommended)
```bash
python start_project.py
```

### Method 2: Manual Start
```bash
cd backend
python main.py
```

### Method 3: With Custom Port
```bash
cd backend
python main.py --port 8080
```

### What You Should See
```
🚀 NEXUS VISION - Fast Video Generation API
Method: Stock Footage Pipeline
GPU Required: NO
Average Generation Time: < 30 seconds
✅ Pexels API key found
INFO: Uvicorn running on http://0.0.0.0:8000
INFO: Application startup complete
```

### Accessing the Application

1. **Homepage**: http://localhost:8000
2. **Dashboard**: http://localhost:8000#dashboard
3. **API Docs**: http://localhost:8000/docs
4. **Health Check**: http://localhost:8000/api/health

---

## Using the Application

### Generate Your First Video

1. Open http://localhost:8000
2. Click "Launch Dashboard"
3. Enter a prompt:
   ```
   A beautiful sunset over mountains with flowing clouds
   ```
4. Select settings:
   - **Mode**: Fast Mode (< 10s)
   - **Duration**: 8 seconds
   - **Resolution**: 1080p
   - **FPS**: 30 FPS
5. Click "Generate Video"
6. Wait 10-30 seconds
7. Watch and download your video!

### Example Prompts

Try these prompts for great results:

```
Ocean waves crashing on a beach at golden hour
City lights at night with time-lapse effect
Northern lights dancing in the arctic sky
Cherry blossoms falling in a Japanese garden
Aerial view of a winding mountain road
Raindrops falling on a window with city lights
Coffee being poured into a cup in slow motion
```

---

## Troubleshooting

### Issue: "ModuleNotFoundError"
**Solution:**
```bash
pip install -r requirements.txt
```

### Issue: "Port 8000 already in use"
**Solution 1 - Use different port:**
```bash
cd backend
python main.py --port 8080
```

**Solution 2 - Kill existing process:**

**Windows:**
```cmd
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

**Linux/Mac:**
```bash
lsof -ti:8000 | xargs kill -9
```

### Issue: "FFmpeg not found"
**Solution:**

**Windows:**
```bash
pip install imageio-ffmpeg
```

**Linux:**
```bash
sudo apt-get install ffmpeg
```

**Mac:**
```bash
brew install ffmpeg
```

### Issue: "No Pexels API key found"
**This is just a warning, not an error!**
- System works without API key
- Get free API key for better results
- See [API Key Setup](#api-key-setup)

### Issue: Slow video generation
**Causes & Solutions:**
- **Slow internet**: Check connection
- **First run**: FFmpeg auto-installs (wait)
- **No API key**: Get Pexels API key
- **Large videos**: Use shorter duration

### Issue: Video quality is low
**Solutions:**
1. Get Pexels API key for HD clips
2. Select "1080p" resolution
3. Use "Quality Mode" instead of "Fast Mode"

---

## Advanced Configuration

### Change Video Settings

Edit `backend/video_editor.py`:

```python
# Resolution
clip = clip.resize(height=1080)  # 720, 1080, or 1440

# Frame Rate
final_video.write_videofile(output_path, fps=30)  # 24, 30, or 60

# Encoding Speed
preset='medium'  # ultrafast, fast, medium, slow
```

### Change Number of Scenes

Edit `backend/script_generator.py`:

```python
keywords = self.extract_keywords(prompt)
return keywords[:5]  # Change to 3, 5, or 7
```

### Change Clip Duration

Edit `backend/script_generator.py`:

```python
'duration': 3.0  # Change to 2.0, 3.0, 4.0, or 5.0
```

### Enable Debug Logging

Edit `backend/main.py`:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

---

## Project Structure

```
Text-to-Video-Finetuning-Enhanced/
├── backend/
│   ├── main.py                      # FastAPI server
│   ├── video_generator.py           # Main orchestration
│   ├── script_generator.py          # Prompt → Keywords
│   ├── clip_fetcher.py              # Download clips
│   ├── video_editor.py              # Combine clips
│   ├── ultra_fast_generator.py      # Fast generation
│   ├── smart_video_generator.py     # Smart generation
│   ├── batch_video_generator.py     # Batch processing
│   └── requirements.txt             # Dependencies
├── frontend/
│   ├── index.html                   # Main UI
│   ├── index_v3.html                # Improved UI
│   ├── styles.css                   # Styles
│   ├── app.js                       # JavaScript
│   └── app_v3.js                    # Improved JS
├── outputs/
│   ├── clips/                       # Downloaded clips cache
│   └── videos/                      # Generated videos
├── start_project.py                 # Quick start script
├── requirements.txt                 # Python dependencies
└── COMPLETE_SETUP_INSTRUCTIONS.md   # This file
```

---

## Testing the System

### Test 1: Health Check
```bash
curl http://localhost:8000/api/health
```

**Expected:**
```json
{
  "status": "online",
  "method": "stock_footage_pipeline",
  "gpu_required": false
}
```

### Test 2: Generate Test Video
```bash
cd backend
python test_system.py
```

### Test 3: API Documentation
Visit: http://localhost:8000/docs

---

## Performance Tips

### 1. Enable Clip Caching
Clips are automatically cached in `outputs/clips/`
- Keep this folder to speed up repeated keywords
- Clear periodically to save space

### 2. Use SSD Storage
Store `outputs/` on SSD for faster video export

### 3. Optimize for Speed
```python
# In video_editor.py
preset='ultrafast'  # Fastest encoding
threads=4           # Use multiple cores
```

### 4. Batch Generation
Use the batch generator for multiple videos:
```bash
cd backend
python batch_video_generator.py
```

---

## Deployment

### Local Network Access
Change host in `backend/main.py`:
```python
uvicorn.run(app, host="0.0.0.0", port=8000)
```

Access from other devices: `http://YOUR_IP:8000`

### Production Deployment
```bash
uvicorn backend.main:app --host 0.0.0.0 --port 8000 --workers 4
```

---

## API Usage

### Generate Video via API

```python
import requests

response = requests.post(
    'http://localhost:8000/api/generate',
    json={
        'prompt': 'A beautiful sunset',
        'mode': 'fast',
        'duration': 8
    }
)

result = response.json()
print(f"Video: {result['video_path']}")
```

### WebSocket Connection

```javascript
const ws = new WebSocket('ws://localhost:8000/ws/generate');

ws.onopen = () => {
    ws.send(JSON.stringify({
        prompt: 'Ocean waves',
        mode: 'fast',
        duration: 8
    }));
};

ws.onmessage = (event) => {
    const data = JSON.parse(event.data);
    console.log(data);
};
```

---

## Environment Variables

### PEXELS_API_KEY
- **Purpose**: Access Pexels stock footage API
- **Required**: No (optional but recommended)
- **Get it**: https://www.pexels.com/api/
- **Limit**: 200 requests/hour (free tier)

### PORT
- **Purpose**: Change server port
- **Default**: 8000
- **Usage**: `export PORT=8080`

---

## Verification Checklist

After setup, verify:
- [ ] Python 3.8+ installed
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] Pexels API key set (optional)
- [ ] Server starts without errors
- [ ] Homepage loads at http://localhost:8000
- [ ] Dashboard accessible
- [ ] Test video generates successfully
- [ ] Video plays in browser
- [ ] Download button works

---

## Getting Help

### Check Server Logs
The server prints detailed logs:
```
📝 Step 1: Generating script...
✅ Generated 5 scenes
📥 Step 2: Fetching clips...
✅ Downloaded 5 clips
🎬 Step 3: Creating video...
✅ Video generation complete in 18.3s
```

### Common Error Messages

**"No Pexels API key found"**
- Warning only, system works without it
- Get API key for better results

**"Download failed: 404"**
- Clip URL expired
- System retries automatically

**"Error creating video"**
- Check FFmpeg installation
- Verify clip files exist

### Documentation
- **Setup Guide**: SETUP_GUIDE.md
- **API Keys**: API_KEY_SETUP.md
- **Quick Start**: QUICK_START.md
- **Fast Video**: FAST_VIDEO_GENERATION.md

### Report Issues
GitHub: https://github.com/Prajwal0422/Text-to-Video-Finetuning-Enhanced/issues

---

## Next Steps

1. ✅ **Setup Complete** - You're ready to generate videos!
2. 🎨 **Customize** - Modify prompts and settings
3. 🔧 **Integrate** - Use API in your applications
4. 🚀 **Deploy** - Share with others
5. ⭐ **Star on GitHub** - Support the project!

---

## Quick Command Reference

```bash
# Install dependencies
pip install -r requirements.txt

# Set API key (Windows)
set PEXELS_API_KEY=your_key_here

# Set API key (Linux/Mac)
export PEXELS_API_KEY=your_key_here

# Run server
python start_project.py

# Run with custom port
cd backend && python main.py --port 8080

# Test system
cd backend && python test_system.py

# Check health
curl http://localhost:8000/api/health
```

---

## Summary

**Minimum Setup (2 minutes):**
1. Install Python 3.8+
2. Run: `pip install -r requirements.txt`
3. Run: `python start_project.py`
4. Open: http://localhost:8000

**Recommended Setup (5 minutes):**
1. Do minimum setup
2. Get free Pexels API key
3. Set environment variable
4. Restart server
5. Generate amazing videos!

---

**🎉 You're all set! Start creating amazing videos with NEXUS VISION!**

For questions or issues, check the documentation or open a GitHub issue.

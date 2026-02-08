# NEXUS VISION - Setup Guide

## 🚀 Quick Start (5 minutes)

### Prerequisites
- Python 3.8 or higher
- pip package manager
- Internet connection
- FFmpeg (auto-installed with moviepy)

### Step 1: Clone Repository
```bash
git clone https://github.com/Prajwal0422/Text-to-Video-Finetuning-Enhanced.git
cd Text-to-Video-Finetuning-Enhanced
```

### Step 2: Install Dependencies
```bash
cd backend
pip install -r requirements.txt
```

This installs:
- FastAPI (web framework)
- MoviePy (video editing)
- Requests (API calls)
- Uvicorn (ASGI server)

### Step 3: Get Pexels API Key (Optional)
1. Visit: https://www.pexels.com/api/
2. Sign up for free account
3. Copy your API key
4. Set environment variable:

**Windows:**
```cmd
set PEXELS_API_KEY=your_key_here
```

**Linux/Mac:**
```bash
export PEXELS_API_KEY=your_key_here
```

**Note**: System works without API key using fallback clips

### Step 4: Run Server
```bash
python main.py
```

You should see:
```
🚀 NEXUS VISION - Fast Video Generation API
Method: Stock Footage Pipeline
GPU Required: NO
Average Generation Time: < 30 seconds
INFO: Uvicorn running on http://0.0.0.0:8000
```

### Step 5: Open Browser
Navigate to: **http://localhost:8000**

You'll see the NEXUS VISION home page!

## 🎬 Generate Your First Video

1. Click "Launch Dashboard"
2. Enter a prompt: "A beautiful sunset over mountains"
3. Click "Generate Video"
4. Wait 15-30 seconds
5. Watch your video!

## 🔧 Troubleshooting

### Issue: ModuleNotFoundError
**Solution**: Install dependencies
```bash
pip install -r requirements.txt
```

### Issue: FFmpeg not found
**Solution**: MoviePy will auto-download FFmpeg on first run. If it fails:

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

### Issue: Port 8000 already in use
**Solution**: Change port in main.py:
```python
uvicorn.run(app, host="0.0.0.0", port=8001)  # Use 8001 instead
```

### Issue: Slow video generation
**Causes**:
- Slow internet connection (downloading clips)
- First run (FFmpeg installation)
- No API key (using fallback)

**Solutions**:
- Get Pexels API key for faster clip access
- Wait for first run to complete setup
- Check internet connection

### Issue: Video quality is low
**Solution**: The system uses HD clips by default. To improve:
1. Get Pexels API key for better clip selection
2. Modify `video_editor.py` to use 1080p:
```python
clip = clip.resize(height=1080)  # Instead of 720
```

## 📁 Project Structure

```
Text-to-Video-Finetuning-Enhanced/
├── backend/
│   ├── main.py                 # FastAPI server
│   ├── video_generator.py      # Main orchestration
│   ├── script_generator.py     # Prompt → Keywords
│   ├── clip_fetcher.py         # Download stock footage
│   ├── video_editor.py         # Combine clips
│   └── requirements.txt        # Dependencies
├── frontend/
│   ├── home.html              # Landing page
│   ├── home.css               # Landing styles
│   ├── index.html             # Dashboard
│   ├── styles.css             # Dashboard styles
│   └── app.js                 # WebSocket client
├── outputs/
│   ├── clips/                 # Downloaded clips cache
│   └── videos/                # Generated videos
└── README.md
```

## 🎯 Testing the System

### Test 1: Basic Generation
```bash
cd backend
python video_generator.py
```

This runs the test suite with sample prompts.

### Test 2: API Health Check
```bash
curl http://localhost:8000/api/health
```

Expected response:
```json
{
  "status": "online",
  "method": "stock_footage_pipeline",
  "gpu_required": false
}
```

### Test 3: Manual Generation
```python
from video_generator import VideoGenerator

gen = VideoGenerator()
result = gen.generate("Ocean waves on a beach")

if result['success']:
    print(f"Video: {result['video_path']}")
    print(f"Time: {result['duration']:.1f}s")
```

## 🔐 Environment Variables

### PEXELS_API_KEY (Optional)
- **Purpose**: Access Pexels stock footage API
- **Get it**: https://www.pexels.com/api/
- **Limit**: 200 requests/hour (free tier)
- **Fallback**: System works without it

### Setting Permanently

**Windows (PowerShell):**
```powershell
[System.Environment]::SetEnvironmentVariable('PEXELS_API_KEY', 'your_key', 'User')
```

**Linux/Mac (.bashrc or .zshrc):**
```bash
echo 'export PEXELS_API_KEY="your_key"' >> ~/.bashrc
source ~/.bashrc
```

## 📊 Performance Optimization

### 1. Enable Clip Caching
Clips are automatically cached in `outputs/clips/`. Keep this folder to speed up repeated keywords.

### 2. Use SSD Storage
Store `outputs/` on SSD for faster video export.

### 3. Increase Thread Pool
In `main.py`, increase workers:
```python
executor = ThreadPoolExecutor(max_workers=4)  # Default is 2
```

### 4. Reduce Video Quality (Faster Export)
In `video_editor.py`:
```python
final_video.write_videofile(
    output_path,
    fps=24,
    codec='libx264',
    preset='ultrafast',  # Fastest encoding
    threads=4
)
```

## 🌐 Deployment

### Local Network Access
Change host in `main.py`:
```python
uvicorn.run(app, host="0.0.0.0", port=8000)
```

Access from other devices: `http://YOUR_IP:8000`

### Production Deployment
For production, use:
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

### Docker (Optional)
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY backend/requirements.txt .
RUN pip install -r requirements.txt

COPY backend/ .
COPY frontend/ ../frontend/

CMD ["python", "main.py"]
```

## 📝 Configuration

### Clip Duration
In `script_generator.py`:
```python
'duration': 3.0  # Change to 4.0 or 5.0 for longer clips
```

### Number of Scenes
In `script_generator.py`:
```python
keywords = self.extract_keywords(prompt)
return keywords[:5]  # Change to [:3] for fewer scenes
```

### Video Resolution
In `video_editor.py`:
```python
clip = clip.resize(height=720)  # Change to 1080 for HD
```

### Transition Duration
In `video_editor.py`:
```python
self.transition_duration = 0.5  # Change to 1.0 for longer fades
```

## 🆘 Getting Help

### Check Logs
The server prints detailed logs:
```
📝 Step 1: Generating script...
✅ Generated 5 scenes
📥 Step 2: Fetching clips...
🔍 Searching for: sunset
✅ Downloaded 5 clips
🎬 Step 3: Creating video...
✅ Video generation complete in 18.3s
```

### Common Error Messages

**"No Pexels API key found"**
- Not an error, system uses fallback
- Get API key for better results

**"Download failed: 404"**
- Clip URL expired
- System will retry with different clip

**"Error creating video"**
- Check FFmpeg installation
- Verify clip files exist in `outputs/clips/`

### Report Issues
GitHub: https://github.com/Prajwal0422/Text-to-Video-Finetuning-Enhanced/issues

## ✅ Verification Checklist

After setup, verify:
- [ ] Server starts without errors
- [ ] Home page loads at http://localhost:8000
- [ ] Dashboard accessible
- [ ] Test video generates successfully
- [ ] Video plays in browser
- [ ] Download button works
- [ ] Generation completes in < 30s

## 🎓 Next Steps

1. **Customize**: Modify prompts and settings
2. **Integrate**: Use API in your applications
3. **Extend**: Add features like audio or effects
4. **Deploy**: Share with others on your network

---

**Need help? Check FAST_VIDEO_GENERATION.md for detailed documentation**

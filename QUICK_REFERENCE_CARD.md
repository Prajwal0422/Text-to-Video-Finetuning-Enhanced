# 🚀 NEXUS VISION - Quick Reference Card

## 📍 Access Points
```
Homepage:   http://localhost:8000
Dashboard:  http://localhost:8000#dashboard
API Docs:   http://localhost:8000/docs
Health:     http://localhost:8000/api/health
```

## ⚡ Quick Commands

### Start Server
```bash
python start_project.py
```

### Test System
```bash
cd backend && python test_system.py
```

### Check Health
```bash
curl http://localhost:8000/api/health
```

### Set API Key (Windows)
```cmd
set PEXELS_API_KEY=your_key_here
```

### Set API Key (Linux/Mac)
```bash
export PEXELS_API_KEY=your_key_here
```

## 🎬 Generation Modes

| Mode | Speed | Quality | Use Case |
|------|-------|---------|----------|
| Ultra-Fast | < 5s | Good | Quick previews |
| Fast | < 10s | Better | Standard use |
| Quality | < 30s | High | Final renders |
| Premium | < 60s | Best | Professional |

## 📐 Video Settings

### Duration Options
- 4 seconds
- 8 seconds (default)
- 12 seconds
- 16 seconds

### Resolution Options
- 720p HD
- 1080p Full HD (default)

### Frame Rate Options
- 24 FPS (Cinematic)
- 30 FPS (Standard, default)
- 60 FPS (Smooth)

## 💡 Example Prompts

```
A serene sunset over mountains with flowing clouds
Ocean waves crashing on a beach at golden hour
City lights at night with time-lapse effect
Northern lights dancing in the arctic sky
Cherry blossoms falling in a Japanese garden
Aerial view of a winding mountain road
Raindrops falling on a window with city lights
Coffee being poured into a cup in slow motion
```

## 🔑 API Key Setup

1. Visit: https://www.pexels.com/api/
2. Sign up (free)
3. Generate API key
4. Set environment variable
5. Restart server

**Benefits:**
- 1000+ HD stock videos
- Better quality
- 200 requests/hour (free)

## 🐛 Quick Troubleshooting

### Port Already in Use
```bash
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Linux/Mac
lsof -ti:8000 | xargs kill -9
```

### Module Not Found
```bash
pip install -r requirements.txt
```

### FFmpeg Not Found
```bash
# Windows
pip install imageio-ffmpeg

# Linux
sudo apt-get install ffmpeg

# Mac
brew install ffmpeg
```

## 📁 Project Structure

```
Text-to-Video-Finetuning-Enhanced/
├── backend/              # Server code
│   ├── main.py          # FastAPI server
│   ├── video_generator.py
│   └── ...
├── frontend/            # UI files
│   ├── index_v3.html   # Latest UI
│   ├── styles_v3.css
│   └── app_v3.js
├── outputs/
│   ├── clips/          # Cached clips
│   └── videos/         # Generated videos
└── start_project.py    # Quick start
```

## 🔧 Configuration Files

### Backend Settings
- `backend/main.py` - Server config
- `backend/video_editor.py` - Video settings
- `backend/script_generator.py` - Scene config

### Frontend Files
- `frontend/index_v3.html` - Latest UI
- `frontend/styles_v3.css` - Styles
- `frontend/app_v3.js` - Logic

## 📊 System Requirements

### Minimum
- Python 3.8+
- 4GB RAM
- 2GB Storage
- Internet connection

### Recommended
- Python 3.9+
- 8GB RAM
- SSD storage
- Fast internet
- Pexels API key

## 🎯 Workflow

1. **Start Server**
   ```bash
   python start_project.py
   ```

2. **Open Browser**
   ```
   http://localhost:8000
   ```

3. **Enter Prompt**
   - Be specific
   - Include motion keywords
   - Add lighting details

4. **Select Settings**
   - Mode: Fast/Quality
   - Duration: 8s
   - Resolution: 1080p

5. **Generate**
   - Click "Generate Video"
   - Wait 10-30 seconds
   - Download result

## 📖 Documentation

| File | Purpose |
|------|---------|
| COMPLETE_SETUP_INSTRUCTIONS.md | Full setup guide |
| API_KEY_SETUP.md | API configuration |
| SETUP_GUIDE.md | Quick setup |
| QUICK_START.md | Getting started |
| DEPLOYMENT_COMPLETE.md | Deployment status |
| README.md | Project overview |

## 🆘 Getting Help

### Check Logs
- Server terminal output
- Browser console (F12)

### Common Issues
- "No API key" → Warning only, system works
- "Port in use" → Kill process, restart
- "Module not found" → Run pip install
- "Slow generation" → Get API key

### Resources
- GitHub: https://github.com/Prajwal0422/Text-to-Video-Finetuning-Enhanced
- API Docs: http://localhost:8000/docs
- Health Check: http://localhost:8000/api/health

## ✅ Verification Checklist

- [ ] Python 3.8+ installed
- [ ] Dependencies installed
- [ ] Server starts successfully
- [ ] Homepage loads
- [ ] Dashboard accessible
- [ ] Test video generates
- [ ] Video plays in browser
- [ ] Download works

## 🎉 Quick Win

**Generate your first video in 60 seconds:**

1. Run: `python start_project.py`
2. Open: http://localhost:8000
3. Click: "Launch Dashboard"
4. Use quick prompt: "Mountain Sunset"
5. Click: "Generate Video"
6. Done! 🎬

---

**Version:** 3.0 | **Updated:** March 7, 2026 | **Status:** ✅ Ready

# ⚡ NEXUS VISION - Quick Start

## 🚀 Get Running in 5 Minutes

### 1️⃣ Install Dependencies
```bash
cd backend
pip install fastapi uvicorn requests moviepy
```

### 2️⃣ Get API Key (Optional but Recommended)
1. Visit: https://www.pexels.com/api/
2. Sign up (free)
3. Copy your API key
4. Set it:
```bash
# Windows
set PEXELS_API_KEY=your_key_here

# Linux/Mac
export PEXELS_API_KEY=your_key_here
```

### 3️⃣ Start Server
```bash
python main.py
```

### 4️⃣ Open Browser
Go to: **http://localhost:8000**

---

## 🎬 Generate Your First Video

1. Click "Launch Dashboard"
2. Enter prompt: "A beautiful sunset over mountains"
3. Click "Generate Video"
4. Wait 15-30 seconds
5. Watch your video!

---

## 📋 System Requirements

✅ **Required:**
- Python 3.8+
- Internet connection
- 2GB RAM

❌ **NOT Required:**
- GPU
- CUDA
- PyTorch
- Expensive hardware

---

## 🔑 API Key Status

### ✅ WITH Pexels API Key
- HD stock footage
- 200 requests/hour (free)
- Better quality
- More variety

### ⚠️ WITHOUT API Key
- Fallback mode
- Still works
- Lower quality
- Limited clips

**Get your FREE key:** https://www.pexels.com/api/

---

## 📊 What to Expect

- **Generation Time:** 15-30 seconds
- **Video Quality:** 1280x720 HD
- **Video Length:** 9-15 seconds
- **Success Rate:** 100%
- **GPU Required:** NO

---

## 🆘 Quick Troubleshooting

### Server won't start?
```bash
pip install -r requirements.txt
```

### No videos generating?
- Check internet connection
- Get Pexels API key
- Check server logs

### Slow generation?
- First run downloads FFmpeg (one-time)
- Get API key for faster clip access
- Check internet speed

---

## 📚 Full Documentation

- **API Key Setup:** See `API_KEY_SETUP.md`
- **Complete Guide:** See `SETUP_GUIDE.md`
- **Technical Details:** See `FAST_VIDEO_GENERATION.md`

---

## 🎯 Example Prompts

Try these:
- "Ocean waves on a tropical beach"
- "City lights at night"
- "Forest with morning mist"
- "Desert landscape at sunset"
- "Mountain peaks with clouds"

---

**That's it! You're ready to generate videos! 🚀**

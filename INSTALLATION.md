# Installation Guide

## Prerequisites

### Required Software
- Python 3.11 or higher
- pip (Python package manager)
- Git
- FFmpeg

### System Requirements
- 4GB RAM minimum (8GB recommended)
- 2GB free disk space
- Internet connection
- Modern web browser

## Step-by-Step Installation

### 1. Clone Repository
```bash
git clone https://github.com/Prajwal0422/Text-to-Video-Finetuning-Enhanced.git
cd Text-to-Video-Finetuning-Enhanced
```

### 2. Create Virtual Environment (Recommended)
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Install FFmpeg

#### Windows
Download from: https://ffmpeg.org/download.html
Add to PATH

#### Linux
```bash
sudo apt update
sudo apt install ffmpeg
```

#### Mac
```bash
brew install ffmpeg
```

### 5. Configure API Key
Create `.env` file:
```
PEXELS_API_KEY=your_api_key_here
```

Get free API key from: https://www.pexels.com/api/

### 6. Create Output Directories
```bash
mkdir -p outputs/videos
mkdir -p outputs/cache
mkdir -p outputs/normalized
```

### 7. Verify Installation
```bash
python backend/health_check.py
```

### 8. Start Server
```bash
python backend/main.py
```

### 9. Access Dashboard
Open browser: http://localhost:8000/frontend/index_v3.html

## Troubleshooting

### FFmpeg Not Found
- Verify FFmpeg is installed
- Check PATH environment variable
- Restart terminal after installation

### Module Not Found
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Port Already in Use
Change port in `backend/main.py`:
```python
uvicorn.run(app, host="0.0.0.0", port=8001)
```

### API Key Invalid
- Check `.env` file exists
- Verify API key is correct
- Test key at pexels.com

## Next Steps

1. Read QUICK_START.md
2. Try example prompts
3. Review documentation
4. Join community

## Support

- GitHub Issues
- Documentation
- FAQ.md

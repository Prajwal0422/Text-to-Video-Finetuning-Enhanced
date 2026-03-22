# Usage Guide

## Getting Started

### 1. Start the Server
```bash
python backend/main.py
```

### 2. Open Dashboard
Navigate to: `http://localhost:8000/frontend/index_v3.html`

### 3. Enter Your Prompt
Type a description of the video you want to create.

**Good Examples:**
- "Sunset over ocean waves"
- "City skyline at night"
- "Mountain landscape with clouds"

### 4. Configure Settings

#### Generation Mode
- **Ultra Fast**: 5-10 seconds (basic quality)
- **Fast**: 10-20 seconds (good quality) ⭐ Recommended
- **Quality**: 20-30 seconds (high quality)
- **Premium**: 30-60 seconds (best quality)

#### Duration
- 4 seconds: Quick clips
- 8 seconds: Standard ⭐ Recommended
- 12 seconds: Extended
- 16 seconds: Long

#### Resolution
- 720p: HD (faster)
- 1080p: Full HD ⭐ Recommended

#### Frame Rate
- 24 FPS: Cinematic
- 30 FPS: Standard ⭐ Recommended
- 60 FPS: Smooth (larger files)

### 5. Generate Video
Click "Generate Video" button and wait for completion.

## Understanding the Process

### Stage 1: Visual Intent Mapping (< 1s)
- Analyzes your prompt
- Identifies key concepts
- Plans visual scenes

### Stage 2: Script Generation (1-2s)
- Creates scene structure
- Extracts keywords
- Plans video flow

### Stage 3: Clip Fetching (10-15s)
- Searches for matching clips
- Downloads from Pexels
- Ranks by relevance

### Stage 4: Video Composition (5-10s)
- Merges clips
- Normalizes quality
- Exports final video

## Tech Stack Display

Watch the real-time pipeline:
- 🔄 **Retry Manager**: Monitors retry attempts
- 🔀 **Model Router**: Shows active model
- 🎬 **Visual Mapper**: Prompt analysis
- 📥 **Clip Fetcher**: Download progress
- ✂️ **Video Editor**: Composition status

## Tips for Best Results

### Prompt Writing
1. **Be Specific**: "sunset over ocean" > "nature"
2. **Use Adjectives**: "dramatic sunset" > "sunset"
3. **Focus on Visuals**: Describe what you see
4. **Keep it Simple**: 5-10 words ideal
5. **Use Categories**: Nature, city, travel work best

### Avoid
- Abstract concepts: "happiness", "love"
- Complex scenes: "person cooking while talking"
- Rare subjects: "purple elephant"
- Too many elements: "sunset, mountains, ocean, birds, clouds"

## Downloading Videos

### Method 1: Download Button
Click the download button in the result section.

### Method 2: Direct Link
Right-click video → Save video as...

### Method 3: API
Access via: `/outputs/videos/filename.mp4`

## Sharing Videos

### Method 1: Share Button
Click share button for options.

### Method 2: Copy Link
Copy the video URL from browser.

### Method 3: Download & Upload
Download and upload to your platform.

## Troubleshooting

### Generation Failed
1. Try simpler prompt
2. Check internet connection
3. Verify API key
4. Wait and retry

### Slow Generation
1. Use Fast mode
2. Reduce duration
3. Clear cache
4. Check network speed

### Poor Quality
1. Use Quality/Premium mode
2. Choose 1080p resolution
3. Try different prompt
4. Generate multiple versions

## Advanced Usage

### Batch Generation
Generate multiple videos by repeating the process.

### Custom Styles
Experiment with different adjectives:
- "cinematic sunset"
- "dramatic sunset"
- "peaceful sunset"

### Combining Concepts
Use "and" to combine:
- "ocean waves and sunset"
- "city lights and traffic"

## API Usage

### Health Check
```bash
curl http://localhost:8000/api/health
```

### Statistics
```bash
curl http://localhost:8000/api/stats
```

### WebSocket Generation
```javascript
const ws = new WebSocket('ws://localhost:8000/ws/generate');
ws.send(JSON.stringify({prompt: "sunset over ocean"}));
```

## Best Practices

1. **Start Simple**: Test with basic prompts first
2. **Iterate**: Try variations of successful prompts
3. **Save Favorites**: Note prompts that work well
4. **Monitor Stats**: Check API usage regularly
5. **Clear Cache**: Periodically clear old clips

## Getting Help

- Check FAQ.md
- Review TROUBLESHOOTING.md
- Check server logs
- Open GitHub issue

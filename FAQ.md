# Frequently Asked Questions (FAQ)

## General Questions

### What is NEXUS VISION?
NEXUS VISION is an AI-powered text-to-video generation platform that creates videos from text prompts using stock footage and intelligent scene planning.

### How does it work?
1. You enter a text prompt
2. AI analyzes and plans scenes
3. System fetches relevant video clips
4. Clips are edited and merged
5. Final video is generated

### Is it free?
The software is open-source and free. However, you need a Pexels API key (free tier available).

### What can I create?
Nature scenes, cityscapes, travel videos, lifestyle content, and more. Best for stock footage-style videos.

## Technical Questions

### What are the system requirements?
- Python 3.11+
- 4GB RAM minimum
- Internet connection
- FFmpeg installed
- Modern web browser

### How long does generation take?
- Ultra Fast: 5-10 seconds
- Fast: 10-20 seconds
- Quality: 20-30 seconds
- Premium: 30-60 seconds

### What video formats are supported?
Output: MP4 (H.264 codec)
Resolution: 720p or 1080p
Frame rates: 24, 30, or 60 FPS

### Can I use my own video clips?
Not currently. The system uses Pexels API for stock footage.

## Usage Questions

### What makes a good prompt?
- Be specific: "sunset over ocean" vs "nature"
- Use descriptive words: "dramatic", "peaceful", "vibrant"
- Keep it under 100 characters
- Focus on visual elements
- Use recommended categories

### Why did my generation fail?
Common reasons:
- No matching clips found
- API rate limit reached
- Network connection issues
- Invalid prompt
- Server error

### Can I edit the generated video?
The system generates final videos. For editing, download and use video editing software.

### How do I improve video quality?
1. Use Quality or Premium mode
2. Choose 1080p resolution
3. Use specific, descriptive prompts
4. Try different keywords
5. Generate multiple versions

## API Questions

### Do I need an API key?
Yes, you need a free Pexels API key. Sign up at pexels.com/api

### Are there usage limits?
Pexels free tier: 200 requests/hour, 20,000/month

### Can I use other video sources?
Currently only Pexels is supported. More sources planned for future versions.

### Is there a rate limit?
System has built-in retry logic and respects API limits automatically.

## Troubleshooting

### Server won't start
- Check Python version
- Install dependencies
- Verify FFmpeg installation
- Check port 8000 availability

### WebSocket connection failed
- Refresh browser
- Check server status
- Clear browser cache
- Try different browser

### Generation is slow
- Use Fast mode
- Reduce video duration
- Check internet speed
- Clear cache

### No clips found
- Try simpler prompts
- Use different keywords
- Check API quota
- Wait and retry

## Feature Questions

### Can I add music?
Not currently. Audio support planned for v1.2

### Can I add text overlays?
Not yet. Text overlay support coming in v1.2

### Can I save my videos?
Yes, use the download button. Videos auto-delete after 24 hours.

### Can I share videos?
Yes, use the share button or download and share manually.

## Development Questions

### Can I contribute?
Yes! Check CONTRIBUTING.md for guidelines.

### Is it open source?
Yes, available on GitHub under MIT license.

### Can I modify the code?
Yes, feel free to fork and customize.

### How do I report bugs?
Open an issue on GitHub with details and logs.

## Future Plans

### What's coming next?
See ROADMAP.md for detailed plans:
- User authentication
- Video history
- Audio support
- Text overlays
- More video sources

### Will there be a mobile app?
Planned for v2.0 (long-term)

### Will it support longer videos?
Currently max 16 seconds. Longer videos planned for future versions.

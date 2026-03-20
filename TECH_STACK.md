# Technology Stack

## Backend
- **Framework:** FastAPI
- **Language:** Python 3.11
- **Video Processing:** MoviePy
- **API Integration:** Pexels API
- **WebSocket:** Native FastAPI WebSocket

## Frontend
- **HTML5** with semantic markup
- **CSS3** with animations and transitions
- **JavaScript** (Vanilla ES6+)
- **WebSocket** for real-time updates

## AI/ML Components
- **Visual Intent Mapper** - Semantic prompt analysis
- **Script Generator** - Scene planning
- **Clip Ranker** - Relevance scoring
- **Retry Manager** - Exponential backoff
- **Model Router** - Multi-model fallback

## Video Pipeline
1. Visual Intent Mapping
2. Script Generation
3. Clip Fetching (Pexels API)
4. Video Editing (MoviePy)
5. Export & Verification

## Infrastructure
- **Server:** Uvicorn ASGI
- **Concurrency:** ThreadPoolExecutor
- **Caching:** File-based clip cache
- **Logging:** Python logging module

## Development Tools
- **Version Control:** Git
- **Package Manager:** pip
- **Environment:** .env configuration
- **FFmpeg:** Video encoding/decoding

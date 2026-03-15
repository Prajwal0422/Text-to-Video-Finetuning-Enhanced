# Server Status

## Current Configuration

**Server Type**: FastAPI with WebSocket support
**Port**: 8000
**Host**: 0.0.0.0 (accessible from all interfaces)

## Endpoints

### Web Interface
- Landing Page: `http://localhost:8000/frontend/landing.html`
- Get Started: `http://localhost:8000/frontend/get-started.html`
- Dashboard: `http://localhost:8000/frontend/index_v3.html`

### API Endpoints
- Health Check: `http://localhost:8000/api/health`
- WebSocket Generation: `ws://localhost:8000/ws/generate`

## Video Generation

**Method**: Stock Footage Pipeline (Pexels API)
**GPU Required**: No
**Average Time**: < 30 seconds
**Output Format**: MP4
**Output Directory**: `outputs/videos/`

## Starting the Server

```bash
python backend/main.py
```

## Testing

```bash
# Test API generation
python backend/test_api_generation.py
```

## Troubleshooting

1. **WebSocket Connection Failed**
   - Ensure server is running on port 8000
   - Check firewall settings
   - Verify PEXELS_API_KEY is set

2. **Video Generation Fails**
   - Check API key in `.env` file
   - Verify internet connection
   - Check outputs directory exists

3. **CORS Issues**
   - Server allows all origins by default
   - Check browser console for errors

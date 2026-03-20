# API Documentation

## Base URL
```
http://localhost:8000
```

## Endpoints

### Health Check
```http
GET /api/health
```

**Response:**
```json
{
  "status": "online",
  "method": "resilient_pipeline",
  "features": ["retry", "fallback", "timeout", "local_mode"],
  "gpu_required": false
}
```

### Statistics
```http
GET /api/stats
```

**Response:**
```json
{
  "total_requests": 0,
  "successful": 0,
  "failed": 0,
  "retries_used": 0,
  "fallbacks_used": 0,
  "local_mode_used": 0,
  "success_rate": 0.0
}
```

### Video Generation (WebSocket)
```
ws://localhost:8000/ws/generate
```

**Send:**
```json
{
  "prompt": "A beautiful sunset over mountains"
}
```

**Receive (Progress):**
```json
{
  "type": "progress",
  "progress": 50,
  "message": "Fetching clips...",
  "step": "Stage 2/4"
}
```

**Receive (Complete):**
```json
{
  "type": "complete",
  "video_path": "/outputs/videos/video_123.mp4",
  "duration": 25.5,
  "message": "Video created successfully"
}
```

**Receive (Error):**
```json
{
  "type": "error",
  "message": "Generation failed"
}
```

## Static Files

### Frontend
```
/frontend/index_v3.html - Main dashboard
/frontend/landing.html - Landing page
/frontend/get-started.html - Getting started
```

### Outputs
```
/outputs/videos/ - Generated videos
```

## Error Codes
- **200** - Success
- **304** - Not Modified
- **400** - Bad Request
- **500** - Server Error

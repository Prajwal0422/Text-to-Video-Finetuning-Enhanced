# API Integration Guide

## Overview
Complete guide for integrating NEXUS VISION video generation API into your applications.

## Quick Start

### 1. Basic Video Generation

#### Python
```python
import requests
import json

# API endpoint
url = "http://localhost:8000/ws/generate"

# WebSocket connection for real-time progress
import websocket

def on_message(ws, message):
    data = json.loads(message)
    if data['type'] == 'progress':
        print(f"Progress: {data['progress']}% - {data['message']}")
    elif data['type'] == 'complete':
        print(f"Video ready: {data['video_path']}")
        ws.close()

ws = websocket.WebSocketApp(url, on_message=on_message)
ws.send(json.dumps({'prompt': 'ocean waves on beach'}))
ws.run_forever()
```

#### JavaScript
```javascript
const ws = new WebSocket('ws://localhost:8000/ws/generate');

ws.onopen = () => {
  ws.send(JSON.stringify({
    prompt: 'ocean waves on beach'
  }));
};

ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  
  if (data.type === 'progress') {
    console.log(`${data.progress}%: ${data.message}`);
  } else if (data.type === 'complete') {
    console.log(`Video ready: ${data.video_path}`);
    ws.close();
  }
};
```

#### cURL
```bash
# Health check
curl http://localhost:8000/api/health

# Get stats
curl http://localhost:8000/api/stats
```

### 2. REST API Endpoints

#### Health Check
```
GET /api/health
```

Response:
```json
{
  "status": "online",
  "method": "resilient_pipeline",
  "features": ["retry", "fallback", "timeout", "local_mode"],
  "gpu_required": false
}
```

#### Statistics
```
GET /api/stats
```

Response:
```json
{
  "total_requests": 150,
  "successful": 145,
  "failed": 5,
  "success_rate": 96.67,
  "retries_used": 12,
  "fallbacks_used": 3,
  "local_mode_used": 2
}
```

### 3. WebSocket API

#### Connection
```
ws://localhost:8000/ws/generate
```

#### Request Format
```json
{
  "prompt": "your video description here"
}
```

#### Response Types

**Progress Update**
```json
{
  "type": "progress",
  "progress": 50,
  "message": "Downloading clips...",
  "step": "clip_fetching"
}
```

**Success**
```json
{
  "type": "complete",
  "video_path": "/outputs/videos/video_abc123.mp4",
  "duration": 29.3,
  "message": "Video created successfully"
}
```

**Error**
```json
{
  "type": "error",
  "message": "Generation failed: timeout"
}
```

## Advanced Integration

### 1. Batch Processing

```python
import requests

# Add multiple jobs
prompts = [
    "ocean waves",
    "mountain sunset",
    "city lights"
]

job_ids = []
for prompt in prompts:
    response = requests.post(
        'http://localhost:8000/api/batch/add',
        json={'prompt': prompt}
    )
    job_ids.append(response.json()['job_id'])

# Check status
for job_id in job_ids:
    response = requests.get(f'http://localhost:8000/api/batch/status/{job_id}')
    print(response.json())
```

### 2. Webhook Notifications

```python
# Configure webhook
requests.post(
    'http://localhost:8000/api/webhooks/add',
    json={'url': 'https://your-server.com/webhook'}
)

# Your webhook endpoint receives:
{
  "event": "generation_completed",
  "timestamp": "2024-03-23T10:30:00",
  "data": {
    "job_id": "job_123",
    "prompt": "ocean waves",
    "video_path": "/outputs/videos/video_123.mp4",
    "duration": 29.3
  }
}
```

### 3. Custom Quality Settings

```python
# Request with quality settings
ws.send(json.dumps({
    'prompt': 'ocean waves',
    'settings': {
        'quality': 'high',
        'resolution': '1280x720',
        'fps': 30
    }
}))
```

## SDK Examples

### Python SDK

```python
from nexus_vision import VideoGenerator

# Initialize
generator = VideoGenerator(api_url='http://localhost:8000')

# Generate video
result = generator.generate(
    prompt='ocean waves on beach',
    quality='high',
    on_progress=lambda p, m: print(f"{p}%: {m}")
)

if result.success:
    print(f"Video: {result.video_path}")
    print(f"Duration: {result.duration}s")
```

### Node.js SDK

```javascript
const NexusVision = require('nexus-vision-sdk');

const generator = new NexusVision({
  apiUrl: 'http://localhost:8000'
});

generator.generate({
  prompt: 'ocean waves on beach',
  quality: 'high',
  onProgress: (progress, message) => {
    console.log(`${progress}%: ${message}`);
  }
}).then(result => {
  console.log(`Video: ${result.videoPath}`);
}).catch(error => {
  console.error(`Error: ${error.message}`);
});
```

## Error Handling

### Common Errors

| Error Code | Description | Solution |
|------------|-------------|----------|
| 400 | Invalid prompt | Check prompt format |
| 429 | Rate limit exceeded | Wait and retry |
| 500 | Server error | Check server logs |
| 503 | Service unavailable | Server may be restarting |

### Retry Strategy

```python
import time

def generate_with_retry(prompt, max_retries=3):
    for attempt in range(max_retries):
        try:
            result = generate_video(prompt)
            return result
        except Exception as e:
            if attempt < max_retries - 1:
                wait_time = 2 ** attempt  # Exponential backoff
                time.sleep(wait_time)
            else:
                raise
```

## Rate Limiting

### Limits
- 100 requests per minute per IP
- 1000 requests per hour per API key

### Headers
```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1679568000
```

## Authentication

### API Key (Optional)
```python
headers = {
    'Authorization': 'Bearer YOUR_API_KEY'
}

response = requests.post(url, headers=headers, json=data)
```

## Best Practices

### 1. Connection Management
- Reuse WebSocket connections when possible
- Implement reconnection logic
- Handle connection timeouts

### 2. Error Handling
- Always implement try-catch blocks
- Log errors for debugging
- Provide user-friendly error messages

### 3. Performance
- Use batch processing for multiple videos
- Implement caching for repeated prompts
- Monitor generation times

### 4. Security
- Never expose API keys in client-side code
- Use HTTPS in production
- Validate user inputs

## Testing

### Unit Tests
```python
import unittest

class TestVideoGeneration(unittest.TestCase):
    def test_simple_generation(self):
        result = generate_video("ocean waves")
        self.assertTrue(result.success)
        self.assertIsNotNone(result.video_path)
```

### Integration Tests
```python
def test_full_pipeline():
    # Test complete workflow
    result = generate_video("ocean waves")
    assert os.path.exists(result.video_path)
    assert result.duration > 0
```

## Monitoring

### Metrics to Track
- Request count
- Success rate
- Average generation time
- Error rate
- Queue length

### Example Dashboard
```python
# Get metrics
metrics = requests.get('http://localhost:8000/api/metrics').json()

print(f"Success Rate: {metrics['success_rate']}%")
print(f"Avg Duration: {metrics['avg_duration']}s")
print(f"Queue Size: {metrics['queue_size']}")
```

## Support

### Resources
- API Documentation: http://localhost:8000/docs
- GitHub: https://github.com/nexusvision/api
- Discord: https://discord.gg/nexusvision
- Email: support@nexusvision.com

### Getting Help
1. Check documentation
2. Search existing issues
3. Join Discord community
4. Contact support

## Changelog

### v1.0.0 (2024-03-23)
- Initial release
- WebSocket API
- Batch processing
- Webhook notifications
- Quality settings

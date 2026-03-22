# Testing Guide

## Running Tests

### Health Check
```bash
python backend/health_check.py
```

### Video Generation Test
```bash
python backend/test_video_generation.py
```

### Manual Testing

#### 1. Server Start Test
```bash
python backend/main.py
```
Expected: Server starts on port 8000

#### 2. Dashboard Access Test
Navigate to: `http://localhost:8000/frontend/index_v3.html`
Expected: Dashboard loads with animations

#### 3. API Health Test
```bash
curl http://localhost:8000/api/health
```
Expected: JSON response with status "online"

#### 4. Video Generation Test
1. Enter prompt: "sunset over ocean"
2. Click "Generate Video"
3. Wait for completion
Expected: Video generated successfully

## Test Cases

### Positive Tests
- ✅ Simple prompts work
- ✅ Complex prompts work
- ✅ All modes work (Fast/Quality/Premium)
- ✅ All durations work (4s/8s/12s/16s)
- ✅ Download works
- ✅ Share works

### Negative Tests
- ✅ Empty prompt handled
- ✅ Invalid prompt handled
- ✅ Network error handled
- ✅ API limit handled
- ✅ Timeout handled

### Edge Cases
- ✅ Very long prompts
- ✅ Special characters
- ✅ Multiple rapid requests
- ✅ Concurrent users
- ✅ Cache full

## Performance Tests

### Speed Test
- Ultra Fast: < 10s
- Fast: < 20s
- Quality: < 30s
- Premium: < 60s

### Load Test
- 5 concurrent users
- 10 videos per hour
- Cache performance

### Stress Test
- 10 concurrent users
- 50 videos per hour
- Memory usage

## Integration Tests

### API Integration
- Pexels API connection
- FFmpeg integration
- WebSocket communication

### Component Integration
- Visual Mapper → Script Generator
- Script Generator → Clip Fetcher
- Clip Fetcher → Video Editor

## Regression Tests

After each update, verify:
- [ ] Video generation works
- [ ] All modes functional
- [ ] No new errors
- [ ] Performance maintained
- [ ] UI responsive

## Bug Reporting

When reporting bugs, include:
1. Steps to reproduce
2. Expected vs actual behavior
3. Error messages
4. Environment details
5. Screenshots/videos

## Test Coverage

### Backend
- Video generation pipeline
- Retry logic
- Fallback system
- Error handling
- API integration

### Frontend
- UI rendering
- WebSocket connection
- Progress updates
- Animations
- Download/share

## Continuous Testing

### Before Commit
- Run health check
- Test basic generation
- Check for errors

### Before Release
- Full test suite
- Performance tests
- Integration tests
- User acceptance testing

## Known Issues

See GitHub Issues for current known issues.

## Test Environment

### Requirements
- Python 3.11+
- FFmpeg installed
- Internet connection
- Pexels API key
- 4GB RAM minimum

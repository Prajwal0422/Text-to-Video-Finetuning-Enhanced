# System Architecture

## Overview
```
┌─────────────┐
│   Browser   │
│  (Frontend) │
└──────┬──────┘
       │ WebSocket
       │
┌──────▼──────────────────────────┐
│     FastAPI Server              │
│  ┌──────────────────────────┐  │
│  │  Resilient Generator     │  │
│  │  ┌────────────────────┐  │  │
│  │  │  Retry Manager     │  │  │
│  │  │  Model Router      │  │  │
│  │  │  Local Fallback    │  │  │
│  │  └────────────────────┘  │  │
│  └──────────────────────────┘  │
└──────┬──────────────────────────┘
       │
┌──────▼──────────────────────────┐
│   Video Generation Pipeline     │
│  ┌──────────────────────────┐  │
│  │ 1. Visual Intent Mapper  │  │
│  │ 2. Script Generator      │  │
│  │ 3. Clip Fetcher          │  │
│  │ 4. Video Editor          │  │
│  └──────────────────────────┘  │
└──────┬──────────────────────────┘
       │
┌──────▼──────────────────────────┐
│      External Services          │
│  ┌──────────────────────────┐  │
│  │  Pexels API              │  │
│  │  FFmpeg                  │  │
│  └──────────────────────────┘  │
└─────────────────────────────────┘
```

## Components

### Frontend Layer
- **HTML/CSS/JS** - User interface
- **WebSocket Client** - Real-time updates
- **Animation Engine** - Visual effects
- **Tech Stack Display** - Pipeline visualization

### API Layer
- **FastAPI** - Web framework
- **WebSocket Handler** - Real-time communication
- **Static File Server** - Frontend serving
- **CORS Middleware** - Cross-origin support

### Business Logic Layer
- **Resilient Generator** - Main orchestrator
- **Retry Manager** - Error recovery
- **Model Router** - Fallback logic
- **Local Generator** - Offline mode

### Processing Layer
- **Visual Intent Mapper** - Prompt analysis
- **Script Generator** - Scene planning
- **Clip Fetcher** - Video download
- **Video Editor** - Composition

### Data Layer
- **File Cache** - Clip storage
- **Output Directory** - Generated videos
- **Normalized Cache** - Processed clips

## Data Flow

1. **User Input** → Browser
2. **WebSocket** → Server
3. **Resilient Generator** → Pipeline
4. **Visual Mapper** → Semantic analysis
5. **Script Generator** → Scene planning
6. **Clip Fetcher** → API calls
7. **Video Editor** → Composition
8. **Output** → User download

## Error Handling

```
Request → Retry (3x) → Fallback → Local → Success
           ↓            ↓          ↓
         Fail         Fail       Fail
           ↓            ↓          ↓
        Retry      Fallback    Error
```

## Scalability

### Current
- Single server
- Sequential processing
- File-based cache
- Local storage

### Future
- Load balancing
- Parallel processing
- Database cache
- Cloud storage

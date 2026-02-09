"""
NEXUS VISION API - Fast Text-to-Video Generation
Uses stock footage pipeline instead of diffusion models
"""

import os
from dotenv import load_dotenv
import asyncio
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import uvicorn
from concurrent.futures import ThreadPoolExecutor
import json

from video_generator import VideoGenerator

# Load environment variables
load_dotenv()

app = FastAPI(title="NEXUS VISION API - Fast Video Generation")

# Setup CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Thread pool for video generation
executor = ThreadPoolExecutor(max_workers=2)

# Initialize video generator with API key
pexels_key = os.getenv('PEXELS_API_KEY', '2YmxczgDDvKxVncxrEtrnv82ksotaLFirswQk0Xyhng0cgy6GBXbRPmq')
video_gen = VideoGenerator(pexels_api_key=pexels_key)

# Serve Static Files
PROJECT_ROOT = os.path.dirname(os.getcwd())
app.mount("/frontend", StaticFiles(directory=os.path.join(PROJECT_ROOT, "frontend"), html=True), name="frontend")
app.mount("/outputs", StaticFiles(directory=os.path.join(PROJECT_ROOT, "outputs")), name="outputs")

@app.get("/")
async def redirect_to_home():
    from fastapi.responses import RedirectResponse
    return RedirectResponse(url="/frontend/home.html")

@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "online",
        "method": "stock_footage_pipeline",
        "gpu_required": False
    }

@app.websocket("/ws/generate")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for real-time video generation"""
    await websocket.accept()
    
    try:
        # Receive request
        data = await websocket.receive_text()
        request = json.loads(data)
        prompt = request.get('prompt', '')
        
        if not prompt:
            await websocket.send_json({
                'type': 'error',
                'message': 'No prompt provided'
            })
            return
        
        print(f"\n🎬 New generation request: '{prompt}'")
        
        # Progress callback
        async def send_progress(percent, message, step=""):
            await websocket.send_json({
                'type': 'progress',
                'progress': percent,
                'message': message,
                'step': step
            })
        
        # Run generation in thread pool
        loop = asyncio.get_event_loop()
        
        def generate_with_progress():
            def progress_callback(percent, message):
                asyncio.run_coroutine_threadsafe(
                    send_progress(percent, message),
                    loop
                )
            
            return video_gen.generate(prompt, progress_callback)
        
        result = await loop.run_in_executor(executor, generate_with_progress)
        
        if result['success']:
            # Send success
            video_url = f"/outputs/videos/{os.path.basename(result['video_path'])}"
            await websocket.send_json({
                'type': 'complete',
                'video_path': video_url,
                'duration': result['duration'],
                'message': result['message']
            })
        else:
            await websocket.send_json({
                'type': 'error',
                'message': result['message']
            })
    
    except WebSocketDisconnect:
        print("Client disconnected")
    except Exception as e:
        print(f"Error: {e}")
        try:
            await websocket.send_json({
                'type': 'error',
                'message': str(e)
            })
        except:
            pass

if __name__ == "__main__":
    print("=" * 60)
    print("🚀 NEXUS VISION - Fast Video Generation API")
    print("=" * 60)
    print("Method: Stock Footage Pipeline")
    print("GPU Required: NO")
    print("Average Generation Time: < 30 seconds")
    print("=" * 60)
    
    uvicorn.run(app, host="0.0.0.0", port=8000)

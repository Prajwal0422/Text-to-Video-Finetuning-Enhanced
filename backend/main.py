import os
import asyncio
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from concurrent.futures import ThreadPoolExecutor

from backend.pipeline import run_hybrid_pipeline
from backend.progress import ProgressManager

app = FastAPI(title="AETHER-GEN HYBRID API")

# ... (middleware and setup same as before)

# Setup CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Shared thread pool for blocking heavy computations (torch inference)
executor = ThreadPoolExecutor(max_workers=1)

# Serve Static Files
PROJECT_ROOT = os.getcwd()
app.mount("/frontend", StaticFiles(directory=os.path.join(PROJECT_ROOT, "frontend"), html=True), name="frontend")
app.mount("/outputs", StaticFiles(directory=os.path.join(PROJECT_ROOT, "outputs")), name="outputs")

@app.get("/")
async def redirect_to_frontend():
    from fastapi.responses import RedirectResponse
    return RedirectResponse(url="/frontend/index.html")

@app.websocket("/ws/generate")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    progress_mgr = ProgressManager(websocket)
    
    try:
        data = await websocket.receive_json()
        prompt = data.get("prompt")
        num_frames = data.get("num_frames", 12)
        num_steps = data.get("num_steps", 20)

        if not prompt:
            await progress_mgr.send_error("No prompt provided.")
            return

        # Offload blocking inference to thread pool
        loop = asyncio.get_event_loop()
        mode = data.get("mode", "fast")
        video_url = await loop.run_in_executor(
            executor, 
            lambda: run_hybrid_pipeline(prompt, mode, progress_mgr)
        )

        await progress_mgr.send_complete(video_url)

    except WebSocketDisconnect:
        print("Client disconnected")
    except Exception as e:
        await progress_mgr.send_error(str(e))
    finally:
        try:
            await websocket.close()
        except:
            pass

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

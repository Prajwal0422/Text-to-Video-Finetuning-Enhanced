import os
from fastapi import FastAPI, WebSocket
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from backend.websocket import handle_websocket

app = FastAPI(
    title="Text-to-Video Enhanced Platform",
    description="Production-grade AI generation dashboard.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_ROOT = os.path.dirname(BASE_DIR)

# Serve individual root files for the landing page
@app.get("/styles.css")
async def get_styles():
    from fastapi.responses import FileResponse
    return FileResponse(os.path.join(PROJECT_ROOT, "styles.css"))

@app.get("/script.js")
async def get_script():
    from fastapi.responses import FileResponse
    return FileResponse(os.path.join(PROJECT_ROOT, "script.js"))

@app.get("/")
async def get_index():
    from fastapi.responses import FileResponse
    return FileResponse(os.path.join(PROJECT_ROOT, "index.html"))

# Serve other root assets if needed
app.mount("/assets", StaticFiles(directory=PROJECT_ROOT), name="assets")

app.mount("/frontend", StaticFiles(directory=os.path.join(BASE_DIR, "frontend"), html=True), name="frontend")
app.mount("/outputs", StaticFiles(directory=os.path.join(BASE_DIR, "outputs")), name="outputs")

@app.websocket("/ws/stream")
async def websocket_route(websocket: WebSocket):
    await handle_websocket(websocket)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")

import asyncio
import logging

logger = logging.getLogger(__name__)

class ProgressManager:
    def __init__(self, websocket):
        self.websocket = websocket
        self.loop = asyncio.get_event_loop()

    def send_status(self, type, message, progress=None):
        payload = {"type": type, "message": message}
        if progress is not None:
            payload["progress"] = progress
            
        asyncio.run_coroutine_threadsafe(
            self.websocket.send_json(payload), 
            self.loop
        )

    async def send_error(self, message):
        await self.websocket.send_json({"type": "error", "message": message})

    async def send_complete(self, video_url):
        await self.websocket.send_json({
            "type": "complete", 
            "video_url": video_url,
            "message": "Generation successful!"
        })

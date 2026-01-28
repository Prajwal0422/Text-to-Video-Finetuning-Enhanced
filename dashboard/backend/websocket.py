from fastapi import WebSocket, WebSocketDisconnect
import json
import logging
from backend.task_manager import task_manager

logger = logging.getLogger(__name__)

async def handle_websocket(websocket: WebSocket):
    await websocket.accept()
    logger.info("Real-time stream established.")
    
    try:
        data = await websocket.receive_text()
        config = json.loads(data)
        
        prompt = config.get("prompt")
        if not prompt:
            await websocket.send_json({"type": "error", "message": "Prompt is mandatory."})
            await websocket.close()
            return

        async def stream_status(status_obj: dict):
            try:
                await websocket.send_json(status_obj)
            except Exception:
                pass

        await stream_status({"type": "status", "message": "Queueing generation task..."})

        video_url = await task_manager.run_generation(
            task_id="active_job",
            prompt=prompt,
            params=config,
            callback=stream_status
        )

        await stream_status({
            "type": "complete",
            "video_url": video_url,
            "message": "Dynamic video generation finished successfully."
        })

    except WebSocketDisconnect:
        logger.info("Real-time stream disconnected by user.")
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
        try:
            await websocket.send_json({"type": "error", "message": str(e)})
        except Exception:
            pass
    finally:
        try:
            await websocket.close()
        except Exception:
            pass

import os
import uuid
import torch
import logging
import asyncio
from diffusers.utils import export_to_video
from backend.model_loader import ModelLoader

logger = logging.getLogger(__name__)

async def generate_video_async(prompt: str, num_frames: int = 24, num_steps: int = 25, status_callback=None):
    try:
        loader = ModelLoader.get_instance()
        pipe = loader.load_model()

        def progress_callback(step, timestep, latents):
            if status_callback:
                progress = int((step / num_steps) * 100)
                asyncio.run_coroutine_threadsafe(
                    status_callback({
                        "type": "progress",
                        "progress": progress,
                        "message": f"Denoising step {step}/{num_steps}..."
                    }),
                    asyncio.get_event_loop()
                )

        if status_callback:
            await status_callback({"type": "status", "message": "Analyzing prompt & initializing latents..."})

        result = pipe(
            prompt,
            num_frames=num_frames,
            num_inference_steps=num_steps,
            height=320,
            width=576,
            callback=progress_callback,
            callback_steps=1
        )
        
        video_frames = result.frames
        
        if status_callback:
            await status_callback({"type": "status", "message": "Encoding temporal frames to MP4..."})

        video_id = str(uuid.uuid4())[:8]
        output_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "outputs", "videos")
        os.makedirs(output_dir, exist_ok=True)
        
        output_path = os.path.join(output_dir, f"gen_{video_id}.mp4")
        export_to_video(video_frames, output_path, fps=8)
        
        logger.info(f"Persistent video created: {output_path}")
        return f"/outputs/videos/gen_{video_id}.mp4"

    except Exception as e:
        logger.error(f"Inference failure: {e}")
        if status_callback:
            await status_callback({"type": "error", "message": str(e)})
        raise e

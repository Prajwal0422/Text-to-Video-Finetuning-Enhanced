import os
import uuid
import torch
import logging
from diffusers.utils import export_to_video
from backend.model_loader import ModelLoader

logger = logging.getLogger(__name__)

def generate_video(prompt, num_frames=12, num_steps=20, progress_mgr=None):
    try:
        # 1. Load Model (Singleton)
        if progress_mgr:
            progress_mgr.send_status("loading_model", "Synchronizing neural weights...")
        
        loader = ModelLoader.get_instance()
        pipe = loader.load_model()

        # 2. Setup Progress Callback
        def pipe_callback(step, timestep, latents):
            if progress_mgr:
                progress = int((step / num_steps) * 100)
                progress_mgr.send_status(
                    "generating_frames", 
                    f"Denoising latent space: {step}/{num_steps}",
                    progress=progress
                )

        # 3. Launch Generation
        logger.info(f"Starting generation for prompt: {prompt}")
        
        # Use lower resolution for speed/stability
        gen_width = 384 if loader.device == "cpu" else 576
        gen_height = 256 if loader.device == "cpu" else 320

        result = pipe(
            prompt,
            num_frames=num_frames,
            num_inference_steps=num_steps,
            width=gen_width,
            height=gen_height,
            callback=pipe_callback,
            callback_steps=1
        )

        # 4. Export Video
        if progress_mgr:
            progress_mgr.send_status("encoding_video", "Encoding temporal sequence to MP4...")
        
        video_id = str(uuid.uuid4())[:8]
        output_dir = os.path.join(os.getcwd(), "outputs", "videos")
        os.makedirs(output_dir, exist_ok=True)
        
        output_path = os.path.join(output_dir, f"gen_{video_id}.mp4")
        export_to_video(result.frames, output_path, fps=8)
        
        logger.info(f"Video saved to {output_path}")
        return f"/outputs/videos/gen_{video_id}.mp4"

    except Exception as e:
        logger.error(f"Inference error: {e}")
        raise e

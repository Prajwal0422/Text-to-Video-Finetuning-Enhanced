import os
import uuid
import logging
import time
from backend.text_to_image import T2IEngine
from backend.image_to_video import MotionEngine

logger = logging.getLogger(__name__)

def run_hybrid_pipeline(prompt, mode="fast", progress_mgr=None):
    """
    Orchestrates the Hybrid Fast Pipeline: T2I -> Motion -> MP4
    """
    try:
        # 1. T2I Phase
        if progress_mgr:
            progress_mgr.send_status("loading_model", "Initializing Neural Core...")
        
        t2i = T2IEngine.get_instance()
        
        if progress_mgr:
            progress_mgr.send_status("generating_frames", "Materializing Latent Vision...", progress=20)
        
        # SD 1.5: Fast mode 8-10 steps. HQ mode 20-25 steps.
        steps = 8 if mode == "fast" else 20
        image = t2i.generate(prompt, num_steps=steps)
        
        if progress_mgr:
            progress_mgr.send_status("generating_frames", "Finalizing Base Keyframe...", progress=60)

        # 2. Motion Phase
        if progress_mgr:
            progress_mgr.send_status("encoding_video", "Injecting Cinematic Motion...")
            
        video_id = str(uuid.uuid4())[:8]
        output_dir = os.path.join(os.getcwd(), "outputs", "videos")
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, f"hybrid_{video_id}.mp4")

        # Determine motion style based on prompt context (simple heuristic)
        motion = "zoom_in"
        if any(word in prompt.lower() for word in ["landscape", "city", "street"]):
            motion = "pan_right"

        MotionEngine.create_video(image, output_path, motion_type=motion)

        if progress_mgr:
            progress_mgr.send_status("complete", "Synthesis Complete!", progress=100)
            
        return f"/outputs/videos/hybrid_{video_id}.mp4"

    except Exception as e:
        logger.error(f"Hybrid Pipeline Failure: {e}")
        if progress_mgr:
            progress_mgr.send_status("error", str(e))
        raise e

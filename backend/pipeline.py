import os
import uuid
import logging
import time
from text_to_image import T2IEngine
from image_to_video import MotionEngine
from speed_optimizer import GPUAccelerator, PerformanceMonitor, AdaptiveQualityController
from advanced_video_algorithms import SmoothMotionEngine, ColorGrading

logger = logging.getLogger(__name__)

def run_hybrid_pipeline(prompt, mode="fast", progress_mgr=None, motion_type="auto", 
                       fps=30, duration=3, quality="high"):
    """
    Enhanced Hybrid Fast Pipeline: T2I -> Motion -> MP4
    With GPU acceleration, adaptive quality, and advanced motion algorithms
    
    Args:
        prompt: Text description for video generation
        mode: 'fast' (8 steps) or 'quality' (20 steps)
        progress_mgr: Progress callback manager
        motion_type: Motion algorithm ('auto', 'zoom_in', 'pan_right', 'ken_burns', etc.)
        fps: Target frames per second (higher = smoother)
        duration: Video duration in seconds
        quality: 'fast', 'balanced', 'high', 'ultra'
    """
    try:
        # Initialize performance monitoring
        perf_monitor = PerformanceMonitor()
        perf_monitor.start_timer('total_pipeline')
        
        # Initialize GPU acceleration
        gpu_accel = GPUAccelerator()
        if gpu_accel.cuda_available:
            logger.info("🚀 GPU acceleration enabled")
        
        # 1. T2I Phase
        if progress_mgr:
            progress_mgr.send_status("loading_model", "Initializing Neural Core...")
        
        perf_monitor.start_timer('t2i_generation')
        t2i = T2IEngine.get_instance()
        
        if progress_mgr:
            progress_mgr.send_status("generating_frames", "Materializing Latent Vision...", progress=20)
        
        # Adaptive steps based on mode
        steps = 8 if mode == "fast" else 20
        image = t2i.generate(prompt, num_steps=steps)
        
        t2i_time = perf_monitor.end_timer('t2i_generation')
        logger.info(f"✅ T2I generation completed in {t2i_time:.2f}s")
        
        if progress_mgr:
            progress_mgr.send_status("generating_frames", "Finalizing Base Keyframe...", progress=60)

        # 2. Motion Phase with Advanced Algorithms
        if progress_mgr:
            progress_mgr.send_status("encoding_video", "Injecting Cinematic Motion...")
        
        perf_monitor.start_timer('motion_generation')
        
        video_id = str(uuid.uuid4())[:8]
        output_dir = os.path.join(os.getcwd(), "outputs", "videos")
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, f"hybrid_{video_id}.mp4")

        # Intelligent motion selection
        if motion_type == "auto":
            motion = _select_motion_type(prompt)
        else:
            motion = motion_type
        
        logger.info(f"🎬 Applying motion: {motion}")
        
        # Apply color grading for cinematic look
        image_array = ColorGrading.apply_lut(image, lut_type='cinematic')
        image_array = ColorGrading.vignette(image_array, intensity=0.3)
        
        # Generate video with advanced motion
        MotionEngine.create_video(
            image_array, 
            output_path, 
            duration=duration,
            fps=fps,
            motion_type=motion,
            quality=quality
        )
        
        motion_time = perf_monitor.end_timer('motion_generation')
        logger.info(f"✅ Motion generation completed in {motion_time:.2f}s")

        if progress_mgr:
            progress_mgr.send_status("complete", "Synthesis Complete!", progress=100)
        
        total_time = perf_monitor.end_timer('total_pipeline')
        logger.info(f"🎉 Total pipeline time: {total_time:.2f}s")
        
        # Performance report
        perf_report = perf_monitor.get_report()
        logger.info(f"📊 Performance: {perf_report}")
            
        return f"/outputs/videos/hybrid_{video_id}.mp4"

    except Exception as e:
        logger.error(f"Hybrid Pipeline Failure: {e}")
        if progress_mgr:
            progress_mgr.send_status("error", str(e))
        raise e


def _select_motion_type(prompt: str) -> str:
    """Intelligently select motion type based on prompt content"""
    prompt_lower = prompt.lower()
    
    # Landscape/nature scenes
    if any(word in prompt_lower for word in ["landscape", "mountain", "valley", "horizon", "vista"]):
        return "pan_right"
    
    # Ocean/water scenes
    if any(word in prompt_lower for word in ["ocean", "sea", "water", "wave", "beach"]):
        return "breathe"
    
    # City/urban scenes
    if any(word in prompt_lower for word in ["city", "urban", "street", "building", "skyline"]):
        return "ken_burns"
    
    # Portrait/close-up
    if any(word in prompt_lower for word in ["portrait", "face", "person", "close-up"]):
        return "zoom_in"
    
    # Space/cosmic scenes
    if any(word in prompt_lower for word in ["space", "galaxy", "stars", "cosmic", "nebula"]):
        return "rotate_cw"
    
    # Action/dynamic scenes
    if any(word in prompt_lower for word in ["action", "fast", "dynamic", "motion", "speed"]):
        return "dolly_zoom"
    
    # Default: smooth zoom
    return "zoom_in"


def run_fast_pipeline(prompt, progress_mgr=None):
    """Ultra-fast pipeline optimized for speed"""
    return run_hybrid_pipeline(
        prompt, 
        mode="fast", 
        progress_mgr=progress_mgr,
        fps=24,
        duration=3,
        quality="balanced"
    )


def run_quality_pipeline(prompt, progress_mgr=None):
    """High-quality pipeline optimized for visual fidelity"""
    return run_hybrid_pipeline(
        prompt,
        mode="quality",
        progress_mgr=progress_mgr,
        fps=30,
        duration=4,
        quality="ultra"
    )

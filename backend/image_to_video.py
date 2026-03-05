"""
Image to Video Conversion Module

This module provides motion effects to convert static images into dynamic videos.
Supports both basic and enhanced motion engines with various algorithms.

Features:
- Multiple motion types (zoom, pan, rotate, etc.)
- Quality modes (fast, balanced, quality)
- GPU acceleration support
- Optical flow interpolation
- Motion blur effects
- Cinematic post-processing

Performance:
- Fast mode: 5-8 seconds
- Balanced mode: 8-12 seconds  
- Quality mode: 15-20 seconds

Usage:
    from image_to_video import MotionEngine
    
    engine = MotionEngine()
    engine.create_video(
        image, "output.mp4",
        motion_type="zoom_in",
        quality_mode="balanced"
    )
"""

import cv2
import numpy as np
import imageio
from PIL import Image
import os

# Import enhanced engine if available
# Enhanced engine provides advanced algorithms for smoother motion
# Falls back to basic engine if dependencies not installed
try:
    from enhanced_motion_engine import EnhancedMotionEngine
    ENHANCED_AVAILABLE = True
except ImportError:
    ENHANCED_AVAILABLE = False

class MotionEngine:
    @staticmethod
    def create_video(image, output_path, duration=3, fps=24, motion_type="zoom_in",
                    use_enhanced=True, quality_mode="balanced"):
        """
        Applies cinematic motion transforms to a static image to create a high-quality video sequence.
        
        Args:
            image: PIL Image or numpy array
            output_path: Output file path
            duration: Video duration in seconds
            fps: Frames per second
            motion_type: Type of motion effect
            use_enhanced: Use enhanced engine with all optimizations
            quality_mode: "fast", "balanced", or "quality"
        """
        # Use enhanced engine if available and requested
        if use_enhanced and ENHANCED_AVAILABLE:
            engine = EnhancedMotionEngine(quality_mode=quality_mode)
            return engine.create_video(
                image, output_path, duration=duration, 
                fps=fps, motion_type=motion_type
            )
        
        # Fallback to basic engine
        img_np = np.array(image)
        h, w, _ = img_np.shape
        frames = []
        num_frames = duration * fps

        for i in range(num_frames):
            t = i / num_frames
            
            if motion_type == "zoom_in":
                # Zoom In: Scale from 1.0 to 1.15
                scale = 1.0 + (t * 0.15)
                new_w, new_h = int(w * scale), int(h * scale)
                frame = cv2.resize(img_np, (new_w, new_h), interpolation=cv2.INTER_LANCZOS4)
                
                # Center Crop back to original size
                x = (new_w - w) // 2
                y = (new_h - h) // 2
                frame = frame[y:y+h, x:x+w]
                
            elif motion_type == "pan_right":
                # Pan Right: Slide window across a slightly larger scaled image
                scale = 1.1
                new_w, new_h = int(w * scale), int(h * scale)
                temp_img = cv2.resize(img_np, (new_w, new_h))
                
                max_x = new_w - w
                x = int(t * max_x)
                y = (new_h - h) // 2
                frame = temp_img[y:y+h, x:x+w]
                
            else: # Default: Subtle breathe
                scale = 1.0 + (np.sin(t * np.pi) * 0.05)
                new_w, new_h = int(w * scale), int(h * scale)
                frame = cv2.resize(img_np, (new_w, new_h))
                x = (new_w - w) // 2
                y = (new_h - h) // 2
                frame = frame[y:y+h, x:x+w]

            frames.append(frame)

        # Save as MP4
        imageio.mimsave(output_path, frames, fps=fps, quality=9)
        return output_path

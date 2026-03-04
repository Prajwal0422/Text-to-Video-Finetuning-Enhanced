"""
Enhanced Motion Engine with Advanced Algorithms
Integrates all speed and smoothness optimizations
"""

import cv2
import numpy as np
import imageio
from typing import List, Optional
from advanced_video_algorithms import (
    EasingFunctions, OpticalFlowSmoother, MotionBlurEngine,
    AdaptiveFrameRateOptimizer, AdvancedStabilizer, ColorGradingEngine
)
from speed_optimizer import (
    MultiThreadProcessor, MemoryOptimizer, CompressionOptimizer,
    GPUAccelerator, AdaptiveQualityManager, PreprocessingPipeline
)
from video_effects import TransitionEffects, CinematicEffects, MotionEffects


class EnhancedMotionEngine:
    """
    Next-generation motion engine with all optimizations
    """
    
    def __init__(self, quality_mode: str = "balanced"):
        self.quality_mode = quality_mode
        self.processor = MultiThreadProcessor()
        self.use_gpu = GPUAccelerator.is_gpu_available()
        
    def create_video(self, image, output_path: str, 
                    duration: int = 3, fps: Optional[int] = None,
                    motion_type: str = "zoom_in",
                    apply_effects: bool = True,
                    stabilize: bool = True) -> str:
        """
        Create high-quality video with all enhancements
        
        Args:
            image: PIL Image or numpy array
            output_path: Output file path
            duration: Video duration in seconds
            fps: Frames per second (auto-calculated if None)
            motion_type: Type of motion effect
            apply_effects: Apply cinematic effects
            stabilize: Apply stabilization
        """
        # Convert to numpy array
        img_np = np.array(image)
        h, w = img_np.shape[:2]
        
        # Optimize frame size for processing
        img_np = MemoryOptimizer.process_in_chunks(
            [img_np],
            lambda f: f
        )[0]
        
        # Calculate optimal FPS
        if fps is None:
            motion_intensity = self._estimate_motion_intensity(motion_type)
            fps = AdaptiveFrameRateOptimizer.calculate_optimal_fps(
                motion_intensity, self.quality_mode
            )
        
        num_frames = duration * fps
        
        # Generate base frames with motion
        print(f"🎬 Generating {num_frames} frames at {fps} FPS...")
        frames = self._generate_motion_frames(
            img_np, num_frames, motion_type
        )
        
        # Apply frame interpolation for smoothness
        if self.quality_mode in ["balanced", "quality"]:
            print("🔄 Applying optical flow interpolation...")
            frames = self._interpolate_frames(frames)
        
        # Apply stabilization
        if stabilize and len(frames) > 10:
            print("📐 Stabilizing sequence...")
            frames = AdvancedStabilizer.stabilize_sequence(frames)
        
        # Apply cinematic effects
        if apply_effects:
            print("🎨 Applying cinematic effects...")
            frames = self._apply_cinematic_effects(frames)
        
        # Optimize and save
        print("💾 Encoding video...")
        self._save_optimized_video(frames, output_path, fps)
        
        print(f"✅ Video created: {output_path}")
        return output_path
    
    def _generate_motion_frames(self, img_np: np.ndarray, 
                               num_frames: int,
                               motion_type: str) -> List[np.ndarray]:
        """Generate frames with smooth motion"""
        h, w = img_np.shape[:2]
        
        def generate_frame(i):
            t = i / num_frames
            
            # Apply easing for smooth motion
            eased_t = EasingFunctions.ease_in_out_cubic(t)
            
            if motion_type == "zoom_in":
                return self._apply_zoom(img_np, eased_t, zoom_in=True)
            
            elif motion_type == "zoom_out":
                return self._apply_zoom(img_np, eased_t, zoom_in=False)
            
            elif motion_type == "pan_right":
                return self._apply_pan(img_np, eased_t, direction="right")
            
            elif motion_type == "pan_left":
                return self._apply_pan(img_np, eased_t, direction="left")
            
            elif motion_type == "pan_up":
                return self._apply_pan(img_np, eased_t, direction="up")
            
            elif motion_type == "pan_down":
                return self._apply_pan(img_np, eased_t, direction="down")
            
            elif motion_type == "rotate_cw":
                return self._apply_rotation(img_np, eased_t, clockwise=True)
            
            elif motion_type == "rotate_ccw":
                return self._apply_rotation(img_np, eased_t, clockwise=False)
            
            elif motion_type == "ken_burns":
                return MotionEffects.ken_burns_effect(img_np, eased_t)
            
            elif motion_type == "dolly_zoom":
                return MotionEffects.dolly_zoom(img_np, eased_t)
            
            elif motion_type == "breathe":
                # Subtle breathing effect
                breathe_t = np.sin(eased_t * np.pi * 2) * 0.5 + 0.5
                return self._apply_zoom(img_np, breathe_t * 0.1, zoom_in=True)
            
            else:  # Default: subtle zoom
                return self._apply_zoom(img_np, eased_t * 0.1, zoom_in=True)
        
        # Parallel frame generation
        frames = self.processor.process_frames_parallel(
            list(range(num_frames)),
            generate_frame
        )
        
        return frames
    
    def _apply_zoom(self, frame: np.ndarray, progress: float,
                   zoom_in: bool = True) -> np.ndarray:
        """Apply smooth zoom effect"""
        h, w = frame.shape[:2]
        
        if zoom_in:
            scale = 1.0 + progress * 0.2
        else:
            scale = 1.2 - progress * 0.2
        
        new_h, new_w = int(h * scale), int(w * scale)
        
        # Use GPU if available
        if self.use_gpu:
            zoomed = GPUAccelerator.resize_gpu(frame, (new_w, new_h))
        else:
            zoomed = cv2.resize(frame, (new_w, new_h), 
                              interpolation=cv2.INTER_LANCZOS4)
        
        # Center crop
        y = (new_h - h) // 2
        x = (new_w - w) // 2
        result = zoomed[y:y+h, x:x+w]
        
        # Apply subtle motion blur for realism
        if progress > 0.01:
            blur_strength = int(progress * 5)
            if blur_strength > 0:
                result = MotionBlurEngine.apply_zoom_blur(result, progress * 0.02)
        
        return result
    
    def _apply_pan(self, frame: np.ndarray, progress: float,
                  direction: str = "right") -> np.ndarray:
        """Apply smooth pan effect"""
        h, w = frame.shape[:2]
        
        # Scale up for panning
        scale = 1.15
        new_h, new_w = int(h * scale), int(w * scale)
        scaled = cv2.resize(frame, (new_w, new_h), 
                          interpolation=cv2.INTER_LANCZOS4)
        
        # Calculate pan offset
        if direction == "right":
            max_x = new_w - w
            x = int(progress * max_x)
            y = (new_h - h) // 2
            angle = 0
        elif direction == "left":
            max_x = new_w - w
            x = int((1 - progress) * max_x)
            y = (new_h - h) // 2
            angle = 180
        elif direction == "down":
            max_y = new_h - h
            x = (new_w - w) // 2
            y = int(progress * max_y)
            angle = 90
        else:  # up
            max_y = new_h - h
            x = (new_w - w) // 2
            y = int((1 - progress) * max_y)
            angle = 270
        
        result = scaled[y:y+h, x:x+w]
        
        # Apply directional motion blur
        if progress > 0.01 and self.quality_mode != "fast":
            blur_strength = min(int(progress * 10), 15)
            result = MotionBlurEngine.apply_directional_blur(
                result, angle, blur_strength
            )
        
        return result
    
    def _apply_rotation(self, frame: np.ndarray, progress: float,
                       clockwise: bool = True) -> np.ndarray:
        """Apply smooth rotation effect"""
        h, w = frame.shape[:2]
        
        # Rotation angle
        max_angle = 15  # degrees
        angle = progress * max_angle * (1 if clockwise else -1)
        
        # Rotation matrix
        center = (w // 2, h // 2)
        M = cv2.getRotationMatrix2D(center, angle, 1.0)
        
        result = cv2.warpAffine(frame, M, (w, h), 
                               flags=cv2.INTER_LANCZOS4,
                               borderMode=cv2.BORDER_REFLECT)
        
        return result
    
    def _interpolate_frames(self, frames: List[np.ndarray],
                           factor: int = 1) -> List[np.ndarray]:
        """Add interpolated frames for extra smoothness"""
        if factor == 0 or len(frames) < 2:
            return frames
        
        interpolated = [frames[0]]
        
        for i in range(len(frames) - 1):
            interpolated.append(frames[i])
            
            # Generate intermediate frames
            intermediate = OpticalFlowSmoother.interpolate_frames(
                frames[i], frames[i + 1], num_intermediate=factor
            )
            interpolated.extend(intermediate)
        
        interpolated.append(frames[-1])
        return interpolated
    
    def _apply_cinematic_effects(self, frames: List[np.ndarray]) -> List[np.ndarray]:
        """Apply cinematic post-processing"""
        
        def process_frame(frame):
            result = frame
            
            # Color grading
            result = ColorGradingEngine.apply_lut(result, "cinematic")
            result = ColorGradingEngine.enhance_contrast(result, 1.1)
            
            # Vignette
            result = CinematicEffects.add_vignette(result, 0.3)
            
            # Subtle film grain
            if self.quality_mode == "quality":
                result = CinematicEffects.add_film_grain(result, 0.02)
            
            return result
        
        # Parallel processing
        return self.processor.process_frames_parallel(frames, process_frame)
    
    def _save_optimized_video(self, frames: List[np.ndarray],
                             output_path: str, fps: int):
        """Save video with optimal compression"""
        h, w = frames[0].shape[:2]
        
        # Get optimal codec and settings
        fourcc, crf = CompressionOptimizer.get_optimal_codec(self.quality_mode)
        bitrate = CompressionOptimizer.optimize_bitrate(
            (w, h), fps, self.quality_mode
        )
        
        # Save with imageio for better quality
        imageio.mimsave(
            output_path,
            frames,
            fps=fps,
            quality=10 if self.quality_mode == "quality" else 8,
            codec='libx264',
            pixelformat='yuv420p',
            output_params=['-crf', str(crf)]
        )
    
    def _estimate_motion_intensity(self, motion_type: str) -> float:
        """Estimate motion intensity for FPS optimization"""
        intensity_map = {
            "zoom_in": 0.5,
            "zoom_out": 0.5,
            "pan_right": 0.7,
            "pan_left": 0.7,
            "pan_up": 0.7,
            "pan_down": 0.7,
            "rotate_cw": 0.8,
            "rotate_ccw": 0.8,
            "ken_burns": 0.6,
            "dolly_zoom": 0.9,
            "breathe": 0.3
        }
        return intensity_map.get(motion_type, 0.5)


# Convenience function for backward compatibility
def create_enhanced_video(image, output_path: str, **kwargs) -> str:
    """Create video with enhanced motion engine"""
    engine = EnhancedMotionEngine(quality_mode=kwargs.get("quality_mode", "balanced"))
    return engine.create_video(image, output_path, **kwargs)

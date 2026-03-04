"""
Advanced Video Generation Algorithms
Implements cutting-edge techniques for speed and smoothness optimization
"""

import cv2
import numpy as np
from typing import Tuple, List, Optional
from scipy.interpolate import interp1d
from scipy.ndimage import gaussian_filter


class EasingFunctions:
    """Mathematical easing functions for smooth motion"""
    
    @staticmethod
    def ease_in_out_cubic(t: float) -> float:
        """Smooth acceleration and deceleration"""
        return 4 * t * t * t if t < 0.5 else 1 - pow(-2 * t + 2, 3) / 2
    
    @staticmethod
    def ease_in_out_quint(t: float) -> float:
        """Very smooth motion curve"""
        return 16 * t * t * t * t * t if t < 0.5 else 1 - pow(-2 * t + 2, 5) / 2
    
    @staticmethod
    def ease_out_expo(t: float) -> float:
        """Fast start, smooth stop"""
        return 1 if t == 1 else 1 - pow(2, -10 * t)
    
    @staticmethod
    def ease_in_out_sine(t: float) -> float:
        """Sinusoidal smooth motion"""
        return -(np.cos(np.pi * t) - 1) / 2
    
    @staticmethod
    def ease_in_out_back(t: float) -> float:
        """Slight overshoot for dynamic feel"""
        c1 = 1.70158
        c2 = c1 * 1.525
        return (pow(2 * t, 2) * ((c2 + 1) * 2 * t - c2) / 2 if t < 0.5 
                else (pow(2 * t - 2, 2) * ((c2 + 1) * (t * 2 - 2) + c2) + 2) / 2)


class OpticalFlowSmoother:
    """Advanced frame interpolation using optical flow"""
    
    @staticmethod
    def interpolate_frames(frame1: np.ndarray, frame2: np.ndarray, 
                          num_intermediate: int = 2) -> List[np.ndarray]:
        """Generate smooth intermediate frames between two frames"""
        gray1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
        gray2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
        
        # Calculate optical flow
        flow = cv2.calcOpticalFlowFarneback(
            gray1, gray2, None, 
            pyr_scale=0.5, levels=3, winsize=15,
            iterations=3, poly_n=5, poly_sigma=1.2, flags=0
        )
        
        interpolated = []
        for i in range(1, num_intermediate + 1):
            alpha = i / (num_intermediate + 1)
            
            # Warp frame1 towards frame2
            h, w = flow.shape[:2]
            flow_map = np.column_stack([
                (np.arange(w) + flow[..., 0] * alpha).ravel(),
                (np.arange(h).reshape(-1, 1) + flow[..., 1] * alpha).ravel()
            ]).reshape(h, w, 2).astype(np.float32)
            
            warped = cv2.remap(frame1, flow_map, None, cv2.INTER_LINEAR)
            
            # Blend with frame2
            blended = cv2.addWeighted(warped, 1 - alpha, frame2, alpha, 0)
            interpolated.append(blended)
        
        return interpolated


class MotionBlurEngine:
    """Realistic motion blur for cinematic feel"""
    
    @staticmethod
    def apply_directional_blur(frame: np.ndarray, angle: float, 
                               strength: int = 15) -> np.ndarray:
        """Apply motion blur in specific direction"""
        if strength == 0:
            return frame
        
        # Create motion blur kernel
        kernel_size = strength
        kernel = np.zeros((kernel_size, kernel_size))
        
        # Calculate kernel line based on angle
        center = kernel_size // 2
        angle_rad = np.deg2rad(angle)
        
        for i in range(kernel_size):
            offset = i - center
            x = int(center + offset * np.cos(angle_rad))
            y = int(center + offset * np.sin(angle_rad))
            if 0 <= x < kernel_size and 0 <= y < kernel_size:
                kernel[y, x] = 1
        
        kernel = kernel / np.sum(kernel)
        
        # Apply blur
        return cv2.filter2D(frame, -1, kernel)
    
    @staticmethod
    def apply_zoom_blur(frame: np.ndarray, strength: float = 0.02) -> np.ndarray:
        """Apply radial zoom blur effect"""
        h, w = frame.shape[:2]
        center_x, center_y = w // 2, h // 2
        
        result = np.zeros_like(frame, dtype=np.float32)
        num_samples = 10
        
        for i in range(num_samples):
            scale = 1.0 + (i / num_samples) * strength
            scaled_h, scaled_w = int(h * scale), int(w * scale)
            
            # Resize and crop to center
            scaled = cv2.resize(frame, (scaled_w, scaled_h))
            y_start = (scaled_h - h) // 2
            x_start = (scaled_w - w) // 2
            cropped = scaled[y_start:y_start+h, x_start:x_start+w]
            
            result += cropped.astype(np.float32)
        
        return (result / num_samples).astype(np.uint8)


class AdaptiveFrameRateOptimizer:
    """Dynamic FPS optimization for performance"""
    
    @staticmethod
    def calculate_optimal_fps(motion_intensity: float, target_quality: str = "balanced") -> int:
        """Determine optimal FPS based on motion and quality target"""
        base_fps = {
            "fast": 24,
            "balanced": 30,
            "quality": 60
        }
        
        fps = base_fps.get(target_quality, 30)
        
        # Adjust based on motion intensity
        if motion_intensity > 0.7:
            fps = min(fps + 6, 60)
        elif motion_intensity < 0.3:
            fps = max(fps - 6, 24)
        
        return fps
    
    @staticmethod
    def estimate_motion_intensity(frames: List[np.ndarray]) -> float:
        """Estimate motion intensity from frame sequence"""
        if len(frames) < 2:
            return 0.5
        
        diffs = []
        for i in range(len(frames) - 1):
            gray1 = cv2.cvtColor(frames[i], cv2.COLOR_BGR2GRAY)
            gray2 = cv2.cvtColor(frames[i + 1], cv2.COLOR_BGR2GRAY)
            diff = np.mean(np.abs(gray1.astype(float) - gray2.astype(float)))
            diffs.append(diff)
        
        return np.mean(diffs) / 255.0


class AdvancedStabilizer:
    """Video stabilization for smooth playback"""
    
    @staticmethod
    def stabilize_sequence(frames: List[np.ndarray], 
                          smoothing_window: int = 30) -> List[np.ndarray]:
        """Apply stabilization to frame sequence"""
        if len(frames) < 2:
            return frames
        
        # Detect features in first frame
        prev_gray = cv2.cvtColor(frames[0], cv2.COLOR_BGR2GRAY)
        prev_pts = cv2.goodFeaturesToTrack(prev_gray, maxCorners=200,
                                           qualityLevel=0.01, minDistance=30)
        
        transforms = []
        
        for frame in frames[1:]:
            curr_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            # Calculate optical flow
            curr_pts, status, _ = cv2.calcOpticalFlowPyrLK(
                prev_gray, curr_gray, prev_pts, None
            )
            
            # Filter valid points
            idx = np.where(status == 1)[0]
            prev_pts_valid = prev_pts[idx]
            curr_pts_valid = curr_pts[idx]
            
            # Estimate transform
            if len(prev_pts_valid) >= 3:
                transform = cv2.estimateAffinePartial2D(
                    prev_pts_valid, curr_pts_valid
                )[0]
                transforms.append(transform)
            else:
                transforms.append(np.eye(2, 3, dtype=np.float32))
            
            prev_gray = curr_gray
            prev_pts = cv2.goodFeaturesToTrack(curr_gray, maxCorners=200,
                                              qualityLevel=0.01, minDistance=30)
        
        # Smooth transforms
        trajectory = np.cumsum(transforms, axis=0)
        smoothed_trajectory = gaussian_filter(trajectory, sigma=smoothing_window, 
                                             axes=0, mode='nearest')
        
        # Apply smoothed transforms
        stabilized = [frames[0]]
        for i, frame in enumerate(frames[1:]):
            smooth_transform = smoothed_trajectory[i]
            h, w = frame.shape[:2]
            stabilized_frame = cv2.warpAffine(frame, smooth_transform, (w, h))
            stabilized.append(stabilized_frame)
        
        return stabilized


class ColorGradingEngine:
    """Professional color grading for cinematic look"""
    
    @staticmethod
    def apply_lut(frame: np.ndarray, lut_type: str = "cinematic") -> np.ndarray:
        """Apply color lookup table"""
        if lut_type == "cinematic":
            # Teal and orange look
            frame = frame.astype(np.float32)
            frame[:, :, 0] = np.clip(frame[:, :, 0] * 1.1, 0, 255)  # Blue
            frame[:, :, 1] = np.clip(frame[:, :, 1] * 0.95, 0, 255)  # Green
            frame[:, :, 2] = np.clip(frame[:, :, 2] * 1.05, 0, 255)  # Red
            return frame.astype(np.uint8)
        
        elif lut_type == "warm":
            frame = frame.astype(np.float32)
            frame[:, :, 2] = np.clip(frame[:, :, 2] * 1.15, 0, 255)
            frame[:, :, 1] = np.clip(frame[:, :, 1] * 1.05, 0, 255)
            return frame.astype(np.uint8)
        
        elif lut_type == "cool":
            frame = frame.astype(np.float32)
            frame[:, :, 0] = np.clip(frame[:, :, 0] * 1.15, 0, 255)
            return frame.astype(np.uint8)
        
        return frame
    
    @staticmethod
    def enhance_contrast(frame: np.ndarray, strength: float = 1.2) -> np.ndarray:
        """Enhance contrast with S-curve"""
        lab = cv2.cvtColor(frame, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)
        
        # Apply S-curve to L channel
        l = l.astype(np.float32) / 255.0
        l = np.power(l, strength)
        l = (l * 255).astype(np.uint8)
        
        lab = cv2.merge([l, a, b])
        return cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)


class PerformanceOptimizer:
    """GPU acceleration and memory optimization"""
    
    @staticmethod
    def enable_gpu_acceleration() -> bool:
        """Check and enable GPU acceleration"""
        try:
            if cv2.cuda.getCudaEnabledDeviceCount() > 0:
                return True
        except:
            pass
        return False
    
    @staticmethod
    def optimize_frame_size(frame: np.ndarray, max_dimension: int = 1920) -> np.ndarray:
        """Resize frame for optimal processing"""
        h, w = frame.shape[:2]
        if max(h, w) > max_dimension:
            scale = max_dimension / max(h, w)
            new_w, new_h = int(w * scale), int(h * scale)
            return cv2.resize(frame, (new_w, new_h), interpolation=cv2.INTER_AREA)
        return frame
    
    @staticmethod
    def batch_process_frames(frames: List[np.ndarray], 
                            process_func, batch_size: int = 10) -> List[np.ndarray]:
        """Process frames in batches for memory efficiency"""
        results = []
        for i in range(0, len(frames), batch_size):
            batch = frames[i:i + batch_size]
            processed = [process_func(frame) for frame in batch]
            results.extend(processed)
        return results

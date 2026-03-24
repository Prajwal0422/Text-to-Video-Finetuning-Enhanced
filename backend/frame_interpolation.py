"""
Frame Interpolation
Create smooth slow motion and increase FPS
"""

import cv2
import numpy as np
from typing import Optional
import os

class FrameInterpolation:
    """Frame interpolation for smooth video"""
    
    def __init__(self):
        self.interpolation_methods = {
            'linear': 'Simple linear interpolation',
            'optical_flow': 'Optical flow based interpolation',
            'blend': 'Frame blending'
        }
    
    def interpolate_linear(
        self,
        frame1: np.ndarray,
        frame2: np.ndarray,
        alpha: float = 0.5
    ) -> np.ndarray:
        """Linear interpolation between two frames"""
        return cv2.addWeighted(frame1, 1 - alpha, frame2, alpha, 0)
    
    def interpolate_optical_flow(
        self,
        frame1: np.ndarray,
        frame2: np.ndarray,
        alpha: float = 0.5
    ) -> np.ndarray:
        """Optical flow based interpolation"""
        gray1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
        gray2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
        
        # Calculate optical flow
        flow = cv2.calcOpticalFlowFarneback(
            gray1, gray2, None,
            0.5, 3, 15, 3, 5, 1.2, 0
        )
        
        # Warp frame1 towards frame2
        h, w = frame1.shape[:2]
        flow_map = np.column_stack([
            (np.arange(w) + flow[:, :, 0] * alpha).ravel(),
            (np.arange(h).reshape(-1, 1) + flow[:, :, 1] * alpha).ravel()
        ])
        
        flow_map = flow_map.reshape(h, w, 2).astype(np.float32)
        
        warped = cv2.remap(
            frame1, flow_map, None,
            cv2.INTER_LINEAR
        )
        
        # Blend with frame2
        return cv2.addWeighted(warped, 1 - alpha, frame2, alpha, 0)
    
    def create_slow_motion(
        self,
        video_path: str,
        output_path: str,
        slow_factor: float = 2.0,
        method: str = 'linear'
    ) -> str:
        """
        Create slow motion video
        
        Args:
            video_path: Input video path
            output_path: Output video path
            slow_factor: Slow motion factor (2.0 = half speed)
            method: Interpolation method
        
        Returns:
            Path to output video
        """
        cap = cv2.VideoCapture(video_path)
        
        # Get video properties
        fps = cap.get(cv2.CAP_PROP_FPS)
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        
        # Create writer
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
        
        prev_frame = None
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            if prev_frame is not None:
                # Generate intermediate frames
                num_intermediate = int(slow_factor) - 1
                
                for i in range(num_intermediate + 1):
                    alpha = i / (num_intermediate + 1)
                    
                    if method == 'linear':
                        interp_frame = self.interpolate_linear(prev_frame, frame, alpha)
                    elif method == 'optical_flow':
                        interp_frame = self.interpolate_optical_flow(prev_frame, frame, alpha)
                    else:
                        interp_frame = self.interpolate_linear(prev_frame, frame, alpha)
                    
                    out.write(interp_frame)
            
            out.write(frame)
            prev_frame = frame
        
        cap.release()
        out.release()
        
        return output_path
    
    def increase_fps(
        self,
        video_path: str,
        output_path: str,
        target_fps: int = 60
    ) -> str:
        """Increase video FPS with interpolation"""
        cap = cv2.VideoCapture(video_path)
        
        original_fps = cap.get(cv2.CAP_PROP_FPS)
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        
        # Calculate interpolation factor
        factor = target_fps / original_fps
        
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(output_path, fourcc, target_fps, (width, height))
        
        prev_frame = None
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            if prev_frame is not None:
                # Generate intermediate frames
                num_intermediate = int(factor) - 1
                
                for i in range(1, num_intermediate + 1):
                    alpha = i / (num_intermediate + 1)
                    interp_frame = self.interpolate_linear(prev_frame, frame, alpha)
                    out.write(interp_frame)
            
            out.write(frame)
            prev_frame = frame
        
        cap.release()
        out.release()
        
        return output_path
    
    def create_time_lapse(
        self,
        video_path: str,
        output_path: str,
        speed_factor: float = 4.0
    ) -> str:
        """Create time-lapse (fast motion)"""
        cap = cv2.VideoCapture(video_path)
        
        fps = cap.get(cv2.CAP_PROP_FPS)
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
        
        frame_count = 0
        skip_frames = int(speed_factor)
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            if frame_count % skip_frames == 0:
                out.write(frame)
            
            frame_count += 1
        
        cap.release()
        out.release()
        
        return output_path


if __name__ == "__main__":
    interpolator = FrameInterpolation()
    print("Frame Interpolation System Ready")
    print("Available methods:", list(interpolator.interpolation_methods.keys()))

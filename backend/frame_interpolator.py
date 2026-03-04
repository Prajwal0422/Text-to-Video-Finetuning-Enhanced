"""
Frame Interpolation Module
High-quality frame interpolation using optical flow
"""

import cv2
import numpy as np
from typing import List


class FrameInterpolator:
    """Advanced frame interpolation engine"""
    
    def __init__(self, method: str = "optical_flow"):
        self.method = method
    
    def interpolate(self, frame1: np.ndarray, frame2: np.ndarray, 
                   num_frames: int = 1) -> List[np.ndarray]:
        """
        Interpolate frames between two frames
        
        Args:
            frame1: First frame
            frame2: Second frame
            num_frames: Number of intermediate frames to generate
            
        Returns:
            List of interpolated frames
        """
        if self.method == "optical_flow":
            return self._optical_flow_interpolation(frame1, frame2, num_frames)
        elif self.method == "linear":
            return self._linear_interpolation(frame1, frame2, num_frames)
        else:
            return self._optical_flow_interpolation(frame1, frame2, num_frames)
    
    def _optical_flow_interpolation(self, frame1: np.ndarray, frame2: np.ndarray,
                                   num_frames: int) -> List[np.ndarray]:
        """Optical flow based interpolation"""
        gray1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
        gray2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
        
        # Calculate optical flow
        flow = cv2.calcOpticalFlowFarneback(
            gray1, gray2, None,
            pyr_scale=0.5, levels=3, winsize=15,
            iterations=3, poly_n=5, poly_sigma=1.2, flags=0
        )
        
        interpolated = []
        h, w = frame1.shape[:2]
        
        for i in range(1, num_frames + 1):
            alpha = i / (num_frames + 1)
            
            # Create flow map
            flow_map = np.zeros((h, w, 2), dtype=np.float32)
            flow_map[:, :, 0] = np.arange(w)
            flow_map[:, :, 1] = np.arange(h).reshape(-1, 1)
            flow_map += flow * alpha
            
            # Warp frame1
            warped = cv2.remap(frame1, flow_map, None, cv2.INTER_LINEAR)
            
            # Blend with frame2
            blended = cv2.addWeighted(warped, 1 - alpha, frame2, alpha, 0)
            interpolated.append(blended)
        
        return interpolated
    
    def _linear_interpolation(self, frame1: np.ndarray, frame2: np.ndarray,
                             num_frames: int) -> List[np.ndarray]:
        """Simple linear interpolation"""
        interpolated = []
        
        for i in range(1, num_frames + 1):
            alpha = i / (num_frames + 1)
            blended = cv2.addWeighted(frame1, 1 - alpha, frame2, alpha, 0)
            interpolated.append(blended)
        
        return interpolated
    
    def batch_interpolate(self, frames: List[np.ndarray],
                         num_intermediate: int = 1) -> List[np.ndarray]:
        """Interpolate between all consecutive frame pairs"""
        result = [frames[0]]
        
        for i in range(len(frames) - 1):
            intermediate = self.interpolate(frames[i], frames[i + 1], num_intermediate)
            result.extend(intermediate)
            result.append(frames[i + 1])
        
        return result

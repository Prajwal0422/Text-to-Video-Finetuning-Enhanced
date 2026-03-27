"""
Video Stabilization
Stabilize shaky video footage
"""

import cv2
import numpy as np
from typing import List, Tuple
import os

class VideoStabilization:
    """Stabilize shaky videos"""
    
    def __init__(self):
        self.smoothing_radius = 30
    
    def stabilize_video(
        self,
        input_path: str,
        output_path: str,
        smoothing_radius: int = 30
    ) -> str:
        """
        Stabilize video using optical flow
        
        Args:
            input_path: Input video path
            output_path: Output video path
            smoothing_radius: Smoothing window size
        
        Returns:
            Path to stabilized video
        """
        cap = cv2.VideoCapture(input_path)
        
        # Get video properties
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        n_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        
        # Read first frame
        _, prev_frame = cap.read()
        prev_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)
        
        # Pre-define transformation-store array
        transforms = np.zeros((n_frames-1, 3), np.float32)
        
        print("Analyzing camera motion...")
        for i in range(n_frames-2):
            # Detect feature points
            prev_pts = cv2.goodFeaturesToTrack(
                prev_gray,
                maxCorners=200,
                qualityLevel=0.01,
                minDistance=30,
                blockSize=3
            )
            
            # Read next frame
            success, curr_frame = cap.read()
            if not success:
                break
            
            curr_gray = cv2.cvtColor(curr_frame, cv2.COLOR_BGR2GRAY)
            
            # Calculate optical flow
            curr_pts, status, err = cv2.calcOpticalFlowPyrLK(
                prev_gray, curr_gray, prev_pts, None
            )
            
            # Filter only valid points
            idx = np.where(status==1)[0]
            prev_pts = prev_pts[idx]
            curr_pts = curr_pts[idx]
            
            # Find transformation matrix
            m = cv2.estimateAffinePartial2D(prev_pts, curr_pts)[0]
            
            # Extract translation
            dx = m[0,2]
            dy = m[1,2]
            
            # Extract rotation angle
            da = np.arctan2(m[1,0], m[0,0])
            
            transforms[i] = [dx, dy, da]
            
            prev_gray = curr_gray
        
        # Compute trajectory
        trajectory = np.cumsum(transforms, axis=0)
        
        # Smooth trajectory
        smoothed_trajectory = self._smooth(trajectory, smoothing_radius)
        
        # Calculate difference
        difference = smoothed_trajectory - trajectory
        transforms_smooth = transforms + difference
        
        # Reset stream
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        
        # Write stabilized video
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
        
        print("Applying stabilization...")
        for i in range(n_frames-2):
            success, frame = cap.read()
            if not success:
                break
            
            # Extract transformations
            dx = transforms_smooth[i,0]
            dy = transforms_smooth[i,1]
            da = transforms_smooth[i,2]
            
            # Reconstruct transformation matrix
            m = np.zeros((2,3), np.float32)
            m[0,0] = np.cos(da)
            m[0,1] = -np.sin(da)
            m[1,0] = np.sin(da)
            m[1,1] = np.cos(da)
            m[0,2] = dx
            m[1,2] = dy
            
            # Apply transformation
            frame_stabilized = cv2.warpAffine(frame, m, (width, height))
            
            # Fix border artifacts
            frame_stabilized = self._fix_border(frame_stabilized)
            
            out.write(frame_stabilized)
        
        cap.release()
        out.release()
        
        print(f"✅ Stabilization complete: {output_path}")
        return output_path
    
    def _smooth(self, trajectory: np.ndarray, radius: int) -> np.ndarray:
        """Smooth trajectory using moving average"""
        smoothed = np.copy(trajectory)
        for i in range(3):
            smoothed[:,i] = self._moving_average(trajectory[:,i], radius)
        return smoothed
    
    def _moving_average(self, curve: np.ndarray, radius: int) -> np.ndarray:
        """Calculate moving average"""
        window_size = 2 * radius + 1
        f = np.ones(window_size) / window_size
        curve_pad = np.lib.pad(curve, (radius, radius), 'edge')
        curve_smoothed = np.convolve(curve_pad, f, mode='same')
        return curve_smoothed[radius:-radius]
    
    def _fix_border(self, frame: np.ndarray) -> np.ndarray:
        """Fix black borders by scaling"""
        h, w = frame.shape[:2]
        
        # Scale up slightly to remove borders
        scale = 1.04
        new_h, new_w = int(h * scale), int(w * scale)
        
        # Resize
        frame_scaled = cv2.resize(frame, (new_w, new_h))
        
        # Crop to original size
        start_h = (new_h - h) // 2
        start_w = (new_w - w) // 2
        
        return frame_scaled[start_h:start_h+h, start_w:start_w+w]


if __name__ == "__main__":
    stabilizer = VideoStabilization()
    print("Video Stabilization System Ready")

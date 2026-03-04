"""
Video Stabilization
Advanced stabilization using feature tracking
"""

import cv2
import numpy as np
from scipy.ndimage import gaussian_filter
from typing import List


class VideoStabilizer:
    """Video stabilization engine"""
    
    def __init__(self, smoothing_window: int = 30):
        self.smoothing_window = smoothing_window
    
    def stabilize(self, frames: List[np.ndarray]) -> List[np.ndarray]:
        """
        Stabilize video sequence
        
        Args:
            frames: List of video frames
            
        Returns:
            List of stabilized frames
        """
        if len(frames) < 2:
            return frames
        
        # Detect features and track motion
        transforms = self._calculate_transforms(frames)
        
        # Smooth transforms
        smoothed_transforms = self._smooth_transforms(transforms)
        
        # Apply stabilization
        stabilized = self._apply_transforms(frames, smoothed_transforms)
        
        return stabilized
    
    def _calculate_transforms(self, frames: List[np.ndarray]) -> List[np.ndarray]:
        """Calculate frame-to-frame transforms"""
        transforms = []
        
        # Convert first frame to grayscale
        prev_gray = cv2.cvtColor(frames[0], cv2.COLOR_BGR2GRAY)
        
        # Detect features in first frame
        prev_pts = cv2.goodFeaturesToTrack(
            prev_gray,
            maxCorners=200,
            qualityLevel=0.01,
            minDistance=30,
            blockSize=3
        )
        
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
                transform, _ = cv2.estimateAffinePartial2D(
                    prev_pts_valid, curr_pts_valid
                )
                
                if transform is not None:
                    transforms.append(transform)
                else:
                    # Use identity transform if estimation fails
                    transforms.append(np.eye(2, 3, dtype=np.float32))
            else:
                # Not enough points, use identity
                transforms.append(np.eye(2, 3, dtype=np.float32))
            
            # Update for next iteration
            prev_gray = curr_gray
            prev_pts = cv2.goodFeaturesToTrack(
                curr_gray,
                maxCorners=200,
                qualityLevel=0.01,
                minDistance=30,
                blockSize=3
            )
        
        return transforms
    
    def _smooth_transforms(self, transforms: List[np.ndarray]) -> List[np.ndarray]:
        """Smooth transforms using Gaussian filter"""
        if len(transforms) == 0:
            return transforms
        
        # Convert to trajectory
        trajectory = np.cumsum(transforms, axis=0)
        
        # Apply Gaussian smoothing
        smoothed_trajectory = gaussian_filter(
            trajectory,
            sigma=self.smoothing_window,
            axes=0,
            mode='nearest'
        )
        
        # Convert back to transforms
        smoothed_transforms = []
        for i in range(len(transforms)):
            if i == 0:
                smoothed_transforms.append(smoothed_trajectory[i])
            else:
                diff = smoothed_trajectory[i] - smoothed_trajectory[i-1]
                smoothed_transforms.append(diff)
        
        return smoothed_transforms
    
    def _apply_transforms(self, frames: List[np.ndarray],
                         transforms: List[np.ndarray]) -> List[np.ndarray]:
        """Apply smoothed transforms to frames"""
        stabilized = [frames[0]]  # First frame unchanged
        
        h, w = frames[0].shape[:2]
        
        for i, frame in enumerate(frames[1:]):
            if i < len(transforms):
                transform = transforms[i]
                
                # Apply transform
                stabilized_frame = cv2.warpAffine(
                    frame, transform, (w, h),
                    borderMode=cv2.BORDER_REFLECT
                )
                
                stabilized.append(stabilized_frame)
            else:
                stabilized.append(frame)
        
        return stabilized
    
    def analyze_stability(self, frames: List[np.ndarray]) -> dict:
        """
        Analyze video stability metrics
        
        Returns:
            Dictionary with stability metrics
        """
        if len(frames) < 2:
            return {"stable": True, "shake_score": 0.0}
        
        transforms = self._calculate_transforms(frames)
        
        # Calculate shake score (average transform magnitude)
        shake_scores = []
        for transform in transforms:
            # Extract translation
            dx = transform[0, 2]
            dy = transform[1, 2]
            magnitude = np.sqrt(dx**2 + dy**2)
            shake_scores.append(magnitude)
        
        avg_shake = np.mean(shake_scores)
        max_shake = np.max(shake_scores)
        
        return {
            "stable": avg_shake < 5.0,
            "shake_score": float(avg_shake),
            "max_shake": float(max_shake),
            "num_frames": len(frames)
        }

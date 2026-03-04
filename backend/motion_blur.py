"""
Motion Blur Effects
Realistic motion blur for cinematic feel
"""

import cv2
import numpy as np


class MotionBlur:
    """Motion blur effect generator"""
    
    @staticmethod
    def directional_blur(frame: np.ndarray, angle: float, 
                        strength: int = 15) -> np.ndarray:
        """
        Apply directional motion blur
        
        Args:
            frame: Input frame
            angle: Blur direction in degrees (0-360)
            strength: Blur strength (kernel size)
            
        Returns:
            Blurred frame
        """
        if strength == 0 or strength < 3:
            return frame
        
        # Ensure odd kernel size
        kernel_size = strength if strength % 2 == 1 else strength + 1
        
        # Create motion blur kernel
        kernel = np.zeros((kernel_size, kernel_size))
        center = kernel_size // 2
        angle_rad = np.deg2rad(angle)
        
        # Draw line in kernel
        for i in range(kernel_size):
            offset = i - center
            x = int(center + offset * np.cos(angle_rad))
            y = int(center + offset * np.sin(angle_rad))
            
            if 0 <= x < kernel_size and 0 <= y < kernel_size:
                kernel[y, x] = 1
        
        # Normalize kernel
        kernel = kernel / np.sum(kernel) if np.sum(kernel) > 0 else kernel
        
        # Apply blur
        return cv2.filter2D(frame, -1, kernel)
    
    @staticmethod
    def zoom_blur(frame: np.ndarray, strength: float = 0.02,
                 center: tuple = None) -> np.ndarray:
        """
        Apply radial zoom blur effect
        
        Args:
            frame: Input frame
            strength: Blur strength (0-1)
            center: Center point (x, y), None for image center
            
        Returns:
            Blurred frame
        """
        h, w = frame.shape[:2]
        
        if center is None:
            center = (w // 2, h // 2)
        
        result = np.zeros_like(frame, dtype=np.float32)
        num_samples = 10
        
        for i in range(num_samples):
            # Calculate scale for this sample
            scale = 1.0 + (i / num_samples) * strength
            
            # Calculate new dimensions
            new_h, new_w = int(h * scale), int(w * scale)
            
            # Resize frame
            scaled = cv2.resize(frame, (new_w, new_h))
            
            # Calculate crop coordinates to center on specified point
            y_start = int((new_h - h) / 2)
            x_start = int((new_w - w) / 2)
            
            # Ensure we don't go out of bounds
            y_start = max(0, min(y_start, new_h - h))
            x_start = max(0, min(x_start, new_w - w))
            
            # Crop to original size
            cropped = scaled[y_start:y_start+h, x_start:x_start+w]
            
            # Accumulate
            result += cropped.astype(np.float32)
        
        # Average all samples
        return (result / num_samples).astype(np.uint8)
    
    @staticmethod
    def radial_blur(frame: np.ndarray, strength: int = 10,
                   center: tuple = None) -> np.ndarray:
        """
        Apply radial motion blur (spinning effect)
        
        Args:
            frame: Input frame
            strength: Number of rotation samples
            center: Center point (x, y), None for image center
            
        Returns:
            Blurred frame
        """
        h, w = frame.shape[:2]
        
        if center is None:
            center = (w // 2, h // 2)
        
        result = np.zeros_like(frame, dtype=np.float32)
        
        # Sample multiple rotations
        for i in range(strength):
            angle = (i / strength) * 5  # Max 5 degrees rotation
            
            # Rotation matrix
            M = cv2.getRotationMatrix2D(center, angle, 1.0)
            
            # Rotate frame
            rotated = cv2.warpAffine(frame, M, (w, h))
            
            # Accumulate
            result += rotated.astype(np.float32)
        
        # Average all samples
        return (result / strength).astype(np.uint8)
    
    @staticmethod
    def apply_motion_blur_to_sequence(frames: list, motion_type: str,
                                     strength: int = 10) -> list:
        """
        Apply motion blur to entire frame sequence
        
        Args:
            frames: List of frames
            motion_type: Type of motion ('pan', 'zoom', 'rotate')
            strength: Blur strength
            
        Returns:
            List of blurred frames
        """
        blurred_frames = []
        
        for i, frame in enumerate(frames):
            if motion_type == 'pan':
                # Horizontal blur for panning
                angle = 0  # Horizontal
                blurred = MotionBlur.directional_blur(frame, angle, strength)
            
            elif motion_type == 'zoom':
                # Radial blur for zooming
                blur_strength = strength / 500.0  # Normalize
                blurred = MotionBlur.zoom_blur(frame, blur_strength)
            
            elif motion_type == 'rotate':
                # Radial blur for rotation
                blurred = MotionBlur.radial_blur(frame, strength)
            
            else:
                blurred = frame
            
            blurred_frames.append(blurred)
        
        return blurred_frames

"""
Color Grading Engine
Professional color correction and grading
"""

import cv2
import numpy as np


class ColorGrading:
    """Professional color grading tools"""
    
    @staticmethod
    def apply_lut(frame: np.ndarray, lut_type: str = "cinematic") -> np.ndarray:
        """
        Apply color lookup table
        
        Args:
            frame: Input frame
            lut_type: LUT type ('cinematic', 'warm', 'cool', 'vintage')
            
        Returns:
            Graded frame
        """
        frame_float = frame.astype(np.float32)
        
        if lut_type == "cinematic":
            # Teal and orange Hollywood look
            frame_float[:, :, 0] = np.clip(frame_float[:, :, 0] * 1.1, 0, 255)  # Blue
            frame_float[:, :, 1] = np.clip(frame_float[:, :, 1] * 0.95, 0, 255)  # Green
            frame_float[:, :, 2] = np.clip(frame_float[:, :, 2] * 1.05, 0, 255)  # Red
        
        elif lut_type == "warm":
            # Warm sunset look
            frame_float[:, :, 0] = np.clip(frame_float[:, :, 0] * 0.9, 0, 255)  # Less blue
            frame_float[:, :, 1] = np.clip(frame_float[:, :, 1] * 1.05, 0, 255)  # More green
            frame_float[:, :, 2] = np.clip(frame_float[:, :, 2] * 1.15, 0, 255)  # More red
        
        elif lut_type == "cool":
            # Cool blue look
            frame_float[:, :, 0] = np.clip(frame_float[:, :, 0] * 1.15, 0, 255)  # More blue
            frame_float[:, :, 1] = np.clip(frame_float[:, :, 1] * 1.05, 0, 255)  # Slight green
            frame_float[:, :, 2] = np.clip(frame_float[:, :, 2] * 0.95, 0, 255)  # Less red
        
        elif lut_type == "vintage":
            # Vintage film look
            frame_float[:, :, 0] = np.clip(frame_float[:, :, 0] * 0.95, 0, 255)
            frame_float[:, :, 1] = np.clip(frame_float[:, :, 1] * 1.1, 0, 255)
            frame_float[:, :, 2] = np.clip(frame_float[:, :, 2] * 1.05, 0, 255)
        
        return frame_float.astype(np.uint8)
    
    @staticmethod
    def enhance_contrast(frame: np.ndarray, strength: float = 1.2) -> np.ndarray:
        """
        Enhance contrast using S-curve
        
        Args:
            frame: Input frame
            strength: Contrast strength (1.0 = no change)
            
        Returns:
            Contrast-enhanced frame
        """
        # Convert to LAB color space
        lab = cv2.cvtColor(frame, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)
        
        # Apply S-curve to L channel
        l_float = l.astype(np.float32) / 255.0
        l_curved = np.power(l_float, strength)
        l_curved = (l_curved * 255).astype(np.uint8)
        
        # Merge back
        lab = cv2.merge([l_curved, a, b])
        return cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)
    
    @staticmethod
    def adjust_saturation(frame: np.ndarray, factor: float = 1.2) -> np.ndarray:
        """
        Adjust color saturation
        
        Args:
            frame: Input frame
            factor: Saturation factor (1.0 = no change, >1 = more saturated)
            
        Returns:
            Saturation-adjusted frame
        """
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV).astype(np.float32)
        hsv[:, :, 1] = np.clip(hsv[:, :, 1] * factor, 0, 255)
        return cv2.cvtColor(hsv.astype(np.uint8), cv2.COLOR_HSV2BGR)
    
    @staticmethod
    def color_temperature(frame: np.ndarray, temperature: int) -> np.ndarray:
        """
        Adjust color temperature
        
        Args:
            frame: Input frame
            temperature: Temperature shift (-100 to 100, negative=cooler, positive=warmer)
            
        Returns:
            Temperature-adjusted frame
        """
        frame_float = frame.astype(np.float32)
        
        if temperature > 0:  # Warmer
            factor = temperature / 100.0
            frame_float[:, :, 2] *= (1 + factor * 0.3)  # More red
            frame_float[:, :, 0] *= (1 - factor * 0.2)  # Less blue
        else:  # Cooler
            factor = -temperature / 100.0
            frame_float[:, :, 0] *= (1 + factor * 0.3)  # More blue
            frame_float[:, :, 2] *= (1 - factor * 0.2)  # Less red
        
        return np.clip(frame_float, 0, 255).astype(np.uint8)
    
    @staticmethod
    def vignette(frame: np.ndarray, intensity: float = 0.5) -> np.ndarray:
        """
        Add vignette effect
        
        Args:
            frame: Input frame
            intensity: Vignette intensity (0-1)
            
        Returns:
            Frame with vignette
        """
        h, w = frame.shape[:2]
        
        # Create radial gradient
        y, x = np.ogrid[:h, :w]
        center_y, center_x = h // 2, w // 2
        
        # Calculate distance from center
        dist = np.sqrt((x - center_x)**2 + (y - center_y)**2)
        max_dist = np.sqrt(center_x**2 + center_y**2)
        
        # Create vignette mask
        vignette_mask = 1 - (dist / max_dist) * intensity
        vignette_mask = np.clip(vignette_mask, 0, 1)
        
        # Apply to each channel
        result = frame.astype(np.float32)
        for i in range(3):
            result[:, :, i] *= vignette_mask
        
        return result.astype(np.uint8)
    
    @staticmethod
    def teal_orange_grade(frame: np.ndarray, strength: float = 0.5) -> np.ndarray:
        """
        Apply Hollywood teal and orange color grade
        
        Args:
            frame: Input frame
            strength: Effect strength (0-1)
            
        Returns:
            Graded frame
        """
        # Convert to LAB
        lab = cv2.cvtColor(frame, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)
        
        # Push colors toward teal/orange
        a_float = a.astype(np.float32)
        b_float = b.astype(np.float32)
        
        # Shift a channel (green-red axis)
        a_float = a_float + (128 - a_float) * strength * 0.3
        
        # Shift b channel (blue-yellow axis)
        b_float = b_float + (b_float - 128) * strength * 0.5
        
        a_adjusted = np.clip(a_float, 0, 255).astype(np.uint8)
        b_adjusted = np.clip(b_float, 0, 255).astype(np.uint8)
        
        # Merge back
        lab = cv2.merge([l, a_adjusted, b_adjusted])
        return cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)

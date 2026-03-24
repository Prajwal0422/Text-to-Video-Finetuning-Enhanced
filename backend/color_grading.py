"""
Color Grading System
Professional color grading and LUT application
"""

import cv2
import numpy as np
from typing import Optional, Tuple
import os

class ColorGrading:
    """Professional color grading tools"""
    
    # Predefined color grades
    PRESETS = {
        'cinematic': {
            'shadows': (-10, -5, 5),
            'midtones': (0, 0, 0),
            'highlights': (10, 5, -5),
            'saturation': 1.1
        },
        'warm': {
            'shadows': (5, 0, -10),
            'midtones': (10, 5, -5),
            'highlights': (15, 10, 0),
            'saturation': 1.2
        },
        'cool': {
            'shadows': (-10, -5, 10),
            'midtones': (-5, 0, 10),
            'highlights': (0, 5, 15),
            'saturation': 1.1
        },
        'vintage': {
            'shadows': (10, 5, 0),
            'midtones': (15, 10, 5),
            'highlights': (20, 15, 10),
            'saturation': 0.8
        },
        'dramatic': {
            'shadows': (-20, -10, 0),
            'midtones': (0, 0, 0),
            'highlights': (20, 10, 0),
            'saturation': 1.3
        }
    }
    
    def __init__(self):
        self.lut_dir = "luts"
        os.makedirs(self.lut_dir, exist_ok=True)
    
    def apply_color_grade(
        self,
        frame: np.ndarray,
        preset: str = 'cinematic'
    ) -> np.ndarray:
        """Apply color grade preset"""
        if preset not in self.PRESETS:
            raise ValueError(f"Unknown preset: {preset}")
        
        grade = self.PRESETS[preset]
        
        # Convert to float for processing
        img = frame.astype(np.float32) / 255.0
        
        # Split into RGB channels
        b, g, r = cv2.split(img)
        
        # Apply shadow adjustments (dark areas)
        shadow_mask = self._create_luminance_mask(img, 0, 0.3)
        b += shadow_mask * grade['shadows'][0] / 255.0
        g += shadow_mask * grade['shadows'][1] / 255.0
        r += shadow_mask * grade['shadows'][2] / 255.0
        
        # Apply midtone adjustments
        midtone_mask = self._create_luminance_mask(img, 0.3, 0.7)
        b += midtone_mask * grade['midtones'][0] / 255.0
        g += midtone_mask * grade['midtones'][1] / 255.0
        r += midtone_mask * grade['midtones'][2] / 255.0
        
        # Apply highlight adjustments (bright areas)
        highlight_mask = self._create_luminance_mask(img, 0.7, 1.0)
        b += highlight_mask * grade['highlights'][0] / 255.0
        g += highlight_mask * grade['highlights'][1] / 255.0
        r += highlight_mask * grade['highlights'][2] / 255.0
        
        # Merge channels
        img = cv2.merge([b, g, r])
        
        # Adjust saturation
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        hsv[:, :, 1] *= grade['saturation']
        img = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
        
        # Clip and convert back
        img = np.clip(img, 0, 1)
        return (img * 255).astype(np.uint8)
    
    def _create_luminance_mask(
        self,
        img: np.ndarray,
        min_val: float,
        max_val: float
    ) -> np.ndarray:
        """Create luminance-based mask"""
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        mask = np.zeros_like(gray)
        mask[(gray >= min_val) & (gray <= max_val)] = 1.0
        
        # Smooth mask
        mask = cv2.GaussianBlur(mask, (21, 21), 0)
        
        return mask
    
    def adjust_temperature(
        self,
        frame: np.ndarray,
        temperature: int = 0
    ) -> np.ndarray:
        """
        Adjust color temperature
        Negative = cooler (blue), Positive = warmer (orange)
        """
        img = frame.astype(np.float32)
        
        if temperature > 0:
            # Warmer
            img[:, :, 2] += temperature  # More red
            img[:, :, 0] -= temperature * 0.5  # Less blue
        else:
            # Cooler
            img[:, :, 0] -= temperature  # More blue
            img[:, :, 2] += temperature * 0.5  # Less red
        
        return np.clip(img, 0, 255).astype(np.uint8)
    
    def adjust_tint(
        self,
        frame: np.ndarray,
        tint: int = 0
    ) -> np.ndarray:
        """
        Adjust green/magenta tint
        Negative = magenta, Positive = green
        """
        img = frame.astype(np.float32)
        
        if tint > 0:
            # More green
            img[:, :, 1] += tint
        else:
            # More magenta (less green, more red+blue)
            img[:, :, 1] += tint
            img[:, :, 0] -= tint * 0.5
            img[:, :, 2] -= tint * 0.5
        
        return np.clip(img, 0, 255).astype(np.uint8)
    
    def apply_lut(
        self,
        frame: np.ndarray,
        lut_path: str
    ) -> np.ndarray:
        """Apply 3D LUT (Look-Up Table)"""
        # Placeholder for LUT application
        # Would require actual LUT file parsing
        return frame
    
    def create_custom_grade(
        self,
        shadows: Tuple[int, int, int] = (0, 0, 0),
        midtones: Tuple[int, int, int] = (0, 0, 0),
        highlights: Tuple[int, int, int] = (0, 0, 0),
        saturation: float = 1.0
    ) -> dict:
        """Create custom color grade"""
        return {
            'shadows': shadows,
            'midtones': midtones,
            'highlights': highlights,
            'saturation': saturation
        }
    
    def get_available_presets(self) -> list:
        """Get list of available presets"""
        return list(self.PRESETS.keys())


if __name__ == "__main__":
    grading = ColorGrading()
    
    print("Available Color Grades:")
    for preset in grading.get_available_presets():
        print(f"  - {preset}")

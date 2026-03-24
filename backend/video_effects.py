"""
Video Effects
Advanced video effects and filters
"""

import cv2
import numpy as np
from typing import Optional, Dict
from moviepy import VideoFileClip

class VideoEffects:
    """Apply various effects to videos"""
    
    def __init__(self):
        self.effects = {
            'blur': 'Gaussian blur effect',
            'sharpen': 'Sharpen video',
            'grayscale': 'Convert to black and white',
            'sepia': 'Vintage sepia tone',
            'vignette': 'Dark edges effect',
            'brightness': 'Adjust brightness',
            'contrast': 'Adjust contrast',
            'saturation': 'Adjust color saturation'
        }
    
    def apply_blur(self, frame: np.ndarray, strength: int = 15) -> np.ndarray:
        """Apply Gaussian blur"""
        return cv2.GaussianBlur(frame, (strength, strength), 0)
    
    def apply_sharpen(self, frame: np.ndarray) -> np.ndarray:
        """Sharpen image"""
        kernel = np.array([[-1,-1,-1],
                          [-1, 9,-1],
                          [-1,-1,-1]])
        return cv2.filter2D(frame, -1, kernel)
    
    def apply_grayscale(self, frame: np.ndarray) -> np.ndarray:
        """Convert to grayscale"""
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        return cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
    
    def apply_sepia(self, frame: np.ndarray) -> np.ndarray:
        """Apply sepia tone"""
        kernel = np.array([[0.272, 0.534, 0.131],
                          [0.349, 0.686, 0.168],
                          [0.393, 0.769, 0.189]])
        return cv2.transform(frame, kernel)
    
    def apply_vignette(self, frame: np.ndarray, strength: float = 0.5) -> np.ndarray:
        """Apply vignette effect"""
        rows, cols = frame.shape[:2]
        
        # Create radial gradient
        X = np.linspace(-1, 1, cols)
        Y = np.linspace(-1, 1, rows)
        X, Y = np.meshgrid(X, Y)
        
        radius = np.sqrt(X**2 + Y**2)
        mask = 1 - np.clip(radius * strength, 0, 1)
        mask = np.dstack([mask] * 3)
        
        return (frame * mask).astype(np.uint8)
    
    def adjust_brightness(self, frame: np.ndarray, value: int = 30) -> np.ndarray:
        """Adjust brightness"""
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        h, s, v = cv2.split(hsv)
        
        v = cv2.add(v, value)
        v = np.clip(v, 0, 255)
        
        final_hsv = cv2.merge((h, s, v))
        return cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)
    
    def adjust_contrast(self, frame: np.ndarray, alpha: float = 1.5) -> np.ndarray:
        """Adjust contrast"""
        return cv2.convertScaleAbs(frame, alpha=alpha, beta=0)
    
    def adjust_saturation(self, frame: np.ndarray, value: int = 30) -> np.ndarray:
        """Adjust color saturation"""
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        h, s, v = cv2.split(hsv)
        
        s = cv2.add(s, value)
        s = np.clip(s, 0, 255)
        
        final_hsv = cv2.merge((h, s, v))
        return cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)
    
    def apply_effect(
        self,
        video_path: str,
        effect_name: str,
        output_path: str,
        **kwargs
    ) -> str:
        """Apply effect to entire video"""
        clip = VideoFileClip(video_path)
        
        effect_map = {
            'blur': lambda f: self.apply_blur(f, kwargs.get('strength', 15)),
            'sharpen': self.apply_sharpen,
            'grayscale': self.apply_grayscale,
            'sepia': self.apply_sepia,
            'vignette': lambda f: self.apply_vignette(f, kwargs.get('strength', 0.5)),
            'brightness': lambda f: self.adjust_brightness(f, kwargs.get('value', 30)),
            'contrast': lambda f: self.adjust_contrast(f, kwargs.get('alpha', 1.5)),
            'saturation': lambda f: self.adjust_saturation(f, kwargs.get('value', 30))
        }
        
        if effect_name not in effect_map:
            raise ValueError(f"Unknown effect: {effect_name}")
        
        effect_func = effect_map[effect_name]
        processed_clip = clip.fl_image(effect_func)
        
        processed_clip.write_videofile(output_path, codec='libx264')
        
        clip.close()
        processed_clip.close()
        
        return output_path
    
    def get_available_effects(self) -> Dict[str, str]:
        """Get list of available effects"""
        return self.effects


if __name__ == "__main__":
    effects = VideoEffects()
    print("Available Effects:")
    for name, desc in effects.get_available_effects().items():
        print(f"  - {name}: {desc}")

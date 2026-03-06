"""
Professional Video Effects Library
Cinematic transitions, filters, and visual enhancements
"""

import cv2
import numpy as np
from typing import List, Tuple

try:
    from .advanced_video_algorithms import EasingFunctions
except ImportError:
    from advanced_video_algorithms import EasingFunctions


class TransitionEffects:
    """Professional transition effects between clips"""
    
    @staticmethod
    def crossfade(frame1: np.ndarray, frame2: np.ndarray, 
                  progress: float) -> np.ndarray:
        """Smooth crossfade transition"""
        alpha = EasingFunctions.ease_in_out_cubic(progress)
        return cv2.addWeighted(frame1, 1 - alpha, frame2, alpha, 0)
    
    @staticmethod
    def slide_left(frame1: np.ndarray, frame2: np.ndarray,
                   progress: float) -> np.ndarray:
        """Slide transition from right to left"""
        h, w = frame1.shape[:2]
        offset = int(w * EasingFunctions.ease_in_out_quint(progress))
        
        result = np.zeros_like(frame1)
        
        # Frame1 slides out
        if offset < w:
            result[:, :w-offset] = frame1[:, offset:]
        
        # Frame2 slides in
        if offset > 0:
            result[:, w-offset:] = frame2[:, :offset]
        
        return result
    
    @staticmethod
    def zoom_transition(frame1: np.ndarray, frame2: np.ndarray,
                       progress: float) -> np.ndarray:
        """Zoom out from frame1, zoom in to frame2"""
        h, w = frame1.shape[:2]
        
        if progress < 0.5:
            # Zoom out from frame1
            t = progress * 2
            scale = 1.0 + t * 0.5
            alpha = 1.0 - t
        else:
            # Zoom in to frame2
            t = (progress - 0.5) * 2
            scale = 1.5 - t * 0.5
            alpha = t
            frame1 = frame2
        
        # Apply zoom
        new_h, new_w = int(h * scale), int(w * scale)
        zoomed = cv2.resize(frame1, (new_w, new_h))
        
        # Center crop
        y = (new_h - h) // 2
        x = (new_w - w) // 2
        cropped = zoomed[y:y+h, x:x+w]
        
        # Fade
        result = (cropped * alpha).astype(np.uint8)
        if progress >= 0.5:
            result = cv2.addWeighted(result, 1, frame2, 1 - alpha, 0)
        
        return result
    
    @staticmethod
    def wipe_down(frame1: np.ndarray, frame2: np.ndarray,
                  progress: float) -> np.ndarray:
        """Wipe transition from top to bottom"""
        h = frame1.shape[0]
        split = int(h * EasingFunctions.ease_in_out_cubic(progress))
        
        result = frame1.copy()
        result[split:] = frame2[split:]
        
        return result
    
    @staticmethod
    def blur_transition(frame1: np.ndarray, frame2: np.ndarray,
                       progress: float) -> np.ndarray:
        """Blur out and blur in transition"""
        if progress < 0.5:
            t = progress * 2
            blur_amount = int(t * 20) * 2 + 1
            blurred = cv2.GaussianBlur(frame1, (blur_amount, blur_amount), 0)
            return cv2.addWeighted(frame1, 1 - t, blurred, t, 0)
        else:
            t = (progress - 0.5) * 2
            blur_amount = int((1 - t) * 20) * 2 + 1
            blurred = cv2.GaussianBlur(frame2, (blur_amount, blur_amount), 0)
            return cv2.addWeighted(blurred, 1 - t, frame2, t, 0)


class CinematicEffects:
    """Cinematic visual effects"""
    
    @staticmethod
    def add_letterbox(frame: np.ndarray, ratio: float = 2.39) -> np.ndarray:
        """Add cinematic letterbox bars"""
        h, w = frame.shape[:2]
        target_h = int(w / ratio)
        bar_h = (h - target_h) // 2
        
        result = frame.copy()
        result[:bar_h] = 0
        result[h-bar_h:] = 0
        
        return result
    
    @staticmethod
    def add_vignette(frame: np.ndarray, strength: float = 0.5) -> np.ndarray:
        """Add vignette effect"""
        h, w = frame.shape[:2]
        
        # Create radial gradient
        y, x = np.ogrid[:h, :w]
        center_y, center_x = h // 2, w // 2
        
        # Calculate distance from center
        dist = np.sqrt((x - center_x)**2 + (y - center_y)**2)
        max_dist = np.sqrt(center_x**2 + center_y**2)
        
        # Create vignette mask
        vignette = 1 - (dist / max_dist) * strength
        vignette = np.clip(vignette, 0, 1)
        
        # Apply to each channel
        result = frame.copy().astype(np.float32)
        for i in range(3):
            result[:, :, i] *= vignette
        
        return result.astype(np.uint8)
    
    @staticmethod
    def add_film_grain(frame: np.ndarray, intensity: float = 0.05) -> np.ndarray:
        """Add film grain texture"""
        noise = np.random.normal(0, intensity * 255, frame.shape).astype(np.float32)
        result = frame.astype(np.float32) + noise
        return np.clip(result, 0, 255).astype(np.uint8)
    
    @staticmethod
    def chromatic_aberration(frame: np.ndarray, strength: int = 2) -> np.ndarray:
        """Add chromatic aberration effect"""
        b, g, r = cv2.split(frame)
        
        # Shift red channel
        M_r = np.float32([[1, 0, strength], [0, 1, 0]])
        r = cv2.warpAffine(r, M_r, (frame.shape[1], frame.shape[0]))
        
        # Shift blue channel
        M_b = np.float32([[1, 0, -strength], [0, 1, 0]])
        b = cv2.warpAffine(b, M_b, (frame.shape[1], frame.shape[0]))
        
        return cv2.merge([b, g, r])
    
    @staticmethod
    def lens_distortion(frame: np.ndarray, strength: float = 0.1) -> np.ndarray:
        """Add lens distortion effect"""
        h, w = frame.shape[:2]
        
        # Camera matrix
        camera_matrix = np.array([[w, 0, w/2],
                                 [0, h, h/2],
                                 [0, 0, 1]], dtype=np.float32)
        
        # Distortion coefficients
        dist_coeffs = np.array([strength, 0, 0, 0], dtype=np.float32)
        
        # Apply distortion
        result = cv2.undistort(frame, camera_matrix, dist_coeffs)
        return result


class MotionEffects:
    """Dynamic motion effects"""
    
    @staticmethod
    def ken_burns_effect(frame: np.ndarray, progress: float,
                        zoom_in: bool = True) -> np.ndarray:
        """Ken Burns pan and zoom effect"""
        h, w = frame.shape[:2]
        
        # Eased progress
        t = EasingFunctions.ease_in_out_cubic(progress)
        
        if zoom_in:
            scale = 1.0 + t * 0.2
            pan_x = t * 0.1
            pan_y = t * 0.05
        else:
            scale = 1.2 - t * 0.2
            pan_x = (1 - t) * 0.1
            pan_y = (1 - t) * 0.05
        
        # Create transformation matrix
        center_x, center_y = w // 2, h // 2
        M = cv2.getRotationMatrix2D((center_x, center_y), 0, scale)
        M[0, 2] += pan_x * w
        M[1, 2] += pan_y * h
        
        result = cv2.warpAffine(frame, M, (w, h))
        return result
    
    @staticmethod
    def parallax_effect(foreground: np.ndarray, background: np.ndarray,
                       progress: float, depth: float = 0.5) -> np.ndarray:
        """Parallax scrolling effect"""
        h, w = foreground.shape[:2]
        
        # Different speeds for layers
        bg_offset = int(progress * w * depth)
        fg_offset = int(progress * w)
        
        # Shift layers
        bg_shifted = np.roll(background, bg_offset, axis=1)
        fg_shifted = np.roll(foreground, fg_offset, axis=1)
        
        # Blend with alpha
        result = cv2.addWeighted(bg_shifted, 0.6, fg_shifted, 0.4, 0)
        return result
    
    @staticmethod
    def dolly_zoom(frame: np.ndarray, progress: float) -> np.ndarray:
        """Dolly zoom (Vertigo) effect"""
        h, w = frame.shape[:2]
        
        # Zoom changes while maintaining subject size
        t = EasingFunctions.ease_in_out_cubic(progress)
        zoom = 1.0 + t * 0.3
        
        # Zoom in
        new_h, new_w = int(h * zoom), int(w * zoom)
        zoomed = cv2.resize(frame, (new_w, new_h))
        
        # Crop to maintain center
        y = (new_h - h) // 2
        x = (new_w - w) // 2
        result = zoomed[y:y+h, x:x+w]
        
        return result


class ColorEffects:
    """Color grading and correction effects"""
    
    @staticmethod
    def color_temperature(frame: np.ndarray, temperature: int) -> np.ndarray:
        """Adjust color temperature (-100 to 100)"""
        result = frame.copy().astype(np.float32)
        
        if temperature > 0:  # Warmer
            result[:, :, 2] *= (1 + temperature / 100 * 0.3)  # More red
            result[:, :, 0] *= (1 - temperature / 100 * 0.2)  # Less blue
        else:  # Cooler
            result[:, :, 0] *= (1 - temperature / 100 * 0.3)  # More blue
            result[:, :, 2] *= (1 + temperature / 100 * 0.2)  # Less red
        
        return np.clip(result, 0, 255).astype(np.uint8)
    
    @staticmethod
    def teal_orange_grade(frame: np.ndarray, strength: float = 0.5) -> np.ndarray:
        """Hollywood teal and orange color grade"""
        # Convert to LAB
        lab = cv2.cvtColor(frame, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)
        
        # Push colors toward teal/orange
        a = a.astype(np.float32)
        b = b.astype(np.float32)
        
        a = a + (128 - a) * strength * 0.3
        b = b + (b - 128) * strength * 0.5
        
        a = np.clip(a, 0, 255).astype(np.uint8)
        b = np.clip(b, 0, 255).astype(np.uint8)
        
        lab = cv2.merge([l, a, b])
        return cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)
    
    @staticmethod
    def bleach_bypass(frame: np.ndarray, strength: float = 0.5) -> np.ndarray:
        """Bleach bypass effect"""
        # Desaturate
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray_3ch = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
        
        # Blend with original
        result = cv2.addWeighted(frame, 1 - strength, gray_3ch, strength, 0)
        
        # Increase contrast
        result = cv2.convertScaleAbs(result, alpha=1.2, beta=-20)
        
        return result
    
    @staticmethod
    def split_tone(frame: np.ndarray, 
                   shadow_color: Tuple[int, int, int],
                   highlight_color: Tuple[int, int, int],
                   strength: float = 0.3) -> np.ndarray:
        """Split toning effect"""
        # Create luminance mask
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Shadow and highlight masks
        shadow_mask = (255 - gray) / 255.0
        highlight_mask = gray / 255.0
        
        result = frame.copy().astype(np.float32)
        
        # Apply colors
        for i in range(3):
            result[:, :, i] += shadow_color[i] * shadow_mask * strength
            result[:, :, i] += highlight_color[i] * highlight_mask * strength
        
        return np.clip(result, 0, 255).astype(np.uint8)


class TextOverlay:
    """Text and title effects"""
    
    @staticmethod
    def add_title(frame: np.ndarray, text: str, 
                  position: str = "center",
                  font_scale: float = 2.0,
                  color: Tuple[int, int, int] = (255, 255, 255)) -> np.ndarray:
        """Add text title to frame"""
        result = frame.copy()
        font = cv2.FONT_HERSHEY_SIMPLEX
        thickness = 3
        
        # Get text size
        (text_w, text_h), baseline = cv2.getTextSize(
            text, font, font_scale, thickness
        )
        
        h, w = frame.shape[:2]
        
        # Calculate position
        if position == "center":
            x = (w - text_w) // 2
            y = (h + text_h) // 2
        elif position == "top":
            x = (w - text_w) // 2
            y = text_h + 50
        elif position == "bottom":
            x = (w - text_w) // 2
            y = h - 50
        
        # Add shadow
        cv2.putText(result, text, (x + 2, y + 2), font, font_scale,
                   (0, 0, 0), thickness + 2, cv2.LINE_AA)
        
        # Add text
        cv2.putText(result, text, (x, y), font, font_scale,
                   color, thickness, cv2.LINE_AA)
        
        return result
    
    @staticmethod
    def animated_title(frame: np.ndarray, text: str, progress: float) -> np.ndarray:
        """Animated title with fade in"""
        alpha = EasingFunctions.ease_out_expo(min(progress * 2, 1.0))
        
        # Create title
        titled = TextOverlay.add_title(frame, text)
        
        # Fade in
        result = cv2.addWeighted(frame, 1 - alpha, titled, alpha, 0)
        return result

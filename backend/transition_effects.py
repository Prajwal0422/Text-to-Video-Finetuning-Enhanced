"""
Transition Effects
Professional transitions between video clips
"""

import cv2
import numpy as np
from .advanced_video_algorithms import EasingFunctions


class TransitionEffects:
    """Professional video transition effects"""
    
    @staticmethod
    def crossfade(frame1: np.ndarray, frame2: np.ndarray,
                 progress: float, easing: str = "cubic") -> np.ndarray:
        """
        Smooth crossfade transition
        
        Args:
            frame1: First frame
            frame2: Second frame
            progress: Transition progress (0-1)
            easing: Easing function name
            
        Returns:
            Blended frame
        """
        # Apply easing
        if easing == "cubic":
            alpha = EasingFunctions.ease_in_out_cubic(progress)
        elif easing == "sine":
            alpha = EasingFunctions.ease_in_out_sine(progress)
        else:
            alpha = progress
        
        return cv2.addWeighted(frame1, 1 - alpha, frame2, alpha, 0)
    
    @staticmethod
    def slide(frame1: np.ndarray, frame2: np.ndarray,
             progress: float, direction: str = "left") -> np.ndarray:
        """
        Slide transition
        
        Args:
            frame1: First frame
            frame2: Second frame
            progress: Transition progress (0-1)
            direction: Slide direction ('left', 'right', 'up', 'down')
            
        Returns:
            Transitioned frame
        """
        h, w = frame1.shape[:2]
        eased = EasingFunctions.ease_in_out_quint(progress)
        
        result = np.zeros_like(frame1)
        
        if direction == "left":
            offset = int(w * eased)
            if offset < w:
                result[:, :w-offset] = frame1[:, offset:]
            if offset > 0:
                result[:, w-offset:] = frame2[:, :offset]
        
        elif direction == "right":
            offset = int(w * eased)
            if offset < w:
                result[:, offset:] = frame1[:, :w-offset]
            if offset > 0:
                result[:, :offset] = frame2[:, w-offset:]
        
        elif direction == "up":
            offset = int(h * eased)
            if offset < h:
                result[:h-offset, :] = frame1[offset:, :]
            if offset > 0:
                result[h-offset:, :] = frame2[:offset, :]
        
        elif direction == "down":
            offset = int(h * eased)
            if offset < h:
                result[offset:, :] = frame1[:h-offset, :]
            if offset > 0:
                result[:offset, :] = frame2[h-offset:, :]
        
        return result
    
    @staticmethod
    def wipe(frame1: np.ndarray, frame2: np.ndarray,
            progress: float, direction: str = "horizontal") -> np.ndarray:
        """
        Wipe transition
        
        Args:
            frame1: First frame
            frame2: Second frame
            progress: Transition progress (0-1)
            direction: Wipe direction ('horizontal', 'vertical')
            
        Returns:
            Transitioned frame
        """
        h, w = frame1.shape[:2]
        eased = EasingFunctions.ease_in_out_cubic(progress)
        
        result = frame1.copy()
        
        if direction == "horizontal":
            split = int(w * eased)
            result[:, split:] = frame2[:, split:]
        else:  # vertical
            split = int(h * eased)
            result[split:, :] = frame2[split:, :]
        
        return result
    
    @staticmethod
    def zoom_transition(frame1: np.ndarray, frame2: np.ndarray,
                       progress: float) -> np.ndarray:
        """
        Zoom transition (zoom out from frame1, zoom in to frame2)
        
        Args:
            frame1: First frame
            frame2: Second frame
            progress: Transition progress (0-1)
            
        Returns:
            Transitioned frame
        """
        h, w = frame1.shape[:2]
        
        if progress < 0.5:
            # Zoom out from frame1
            t = progress * 2
            scale = 1.0 + t * 0.5
            alpha = 1.0 - t
            current_frame = frame1
        else:
            # Zoom in to frame2
            t = (progress - 0.5) * 2
            scale = 1.5 - t * 0.5
            alpha = t
            current_frame = frame2
        
        # Apply zoom
        new_h, new_w = int(h * scale), int(w * scale)
        zoomed = cv2.resize(current_frame, (new_w, new_h))
        
        # Center crop
        y = (new_h - h) // 2
        x = (new_w - w) // 2
        cropped = zoomed[y:y+h, x:x+w]
        
        # Fade
        if progress < 0.5:
            result = (cropped * alpha).astype(np.uint8)
        else:
            black = np.zeros_like(frame2)
            result = cv2.addWeighted(black, 1 - alpha, cropped, alpha, 0)
        
        return result
    
    @staticmethod
    def blur_transition(frame1: np.ndarray, frame2: np.ndarray,
                       progress: float) -> np.ndarray:
        """
        Blur transition (blur out and blur in)
        
        Args:
            frame1: First frame
            frame2: Second frame
            progress: Transition progress (0-1)
            
        Returns:
            Transitioned frame
        """
        if progress < 0.5:
            # Blur out frame1
            t = progress * 2
            blur_amount = int(t * 20) * 2 + 1
            blurred = cv2.GaussianBlur(frame1, (blur_amount, blur_amount), 0)
            return cv2.addWeighted(frame1, 1 - t, blurred, t, 0)
        else:
            # Blur in frame2
            t = (progress - 0.5) * 2
            blur_amount = int((1 - t) * 20) * 2 + 1
            blurred = cv2.GaussianBlur(frame2, (blur_amount, blur_amount), 0)
            return cv2.addWeighted(blurred, 1 - t, frame2, t, 0)
    
    @staticmethod
    def create_transition_sequence(frame1: np.ndarray, frame2: np.ndarray,
                                  transition_type: str, num_frames: int = 30) -> list:
        """
        Create a sequence of transition frames
        
        Args:
            frame1: First frame
            frame2: Second frame
            transition_type: Type of transition
            num_frames: Number of transition frames
            
        Returns:
            List of transition frames
        """
        frames = []
        
        for i in range(num_frames):
            progress = i / (num_frames - 1)
            
            if transition_type == "crossfade":
                frame = TransitionEffects.crossfade(frame1, frame2, progress)
            elif transition_type == "slide_left":
                frame = TransitionEffects.slide(frame1, frame2, progress, "left")
            elif transition_type == "slide_right":
                frame = TransitionEffects.slide(frame1, frame2, progress, "right")
            elif transition_type == "wipe":
                frame = TransitionEffects.wipe(frame1, frame2, progress)
            elif transition_type == "zoom":
                frame = TransitionEffects.zoom_transition(frame1, frame2, progress)
            elif transition_type == "blur":
                frame = TransitionEffects.blur_transition(frame1, frame2, progress)
            else:
                frame = TransitionEffects.crossfade(frame1, frame2, progress)
            
            frames.append(frame)
        
        return frames

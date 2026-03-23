"""
Transition Effects
Adds smooth transitions between video clips
"""

from typing import List, Optional
from moviepy import VideoFileClip, CompositeVideoClip
from moviepy.video.fx import fadein, fadeout, crossfadein, crossfadeout
import numpy as np

class TransitionEffects:
    """Manages video transitions"""
    
    TRANSITIONS = {
        'fade': 'Simple fade transition',
        'crossfade': 'Crossfade between clips',
        'slide': 'Slide transition',
        'zoom': 'Zoom transition',
        'wipe': 'Wipe transition'
    }
    
    def __init__(self, transition_duration: float = 0.5):
        self.transition_duration = transition_duration
    
    def apply_fade(
        self,
        clip: VideoFileClip,
        fade_in: bool = True,
        fade_out: bool = True
    ) -> VideoFileClip:
        """Apply fade in/out to clip"""
        if fade_in:
            clip = fadein(clip, self.transition_duration)
        
        if fade_out:
            clip = fadeout(clip, self.transition_duration)
        
        return clip
    
    def apply_crossfade(
        self,
        clip1: VideoFileClip,
        clip2: VideoFileClip
    ) -> VideoFileClip:
        """Apply crossfade between two clips"""
        # Add fadeout to first clip
        clip1 = fadeout(clip1, self.transition_duration)
        
        # Add fadein to second clip
        clip2 = fadein(clip2, self.transition_duration)
        
        # Overlap clips
        clip2 = clip2.set_start(clip1.duration - self.transition_duration)
        
        return CompositeVideoClip([clip1, clip2])
    
    def apply_slide(
        self,
        clip: VideoFileClip,
        direction: str = 'left'
    ) -> VideoFileClip:
        """Apply slide transition"""
        w, h = clip.size
        
        def position(t):
            if direction == 'left':
                return (w * (1 - t / self.transition_duration), 0)
            elif direction == 'right':
                return (-w * (1 - t / self.transition_duration), 0)
            elif direction == 'up':
                return (0, h * (1 - t / self.transition_duration))
            else:  # down
                return (0, -h * (1 - t / self.transition_duration))
        
        return clip.set_position(position)
    
    def apply_zoom(
        self,
        clip: VideoFileClip,
        zoom_in: bool = True
    ) -> VideoFileClip:
        """Apply zoom transition"""
        def zoom_effect(get_frame, t):
            frame = get_frame(t)
            
            if zoom_in:
                scale = 1 + (t / clip.duration) * 0.2
            else:
                scale = 1.2 - (t / clip.duration) * 0.2
            
            h, w = frame.shape[:2]
            new_h, new_w = int(h * scale), int(w * scale)
            
            # Resize frame
            import cv2
            resized = cv2.resize(frame, (new_w, new_h))
            
            # Crop to original size
            start_h = (new_h - h) // 2
            start_w = (new_w - w) // 2
            cropped = resized[start_h:start_h+h, start_w:start_w+w]
            
            return cropped
        
        return clip.fl(zoom_effect)
    
    def create_transition_sequence(
        self,
        clips: List[VideoFileClip],
        transition_type: str = 'crossfade'
    ) -> VideoFileClip:
        """Create sequence with transitions"""
        if not clips:
            raise ValueError("No clips provided")
        
        if len(clips) == 1:
            return clips[0]
        
        result = clips[0]
        
        for clip in clips[1:]:
            if transition_type == 'crossfade':
                result = self.apply_crossfade(result, clip)
            elif transition_type == 'fade':
                result = fadeout(result, self.transition_duration)
                clip = fadein(clip, self.transition_duration)
                clip = clip.set_start(result.duration)
                result = CompositeVideoClip([result, clip])
            else:
                # No transition, just concatenate
                clip = clip.set_start(result.duration)
                result = CompositeVideoClip([result, clip])
        
        return result
    
    def get_available_transitions(self) -> List[Dict]:
        """Get list of available transitions"""
        return [
            {'name': name, 'description': desc}
            for name, desc in self.TRANSITIONS.items()
        ]


if __name__ == "__main__":
    effects = TransitionEffects()
    
    print("Available Transitions:")
    for transition in effects.get_available_transitions():
        print(f"  - {transition['name']}: {transition['description']}")

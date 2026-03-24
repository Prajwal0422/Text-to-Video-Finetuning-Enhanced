"""
Audio Effects
Apply audio effects and enhancements
"""

import numpy as np
from typing import Optional, Tuple
import os

class AudioEffects:
    """Audio effects and processing"""
    
    def __init__(self):
        self.effects = {
            'fade_in': 'Fade in audio',
            'fade_out': 'Fade out audio',
            'normalize': 'Normalize audio levels',
            'amplify': 'Amplify audio',
            'echo': 'Add echo effect',
            'reverb': 'Add reverb effect'
        }
    
    def apply_fade_in(
        self,
        audio_data: np.ndarray,
        sample_rate: int,
        duration: float = 1.0
    ) -> np.ndarray:
        """Apply fade in effect"""
        fade_samples = int(sample_rate * duration)
        fade_curve = np.linspace(0, 1, fade_samples)
        
        audio_data[:fade_samples] *= fade_curve
        
        return audio_data
    
    def apply_fade_out(
        self,
        audio_data: np.ndarray,
        sample_rate: int,
        duration: float = 1.0
    ) -> np.ndarray:
        """Apply fade out effect"""
        fade_samples = int(sample_rate * duration)
        fade_curve = np.linspace(1, 0, fade_samples)
        
        audio_data[-fade_samples:] *= fade_curve
        
        return audio_data
    
    def normalize_audio(
        self,
        audio_data: np.ndarray,
        target_level: float = 0.9
    ) -> np.ndarray:
        """Normalize audio to target level"""
        max_val = np.max(np.abs(audio_data))
        
        if max_val > 0:
            audio_data = audio_data * (target_level / max_val)
        
        return audio_data
    
    def amplify_audio(
        self,
        audio_data: np.ndarray,
        gain_db: float = 6.0
    ) -> np.ndarray:
        """Amplify audio by gain in dB"""
        gain_linear = 10 ** (gain_db / 20)
        audio_data = audio_data * gain_linear
        
        # Clip to prevent distortion
        audio_data = np.clip(audio_data, -1.0, 1.0)
        
        return audio_data
    
    def add_echo(
        self,
        audio_data: np.ndarray,
        sample_rate: int,
        delay: float = 0.3,
        decay: float = 0.5
    ) -> np.ndarray:
        """Add echo effect"""
        delay_samples = int(sample_rate * delay)
        
        # Create echo
        echo = np.zeros_like(audio_data)
        echo[delay_samples:] = audio_data[:-delay_samples] * decay
        
        # Mix with original
        audio_data = audio_data + echo
        
        # Normalize
        audio_data = self.normalize_audio(audio_data)
        
        return audio_data
    
    def add_reverb(
        self,
        audio_data: np.ndarray,
        sample_rate: int,
        room_size: float = 0.5
    ) -> np.ndarray:
        """Add simple reverb effect"""
        # Simple reverb using multiple delays
        delays = [0.03, 0.05, 0.07, 0.09]
        decays = [0.3, 0.25, 0.2, 0.15]
        
        reverb = np.zeros_like(audio_data)
        
        for delay, decay in zip(delays, decays):
            delay_samples = int(sample_rate * delay * room_size)
            if delay_samples < len(audio_data):
                temp = np.zeros_like(audio_data)
                temp[delay_samples:] = audio_data[:-delay_samples] * decay
                reverb += temp
        
        # Mix with original
        audio_data = audio_data * 0.7 + reverb * 0.3
        
        # Normalize
        audio_data = self.normalize_audio(audio_data)
        
        return audio_data
    
    def apply_low_pass_filter(
        self,
        audio_data: np.ndarray,
        sample_rate: int,
        cutoff_freq: float = 5000
    ) -> np.ndarray:
        """Apply low-pass filter"""
        from scipy import signal
        
        nyquist = sample_rate / 2
        normalized_cutoff = cutoff_freq / nyquist
        
        b, a = signal.butter(4, normalized_cutoff, btype='low')
        filtered = signal.filtfilt(b, a, audio_data)
        
        return filtered
    
    def apply_high_pass_filter(
        self,
        audio_data: np.ndarray,
        sample_rate: int,
        cutoff_freq: float = 100
    ) -> np.ndarray:
        """Apply high-pass filter"""
        from scipy import signal
        
        nyquist = sample_rate / 2
        normalized_cutoff = cutoff_freq / nyquist
        
        b, a = signal.butter(4, normalized_cutoff, btype='high')
        filtered = signal.filtfilt(b, a, audio_data)
        
        return filtered
    
    def get_available_effects(self) -> dict:
        """Get list of available effects"""
        return self.effects


if __name__ == "__main__":
    effects = AudioEffects()
    
    print("Available Audio Effects:")
    for name, desc in effects.get_available_effects().items():
        print(f"  - {name}: {desc}")

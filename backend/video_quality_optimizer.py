"""
Video Quality Optimizer
Automatically adjusts video quality based on content and requirements
"""

from typing import Dict, Tuple, Optional
import os

class VideoQualityOptimizer:
    """Optimizes video quality settings based on content type"""
    
    # Quality presets
    PRESETS = {
        'low': {
            'width': 480,
            'height': 270,
            'fps': 24,
            'bitrate': '500k',
            'crf': 28
        },
        'medium': {
            'width': 640,
            'height': 360,
            'fps': 24,
            'bitrate': '1000k',
            'crf': 23
        },
        'high': {
            'width': 1280,
            'height': 720,
            'fps': 30,
            'bitrate': '2500k',
            'crf': 20
        },
        'ultra': {
            'width': 1920,
            'height': 1080,
            'fps': 30,
            'bitrate': '5000k',
            'crf': 18
        }
    }
    
    def __init__(self, default_preset: str = 'medium'):
        self.default_preset = default_preset
    
    def get_optimal_settings(
        self,
        content_type: str = 'general',
        target_size_mb: Optional[float] = None,
        duration: float = 10.0
    ) -> Dict:
        """
        Get optimal video settings based on content type and constraints
        
        Args:
            content_type: Type of content ('action', 'nature', 'text', 'general')
            target_size_mb: Target file size in MB
            duration: Video duration in seconds
        
        Returns:
            Dictionary with optimal settings
        """
        # Start with default preset
        settings = self.PRESETS[self.default_preset].copy()
        
        # Adjust based on content type
        if content_type == 'action':
            # Higher FPS for action content
            settings['fps'] = 30
            settings['bitrate'] = '1500k'
        elif content_type == 'text':
            # Lower settings for text/slides
            settings['fps'] = 24
            settings['crf'] = 25
        elif content_type == 'nature':
            # Higher quality for nature/scenic content
            settings['crf'] = 21
            settings['bitrate'] = '1200k'
        
        # Adjust for target file size
        if target_size_mb:
            estimated_bitrate = self._calculate_bitrate_for_size(
                target_size_mb, duration
            )
            settings['bitrate'] = f"{int(estimated_bitrate)}k"
        
        return settings
    
    def _calculate_bitrate_for_size(
        self,
        target_size_mb: float,
        duration: float
    ) -> int:
        """Calculate required bitrate to achieve target file size"""
        # Convert MB to bits
        target_bits = target_size_mb * 8 * 1024 * 1024
        # Calculate bitrate (bits per second)
        bitrate_bps = target_bits / duration
        # Convert to kbps
        bitrate_kbps = bitrate_bps / 1000
        return int(bitrate_kbps)
    
    def estimate_file_size(
        self,
        bitrate_kbps: int,
        duration: float
    ) -> float:
        """Estimate output file size in MB"""
        # Calculate total bits
        total_bits = bitrate_kbps * 1000 * duration
        # Convert to MB
        size_mb = total_bits / (8 * 1024 * 1024)
        return size_mb
    
    def get_resolution_for_bandwidth(
        self,
        bandwidth_mbps: float
    ) -> Tuple[int, int]:
        """Get optimal resolution for given bandwidth"""
        if bandwidth_mbps >= 5:
            return (1920, 1080)  # Full HD
        elif bandwidth_mbps >= 2.5:
            return (1280, 720)   # HD
        elif bandwidth_mbps >= 1:
            return (640, 360)    # SD
        else:
            return (480, 270)    # Low
    
    def analyze_content(self, prompt: str) -> str:
        """Analyze prompt to determine content type"""
        prompt_lower = prompt.lower()
        
        # Action keywords
        action_keywords = ['action', 'fast', 'sport', 'race', 'fight', 'chase', 'running']
        if any(kw in prompt_lower for kw in action_keywords):
            return 'action'
        
        # Nature keywords
        nature_keywords = ['nature', 'landscape', 'scenic', 'mountain', 'ocean', 'forest', 'sunset']
        if any(kw in prompt_lower for kw in nature_keywords):
            return 'nature'
        
        # Text keywords
        text_keywords = ['text', 'presentation', 'slide', 'document', 'title']
        if any(kw in prompt_lower for kw in text_keywords):
            return 'text'
        
        return 'general'
    
    def get_adaptive_settings(
        self,
        prompt: str,
        target_size_mb: Optional[float] = None,
        duration: float = 10.0
    ) -> Dict:
        """
        Get adaptive settings based on prompt analysis
        
        Args:
            prompt: Video generation prompt
            target_size_mb: Optional target file size
            duration: Video duration
        
        Returns:
            Optimized settings dictionary
        """
        content_type = self.analyze_content(prompt)
        settings = self.get_optimal_settings(content_type, target_size_mb, duration)
        
        return {
            'content_type': content_type,
            'settings': settings,
            'estimated_size_mb': self.estimate_file_size(
                int(settings['bitrate'].replace('k', '')),
                duration
            )
        }


# Example usage
if __name__ == "__main__":
    optimizer = VideoQualityOptimizer()
    
    # Test different prompts
    test_prompts = [
        "Fast car racing on highway",
        "Beautiful mountain landscape at sunset",
        "Presentation slides with text",
        "City street at night"
    ]
    
    print("=" * 60)
    print("VIDEO QUALITY OPTIMIZER - TEST")
    print("=" * 60)
    
    for prompt in test_prompts:
        print(f"\nPrompt: '{prompt}'")
        result = optimizer.get_adaptive_settings(prompt, target_size_mb=3.0, duration=12.0)
        
        print(f"  Content Type: {result['content_type']}")
        print(f"  Resolution: {result['settings']['width']}x{result['settings']['height']}")
        print(f"  FPS: {result['settings']['fps']}")
        print(f"  Bitrate: {result['settings']['bitrate']}")
        print(f"  CRF: {result['settings']['crf']}")
        print(f"  Estimated Size: {result['estimated_size_mb']:.2f} MB")

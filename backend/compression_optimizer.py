"""
Compression Optimization
Optimal codec selection and bitrate calculation
"""

import cv2
from typing import Tuple


class CompressionOptimizer:
    """Optimize video compression settings"""
    
    QUALITY_PRESETS = {
        "fast": {
            "codec": "mp4v",
            "crf": 28,
            "preset": "ultrafast",
            "bitrate_multiplier": 0.5
        },
        "balanced": {
            "codec": "avc1",  # H.264
            "crf": 23,
            "preset": "medium",
            "bitrate_multiplier": 1.0
        },
        "quality": {
            "codec": "avc1",  # H.264
            "crf": 18,
            "preset": "slow",
            "bitrate_multiplier": 1.5
        },
        "max": {
            "codec": "hev1",  # H.265
            "crf": 20,
            "preset": "slow",
            "bitrate_multiplier": 1.2
        }
    }
    
    @staticmethod
    def get_codec(quality: str = "balanced") -> Tuple[int, int]:
        """
        Get optimal codec and CRF value
        
        Args:
            quality: Quality preset name
            
        Returns:
            Tuple of (fourcc, crf)
        """
        preset = CompressionOptimizer.QUALITY_PRESETS.get(
            quality,
            CompressionOptimizer.QUALITY_PRESETS["balanced"]
        )
        
        codec_str = preset["codec"]
        crf = preset["crf"]
        
        # Convert codec string to fourcc
        fourcc = cv2.VideoWriter_fourcc(*codec_str)
        
        return fourcc, crf
    
    @staticmethod
    def calculate_bitrate(width: int, height: int, fps: int,
                         quality: str = "balanced") -> int:
        """
        Calculate optimal bitrate
        
        Args:
            width: Video width
            height: Video height
            fps: Frames per second
            quality: Quality preset name
            
        Returns:
            Bitrate in kbps
        """
        preset = CompressionOptimizer.QUALITY_PRESETS.get(
            quality,
            CompressionOptimizer.QUALITY_PRESETS["balanced"]
        )
        
        # Base bitrate per megapixel at 30fps
        base_bitrate = 4000  # kbps
        
        # Calculate megapixels
        pixels = width * height
        megapixels = pixels / (1920 * 1080)
        
        # Adjust for FPS
        fps_factor = fps / 30.0
        
        # Apply quality multiplier
        quality_multiplier = preset["bitrate_multiplier"]
        
        # Calculate final bitrate
        bitrate = int(base_bitrate * megapixels * fps_factor * quality_multiplier)
        
        return max(bitrate, 500)  # Minimum 500 kbps
    
    @staticmethod
    def get_encoder_params(quality: str = "balanced") -> dict:
        """
        Get encoder parameters for quality preset
        
        Args:
            quality: Quality preset name
            
        Returns:
            Dictionary of encoder parameters
        """
        preset = CompressionOptimizer.QUALITY_PRESETS.get(
            quality,
            CompressionOptimizer.QUALITY_PRESETS["balanced"]
        )
        
        return {
            "codec": preset["codec"],
            "crf": preset["crf"],
            "preset": preset["preset"],
            "bitrate_multiplier": preset["bitrate_multiplier"]
        }
    
    @staticmethod
    def estimate_file_size(width: int, height: int, fps: int,
                          duration: float, quality: str = "balanced") -> float:
        """
        Estimate output file size
        
        Args:
            width: Video width
            height: Video height
            fps: Frames per second
            duration: Duration in seconds
            quality: Quality preset name
            
        Returns:
            Estimated file size in MB
        """
        bitrate = CompressionOptimizer.calculate_bitrate(width, height, fps, quality)
        
        # Convert to bytes per second
        bytes_per_second = (bitrate * 1000) / 8
        
        # Calculate total size
        total_bytes = bytes_per_second * duration
        
        # Convert to MB
        size_mb = total_bytes / (1024 * 1024)
        
        return size_mb
    
    @staticmethod
    def recommend_quality(width: int, height: int, target_size_mb: float,
                         duration: float, fps: int = 30) -> str:
        """
        Recommend quality preset based on target file size
        
        Args:
            width: Video width
            height: Video height
            target_size_mb: Target file size in MB
            duration: Duration in seconds
            fps: Frames per second
            
        Returns:
            Recommended quality preset name
        """
        for quality in ["fast", "balanced", "quality", "max"]:
            estimated_size = CompressionOptimizer.estimate_file_size(
                width, height, fps, duration, quality
            )
            
            if estimated_size <= target_size_mb:
                return quality
        
        return "fast"  # Fallback to fastest compression

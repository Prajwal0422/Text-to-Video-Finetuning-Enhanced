"""
NEXUS VISION - Configuration Management
Centralized configuration for the application
"""

import os
from pathlib import Path

class Config:
    """Application configuration"""
    
    # Base paths
    BASE_DIR = Path(__file__).parent.parent
    BACKEND_DIR = BASE_DIR / "backend"
    FRONTEND_DIR = BASE_DIR / "frontend"
    OUTPUTS_DIR = BASE_DIR / "outputs"
    CLIPS_DIR = OUTPUTS_DIR / "clips"
    VIDEOS_DIR = OUTPUTS_DIR / "videos"
    
    # Server settings
    HOST = os.getenv("HOST", "0.0.0.0")
    PORT = int(os.getenv("PORT", 8000))
    DEBUG = os.getenv("DEBUG", "false").lower() == "true"
    
    # API Keys
    PEXELS_API_KEY = os.getenv("PEXELS_API_KEY", "")
    
    # Video generation defaults
    DEFAULT_RESOLUTION = int(os.getenv("DEFAULT_RESOLUTION", 1080))
    DEFAULT_FPS = int(os.getenv("DEFAULT_FPS", 30))
    DEFAULT_DURATION = int(os.getenv("DEFAULT_DURATION", 8))
    
    # Cache settings
    ENABLE_CACHE = os.getenv("ENABLE_CACHE", "true").lower() == "true"
    MAX_CACHE_SIZE_GB = int(os.getenv("MAX_CACHE_SIZE_GB", 5))
    
    # Performance settings
    MAX_WORKERS = int(os.getenv("MAX_WORKERS", 4))
    ENABLE_GPU = os.getenv("ENABLE_GPU", "false").lower() == "true"
    
    # Logging
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    
    # Video settings
    VIDEO_CODEC = "libx264"
    VIDEO_PRESET = "medium"  # ultrafast, fast, medium, slow
    VIDEO_BITRATE = "5000k"
    
    # Generation modes
    MODES = {
        "ultra-fast": {"max_time": 5, "quality": "low"},
        "fast": {"max_time": 10, "quality": "medium"},
        "quality": {"max_time": 30, "quality": "high"},
        "premium": {"max_time": 60, "quality": "ultra"}
    }
    
    @classmethod
    def ensure_directories(cls):
        """Create necessary directories if they don't exist"""
        cls.OUTPUTS_DIR.mkdir(exist_ok=True)
        cls.CLIPS_DIR.mkdir(exist_ok=True)
        cls.VIDEOS_DIR.mkdir(exist_ok=True)
    
    @classmethod
    def get_mode_config(cls, mode: str) -> dict:
        """Get configuration for a generation mode"""
        return cls.MODES.get(mode, cls.MODES["fast"])
    
    @classmethod
    def has_api_key(cls) -> bool:
        """Check if Pexels API key is configured"""
        return bool(cls.PEXELS_API_KEY)

# Initialize directories on import
Config.ensure_directories()

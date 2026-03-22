"""
Configuration Management for NEXUS VISION
Centralized configuration for all backend services
"""

import os
from typing import Dict, Any
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Application configuration"""
    
    # API Keys
    PEXELS_API_KEY = os.getenv('PEXELS_API_KEY', '2YmxczgDDvKxVncxrEtrnv82ksotaLFirswQk0Xyhng0cgy6GBXbRPmq')
    
    # Server Settings
    HOST = os.getenv('HOST', '0.0.0.0')
    PORT = int(os.getenv('PORT', 8000))
    DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
    
    # Video Generation Settings
    CLIP_DURATION = 4.0  # seconds per clip
    TARGET_WIDTH = 640
    TARGET_HEIGHT = 360
    FPS = 24
    MIN_CLIP_DURATION = 1.0
    TARGET_TOTAL_DURATION = (12, 16)  # min, max seconds
    
    # Resilient System Settings
    RETRY_MAX_ATTEMPTS = 3
    RETRY_BASE_DELAY = 5  # seconds
    GENERATION_TIMEOUT = 60  # seconds
    
    # Paths
    OUTPUT_DIR = "outputs/videos"
    CLIPS_DIR = "outputs/clips"
    NORMALIZED_DIR = "outputs/normalized"
    
    # Performance
    MAX_WORKERS = 2
    MAX_CONCURRENT_GENERATIONS = 3
    
    @classmethod
    def get_all(cls) -> Dict[str, Any]:
        """Get all configuration as dictionary"""
        return {
            'pexels_api_key': cls.PEXELS_API_KEY[:10] + '...',  # Masked
            'host': cls.HOST,
            'port': cls.PORT,
            'debug': cls.DEBUG,
            'clip_duration': cls.CLIP_DURATION,
            'target_resolution': f"{cls.TARGET_WIDTH}x{cls.TARGET_HEIGHT}",
            'fps': cls.FPS,
            'retry_attempts': cls.RETRY_MAX_ATTEMPTS,
            'timeout': cls.GENERATION_TIMEOUT
        }
    
    @classmethod
    def validate(cls) -> bool:
        """Validate configuration"""
        if not cls.PEXELS_API_KEY:
            print("⚠️  Warning: PEXELS_API_KEY not set")
            return False
        
        # Create required directories
        os.makedirs(cls.OUTPUT_DIR, exist_ok=True)
        os.makedirs(cls.CLIPS_DIR, exist_ok=True)
        os.makedirs(cls.NORMALIZED_DIR, exist_ok=True)
        
        return True


# Export singleton instance
config = Config()

if __name__ == "__main__":
    print("Configuration:")
    for key, value in Config.get_all().items():
        print(f"  {key}: {value}")
    
    if Config.validate():
        print("\n✅ Configuration valid")
    else:
        print("\n❌ Configuration invalid")

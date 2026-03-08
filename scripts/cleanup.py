"""
Cleanup script for NEXUS VISION
Removes old cache files and temporary data
"""

import sys
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))

from config import Config
from utils import clean_old_files, get_cache_size, get_file_size

def cleanup_cache(max_age_days: int = 7):
    """Clean old cache files"""
    print("🧹 Cleaning cache...")
    
    # Get initial size
    initial_size = get_cache_size(Config.CLIPS_DIR)
    print(f"Initial cache size: {get_file_size(Config.CLIPS_DIR) if Config.CLIPS_DIR.exists() else '0 B'}")
    
    # Clean old files
    clean_old_files(Config.CLIPS_DIR, max_age_days)
    clean_old_files(Config.VIDEOS_DIR, max_age_days)
    
    # Get final size
    final_size = get_cache_size(Config.CLIPS_DIR)
    freed = initial_size - final_size
    
    print(f"Final cache size: {get_file_size(Config.CLIPS_DIR) if Config.CLIPS_DIR.exists() else '0 B'}")
    print(f"✅ Freed {freed / (1024*1024):.1f} MB")

if __name__ == "__main__":
    max_age = int(sys.argv[1]) if len(sys.argv) > 1 else 7
    cleanup_cache(max_age)

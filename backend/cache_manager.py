"""
Cache Management
Intelligent caching for video operations
"""

import os
import hashlib
import pickle
import numpy as np
from typing import Any, Optional
import logging

logger = logging.getLogger(__name__)


class CacheManager:
    """Manage cache for video operations"""
    
    def __init__(self, cache_dir: str = ".cache/video"):
        self.cache_dir = cache_dir
        self.enabled = True
        self._ensure_cache_dir()
    
    def _ensure_cache_dir(self):
        """Create cache directory if it doesn't exist"""
        os.makedirs(self.cache_dir, exist_ok=True)
    
    def _get_cache_key(self, data: Any) -> str:
        """Generate cache key from data"""
        try:
            serialized = pickle.dumps(data)
            return hashlib.md5(serialized).hexdigest()
        except:
            # Fallback to string representation
            return hashlib.md5(str(data).encode()).hexdigest()
    
    def get_cache_path(self, key: str, extension: str = ".npy") -> str:
        """Get full cache file path"""
        return os.path.join(self.cache_dir, f"{key}{extension}")
    
    def has_cached(self, key: str, extension: str = ".npy") -> bool:
        """Check if cached data exists"""
        if not self.enabled:
            return False
        
        cache_path = self.get_cache_path(key, extension)
        return os.path.exists(cache_path)
    
    def load_frame(self, key: str) -> Optional[np.ndarray]:
        """Load cached frame"""
        if not self.enabled:
            return None
        
        cache_path = self.get_cache_path(key, ".npy")
        
        if os.path.exists(cache_path):
            try:
                frame = np.load(cache_path)
                logger.debug(f"Cache hit: {key}")
                return frame
            except Exception as e:
                logger.warning(f"Failed to load cache {key}: {e}")
                return None
        
        return None
    
    def save_frame(self, key: str, frame: np.ndarray):
        """Save frame to cache"""
        if not self.enabled:
            return
        
        cache_path = self.get_cache_path(key, ".npy")
        
        try:
            np.save(cache_path, frame)
            logger.debug(f"Cached: {key}")
        except Exception as e:
            logger.warning(f"Failed to cache {key}: {e}")
    
    def load_data(self, key: str) -> Optional[Any]:
        """Load cached data (pickle)"""
        if not self.enabled:
            return None
        
        cache_path = self.get_cache_path(key, ".pkl")
        
        if os.path.exists(cache_path):
            try:
                with open(cache_path, 'rb') as f:
                    data = pickle.load(f)
                logger.debug(f"Cache hit: {key}")
                return data
            except Exception as e:
                logger.warning(f"Failed to load cache {key}: {e}")
                return None
        
        return None
    
    def save_data(self, key: str, data: Any):
        """Save data to cache (pickle)"""
        if not self.enabled:
            return
        
        cache_path = self.get_cache_path(key, ".pkl")
        
        try:
            with open(cache_path, 'wb') as f:
                pickle.dump(data, f)
            logger.debug(f"Cached: {key}")
        except Exception as e:
            logger.warning(f"Failed to cache {key}: {e}")
    
    def clear_cache(self):
        """Clear all cached data"""
        try:
            for filename in os.listdir(self.cache_dir):
                file_path = os.path.join(self.cache_dir, filename)
                if os.path.isfile(file_path):
                    os.remove(file_path)
            logger.info("Cache cleared")
        except Exception as e:
            logger.warning(f"Failed to clear cache: {e}")
    
    def get_cache_size(self) -> int:
        """Get total cache size in bytes"""
        total_size = 0
        
        try:
            for filename in os.listdir(self.cache_dir):
                file_path = os.path.join(self.cache_dir, filename)
                if os.path.isfile(file_path):
                    total_size += os.path.getsize(file_path)
        except:
            pass
        
        return total_size
    
    def get_cache_info(self) -> dict:
        """Get cache statistics"""
        try:
            files = os.listdir(self.cache_dir)
            size = self.get_cache_size()
            
            return {
                "enabled": self.enabled,
                "directory": self.cache_dir,
                "file_count": len(files),
                "size_bytes": size,
                "size_mb": size / (1024 * 1024)
            }
        except:
            return {
                "enabled": self.enabled,
                "directory": self.cache_dir,
                "file_count": 0,
                "size_bytes": 0,
                "size_mb": 0
            }
    
    def enable(self):
        """Enable caching"""
        self.enabled = True
        logger.info("Cache enabled")
    
    def disable(self):
        """Disable caching"""
        self.enabled = False
        logger.info("Cache disabled")


# Global cache manager
_global_cache = None


def get_cache_manager() -> CacheManager:
    """Get global cache manager instance"""
    global _global_cache
    if _global_cache is None:
        _global_cache = CacheManager()
    return _global_cache

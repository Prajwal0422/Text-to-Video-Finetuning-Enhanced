"""
Cache Manager for Video Clips
Manages downloaded clips and prevents redundant downloads
"""

import os
import json
import hashlib
from typing import Optional, Dict
from datetime import datetime, timedelta

class CacheManager:
    """Manages clip cache with expiration"""
    
    def __init__(self, cache_dir: str = "outputs/clips", cache_duration_days: int = 7):
        self.cache_dir = cache_dir
        self.cache_duration = timedelta(days=cache_duration_days)
        self.cache_index_file = os.path.join(cache_dir, "cache_index.json")
        
        os.makedirs(cache_dir, exist_ok=True)
        self.cache_index = self._load_index()
    
    def _load_index(self) -> Dict:
        """Load cache index from disk"""
        if os.path.exists(self.cache_index_file):
            try:
                with open(self.cache_index_file, 'r') as f:
                    return json.load(f)
            except:
                return {}
        return {}
    
    def _save_index(self):
        """Save cache index to disk"""
        with open(self.cache_index_file, 'w') as f:
            json.dump(self.cache_index, f, indent=2)
    
    def get_cache_key(self, query: str) -> str:
        """Generate cache key from query"""
        return hashlib.md5(query.lower().encode()).hexdigest()
    
    def get_cached_clip(self, query: str) -> Optional[str]:
        """Get cached clip path if available and not expired"""
        cache_key = self.get_cache_key(query)
        
        if cache_key in self.cache_index:
            entry = self.cache_index[cache_key]
            cached_time = datetime.fromisoformat(entry['timestamp'])
            
            # Check if expired
            if datetime.now() - cached_time < self.cache_duration:
                clip_path = entry['path']
                if os.path.exists(clip_path):
                    return clip_path
        
        return None
    
    def cache_clip(self, query: str, clip_path: str):
        """Add clip to cache"""
        cache_key = self.get_cache_key(query)
        
        self.cache_index[cache_key] = {
            'query': query,
            'path': clip_path,
            'timestamp': datetime.now().isoformat()
        }
        
        self._save_index()
    
    def clean_expired(self):
        """Remove expired cache entries"""
        now = datetime.now()
        expired_keys = []
        
        for key, entry in self.cache_index.items():
            cached_time = datetime.fromisoformat(entry['timestamp'])
            if now - cached_time >= self.cache_duration:
                expired_keys.append(key)
                # Delete file if exists
                if os.path.exists(entry['path']):
                    try:
                        os.remove(entry['path'])
                    except:
                        pass
        
        for key in expired_keys:
            del self.cache_index[key]
        
        if expired_keys:
            self._save_index()
            print(f"🗑️  Cleaned {len(expired_keys)} expired cache entries")
    
    def get_stats(self) -> Dict:
        """Get cache statistics"""
        total_entries = len(self.cache_index)
        total_size = 0
        
        for entry in self.cache_index.values():
            if os.path.exists(entry['path']):
                total_size += os.path.getsize(entry['path'])
        
        return {
            'total_entries': total_entries,
            'total_size_mb': round(total_size / (1024 * 1024), 2),
            'cache_dir': self.cache_dir
        }

"""
Intelligent Video Cache System
Caches generated videos and clips for faster retrieval
"""

import os
import hashlib
import json
import time
from typing import Optional, Dict, List
from datetime import datetime, timedelta
import shutil

class VideoCache:
    def __init__(self, cache_dir: str = "outputs/cache", max_size_mb: int = 500):
        self.cache_dir = cache_dir
        self.max_size_bytes = max_size_mb * 1024 * 1024
        self.metadata_file = os.path.join(cache_dir, "cache_metadata.json")
        
        os.makedirs(cache_dir, exist_ok=True)
        self.metadata = self._load_metadata()
    
    def _load_metadata(self) -> Dict:
        """Load cache metadata"""
        if os.path.exists(self.metadata_file):
            try:
                with open(self.metadata_file, 'r') as f:
                    return json.load(f)
            except:
                return {'entries': {}, 'total_size': 0}
        return {'entries': {}, 'total_size': 0}
    
    def _save_metadata(self):
        """Save cache metadata"""
        with open(self.metadata_file, 'w') as f:
            json.dump(self.metadata, f, indent=2)
    
    def _get_cache_key(self, prompt: str, mode: str = "standard") -> str:
        """Generate cache key from prompt and mode"""
        key_string = f"{prompt.lower().strip()}_{mode}"
        return hashlib.md5(key_string.encode()).hexdigest()
    
    def get(self, prompt: str, mode: str = "standard") -> Optional[str]:
        """Get cached video if exists"""
        cache_key = self._get_cache_key(prompt, mode)
        
        if cache_key in self.metadata['entries']:
            entry = self.metadata['entries'][cache_key]
            filepath = entry['filepath']
            
            # Check if file exists
            if os.path.exists(filepath):
                # Update access time
                entry['last_accessed'] = datetime.now().isoformat()
                entry['access_count'] += 1
                self._save_metadata()
                
                print(f"✅ Cache HIT: {prompt[:30]}")
                return filepath
            else:
                # Remove invalid entry
                del self.metadata['entries'][cache_key]
                self._save_metadata()
        
        print(f"❌ Cache MISS: {prompt[:30]}")
        return None
    
    def put(self, prompt: str, video_path: str, mode: str = "standard") -> bool:
        """Cache a generated video"""
        if not os.path.exists(video_path):
            return False
        
        cache_key = self._get_cache_key(prompt, mode)
        file_size = os.path.getsize(video_path)
        
        # Check if we need to make space
        if self.metadata['total_size'] + file_size > self.max_size_bytes:
            self._evict_old_entries(file_size)
        
        # Copy to cache
        cache_filename = f"{cache_key}.mp4"
        cache_path = os.path.join(self.cache_dir, cache_filename)
        
        try:
            shutil.copy2(video_path, cache_path)
            
            # Update metadata
            self.metadata['entries'][cache_key] = {
                'prompt': prompt,
                'mode': mode,
                'filepath': cache_path,
                'size': file_size,
                'created': datetime.now().isoformat(),
                'last_accessed': datetime.now().isoformat(),
                'access_count': 0
            }
            
            self.metadata['total_size'] += file_size
            self._save_metadata()
            
            print(f"✅ Cached: {prompt[:30]} ({file_size / 1024:.1f}KB)")
            return True
            
        except Exception as e:
            print(f"❌ Cache failed: {e}")
            return False
    
    def _evict_old_entries(self, needed_space: int):
        """Evict least recently used entries to make space"""
        print(f"🗑️  Evicting cache entries to free {needed_space / 1024:.1f}KB")
        
        # Sort by last accessed (oldest first)
        entries = sorted(
            self.metadata['entries'].items(),
            key=lambda x: x[1]['last_accessed']
        )
        
        freed_space = 0
        for cache_key, entry in entries:
            if freed_space >= needed_space:
                break
            
            # Remove file
            filepath = entry['filepath']
            if os.path.exists(filepath):
                os.remove(filepath)
                freed_space += entry['size']
                self.metadata['total_size'] -= entry['size']
            
            # Remove from metadata
            del self.metadata['entries'][cache_key]
            print(f"  Evicted: {entry['prompt'][:30]}")
        
        self._save_metadata()
        print(f"✅ Freed {freed_space / 1024:.1f}KB")
    
    def get_stats(self) -> Dict:
        """Get cache statistics"""
        total_entries = len(self.metadata['entries'])
        total_size_mb = self.metadata['total_size'] / (1024 * 1024)
        max_size_mb = self.max_size_bytes / (1024 * 1024)
        usage_percent = (self.metadata['total_size'] / self.max_size_bytes) * 100
        
        # Calculate hit rate (from access counts)
        total_accesses = sum(e['access_count'] for e in self.metadata['entries'].values())
        
        return {
            'total_entries': total_entries,
            'total_size_mb': round(total_size_mb, 2),
            'max_size_mb': max_size_mb,
            'usage_percent': round(usage_percent, 1),
            'total_accesses': total_accesses
        }
    
    def clear(self):
        """Clear entire cache"""
        for entry in self.metadata['entries'].values():
            filepath = entry['filepath']
            if os.path.exists(filepath):
                os.remove(filepath)
        
        self.metadata = {'entries': {}, 'total_size': 0}
        self._save_metadata()
        print("✅ Cache cleared")
    
    def get_cache_report(self) -> str:
        """Generate formatted cache report"""
        stats = self.get_stats()
        
        report = []
        report.append("=" * 60)
        report.append("VIDEO CACHE REPORT")
        report.append("=" * 60)
        report.append(f"Total Entries: {stats['total_entries']}")
        report.append(f"Cache Size: {stats['total_size_mb']:.2f} MB / {stats['max_size_mb']:.0f} MB")
        report.append(f"Usage: {stats['usage_percent']:.1f}%")
        report.append(f"Total Accesses: {stats['total_accesses']}")
        report.append("")
        
        if self.metadata['entries']:
            report.append("Recent Entries:")
            report.append("-" * 60)
            
            # Sort by created date (newest first)
            sorted_entries = sorted(
                self.metadata['entries'].values(),
                key=lambda x: x['created'],
                reverse=True
            )[:10]
            
            for entry in sorted_entries:
                prompt = entry['prompt'][:40]
                mode = entry['mode']
                size_kb = entry['size'] / 1024
                accesses = entry['access_count']
                report.append(f"{prompt:40} | {mode:10} | {size_kb:6.1f}KB | {accesses} hits")
        
        report.append("=" * 60)
        
        return "\n".join(report)


# Global instance
cache = VideoCache()


if __name__ == "__main__":
    # Test
    print("Video Cache Test")
    print("=" * 60)
    
    # Test cache operations
    test_prompt = "ocean waves at sunset"
    
    # Try to get (should miss)
    result = cache.get(test_prompt)
    print(f"First get: {result}")
    
    # Simulate putting a video
    # cache.put(test_prompt, "test_video.mp4")
    
    # Print report
    print("\n" + cache.get_cache_report())

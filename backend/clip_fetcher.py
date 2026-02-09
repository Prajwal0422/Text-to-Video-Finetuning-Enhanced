"""
Optimized Clip Fetcher - Fast parallel downloads with caching
FIXED: Proper streaming download to prevent 0-second videos
"""

import os
import requests
from typing import List, Dict, Optional
import time
import hashlib
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading

class ClipFetcher:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv('PEXELS_API_KEY', '')
        self.base_url = "https://api.pexels.com/videos/search"
        self.headers = {'Authorization': self.api_key}
        self.download_dir = "outputs/clips"
        self.cache_dir = os.path.join(self.download_dir, "cache")
        os.makedirs(self.cache_dir, exist_ok=True)
        
        # Performance settings
        self.request_timeout = 8
        self.download_timeout = 30  # Increased for full download
        self.max_workers = 3
        self.max_file_size = 10 * 1024 * 1024  # 10MB max
        
        self.cache_lock = threading.Lock()
    
    def _get_cache_key(self, keyword: str) -> str:
        """Generate cache key from keyword"""
        return hashlib.md5(keyword.lower().encode()).hexdigest()
    
    def _get_cached_clip(self, keyword: str) -> Optional[str]:
        """Check if clip exists in cache"""
        cache_key = self._get_cache_key(keyword)
        cache_pattern = os.path.join(self.cache_dir, f"{cache_key}_*.mp4")
        
        import glob
        cached_files = glob.glob(cache_pattern)
        
        if cached_files and os.path.exists(cached_files[0]):
            # Verify file is not empty
            if os.path.getsize(cached_files[0]) > 1000:  # At least 1KB
                print(f"✅ Using cached clip for: {keyword}")
                return cached_files[0]
        return None
    
    def search_videos(self, keyword: str, per_page: int = 3) -> List[Dict]:
        """Search for videos with timeout"""
        if not self.api_key:
            print("⚠️  No Pexels API key. Using fallback.")
            return []
        
        try:
            params = {
                'query': keyword,
                'per_page': per_page,
                'orientation': 'landscape',
                'size': 'small'
            }
            
            response = requests.get(
                self.base_url,
                headers=self.headers,
                params=params,
                timeout=self.request_timeout
            )
            
            if response.status_code == 200:
                data = response.json()
                return data.get('videos', [])
            else:
                print(f"⚠️  API error {response.status_code}")
                return []
                
        except requests.Timeout:
            print(f"⏱️  Timeout searching for: {keyword}")
            return []
        except Exception as e:
            print(f"⚠️  Error: {e}")
            return []
    
    def _select_smallest_video(self, video_files: List[Dict]) -> Optional[Dict]:
        """Select smallest resolution video"""
        if not video_files:
            return None
        
        # Filter for small videos
        small_videos = [vf for vf in video_files if vf.get('width', 9999) <= 640]
        
        if small_videos:
            small_videos.sort(key=lambda x: x.get('width', 9999) * x.get('height', 9999))
            return small_videos[0]
        
        # Fallback
        video_files.sort(key=lambda x: x.get('width', 9999) * x.get('height', 9999))
        return video_files[0]
    
    def download_clip(self, video_url: str, keyword: str) -> Optional[str]:
        """
        ✅ FIXED: Proper streaming download
        Downloads complete video file using streaming
        """
        try:
            cache_key = self._get_cache_key(keyword)
            filename = f"{cache_key}_{keyword[:20]}.mp4"
            filepath = os.path.join(self.cache_dir, filename)
            
            # Skip if already exists and valid
            if os.path.exists(filepath) and os.path.getsize(filepath) > 1000:
                print(f"✅ Using existing: {keyword}")
                return filepath
            
            print(f"📥 Downloading: {keyword}")
            
            # ✅ PROPER STREAMING DOWNLOAD
            response = requests.get(
                video_url, 
                stream=True,  # Enable streaming
                timeout=self.download_timeout
            )
            
            if response.status_code != 200:
                print(f"❌ Download failed: {response.status_code}")
                return None
            
            # Check content length
            content_length = int(response.headers.get('content-length', 0))
            if content_length > self.max_file_size:
                print(f"⚠️  File too large ({content_length / 1024 / 1024:.1f}MB), skipping")
                return None
            
            # ✅ DOWNLOAD WITH PROPER CHUNKING
            downloaded = 0
            with open(filepath, 'wb') as f:
                for chunk in response.iter_content(chunk_size=1024 * 1024):  # 1MB chunks
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)
                        
                        # Enforce size limit
                        if downloaded > self.max_file_size:
                            print(f"⚠️  Size limit exceeded")
                            f.close()
                            if os.path.exists(filepath):
                                os.remove(filepath)
                            return None
            
            # ✅ VERIFY FILE WAS DOWNLOADED
            if not os.path.exists(filepath):
                print(f"❌ File not created: {filepath}")
                return None
            
            file_size = os.path.getsize(filepath)
            if file_size < 1000:  # Less than 1KB = corrupted
                print(f"❌ File too small ({file_size} bytes), corrupted")
                os.remove(filepath)
                return None
            
            print(f"✅ Downloaded: {keyword} ({file_size / 1024:.1f}KB)")
            return filepath
            
        except requests.Timeout:
            print(f"⏱️  Download timeout: {keyword}")
            if os.path.exists(filepath):
                os.remove(filepath)
            return None
        except Exception as e:
            print(f"❌ Error downloading: {e}")
            if os.path.exists(filepath):
                os.remove(filepath)
            return None
    
    def _fetch_single_clip(self, keyword: str) -> Optional[str]:
        """Fetch a single clip with validation"""
        # Check cache first
        cached = self._get_cached_clip(keyword)
        if cached:
            return cached
        
        # Search for videos
        videos = self.search_videos(keyword, per_page=3)
        
        if not videos:
            # Fail-fast: Try fallback
            fallback_keywords = ['nature', 'landscape', 'sky', 'water']
            for fallback in fallback_keywords:
                if fallback != keyword:
                    print(f"🔄 Trying fallback: {fallback}")
                    videos = self.search_videos(fallback, per_page=2)
                    if videos:
                        keyword = fallback
                        break
        
        if not videos:
            return None
        
        video = videos[0]
        video_files = video.get('video_files', [])
        
        # Select smallest resolution
        selected = self._select_smallest_video(video_files)
        
        if not selected:
            return None
        
        video_url = selected.get('link')
        if not video_url:
            return None
        
        # Download with proper streaming
        return self.download_clip(video_url, keyword)
    
    def fetch_clips_for_scenes(self, scenes: List[Dict]) -> List[str]:
        """
        Fetch clips in PARALLEL with validation
        Returns only valid, non-corrupted clips
        """
        # Max 3 clips
        scenes = scenes[:3]
        
        print(f"\n🚀 Fetching {len(scenes)} clips in parallel...")
        
        downloaded_clips = []
        
        # Parallel download
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            future_to_scene = {}
            for scene in scenes:
                keywords = scene.get('keywords', [])
                if keywords:
                    keyword = keywords[0]
                    future = executor.submit(self._fetch_single_clip, keyword)
                    future_to_scene[future] = keyword
            
            # Collect results
            for future in as_completed(future_to_scene):
                keyword = future_to_scene[future]
                try:
                    filepath = future.result()
                    if filepath and os.path.exists(filepath):
                        # ✅ VERIFY FILE IS VALID
                        if os.path.getsize(filepath) > 1000:
                            downloaded_clips.append(filepath)
                        else:
                            print(f"⚠️  Skipping corrupted file: {filepath}")
                except Exception as e:
                    print(f"❌ Failed to fetch {keyword}: {e}")
        
        print(f"✅ Downloaded {len(downloaded_clips)}/{len(scenes)} valid clips")
        
        # Ensure at least 1 clip
        if not downloaded_clips:
            print("⚠️  No clips downloaded, trying emergency fallback")
            fallback = self._fetch_single_clip('nature')
            if fallback and os.path.exists(fallback):
                downloaded_clips.append(fallback)
        
        return downloaded_clips


if __name__ == "__main__":
    # Test
    fetcher = ClipFetcher()
    scenes = [
        {'id': 1, 'keywords': ['sunset']},
        {'id': 2, 'keywords': ['ocean']},
    ]
    
    clips = fetcher.fetch_clips_for_scenes(scenes)
    print(f"\n⚡ Fetched {len(clips)} clips")
    for clip in clips:
        size = os.path.getsize(clip) / 1024
        print(f"  - {clip} ({size:.1f}KB)")

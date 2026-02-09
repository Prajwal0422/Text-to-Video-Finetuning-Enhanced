"""
Optimized Clip Fetcher - Fast parallel downloads with caching
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
        self.request_timeout = 8  # 8 second timeout for API calls
        self.download_timeout = 15  # 15 second timeout for downloads
        self.max_workers = 3  # Parallel downloads
        self.max_file_size = 10 * 1024 * 1024  # 10MB max per clip
        
        # Cache lock for thread safety
        self.cache_lock = threading.Lock()
    
    def _get_cache_key(self, keyword: str) -> str:
        """Generate cache key from keyword"""
        return hashlib.md5(keyword.lower().encode()).hexdigest()
    
    def _get_cached_clip(self, keyword: str) -> Optional[str]:
        """Check if clip exists in cache"""
        cache_key = self._get_cache_key(keyword)
        cache_pattern = os.path.join(self.cache_dir, f"{cache_key}_*.mp4")
        
        # Find cached files
        import glob
        cached_files = glob.glob(cache_pattern)
        
        if cached_files and os.path.exists(cached_files[0]):
            print(f"✅ Using cached clip for: {keyword}")
            return cached_files[0]
        return None
    
    def search_videos(self, keyword: str, per_page: int = 3) -> List[Dict]:
        """Search for videos with timeout and small resolution preference"""
        if not self.api_key:
            print("⚠️  No Pexels API key. Using fallback.")
            return []
        
        try:
            params = {
                'query': keyword,
                'per_page': per_page,
                'orientation': 'landscape',
                'size': 'small'  # Prefer smaller files
            }
            
            response = requests.get(
                self.base_url,
                headers=self.headers,
                params=params,
                timeout=self.request_timeout  # TIMEOUT: 8 seconds
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
        """Select smallest resolution video (width <= 640 preferred)"""
        if not video_files:
            return None
        
        # Filter for small videos first
        small_videos = [vf for vf in video_files if vf.get('width', 9999) <= 640]
        
        if small_videos:
            # Sort by file size (smallest first)
            small_videos.sort(key=lambda x: x.get('width', 9999) * x.get('height', 9999))
            return small_videos[0]
        
        # Fallback: get smallest available
        video_files.sort(key=lambda x: x.get('width', 9999) * x.get('height', 9999))
        return video_files[0]
    
    def download_clip(self, video_url: str, keyword: str) -> Optional[str]:
        """Download a video clip with timeout and size limit"""
        try:
            cache_key = self._get_cache_key(keyword)
            filename = f"{cache_key}_{keyword[:20]}.mp4"
            filepath = os.path.join(self.cache_dir, filename)
            
            # Skip if already exists
            if os.path.exists(filepath):
                return filepath
            
            print(f"📥 Downloading: {keyword}")
            
            # Stream download with timeout
            response = requests.get(
                video_url, 
                stream=True, 
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
            
            # Download with size limit
            downloaded = 0
            with open(filepath, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)
                        
                        # Enforce size limit during download
                        if downloaded > self.max_file_size:
                            print(f"⚠️  Size limit exceeded, aborting")
                            os.remove(filepath)
                            return None
            
            print(f"✅ Downloaded: {keyword} ({downloaded / 1024:.1f}KB)")
            return filepath
            
        except requests.Timeout:
            print(f"⏱️  Download timeout: {keyword}")
            return None
        except Exception as e:
            print(f"❌ Error downloading: {e}")
            if os.path.exists(filepath):
                os.remove(filepath)
            return None
    
    def _fetch_single_clip(self, keyword: str) -> Optional[str]:
        """Fetch a single clip (used in parallel execution)"""
        # Check cache first
        cached = self._get_cached_clip(keyword)
        if cached:
            return cached
        
        # Search for videos
        videos = self.search_videos(keyword, per_page=3)
        
        if not videos:
            # FAIL-FAST: Try fallback keyword
            fallback_keywords = ['nature', 'landscape', 'sky', 'water']
            for fallback in fallback_keywords:
                if fallback != keyword:
                    print(f"🔄 Trying fallback: {fallback}")
                    videos = self.search_videos(fallback, per_page=2)
                    if videos:
                        keyword = fallback  # Use fallback for caching
                        break
        
        if not videos:
            return None
        
        # Get first video
        video = videos[0]
        video_files = video.get('video_files', [])
        
        # Select smallest resolution
        selected = self._select_smallest_video(video_files)
        
        if not selected:
            return None
        
        video_url = selected.get('link')
        if not video_url:
            return None
        
        # Download
        return self.download_clip(video_url, keyword)
    
    def fetch_clips_for_scenes(self, scenes: List[Dict]) -> List[str]:
        """
        Fetch clips in PARALLEL with optimizations:
        - Max 3 clips only
        - Parallel downloads
        - Caching
        - Timeouts
        - Fail-fast
        """
        # LIMIT: Max 3 clips
        scenes = scenes[:3]
        
        print(f"\n🚀 Fetching {len(scenes)} clips in parallel...")
        
        downloaded_clips = []
        
        # PARALLEL DOWNLOAD using ThreadPoolExecutor
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # Submit all download tasks
            future_to_scene = {}
            for scene in scenes:
                keywords = scene.get('keywords', [])
                if keywords:
                    keyword = keywords[0]
                    future = executor.submit(self._fetch_single_clip, keyword)
                    future_to_scene[future] = keyword
            
            # Collect results as they complete
            for future in as_completed(future_to_scene):
                keyword = future_to_scene[future]
                try:
                    filepath = future.result()
                    if filepath:
                        downloaded_clips.append(filepath)
                except Exception as e:
                    print(f"❌ Failed to fetch {keyword}: {e}")
        
        print(f"✅ Downloaded {len(downloaded_clips)}/{len(scenes)} clips")
        
        # Ensure we have at least 1 clip
        if not downloaded_clips:
            print("⚠️  No clips downloaded, using fallback")
            # Try one more fallback
            fallback = self._fetch_single_clip('nature')
            if fallback:
                downloaded_clips.append(fallback)
        
        return downloaded_clips


if __name__ == "__main__":
    # Test optimized fetcher
    import time
    
    fetcher = ClipFetcher()
    scenes = [
        {'id': 1, 'keywords': ['sunset']},
        {'id': 2, 'keywords': ['ocean']},
        {'id': 3, 'keywords': ['mountains']},
    ]
    
    start = time.time()
    clips = fetcher.fetch_clips_for_scenes(scenes)
    elapsed = time.time() - start
    
    print(f"\n⚡ Fetched {len(clips)} clips in {elapsed:.1f}s")
    for clip in clips:
        print(f"  - {clip}")

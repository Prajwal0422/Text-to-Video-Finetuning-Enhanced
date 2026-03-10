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
    
    def search_videos(self, query: str, per_page: int = 10) -> List[Dict]:
        """Search for videos using FULL query with ranking"""
        if not self.api_key:
            print("⚠️  No Pexels API key. Using fallback.")
            return []
        
        try:
            params = {
                'query': query,  # Use full query instead of single keyword
                'per_page': per_page,  # Get more results for ranking
                'orientation': 'landscape',
                'size': 'medium'
            }
            
            response = requests.get(
                self.base_url,
                headers=self.headers,
                params=params,
                timeout=self.request_timeout
            )
            
            if response.status_code == 200:
                data = response.json()
                videos = data.get('videos', [])
                
                # Rank videos by relevance
                ranked_videos = self._rank_videos(videos, query)
                return ranked_videos
            else:
                print(f"⚠️  API error {response.status_code}")
                return []
                
        except requests.Timeout:
            print(f"⏱️  Timeout searching for: {query}")
            return []
        except Exception as e:
            print(f"⚠️  Error: {e}")
            return []
    
    def _rank_videos(self, videos: List[Dict], query: str) -> List[Dict]:
        """Rank videos by keyword match, duration, and resolution"""
        query_words = set(query.lower().split())
        
        scored_videos = []
        for video in videos:
            score = 0
            
            # 1. Keyword match score (most important)
            video_tags = video.get('tags', [])
            if isinstance(video_tags, list):
                video_tags_lower = [tag.lower() for tag in video_tags]
                matches = sum(1 for word in query_words if any(word in tag for tag in video_tags_lower))
                score += matches * 10
            
            # 2. Duration score (prefer 4-10 seconds)
            duration = video.get('duration', 0)
            if 4 <= duration <= 10:
                score += 5
            elif duration > 10:
                score += 2
            
            # 3. Resolution score (prefer HD but not too large)
            video_files = video.get('video_files', [])
            if video_files:
                best_file = max(video_files, key=lambda x: x.get('width', 0))
                width = best_file.get('width', 0)
                if width >= 1280:  # HD
                    score += 3
                elif width >= 640:  # SD
                    score += 2
            
            scored_videos.append((score, video))
        
        # Sort by score descending
        scored_videos.sort(key=lambda x: x[0], reverse=True)
        
        # Return videos only
        return [video for score, video in scored_videos]
    
    def _select_best_video_file(self, video_files: List[Dict]) -> Optional[Dict]:
        """Select best quality video file (prefer landscape, good resolution)"""
        if not video_files:
            return None
        
        # Filter for landscape videos (width > height)
        landscape_videos = [vf for vf in video_files if vf.get('width', 0) > vf.get('height', 0)]
        
        if not landscape_videos:
            landscape_videos = video_files
        
        # Filter for good duration (> 4 seconds implied by API)
        # Prefer HD quality (640-1920 width)
        good_quality = [vf for vf in landscape_videos if 640 <= vf.get('width', 0) <= 1920]
        
        if good_quality:
            # Sort by resolution (prefer higher but not too large)
            good_quality.sort(key=lambda x: abs(x.get('width', 0) - 1280))  # Prefer 720p
            return good_quality[0]
        
        # Fallback: return smallest
        landscape_videos.sort(key=lambda x: x.get('width', 0) * x.get('height', 0))
        return landscape_videos[0]
    
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
    
    def _fetch_single_clip(self, scene: Dict) -> Optional[str]:
        """Fetch a single clip using full scene query"""
        # Use full query from scene
        query = scene.get('query', '')
        if not query:
            keywords = scene.get('keywords', [])
            query = ' '.join(keywords) if keywords else 'nature'
        
        # Check cache first (use first keyword for cache key)
        keywords = scene.get('keywords', [])
        cache_keyword = keywords[0] if keywords else query.split()[0]
        cached = self._get_cached_clip(cache_keyword)
        if cached:
            return cached
        
        # Search for videos using full query
        print(f"🔍 Searching: '{query}'")
        videos = self.search_videos(query, per_page=10)
        
        if not videos:
            # Fail-fast: Try fallback
            fallback_keywords = ['nature', 'landscape', 'sky', 'water']
            for fallback in fallback_keywords:
                if fallback not in query:
                    print(f"🔄 Trying fallback: {fallback}")
                    videos = self.search_videos(fallback, per_page=5)
                    if videos:
                        cache_keyword = fallback
                        break
        
        if not videos:
            return None
        
        # Use best ranked video (first one after ranking)
        video = videos[0]
        video_files = video.get('video_files', [])
        
        # Select best quality video file
        selected = self._select_best_video_file(video_files)
        
        if not selected:
            return None
        
        video_url = selected.get('link')
        if not video_url:
            return None
        
        # Download with proper streaming
        return self.download_clip(video_url, cache_keyword)
    
    def fetch_clips_for_scenes(self, scenes: List[Dict]) -> List[str]:
        """
        Fetch clips in PARALLEL using full scene queries
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
                future = executor.submit(self._fetch_single_clip, scene)
                future_to_scene[future] = scene.get('query', 'scene')
            
            # Collect results
            for future in as_completed(future_to_scene):
                query = future_to_scene[future]
                try:
                    filepath = future.result()
                    if filepath and os.path.exists(filepath):
                        # ✅ VERIFY FILE IS VALID
                        if os.path.getsize(filepath) > 1000:
                            downloaded_clips.append(filepath)
                        else:
                            print(f"⚠️  Skipping corrupted file: {filepath}")
                except Exception as e:
                    print(f"❌ Failed to fetch '{query}': {e}")
        
        print(f"✅ Downloaded {len(downloaded_clips)}/{len(scenes)} valid clips")
        
        # Ensure at least 1 clip
        if not downloaded_clips:
            print("⚠️  No clips downloaded, trying emergency fallback")
            fallback_scene = {'query': 'nature landscape', 'keywords': ['nature']}
            fallback = self._fetch_single_clip(fallback_scene)
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

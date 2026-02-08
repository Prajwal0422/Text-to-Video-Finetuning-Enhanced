"""
Clip Fetcher - Downloads stock video clips from Pexels API
"""

import os
import requests
from typing import List, Dict, Optional
import time

class ClipFetcher:
    def __init__(self, api_key: Optional[str] = None):
        # Pexels API key (free tier: 200 requests/hour)
        self.api_key = api_key or os.getenv('PEXELS_API_KEY', '')
        self.base_url = "https://api.pexels.com/videos/search"
        self.headers = {
            'Authorization': self.api_key
        }
        self.download_dir = "outputs/clips"
        os.makedirs(self.download_dir, exist_ok=True)
    
    def search_videos(self, keyword: str, per_page: int = 5) -> List[Dict]:
        """Search for videos by keyword"""
        if not self.api_key:
            print("⚠️  No Pexels API key found. Using fallback method.")
            return self._get_fallback_clips(keyword)
        
        try:
            params = {
                'query': keyword,
                'per_page': per_page,
                'orientation': 'landscape',
                'size': 'medium'
            }
            
            response = requests.get(
                self.base_url,
                headers=self.headers,
                params=params,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                return data.get('videos', [])
            else:
                print(f"⚠️  API error {response.status_code}. Using fallback.")
                return self._get_fallback_clips(keyword)
                
        except Exception as e:
            print(f"⚠️  Error fetching clips: {e}. Using fallback.")
            return self._get_fallback_clips(keyword)
    
    def _get_fallback_clips(self, keyword: str) -> List[Dict]:
        """Fallback: Return placeholder video info"""
        # In production, you could use local stock footage or other APIs
        return [{
            'id': f'fallback_{keyword}',
            'video_files': [{
                'link': 'https://sample-videos.com/video123/mp4/720/big_buck_bunny_720p_1mb.mp4',
                'quality': 'hd',
                'width': 1280,
                'height': 720
            }]
        }]
    
    def download_clip(self, video_url: str, filename: str) -> Optional[str]:
        """Download a video clip"""
        try:
            filepath = os.path.join(self.download_dir, filename)
            
            # Skip if already exists
            if os.path.exists(filepath):
                return filepath
            
            print(f"📥 Downloading: {filename}")
            response = requests.get(video_url, stream=True, timeout=30)
            
            if response.status_code == 200:
                with open(filepath, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
                print(f"✅ Downloaded: {filename}")
                return filepath
            else:
                print(f"❌ Download failed: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"❌ Error downloading clip: {e}")
            return None
    
    def fetch_clips_for_scenes(self, scenes: List[Dict]) -> List[str]:
        """Fetch video clips for all scenes"""
        downloaded_clips = []
        
        for scene in scenes:
            keywords = scene.get('keywords', [])
            if not keywords:
                continue
            
            keyword = keywords[0]
            print(f"🔍 Searching for: {keyword}")
            
            videos = self.search_videos(keyword, per_page=1)
            
            if videos:
                video = videos[0]
                video_files = video.get('video_files', [])
                
                # Get best quality HD video
                hd_video = None
                for vf in video_files:
                    if vf.get('quality') == 'hd' and vf.get('width', 0) >= 1280:
                        hd_video = vf
                        break
                
                # Fallback to first available
                if not hd_video and video_files:
                    hd_video = video_files[0]
                
                if hd_video:
                    video_url = hd_video.get('link')
                    filename = f"scene_{scene['id']}_{keyword}.mp4"
                    
                    filepath = self.download_clip(video_url, filename)
                    if filepath:
                        downloaded_clips.append(filepath)
            
            # Rate limiting
            time.sleep(0.5)
        
        return downloaded_clips


if __name__ == "__main__":
    # Test
    fetcher = ClipFetcher()
    scenes = [
        {'id': 1, 'keywords': ['sunset']},
        {'id': 2, 'keywords': ['mountains']},
    ]
    clips = fetcher.fetch_clips_for_scenes(scenes)
    print(f"Downloaded {len(clips)} clips")

"""
Local Generation Mode - Lightweight Fallback System
Generates videos using local resources when API models fail
"""

import os
import logging
from typing import Dict, Any, Optional, List
from pathlib import Path
import random

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class LocalGenerator:
    """
    Local video generation fallback
    
    Features:
    - Uses cached clips from previous generations
    - Creates simple compositions without API calls
    - Lightweight and fast
    - Always available (no network required)
    """
    
    def __init__(self, cache_dir: str = "outputs/cache"):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        
        # Stock video categories for fallback
        self.fallback_categories = {
            'nature': ['forest', 'mountain', 'river', 'sunset', 'clouds'],
            'ocean': ['waves', 'beach', 'underwater', 'coast'],
            'city': ['street', 'buildings', 'traffic', 'skyline'],
            'people': ['walking', 'working', 'meeting', 'celebration'],
            'abstract': ['particles', 'motion', 'colors', 'patterns']
        }
    
    def get_cached_clips(self, limit: int = 10) -> List[str]:
        """
        Get available cached video clips
        
        Args:
            limit: Maximum number of clips to return
        
        Returns:
            List of clip file paths
        """
        cache_path = Path("outputs/cache")
        
        if not cache_path.exists():
            logger.warning("⚠️  No cache directory found")
            return []
        
        # Find all video files in cache
        video_extensions = ['.mp4', '.avi', '.mov', '.webm']
        clips = []
        
        for ext in video_extensions:
            clips.extend(cache_path.glob(f'*{ext}'))
        
        # Convert to strings and limit
        clip_paths = [str(clip) for clip in clips][:limit]
        
        logger.info(f"📦 Found {len(clip_paths)} cached clips")
        return clip_paths
    
    def categorize_prompt(self, prompt: str) -> str:
        """
        Categorize prompt into fallback category
        
        Args:
            prompt: User prompt
        
        Returns:
            Category name
        """
        prompt_lower = prompt.lower()
        
        # Check each category
        for category, keywords in self.fallback_categories.items():
            if any(keyword in prompt_lower for keyword in keywords):
                return category
        
        # Default to abstract
        return 'abstract'
    
    def generate_simple_video(
        self,
        prompt: str,
        duration: int = 12
    ) -> Dict[str, Any]:
        """
        Generate video using local resources
        
        Args:
            prompt: Video generation prompt
            duration: Target duration in seconds
        
        Returns:
            Generation result dictionary
        """
        logger.info(f"🏠 Local generation mode: '{prompt}'")
        
        try:
            # Get cached clips
            cached_clips = self.get_cached_clips(limit=5)
            
            if not cached_clips:
                return {
                    'success': False,
                    'error': 'No cached clips available for local generation',
                    'message': 'Please connect to internet for first-time generation'
                }
            
            # Categorize prompt
            category = self.categorize_prompt(prompt)
            logger.info(f"📂 Category: {category}")
            
            # Select random clips (simulate matching)
            num_clips = min(3, len(cached_clips))
            selected_clips = random.sample(cached_clips, num_clips)
            
            logger.info(f"🎬 Selected {len(selected_clips)} clips for composition")
            
            # Import video editor
            try:
                from video_editor import VideoEditor
                editor = VideoEditor()
            except ImportError:
                return {
                    'success': False,
                    'error': 'Video editor not available',
                    'message': 'Cannot create video in local mode'
                }
            
            # Create simple video
            video_path = editor.create_video(
                clip_paths=selected_clips,
                prompt=f"{prompt} (local mode)"
            )
            
            if not video_path:
                return {
                    'success': False,
                    'error': 'Failed to create video',
                    'message': 'Video composition failed'
                }
            
            logger.info(f"✅ Local generation complete: {video_path}")
            
            return {
                'success': True,
                'video_path': video_path,
                'mode': 'local',
                'message': 'Generated using local cached clips',
                'clips_used': len(selected_clips)
            }
        
        except Exception as e:
            logger.error(f"❌ Local generation error: {e}")
            return {
                'success': False,
                'error': str(e),
                'message': f'Local generation failed: {str(e)}'
            }
    
    def check_cache_health(self) -> Dict[str, Any]:
        """
        Check cache status and health
        
        Returns:
            Cache statistics
        """
        cached_clips = self.get_cached_clips(limit=1000)
        
        # Calculate total size
        total_size = 0
        for clip_path in cached_clips:
            try:
                total_size += os.path.getsize(clip_path)
            except:
                pass
        
        # Convert to MB
        total_size_mb = total_size / (1024 * 1024)
        
        return {
            'available': len(cached_clips) > 0,
            'clip_count': len(cached_clips),
            'total_size_mb': round(total_size_mb, 2),
            'cache_dir': str(self.cache_dir)
        }
    
    def is_available(self) -> bool:
        """Check if local generation is available"""
        cached_clips = self.get_cached_clips(limit=1)
        return len(cached_clips) > 0


class LocalGenerationWrapper:
    """
    Wrapper for seamless local generation integration
    
    Automatically falls back to local mode when API fails
    """
    
    def __init__(self, primary_generator, local_generator: LocalGenerator):
        self.primary = primary_generator
        self.local = local_generator
    
    def generate(
        self,
        prompt: str,
        force_local: bool = False,
        progress_callback=None
    ) -> Dict[str, Any]:
        """
        Generate video with automatic fallback
        
        Args:
            prompt: Video generation prompt
            force_local: Force local generation mode
            progress_callback: Progress callback function
        
        Returns:
            Generation result
        """
        # Check if forced to local mode
        if force_local:
            logger.info("🏠 Forced local generation mode")
            if progress_callback:
                progress_callback(10, "Using local generation mode...")
            return self.local.generate_simple_video(prompt)
        
        # Try primary generator first
        try:
            logger.info("🌐 Attempting primary generation...")
            if progress_callback:
                progress_callback(5, "Connecting to API...")
            
            result = self.primary.generate(prompt, progress_callback)
            
            if result.get('success'):
                return result
            
            # Primary failed, try local
            logger.warning("⚠️  Primary generation failed, switching to local mode")
            
        except Exception as e:
            logger.error(f"❌ Primary generation error: {e}")
        
        # Fallback to local
        if self.local.is_available():
            logger.info("🏠 Falling back to local generation...")
            if progress_callback:
                progress_callback(20, "Switching to local generation mode...")
            
            return self.local.generate_simple_video(prompt)
        else:
            return {
                'success': False,
                'error': 'No generation method available',
                'message': 'API unavailable and no cached clips for local generation'
            }


# Example usage
if __name__ == "__main__":
    print("=" * 60)
    print("LOCAL GENERATION MODE - TEST")
    print("=" * 60)
    
    generator = LocalGenerator()
    
    # Check cache health
    health = generator.check_cache_health()
    print(f"\n📊 Cache Health:")
    print(f"   Available: {health['available']}")
    print(f"   Clips: {health['clip_count']}")
    print(f"   Size: {health['total_size_mb']} MB")
    
    # Test generation
    if health['available']:
        print(f"\n🎬 Testing local generation...")
        result = generator.generate_simple_video("A beautiful sunset over mountains")
        
        if result['success']:
            print(f"✅ Success: {result['video_path']}")
            print(f"   Mode: {result['mode']}")
            print(f"   Clips used: {result['clips_used']}")
        else:
            print(f"❌ Failed: {result['message']}")
    else:
        print("\n⚠️  No cached clips available")
        print("   Run a successful generation first to populate cache")

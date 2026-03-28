"""
Fast Video Generator - Optimized for Speed
Ultra-fast video generation with aggressive optimizations
"""

import time
from typing import Dict, Optional
import os

try:
    from .script_generator import ScriptGenerator
    from .clip_fetcher import ClipFetcher
    from .visual_intent_mapper import VisualIntentMapper
    from .video_editor import VideoEditor
except ImportError:
    from script_generator import ScriptGenerator
    from clip_fetcher import ClipFetcher
    from visual_intent_mapper import VisualIntentMapper
    from video_editor import VideoEditor


class FastVideoGenerator:
    """
    Ultra-fast video generator with aggressive optimizations
    
    Speed Improvements:
    - Parallel clip fetching (5 workers instead of 3)
    - Shorter clip duration (3s instead of 4s)
    - Reduced timeouts (5s instead of 8s)
    - Smaller total duration (9-12s instead of 12-16s)
    - Cached clip reuse
    - Optimized FFmpeg settings
    
    Target: < 20 seconds generation time
    """
    
    def __init__(self, pexels_api_key: Optional[str] = None):
        self.visual_mapper = VisualIntentMapper()
        self.script_gen = ScriptGenerator()
        self.clip_fetcher = ClipFetcher(api_key=pexels_api_key)
        self.video_editor = VideoEditor()
        
        # Speed optimizations
        self.clip_fetcher.max_workers = 5  # More parallel downloads
        self.clip_fetcher.request_timeout = 5  # Faster timeout
        self.clip_fetcher.download_timeout = 20  # Faster download timeout
        self.video_editor.clip_duration = 3.0  # Shorter clips
        self.video_editor.target_total_duration = (9, 12)  # Shorter videos
    
    def generate_fast(self, prompt: str, progress_callback=None) -> Dict:
        """
        Fast video generation - optimized for speed
        
        Target: < 20 seconds
        
        Args:
            prompt: Text description
            progress_callback: Optional callback(progress, message)
        
        Returns:
            Generation result
        """
        start_time = time.time()
        
        try:
            # Stage 1: Visual Intent Mapping (< 0.5s)
            if progress_callback:
                progress_callback(5, "Analyzing prompt...")
            
            scenes = self.visual_mapper.map_prompt_to_scenes(prompt)
            
            # Limit to 2 scenes for speed
            scenes = scenes[:2]
            
            # Stage 2: Script Generation (< 0.5s)
            if progress_callback:
                progress_callback(15, "Generating script...")
            
            script = self.script_gen.generate_script(prompt)
            script['scenes'] = scenes
            
            # Stage 3: Fast Clip Fetching (< 10s)
            if progress_callback:
                progress_callback(30, "Fetching clips (fast mode)...")
            
            clip_paths = self.clip_fetcher.fetch_clips_for_scenes(script['scenes'])
            
            if not clip_paths:
                # Quick fallback
                fallback_scenes = [{'query': prompt.split()[0], 'keywords': [prompt.split()[0]]}]
                clip_paths = self.clip_fetcher.fetch_clips_for_scenes(fallback_scenes)
            
            # Stage 4: Fast Video Composition (< 8s)
            if progress_callback:
                progress_callback(70, "Creating video (fast mode)...")
            
            video_path = self.video_editor.create_video(
                clip_paths=clip_paths,
                prompt=prompt
            )
            
            if not video_path:
                return {
                    'success': False,
                    'video_path': None,
                    'duration': time.time() - start_time,
                    'message': 'Failed to create video'
                }
            
            if progress_callback:
                progress_callback(100, "Complete!")
            
            elapsed = time.time() - start_time
            
            return {
                'success': True,
                'video_path': video_path,
                'duration': elapsed,
                'message': f'Fast video created in {elapsed:.1f}s',
                'script': script,
                'mode': 'fast'
            }
            
        except Exception as e:
            elapsed = time.time() - start_time
            
            return {
                'success': False,
                'video_path': None,
                'duration': elapsed,
                'message': f'Error: {str(e)}'
            }
    
    def generate_ultra_fast(self, prompt: str, progress_callback=None) -> Dict:
        """
        Ultra-fast generation - maximum speed, minimal quality
        
        Target: < 15 seconds
        
        Uses:
        - Single scene only
        - Cached clips preferred
        - Minimal processing
        """
        start_time = time.time()
        
        try:
            if progress_callback:
                progress_callback(10, "Ultra-fast mode...")
            
            # Single scene only
            scenes = [{'query': prompt, 'keywords': prompt.split()[:3]}]
            
            if progress_callback:
                progress_callback(30, "Fetching clip...")
            
            clip_paths = self.clip_fetcher.fetch_clips_for_scenes(scenes)
            
            if not clip_paths:
                return {
                    'success': False,
                    'video_path': None,
                    'duration': time.time() - start_time,
                    'message': 'No clips found'
                }
            
            if progress_callback:
                progress_callback(70, "Creating video...")
            
            # Use only first clip for ultra-fast
            video_path = self.video_editor.create_video(
                clip_paths=clip_paths[:1],
                prompt=prompt
            )
            
            elapsed = time.time() - start_time
            
            if progress_callback:
                progress_callback(100, "Complete!")
            
            return {
                'success': True,
                'video_path': video_path,
                'duration': elapsed,
                'message': f'Ultra-fast video created in {elapsed:.1f}s',
                'mode': 'ultra_fast'
            }
            
        except Exception as e:
            elapsed = time.time() - start_time
            
            return {
                'success': False,
                'video_path': None,
                'duration': elapsed,
                'message': f'Error: {str(e)}'
            }


if __name__ == "__main__":
    print("=" * 60)
    print("FAST VIDEO GENERATOR - TEST")
    print("=" * 60)
    
    generator = FastVideoGenerator()
    
    # Test fast mode
    print("\nTesting FAST mode...")
    result = generator.generate_fast("ocean waves")
    
    if result['success']:
        print(f"✅ Generated in {result['duration']:.1f}s")
        print(f"   Video: {result['video_path']}")
    else:
        print(f"❌ Failed: {result['message']}")
    
    # Test ultra-fast mode
    print("\nTesting ULTRA-FAST mode...")
    result = generator.generate_ultra_fast("mountain sunset")
    
    if result['success']:
        print(f"✅ Generated in {result['duration']:.1f}s")
        print(f"   Video: {result['video_path']}")
    else:
        print(f"❌ Failed: {result['message']}")

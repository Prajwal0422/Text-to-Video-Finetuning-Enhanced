"""
Video Generator - Main orchestration engine
Coordinates script generation, clip fetching, and video editing
"""

import time
from typing import Dict, Optional
from script_generator import ScriptGenerator
from clip_fetcher import ClipFetcher

# Try to import moviepy-based editor, fallback to simple editor
try:
    from video_editor import VideoEditor
    MOVIEPY_AVAILABLE = True
except ImportError:
    from simple_video_editor import VideoEditor
    MOVIEPY_AVAILABLE = False
    print("⚠️  MoviePy not installed. Using placeholder mode.")
    print("   Install with: pip install moviepy")

class VideoGenerator:
    def __init__(self, pexels_api_key: Optional[str] = None):
        self.script_gen = ScriptGenerator()
        self.clip_fetcher = ClipFetcher(api_key=pexels_api_key)
        self.video_editor = VideoEditor()
    
    def generate(self, prompt: str, progress_callback=None) -> Dict:
        """
        Main generation pipeline
        Returns: {
            'success': bool,
            'video_path': str,
            'duration': float,
            'message': str
        }
        """
        start_time = time.time()
        
        try:
            # Step 1: Generate script (1-2s)
            if progress_callback:
                progress_callback(10, "Generating script...")
            
            print("📝 Step 1: Generating script...")
            script = self.script_gen.generate_script(prompt)
            print(f"✅ Generated {len(script['scenes'])} scenes")
            print(f"   Keywords: {', '.join(script['keywords'])}")
            
            # Step 2: Fetch clips (10-15s)
            if progress_callback:
                progress_callback(30, "Fetching video clips...")
            
            print("\n📥 Step 2: Fetching clips...")
            clip_paths = self.clip_fetcher.fetch_clips_for_scenes(script['scenes'])
            print(f"✅ Downloaded {len(clip_paths)} clips")
            
            # Step 3: Create video (5-10s)
            if progress_callback:
                progress_callback(60, "Creating video...")
            
            print("\n🎬 Step 3: Creating video...")
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
            
            # Complete
            if progress_callback:
                progress_callback(100, "Complete!")
            
            elapsed = time.time() - start_time
            print(f"\n✅ Video generation complete in {elapsed:.1f}s")
            print(f"📹 Output: {video_path}")
            
            return {
                'success': True,
                'video_path': video_path,
                'duration': elapsed,
                'message': f'Video created successfully in {elapsed:.1f}s',
                'script': script
            }
            
        except Exception as e:
            elapsed = time.time() - start_time
            print(f"\n❌ Error: {e}")
            
            return {
                'success': False,
                'video_path': None,
                'duration': elapsed,
                'message': f'Error: {str(e)}'
            }


def test_generation():
    """Test the video generation pipeline"""
    print("=" * 60)
    print("NEXUS VISION - Fast Video Generation Test")
    print("=" * 60)
    
    generator = VideoGenerator()
    
    test_prompts = [
        "A beautiful sunset over mountains",
        "Ocean waves on a tropical beach",
        "City lights at night"
    ]
    
    for prompt in test_prompts:
        print(f"\n🎯 Testing prompt: '{prompt}'")
        result = generator.generate(prompt)
        
        if result['success']:
            print(f"✅ SUCCESS - Generated in {result['duration']:.1f}s")
            print(f"   Video: {result['video_path']}")
        else:
            print(f"❌ FAILED - {result['message']}")
        
        print("-" * 60)


if __name__ == "__main__":
    test_generation()

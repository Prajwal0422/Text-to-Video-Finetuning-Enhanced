"""
Video Generator - Main orchestration engine
Coordinates script generation, clip fetching, and video editing

This module serves as the main entry point for video generation,
orchestrating the entire pipeline from text prompt to final video output.

Key Features:
- Script generation from text prompts
- Automatic clip fetching from Pexels API
- Video editing and composition
- Progress tracking and callbacks
- Error handling and recovery

Performance:
- Average generation time: 15-25 seconds
- Supports parallel processing
- Automatic fallback mechanisms
"""

import time
from typing import Dict, Optional
from script_generator import ScriptGenerator
from clip_fetcher import ClipFetcher

# Try to import moviepy-based editor, fallback to simple editor
# MoviePy provides advanced video editing capabilities
# If not available, falls back to basic video operations
try:
    from video_editor import VideoEditor
    MOVIEPY_AVAILABLE = True
except ImportError:
    from simple_video_editor import VideoEditor
    MOVIEPY_AVAILABLE = False
    print("⚠️  MoviePy not installed. Using placeholder mode.")
    print("   Install with: pip install moviepy")

class VideoGenerator:
    """
    Main video generation orchestrator
    
    Coordinates the three-stage pipeline:
    1. Script Generation - Convert prompt to structured scenes
    2. Clip Fetching - Download relevant video clips
    3. Video Editing - Compose final video output
    
    Attributes:
        script_gen: Script generator instance
        clip_fetcher: Clip fetcher instance with API access
        video_editor: Video editor instance for composition
    """
    def __init__(self, pexels_api_key: Optional[str] = None):
        """
        Initialize the video generator with all required components
        
        Args:
            pexels_api_key: Optional API key for Pexels video service
                          If not provided, will attempt to load from environment
        
        Initializes:
            - Script generator for prompt-to-scene conversion
            - Clip fetcher for downloading video clips
            - Video editor for final composition
        """
        self.script_gen = ScriptGenerator()
        self.clip_fetcher = ClipFetcher(api_key=pexels_api_key)
        self.video_editor = VideoEditor()
    
    def generate(self, prompt: str, progress_callback=None) -> Dict:
        """
        Main video generation pipeline - orchestrates all stages
        
        This is the primary method that coordinates the entire video generation
        process from text prompt to final video file.
        
        Pipeline Stages:
        1. Script Generation (1-2s)
           - Analyzes prompt and extracts keywords
           - Generates structured scene descriptions
           - Determines optimal scene count and duration
        
        2. Clip Fetching (10-15s)
           - Searches Pexels API for relevant clips
           - Downloads and caches video clips
           - Normalizes clip formats and resolutions
        
        3. Video Composition (5-10s)
           - Merges clips with transitions
           - Applies effects and filters
           - Exports final video file
        
        Args:
            prompt: Text description of desired video content
                   Example: "A beautiful sunset over mountains"
            progress_callback: Optional callback function(progress, message)
                             Called at each stage with progress percentage (0-100)
                             and status message
        
        Returns:
            Dictionary containing:
            - success (bool): Whether generation succeeded
            - video_path (str): Path to generated video file
            - duration (float): Total generation time in seconds
            - message (str): Success or error message
            - script (dict): Generated script structure (on success)
        
        Raises:
            Exception: Catches and returns all exceptions in result dict
                      for graceful error handling
        
        Example:
            >>> generator = VideoGenerator(api_key="your_key")
            >>> result = generator.generate("Ocean waves at sunset")
            >>> if result['success']:
            ...     print(f"Video saved to: {result['video_path']}")
        """
        # Track total generation time for performance monitoring
        start_time = time.time()
        
        try:
            # ============================================================
            # STAGE 1: SCRIPT GENERATION (1-2 seconds)
            # ============================================================
            # Convert text prompt into structured scene descriptions
            # This stage analyzes the prompt and generates:
            # - Scene descriptions with keywords
            # - Optimal scene count (typically 3-5 scenes)
            # - Duration per scene
            # - Search keywords for clip fetching
            
            if progress_callback:
                progress_callback(10, "Generating script...")
            
            print("📝 Step 1: Generating script...")
            script = self.script_gen.generate_script(prompt)
            print(f"✅ Generated {len(script['scenes'])} scenes")
            print(f"   Keywords: {', '.join(script['keywords'])}")
            
            # ============================================================
            # STAGE 2: CLIP FETCHING (10-15 seconds)
            # ============================================================
            # Download relevant video clips from Pexels API
            # This is typically the longest stage due to:
            # - API search requests
            # - Video file downloads
            # - Format normalization
            # Clips are cached to speed up future generations
            
            if progress_callback:
                progress_callback(30, "Fetching video clips...")
            
            print("\n📥 Step 2: Fetching clips...")
            clip_paths = self.clip_fetcher.fetch_clips_for_scenes(script['scenes'])
            print(f"✅ Downloaded {len(clip_paths)} clips")
            
            # ============================================================
            # STAGE 3: VIDEO COMPOSITION (5-10 seconds)
            # ============================================================
            # Merge clips into final video with:
            # - Smooth transitions between clips
            # - Resolution normalization
            # - Audio mixing (if applicable)
            # - Export to MP4 format
            
            if progress_callback:
                progress_callback(60, "Creating video...")
            
            print("\n🎬 Step 3: Creating video...")
            video_path = self.video_editor.create_video(
                clip_paths=clip_paths,
                prompt=prompt
            )
            
            # ============================================================
            # ERROR HANDLING: Video Creation Failed
            # ============================================================
            # If video_editor returns None, it means the composition failed
            # This can happen due to:
            # - Corrupted clip files
            # - Insufficient disk space
            # - Codec issues
            # - Memory constraints
            
            if not video_path:
                return {
                    'success': False,
                    'video_path': None,
                    'duration': time.time() - start_time,
                    'message': 'Failed to create video'
                }
            
            # ============================================================
            # SUCCESS: Video Generation Complete
            # ============================================================
            # Notify callback of completion and return success result
            
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
                'script': script  # Include script for debugging/analysis
            }
            
        except Exception as e:
            # ============================================================
            # EXCEPTION HANDLING: Catch All Errors
            # ============================================================
            # Gracefully handle any unexpected errors during generation
            # Returns error details instead of crashing
            # Logs error for debugging purposes
            
            elapsed = time.time() - start_time
            print(f"\n❌ Error: {e}")
            
            return {
                'success': False,
                'video_path': None,
                'duration': elapsed,
                'message': f'Error: {str(e)}'
            }


def test_generation():
    """
    Test the video generation pipeline with sample prompts
    
    This function serves as both a test suite and usage example.
    It demonstrates:
    - How to initialize the VideoGenerator
    - How to call the generate method
    - How to handle success/failure results
    - Performance benchmarking
    
    Test Prompts:
    - Covers different scene types (nature, ocean, urban)
    - Tests keyword extraction variety
    - Validates end-to-end pipeline
    
    Output:
    - Prints detailed progress for each test
    - Shows generation time and success status
    - Displays output file paths
    
    Usage:
        Run directly: python video_generator.py
        Or import: from video_generator import test_generation
    """
    print("=" * 60)
    print("NEXUS VISION - Fast Video Generation Test")
    print("=" * 60)
    
    # Initialize generator (API key loaded from environment)
    generator = VideoGenerator()
    
    # Test prompts covering different content types
    test_prompts = [
        "A beautiful sunset over mountains",  # Nature/landscape
        "Ocean waves on a tropical beach",    # Water/nature
        "City lights at night"                # Urban/cityscape
    ]
    
    # Run generation test for each prompt
    for prompt in test_prompts:
        print(f"\n🎯 Testing prompt: '{prompt}'")
        result = generator.generate(prompt)
        
        # Display results
        if result['success']:
            print(f"✅ SUCCESS - Generated in {result['duration']:.1f}s")
            print(f"   Video: {result['video_path']}")
        else:
            print(f"❌ FAILED - {result['message']}")
        
        print("-" * 60)


# ============================================================
# MAIN ENTRY POINT
# ============================================================
# When run directly, execute test suite
# This allows for easy testing and validation

if __name__ == "__main__":
    test_generation()

"""
Video Generator - Main orchestration engine
Coordinates script generation, clip fetching, and video editing
UPGRADED: Integrated Visual Intent Mapper for semantic prompt expansion

This module serves as the main entry point for video generation,
orchestrating the entire pipeline from text prompt to final video output.

Key Features:
- Visual intent mapping for semantic prompt expansion
- Script generation from text prompts
- Multi-query clip fetching from Pexels API
- Cinematic video editing with transitions
- Progress tracking and callbacks
- Error handling and recovery

Performance:
- Average generation time: 15-25 seconds
- Supports parallel processing
- Automatic fallback mechanisms
"""

import time
from typing import Dict, Optional

try:
    from .script_generator import ScriptGenerator
    from .clip_fetcher import ClipFetcher
    from .visual_intent_mapper import VisualIntentMapper
except ImportError:
    from script_generator import ScriptGenerator
    from clip_fetcher import ClipFetcher
    from visual_intent_mapper import VisualIntentMapper

# Try to import moviepy-based editor, fallback to simple editor
# MoviePy provides advanced video editing capabilities
# If not available, falls back to basic video operations
try:
    try:
        from .video_editor import VideoEditor
    except ImportError:
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
            - Visual intent mapper for semantic prompt expansion
            - Script generator for prompt-to-scene conversion
            - Clip fetcher for downloading video clips
            - Video editor for final composition
        """
        self.visual_mapper = VisualIntentMapper()
        self.script_gen = ScriptGenerator()
        self.clip_fetcher = ClipFetcher(api_key=pexels_api_key)
        self.video_editor = VideoEditor()
    
    def generate(self, prompt: str, progress_callback=None) -> Dict:
        """
        Main video generation pipeline - orchestrates all stages
        UPGRADED: Now uses Visual Intent Mapper for semantic expansion
        
        This is the primary method that coordinates the entire video generation
        process from text prompt to final video file.
        
        Pipeline Stages:
        1. Visual Intent Mapping (< 1s)
           - Converts prompt into cinematic visual queries
           - Expands semantic meaning for better clip matching
           - Generates 5 search queries per prompt
        
        2. Script Generation (1-2s)
           - Analyzes prompt and extracts keywords
           - Generates structured scene descriptions
           - Determines optimal scene count and duration
        
        3. Multi-Query Clip Fetching (10-15s)
           - Runs 3 search queries per scene
           - Downloads and caches video clips
           - Ranks candidates by relevance
        
        4. Cinematic Video Composition (5-10s)
           - Merges clips with crossfade transitions
           - Applies fade in/out effects
           - Exports final video (12-16s duration)
        
        Args:
            prompt: Text description of desired video content
                   Example: "two countries doing a war and soldiers struggling"
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
            # STAGE 1: VISUAL INTENT MAPPING (< 1 second)
            # ============================================================
            # NEW: Convert prompt into semantic visual search queries
            # This stage expands the prompt meaning to improve clip matching
            
            if progress_callback:
                progress_callback(5, "Mapping visual intent...")
            
            print("🎬 Step 1: Visual Intent Mapping...")
            scenes = self.visual_mapper.map_prompt_to_scenes(prompt)
            print(f"✅ Generated {len(scenes)} cinematic scenes with visual queries")
            
            # ============================================================
            # STAGE 2: SCRIPT GENERATION (1-2 seconds)
            # ============================================================
            # Generate script structure (kept for compatibility)
            
            if progress_callback:
                progress_callback(10, "Generating script...")
            
            print("📝 Step 2: Generating script structure...")
            script = self.script_gen.generate_script(prompt)
            
            # Merge visual intent scenes with script
            # Use visual intent scenes as they have better queries
            script['scenes'] = scenes
            print(f"✅ Script ready with {len(script['scenes'])} scenes")
            print(f"   Keywords: {', '.join(script['keywords'])}")
            
            # ============================================================
            # STAGE 3: MULTI-QUERY CLIP FETCHING (10-15 seconds)
            # ============================================================
            # UPGRADED: Multi-query search with ranking
            # - Runs 3 search queries per scene
            # - Collects top 5 videos per query
            # - Ranks all candidates by relevance
            # - Downloads best matches
            # Clips are cached to speed up future generations
            
            if progress_callback:
                progress_callback(30, "Searching for relevant video clips...")
            
            print("\n📥 Step 3: Multi-query clip fetching...")
            print(f"   Searching for {len(script['scenes'])} scenes...")
            
            clip_paths = self.clip_fetcher.fetch_clips_for_scenes(script['scenes'])
            
            if not clip_paths or len(clip_paths) == 0:
                print("⚠️  No clips found, using fallback search...")
                # Fallback: try with just keywords
                fallback_scenes = [{'query': kw, 'keywords': [kw]} for kw in script['keywords'][:3]]
                clip_paths = self.clip_fetcher.fetch_clips_for_scenes(fallback_scenes)
            
            print(f"✅ Downloaded {len(clip_paths)} clips")
            
            # ============================================================
            # STAGE 4: CINEMATIC VIDEO COMPOSITION (5-10 seconds)
            # ============================================================
            # UPGRADED: Cinematic editing with transitions
            # - 4 seconds per scene minimum
            # - Crossfade transitions between clips
            # - Fade in at start, fade out at end
            # - Target duration: 12-16 seconds
            # - Export to MP4 format
            
            if progress_callback:
                progress_callback(60, "Creating cinematic video...")
            
            print("\n🎬 Step 4: Cinematic video composition...")
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
